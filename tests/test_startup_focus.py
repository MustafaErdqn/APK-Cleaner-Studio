import unittest
from studio.engine import _startup_focus_group, _startup_risk_assessment


class StartupFocusTests(unittest.TestCase):
    def test_foreign_early_helper_is_priority_but_not_proven(self):
        for status in ("candidate", "review"):
            self.assertEqual(_startup_focus_group("Lcom/example/app/Main;", "Lextra/Message;",
                                                  "before_super", status), "priority")

    def test_normal_internal_and_partial_paths_are_not_prioritized(self):
        for target, location, confidence in (
            ("Lcom/example/app/Main;", "before_super", "review"),
            ("Lcom/example/dialogs/Welcome;", "before_super", "candidate"),
            ("Lextra/Message;", "lifecycle", "candidate"),
            ("Lextra/Message;", "before_super", "partial"),
            ("Lextra/Message;", "before_super", "unknown"),
        ):
            with self.subTest(target=target, location=location, confidence=confidence):
                self.assertEqual(_startup_focus_group("Lcom/example/app/Main;", target, location, confidence), "other")

    def test_obfuscated_default_package_is_not_proven_foreign(self):
        self.assertEqual(_startup_focus_group("La;", "Lb;", "before_super", "candidate"), "other")

    def test_multi_signal_ranking_separates_likely_review_and_internal(self):
        likely = _startup_risk_assessment(
            "Lcom/example/app/Main;", "Lextra/Message;", "onCreate",
            "before_super", "candidate", False, 1, "root > helper > Dialog.show",
        )
        review = _startup_risk_assessment(
            "Lcom/example/app/Main;", "Lcom/example/dialogs/Welcome;", "onCreate",
            "before_super", "candidate", False, 1, "root > Dialog.show",
        )
        internal = _startup_risk_assessment(
            "Lcom/example/app/Main;", "Lcom/example/app/Main;", "onResume",
            "lifecycle", "review", False, 5, "root > helper > state > network > callback > Dialog.show > show",
        )
        self.assertEqual(likely["assessment"], "likely_added")
        self.assertEqual(review["assessment"], "needs_review")
        self.assertEqual(internal["assessment"], "likely_internal")
        self.assertGreater(likely["score"], review["score"])
        self.assertGreater(review["score"], internal["score"])

    def test_reused_or_partial_target_is_downranked(self):
        result = _startup_risk_assessment(
            "Lcom/example/app/Main;", "Lextra/Message;", "onCreate",
            "before_super", "partial", True, 6,
            "root > a > b > c > d > e > Toast.show",
        )
        self.assertNotEqual(result["focus"], "priority")
        self.assertTrue(any("birçok" in signal for signal in result["signals"]))

    def test_obfuscation_shape_mismatch_promotes_early_same_namespace_call_for_review(self):
        result = _startup_risk_assessment(
            "Lcom/example/MainActivity;", "Lcom/example/۠ۧۢۥ;", "onResume",
            "before_super", "review", False, 1, "root > helper > Dialog.show",
        )
        self.assertEqual(result["focus"], "review")
        self.assertTrue(any("ad-karartma" in signal for signal in result["signals"]))


if __name__ == "__main__":
    unittest.main()
