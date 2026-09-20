import unittest
from pathlib import Path
from unittest.mock import patch

from studio.engine import compare_message_calls


def call(target_id: str, signature: str, context: str = "") -> dict:
    return {
        "id": f"classes.dex:{target_id}",
        "dex": "classes.dex",
        "target_id": target_id,
        "kind": "Toast",
        "owner_class": "Lexample/MainActivity;",
        "owner_method": "onCreate",
        "target_class": "Landroid/widget/Toast;",
        "target_method": "show",
        "context_signature": context,
        "signature": signature,
    }


def method_call(target_id: str, signature: str, method: str) -> dict:
    item = call(target_id, signature)
    item["owner_method"] = method
    return item


class MessageComparisonTests(unittest.TestCase):
    def test_only_occurrences_exceeding_original_are_returned(self):
        original = [call("old", "same")]
        modified = [call("kept", "same"), call("added", "same"), call("new", "new")]
        with patch("studio.engine.inspect_message_calls", side_effect=[modified, original]):
            result = compare_message_calls(Path("modified.apk"), Path("original.apk"))
        self.assertEqual([item["id"] for item in result], ["classes.dex:added", "classes.dex:new"])
        self.assertTrue(all("signature" not in item and "target_id" not in item for item in result))

    def test_original_only_calls_are_never_selected(self):
        with patch("studio.engine.inspect_message_calls", side_effect=[[call("kept", "same")], [call("old", "same")]]):
            self.assertEqual(compare_message_calls(Path("modified.apk"), Path("original.apk")), [])

    def test_on_create_additions_are_prioritized_without_weakening_comparison(self):
        modified = [
            method_call("later", "later", "openScreen"),
            method_call("startup", "startup", "onCreate"),
        ]
        with patch("studio.engine.inspect_message_calls", side_effect=[modified, []]):
            result = compare_message_calls(Path("modified.apk"), Path("original.apk"))
        self.assertEqual([item["id"] for item in result], ["classes.dex:startup", "classes.dex:later"])

    def test_common_activity_lifecycle_candidates_are_prioritized(self):
        ordinary = method_call("ordinary", "ordinary", "onCreate")
        ordinary["owner_class"] = "Lexample/Worker;"
        settings = method_call("settings", "settings", "onResume")
        settings["owner_class"] = "Lexample/SettingsActivity;"
        with patch("studio.engine.inspect_message_calls", side_effect=[[ordinary, settings], []]):
            result = compare_message_calls(Path("modified.apk"), Path("original.apk"))
        self.assertEqual([item["id"] for item in result], ["classes.dex:settings", "classes.dex:ordinary"])

    def test_context_matching_finds_call_inserted_before_original_occurrence(self):
        original = [call("old", "same", "original-neighborhood")]
        modified = [
            call("injected", "same", "new-neighborhood"),
            call("moved-old", "same", "original-neighborhood"),
        ]
        with patch("studio.engine.inspect_message_calls", side_effect=[modified, original]):
            result = compare_message_calls(Path("modified.apk"), Path("original.apk"))
        self.assertEqual([item["id"] for item in result], ["classes.dex:injected"])


if __name__ == "__main__":
    unittest.main()
