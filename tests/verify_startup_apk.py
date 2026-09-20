"""Opt-in real APK regression: preserves source; patches only temporary DEX copies."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from studio.engine import inspect_startup_calls


def verify(apk, owner):
    before_hash = hashlib.sha256(apk.read_bytes()).hexdigest()
    candidates = inspect_startup_calls(apk)
    selected = [row for row in candidates if row['owner_class'] == owner and row['owner_method'] == 'onResume' and row['kind'] == 'Diyalog']
    assert len(selected) == 2, selected
    assert any(row['deferred'] for row in selected)
    assert any(not row['deferred'] for row in selected)
    assert all('?' not in row['target_method'] for row in selected), 'Unicode metadata lost'
    cp = os.pathsep.join(str(ROOT / 'studio/tools' / name) for name in ('direct-dex-patcher.jar', 'dexlib2-runtime.jar'))
    with tempfile.TemporaryDirectory(prefix='verify-startup-') as folder:
        work = Path(folder)
        with zipfile.ZipFile(apk) as archive:
            source = archive.read('classes.dex')
            dex = work / 'input.dex'
            dex.write_bytes(source)
            output = work / 'patched.dex'
            command = [shutil.which('java'), '-cp', cp, 'local.apkcleaner.dex.DirectDexPatcher', '--input', str(dex), '--output', str(output)]
            for row in selected:
                command.extend(['--startup-target', row['id'].split(':', 1)[1]])
            result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', timeout=60)
            assert result.returncode == 0, result.stderr
            assert 'message_patches=2' in result.stdout, result.stdout
            patched = output.read_bytes()
            assert len(patched) == len(source)
            changed = [i for i in range(32, len(source)) if source[i] != patched[i]]
            assert 0 < len(changed) <= 12 and all(patched[i] == 0 for i in changed)
            copy = work / 'inspection-only.apk'
            with zipfile.ZipFile(copy, 'w') as target:
                for info in archive.infolist():
                    target.writestr(info, patched if info.filename == 'classes.dex' else archive.read(info))
        after = inspect_startup_calls(copy)
        assert {row['id'] for row in after} == {row['id'] for row in candidates} - {row['id'] for row in selected}
    assert hashlib.sha256(apk.read_bytes()).hexdigest() == before_hash
    return {'source_unchanged': True, 'candidates_before': len(candidates), 'selected_roots_removed': len(selected),
            'candidates_after': len(after), 'other_candidates_preserved': True, 'changed_dex_bytes_excluding_header': len(changed)}


if __name__ == '__main__':
    print(json.dumps(verify(Path(sys.argv[1]), sys.argv[2]), indent=2))
