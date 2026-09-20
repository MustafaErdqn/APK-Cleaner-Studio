import ssl
import tempfile
import unittest
from pathlib import Path

from cryptography import x509

from studio.local_tls import ensure_local_tls


class LocalTLSTests(unittest.TestCase):
    def test_certificate_covers_loopback_and_lan_endpoints(self):
        with tempfile.TemporaryDirectory() as name:
            cert_path, key_path, root_path, trusted = ensure_local_tls(
                Path(name), {"localhost", "TEST-PC"}, {"192.168.1.25"}, trust_windows=False
            )
            self.assertFalse(trusted)
            self.assertTrue(root_path.is_file())
            cert = x509.load_pem_x509_certificate(cert_path.read_bytes())
            san = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
            self.assertIn("localhost", san.get_values_for_type(x509.DNSName))
            self.assertIn("test-pc", san.get_values_for_type(x509.DNSName))
            self.assertIn("192.168.1.25", {str(value) for value in san.get_values_for_type(x509.IPAddress)})
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(str(cert_path), str(key_path))
