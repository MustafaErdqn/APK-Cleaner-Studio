from __future__ import annotations

import ipaddress
import os
import ssl
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID


def _write_private_key(path: Path, key) -> None:
    path.write_bytes(
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
    )
    try:
        path.chmod(0o600)
    except OSError:
        pass


def _root_material(directory: Path):
    key_path = directory / "local-root-key.pem"
    cert_path = directory / "local-root-ca.crt"
    if key_path.is_file() and cert_path.is_file():
        try:
            key = serialization.load_pem_private_key(key_path.read_bytes(), password=None)
            cert = x509.load_pem_x509_certificate(cert_path.read_bytes())
            if cert.not_valid_after_utc > datetime.now(timezone.utc) + timedelta(days=30):
                return key, cert, cert_path
        except (ValueError, TypeError, OSError):
            pass

    now = datetime.now(timezone.utc)
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "APK Cleaner Studio Local CA")])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(subject)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(minutes=5))
        .not_valid_after(now + timedelta(days=3650))
        .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
        .add_extension(x509.KeyUsage(True, False, False, False, False, True, True, False, False), critical=True)
        .add_extension(x509.SubjectKeyIdentifier.from_public_key(key.public_key()), critical=False)
        .sign(key, hashes.SHA256())
    )
    _write_private_key(key_path, key)
    cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    return key, cert, cert_path


def root_is_trusted_on_windows(cert_path: Path) -> bool:
    if os.name != "nt" or not hasattr(ssl, "enum_certificates"):
        return False
    try:
        target = x509.load_pem_x509_certificate(cert_path.read_bytes()).public_bytes(serialization.Encoding.DER)
        return any(encoded == "x509_asn" and certificate == target for certificate, encoded, _trust in ssl.enum_certificates("ROOT"))
    except (OSError, ValueError):
        return False


def trust_root_on_windows(cert_path: Path) -> bool:
    if os.name != "nt":
        return False
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    try:
        result = subprocess.run(
            ["certutil", "-user", "-addstore", "-f", "Root", str(cert_path)],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=20,
            creationflags=flags,
            check=False,
        )
        return result.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def ensure_local_tls(directory: Path, hostnames: set[str], addresses: set[str], trust_windows: bool = True) -> tuple[Path, Path, Path, bool]:
    """Create a device-local CA and leaf certificate for the current local endpoints."""
    directory.mkdir(parents=True, exist_ok=True)
    root_key, root_cert, root_path = _root_material(directory)
    now = datetime.now(timezone.utc)
    leaf_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    names: list[x509.GeneralName] = []
    for hostname in sorted({"localhost", *hostnames}):
        value = hostname.strip().lower().rstrip(".")
        if value and len(value) <= 253:
            names.append(x509.DNSName(value))
    for address in sorted({"127.0.0.1", "::1", *addresses}):
        try:
            names.append(x509.IPAddress(ipaddress.ip_address(address)))
        except ValueError:
            continue
    subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "APK Cleaner Studio Local")])
    leaf_cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(root_cert.subject)
        .public_key(leaf_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(minutes=5))
        .not_valid_after(now + timedelta(days=825))
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .add_extension(x509.SubjectAlternativeName(names), critical=False)
        .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]), critical=False)
        .add_extension(x509.KeyUsage(True, False, True, False, False, False, False, False, False), critical=True)
        .sign(root_key, hashes.SHA256())
    )
    key_path = directory / "local-server-key.pem"
    cert_path = directory / "local-server-cert.pem"
    _write_private_key(key_path, leaf_key)
    cert_path.write_bytes(leaf_cert.public_bytes(serialization.Encoding.PEM))
    trusted = trust_root_on_windows(root_path) if trust_windows else root_is_trusted_on_windows(root_path)
    return cert_path, key_path, root_path, trusted
