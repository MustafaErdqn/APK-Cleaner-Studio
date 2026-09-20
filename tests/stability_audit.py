"""Release-candidate audit using the bundled Java tools and real package fixtures."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "studio"))

from engine import Toolchain, inspect_apk, inspect_split_components, merge_split_package, process_apk


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def fixture(pattern: str) -> Path:
    matches = sorted((ROOT / "studio" / "jobs").glob(pattern))
    if not matches:
        # Release temizliği geçici iş klasörlerini boşaltmış olabilir. Kalıcı,
        # sürümden bağımsız denetim fikstürlerini work kökünden kullan.
        persistent = ROOT / "work" / Path(pattern).name
        if persistent.is_file():
            matches = [persistent]
    if not matches:
        raise RuntimeError(f"Gerçek test paketi bulunamadı: {pattern}")
    return matches[0]


def archive_check(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        names = archive.namelist()
        return {
            "bad_entry": bad,
            "entries": len(names),
            "dex": len([name for name in names if Path(name).name.startswith("classes") and name.endswith(".dex")]),
            "signed_entries": len([name for name in names if name.upper().startswith("META-INF/")]),
        }


def verify_signature(path: Path, tools: Toolchain) -> None:
    result = subprocess.run(
        [tools.java, "-jar", str(tools.uber_signer), "--onlyVerify", "--skipZipAlign", "--apks", str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=90,
    )
    if result.returncode:
        raise RuntimeError(f"APK imza doğrulaması başarısız: {result.stdout[-1000:]}")


def require_valid_output(output_dir: Path, result: dict, tools: Toolchain) -> Path:
    output = output_dir / result["output"]
    if not output.is_file() or not result["signed"]:
        raise RuntimeError("Gerçek motor testi imzalı APK üretmedi.")
    archive = archive_check(output)
    if archive["bad_entry"] or not archive["dex"] or not archive["signed_entries"]:
        raise RuntimeError(f"Üretilen APK bütünlük denetiminden geçmedi: {archive}")
    verify_signature(output, tools)
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    started = time.perf_counter()
    tools = Toolchain.detect()
    status = tools.status()
    if not status["fully_ready"]:
        raise RuntimeError(f"Araç zinciri eksik: {status}")

    apk = fixture("*/hello-with-ad-call.apk")
    split = fixture("*/ui-split-preview.apks")
    inspection_times: list[float] = []

    def inspect_once(_index: int) -> dict:
        mark = time.perf_counter()
        report = inspect_apk(apk)
        inspection_times.append(time.perf_counter() - mark)
        return report

    with ThreadPoolExecutor(max_workers=8) as pool:
        inspections = list(pool.map(inspect_once, range(24)))
    if any(row["sha256"] != inspections[0]["sha256"] for row in inspections):
        raise RuntimeError("Eşzamanlı analizler farklı SHA-256 sonucu üretti.")

    source_report = inspections[0]
    with tempfile.TemporaryDirectory(prefix="apkcleaner-stability-") as name:
        temp = Path(name)
        output_dir = temp / "patched"
        progress: list[tuple[int, str]] = []
        result = process_apk(
            apk,
            output_dir,
            mode="balanced",
            progress=lambda message, percent: progress.append((percent, message)),
            patch_ads=True,
            strip_debug=True,
            optimize_apk=True,
            analysis_report=source_report,
        )
        output = require_valid_output(output_dir, result, tools)
        archive = archive_check(output)
        with zipfile.ZipFile(apk) as before, zipfile.ZipFile(output) as after:
            resources_preserved = (
                "resources.arsc" not in before.namelist()
                or digest(before.read("resources.arsc")) == digest(after.read("resources.arsc"))
            )
        if not resources_preserved:
            raise RuntimeError("Normal yama resources.arsc içeriğini beklenmedik biçimde değiştirdi.")
        if result["patches"]["changed_files"] < 1:
            raise RuntimeError("Gerçek DEX örneğinde hiçbir dosya yaması raporlanmadı.")
        if progress and any(later < earlier for (earlier, _), (later, _) in zip(progress, progress[1:])):
            raise RuntimeError("Motor ilerleme değerleri geriye gitti.")

        operation_results = {}
        for mode in ("safe", "deep"):
            operation_dir = temp / mode
            operation = process_apk(
                apk,
                operation_dir,
                mode=mode,
                patch_ads=True,
                analysis_report=source_report,
            )
            require_valid_output(operation_dir, operation, tools)
            operation_results[mode] = operation["duration_seconds"]

        conversion_dir = temp / "convert"
        conversion = process_apk(
            apk,
            conversion_dir,
            patch_ads=False,
            analysis_report=source_report,
        )
        require_valid_output(conversion_dir, conversion, tools)
        operation_results["conversion_only"] = conversion["duration_seconds"]

        resources_dir = temp / "resources"
        resources = process_apk(
            apk,
            resources_dir,
            patch_ads=False,
            deobfuscate_resources=True,
            analysis_report=source_report,
        )
        resources_output = require_valid_output(resources_dir, resources, tools)
        decoded_resources = temp / "resources-audit"
        decode = subprocess.run(
            [
                tools.java,
                "-jar",
                str(tools.apkeditor),
                "d",
                "-i",
                str(resources_output),
                "-o",
                str(decoded_resources),
                "-t",
                "xml",
                "-dex",
                "-keep-res-path",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=120,
        )
        if decode.returncode:
            raise RuntimeError(f"RES denetim açılımı başarısız: {decode.stdout[-1000:]}")
        xml_text = "\n".join(
            path.read_text(encoding="utf-8", errors="ignore")
            for path in decoded_resources.rglob("*.xml")
        )
        numeric_resource_refs = re.findall(r"@(?:0x)?[0-9a-fA-F]{8}\b", xml_text)
        if numeric_resource_refs:
            raise RuntimeError(f"RES işleminden sonra sayısal kaynak başvurusu bulundu: {numeric_resource_refs[:5]}")
        operation_results["resource_deobfuscation"] = resources["duration_seconds"]

        inventory = inspect_split_components(split)
        merge_dir = temp / "split"
        merged, merge_log = merge_split_package(split, merge_dir)
        merged_archive = archive_check(merged)
        merged_report = inspect_apk(merged)
        if merged_archive["bad_entry"] or not merged_report["dex"]:
            raise RuntimeError("Split birleştirme geçerli bir universal APK üretmedi.")

        summary = {
            "toolchain": status,
            "source": {"size": apk.stat().st_size, "networks": source_report["network_count"]},
            "concurrent_inspections": 24,
            "inspection_ms": {
                "average": round(sum(inspection_times) * 1000 / len(inspection_times), 2),
                "max": round(max(inspection_times) * 1000, 2),
            },
            "patch": {
                "duration_seconds": result["duration_seconds"],
                "changed_dex": result["patches"]["changed_files"],
                "debug_removed": result["patches"]["debug_directives_removed"],
                "signed": result["signed"],
                "optimized": result["optimized"],
                "archive": archive,
                "resources_arsc_preserved": resources_preserved,
                "progress_events": len(progress),
            },
            "operation_matrix_seconds": operation_results,
            "resource_numeric_references": 0,
            "split": {
                "abis": inventory["abis"],
                "languages": inventory["languages"],
                "densities": inventory["densities"],
                "output_size": merged.stat().st_size,
                "archive": merged_archive,
                "log_lines": len(merge_log),
            },
            "audit_seconds": round(time.perf_counter() - started, 2),
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
