"""Real assembled multidex fixtures; no third-party APK required."""
import hashlib
import os
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import unittest
import zipfile
import zlib
from unittest.mock import patch

from studio.engine import inspect_startup_calls, process_apk

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "studio" / "tools"


def activity(name, method="onCreate", params="Landroid/os/Bundle;", call="", superclass="Landroid/app/Activity;"):
    return f""".class public Lfixture/{name};
.super {superclass}
.method public {method}({params})V
 .registers 5
 {call}
 return-void
.end method
"""


class StartupCallsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.java = shutil.which("java")
        if not cls.java:
            raise unittest.SkipTest("Java unavailable")
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        cls.cp = os.pathsep.join(str(TOOLS / x) for x in ("direct-dex-patcher.jar", "dexlib2-runtime.jar"))
        helpers = """.class public Lxpk/a;
.super Ljava/lang/Object;
.method public static StartGame(Landroid/content/Context;)V
 .registers 2
 new-instance v0, Landroid/app/AlertDialog$Builder;
 invoke-direct {v0, p0}, Landroid/app/AlertDialog$Builder;-><init>(Landroid/content/Context;)V
 invoke-virtual {v0}, Landroid/app/AlertDialog$Builder;->show()Landroid/app/AlertDialog;
 return-void
.end method
.method public static unrelated(Landroid/content/Context;)V
 .registers 1
 return-void
.end method
.method public static misleadingShowDialog(Landroid/content/Context;)V
 .registers 1
 return-void
.end method
.method public static deferred(Landroid/content/Context;)V
 .registers 3
 new-instance v0, Landroid/os/Handler;
 invoke-direct {v0}, Landroid/os/Handler;-><init>()V
 new-instance v1, Lxpk/a$Task;
 invoke-direct {v1}, Lxpk/a$Task;-><init>()V
 invoke-virtual {v0, v1}, Landroid/os/Handler;->post(Ljava/lang/Runnable;)Z
 return-void
.end method
.method public static mixed(Landroid/content/Context;)V
 .registers 1
 invoke-static {p0}, Lxpk/a;->StartGame(Landroid/content/Context;)V
 invoke-static {}, Lfixture/Native;->unknown()V
 return-void
.end method
"""
        task = """.class public Lxpk/a$Task;
.super Ljava/lang/Object;
.implements Ljava/lang/Runnable;
.method public constructor <init>()V
 .registers 1
 invoke-direct {p0}, Ljava/lang/Object;-><init>()V
 return-void
.end method
.method public run()V
 .registers 2
 const/4 v0, 0
 invoke-static {v0}, Lxpk/a;->StartGame(Landroid/content/Context;)V
 return-void
.end method
"""
        call = "invoke-static/range {p0 .. p0}, Lxpk/a;->StartGame(Landroid/content/Context;)V\n invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V"
        sources = {name: activity(name, call=call) for name in ("MainActivity", "SplashActivity", "SettingsActivity", "FragmentActivity", "a")}
        sources["Resume"] = activity("Resume", "onResume", "", "invoke-static {p0}, Lxpk/a;->deferred(Landroid/content/Context;)V")
        sources["WindowFocus"] = activity("WindowFocus", "onWindowFocusChanged", "Z", "invoke-static {p0}, Lxpk/a;->StartGame(Landroid/content/Context;)V")
        sources["Attached"] = activity("Attached", "onAttachedToWindow", "", "invoke-static {p0}, Lxpk/a;->StartGame(Landroid/content/Context;)V")
        sources["NewIntent"] = activity("NewIntent", "onNewIntent", "Landroid/content/Intent;", "invoke-static {p0}, Lxpk/a;->StartGame(Landroid/content/Context;)V")
        sources["Original"] = activity("Original", call="const/4 v0, 0\n invoke-virtual {v0}, Landroid/app/Dialog;->show()V")
        sources["WrongInstance"] = activity("WrongInstance", call="const/4 v0, 0\n invoke-static {v0}, Lxpk/a;->StartGame(Landroid/content/Context;)V")
        sources["WrongSignature"] = activity("WrongSignature", "onResume", "I", "invoke-static {p0}, Lxpk/a;->StartGame(Landroid/content/Context;)V")
        sources["NotActivity"] = activity("NotActivity", call=call, superclass="Ljava/lang/Object;")
        sources["Misleading"] = activity("Misleading", call="invoke-static {p0}, Lxpk/a;->misleadingShowDialog(Landroid/content/Context;)V")
        sources["Mixed"] = activity("Mixed", call="invoke-static {p0}, Lxpk/a;->mixed(Landroid/content/Context;)V")
        sources["Alias"] = activity("Alias", call="move-object v0, p0\n invoke-static {v0}, Lxpk/a;->StartGame(Landroid/content/Context;)V")
        helpers += """
.method public static ۟ۤۧ(Ljava/lang/Object;I)V
 .registers 2
 check-cast p0, Landroid/app/Activity;
 invoke-static {p0}, Lxpk/a;->StartGame(Landroid/content/Context;)V
 return-void
.end method
.method public static noArgs()V
 .registers 1
 const/4 v0, 0
 invoke-static {v0}, Lxpk/a;->StartGame(Landroid/content/Context;)V
 return-void
.end method
.method public static returnsObject(Ljava/lang/Object;)Ljava/lang/Object;
 .registers 1
 invoke-static {}, Lxpk/a;->noArgs()V
 return-object p0
.end method
.method public static wrapped(Ljava/lang/Object;)V
 .registers 3
 new-instance v0, Lxpk/a$Task;
 invoke-direct {v0}, Lxpk/a$Task;-><init>()V
 const/4 v1, 0
 invoke-static {v1, v0}, Lxpk/a;->bridge(Ljava/lang/Object;Ljava/lang/Object;)V
 return-void
.end method
.method public static bridge(Ljava/lang/Object;Ljava/lang/Object;)V
 .registers 4
 move-object v1, p1
 const/4 v0, 0
 if-eqz v0, :go
 return-void
 :go
 check-cast v1, Ljava/lang/Runnable;
 check-cast p0, Ljava/util/concurrent/Executor;
 invoke-interface {p0, v1}, Ljava/util/concurrent/Executor;->execute(Ljava/lang/Runnable;)V
 return-void
.end method
.method public static native unavailable()V
.end method
"""
        sources["ObjectBridge"] = activity("ObjectBridge", call="const/4 v0, 0\n invoke-static {p0, v0}, Lxpk/a;->۟ۤۧ(Ljava/lang/Object;I)V")
        sources["BranchAlias"] = activity("BranchAlias", call="move-object v0, p0\n if-eqz p1, :go\n nop\n :go\n invoke-static {v0}, Lxpk/a;->StartGame(Landroid/content/Context;)V")
        sources["ChangedAlias"] = activity("ChangedAlias", call="move-object v0, p0\n if-eqz p1, :go\n const/4 v0, 0\n :go\n invoke-static {v0}, Lxpk/a;->StartGame(Landroid/content/Context;)V")
        sources["Parameterless"] = activity("Parameterless", call="invoke-static {}, Lxpk/a;->noArgs()V")
        sources["WrappedRunnable"] = activity("WrappedRunnable", "onResume", "", "invoke-static {p0}, Lxpk/a;->wrapped(Ljava/lang/Object;)V")
        sources["IgnoredResult"] = activity("IgnoredResult", call="invoke-static {p0}, Lxpk/a;->returnsObject(Ljava/lang/Object;)Ljava/lang/Object;")
        sources["UsedResult"] = activity("UsedResult", call="invoke-static {p0}, Lxpk/a;->returnsObject(Ljava/lang/Object;)Ljava/lang/Object;\n move-result-object v0")
        sources["Native"] = activity("Native", call="invoke-static {}, Lxpk/a;->unavailable()V")
        sources["Application"] = activity("Application", "onCreate", "", "invoke-static {}, Lxpk/a;->noArgs()V", "Landroid/app/Application;")
        sources["Fragment"] = activity("Fragment", "onViewCreated", "Landroid/view/View;Landroid/os/Bundle;", "invoke-static {}, Lxpk/a;->noArgs()V", "Landroidx/fragment/app/Fragment;")
        sources["WrongActivityCallback"] = activity("WrongActivityCallback", "onCreate", "", "invoke-static {}, Lxpk/a;->noArgs()V")
        sources["InstanceHelper"] = activity("InstanceHelper", call="invoke-direct {p0}, Lfixture/InstanceHelper;->intro()V") + """
.method private intro()V
 .registers 1
 invoke-static {p0}, Lxpk/a;->StartGame(Landroid/content/Context;)V
 return-void
.end method
"""
        cls.assemble(sources, cls.root / "classes.dex", "one")
        cls.assemble({"a": helpers, "task": task}, cls.root / "classes2.dex", "two")
        cls.apk = cls.root / "fixture.apk"
        with zipfile.ZipFile(cls.apk, "w") as archive:
            for name in ("classes.dex", "classes2.dex"):
                archive.write(cls.root / name, name)
        cls.candidates = inspect_startup_calls(cls.apk)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    @classmethod
    def assemble(cls, sources, output, directory):
        folder = cls.root / directory
        folder.mkdir()
        for name, text in sources.items():
            (folder / (name + ".smali")).write_text(text, encoding="utf-8")
        result = subprocess.run([cls.java, "-cp", str(TOOLS / "APKEditor.jar"), "org.jf.smali.Main", "assemble", str(folder), "-o", str(output)], capture_output=True, text=True, timeout=30)
        if result.returncode or not output.exists():
            raise AssertionError(result.stdout + result.stderr)

    def test_all_activity_names_and_obfuscated_names_are_scanned(self):
        owners = {row["owner_class"] for row in self.candidates}
        for name in ("MainActivity", "SplashActivity", "SettingsActivity", "FragmentActivity", "a", "Alias"):
            self.assertIn(f"Lfixture/{name};", owners)

    def test_non_activity_wrong_signature_and_non_this_are_excluded(self):
        owners = {row["owner_class"] for row in self.candidates}
        for name in ("WrongSignature", "NotActivity", "WrongInstance", "Misleading", "Original"):
            self.assertNotIn(f"Lfixture/{name};", owners)

    def test_cross_dex_helper_and_deferred_on_resume_are_traced(self):
        candidate = next(row for row in self.candidates if row["owner_class"] == "Lfixture/Resume;")
        self.assertTrue(candidate["deferred"])
        self.assertIn("Lxpk/a$Task;->run", candidate["trace"])
        self.assertEqual(candidate["owner_method"], "onResume")
        self.assertEqual(candidate["target_method"], "deferred")

    def test_additional_activity_startup_callbacks_are_traced(self):
        owners = {row["owner_class"] for row in self.candidates}
        for name in ("WindowFocus", "Attached", "NewIntent"):
            self.assertIn(f"Lfixture/{name};", owners)

    def test_mixed_helper_is_reported_for_explicit_review_not_as_proven_mod(self):
        candidate = next(row for row in self.candidates if row["owner_class"] == "Lfixture/Mixed;")
        self.assertEqual(candidate["confidence"], "review")
        self.assertEqual(candidate["provenance"], "unverified")

    def test_object_multiple_arguments_parameterless_and_instance_helpers(self):
        owners = {row['owner_class'] for row in self.candidates}
        for name in ('ObjectBridge', 'BranchAlias', 'Parameterless', 'InstanceHelper', 'Application', 'Fragment', 'IgnoredResult'):
            self.assertIn(f'Lfixture/{name};', owners)
        for name in ('ChangedAlias', 'UsedResult', 'Native', 'WrongActivityCallback'):
            self.assertNotIn(f'Lfixture/{name};', owners)
        row = next(row for row in self.candidates if row['owner_class'] == 'Lfixture/ObjectBridge;')
        self.assertEqual(row['target_method'], '۟ۤۧ')

    def test_runnable_type_survives_object_wrappers_and_conditional_alias(self):
        row = next(row for row in self.candidates if row['owner_class'] == 'Lfixture/WrappedRunnable;')
        self.assertTrue(row['deferred'])
        self.assertIn('bridge', row['trace'])
        self.assertIn('Lxpk/a$Task;->run', row['trace'])

    def test_unused_nonvoid_root_is_patched_without_touching_used_results(self):
        candidate = next(row for row in self.candidates if row['owner_class'] == 'Lfixture/IgnoredResult;')
        output = self.root / 'unused-result.dex'
        result = subprocess.run([self.java, '-cp', self.cp, 'local.apkcleaner.dex.DirectDexPatcher',
            '--input', str(self.root / 'classes.dex'), '--output', str(output), '--startup-target', candidate['id'].split(':')[1]],
            capture_output=True, text=True, encoding='utf-8', timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('message_patches=1', result.stdout)
        original, patched = (self.root / 'classes.dex').read_bytes(), output.read_bytes()
        self.assertEqual(len(original), len(patched))
        offsets = [i for i in range(32, len(original)) if original[i] != patched[i]]
        self.assertLessEqual(max(offsets) - min(offsets), 5)

    def test_selected_root_uses_one_fallthrough_branch_with_lengths_and_checksums_preserved(self):
        candidate = next(row for row in self.candidates if row["owner_class"] == "Lfixture/MainActivity;")
        output = self.root / "patched.dex"
        result = subprocess.run([self.java, "-cp", self.cp, "local.apkcleaner.dex.DirectDexPatcher",
            "--input", str(self.root / "classes.dex"), "--output", str(output), "--mode", "safe",
            "--startup-target", candidate["id"].split(":")[1]], capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("message_patches=1", result.stdout)
        original, patched = (self.root / "classes.dex").read_bytes(), output.read_bytes()
        self.assertEqual(len(original), len(patched))
        offsets = [i for i in range(32, len(original)) if original[i] != patched[i]]
        self.assertTrue(offsets)
        self.assertLessEqual(max(offsets) - min(offsets), 5)
        instruction_start = min(offsets)
        self.assertEqual(patched[instruction_start:instruction_start + 6], b"\x2a\x00\x03\x00\x00\x00")
        self.assertEqual(patched[12:32], hashlib.sha1(patched[32:]).digest())
        self.assertEqual(struct.unpack_from("<I", patched, 8)[0], zlib.adler32(patched[12:]) & 0xffffffff)
        new_apk = self.root / "patched.apk"
        with zipfile.ZipFile(new_apk, "w") as archive:
            archive.writestr("classes.dex", patched)
            archive.write(self.root / "classes2.dex", "classes2.dex")
        after = inspect_startup_calls(new_apk)
        self.assertEqual(len(after), len(self.candidates) - 1)
        self.assertNotIn(candidate["id"], {row["id"] for row in after})

    def test_stale_root_selection_does_not_produce_output(self):
        output = self.root / "stale.dex"
        result = subprocess.run([self.java, "-cp", self.cp, "local.apkcleaner.dex.DirectDexPatcher",
            "--input", str(self.root / "classes.dex"), "--output", str(output), "--startup-target", "lc-stale"], capture_output=True, text=True, timeout=30)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(output.exists())

    def test_process_rejects_stale_or_legacy_show_targets(self):
        with patch("studio.engine.inspect_startup_calls", return_value=[]):
            with self.assertRaisesRegex(ValueError, "eşleşmiyor"):
                process_apk(self.apk, self.root / "result", patch_ads=False,
                            analysis_report={"detections": []}, message_targets=["classes.dex:old-show"])


if __name__ == "__main__":
    unittest.main()
