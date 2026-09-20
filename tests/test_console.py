import contextlib
import io
import os
import re
import sys
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "studio"))

import server
from server import CONSOLE_COLUMNS, CONSOLE_ROWS, CONSOLE_WIDTH, DEFAULT_HOST, StudioServer, colorize_console_line, console_row, print_startup_error, print_startup_panel


class ConsolePresentationTests(unittest.TestCase):
    def test_box_rows_have_a_stable_width(self):
        row = console_row("DURUM", "Yerel motor hazır")
        self.assertEqual(len(row), CONSOLE_WIDTH)
        self.assertTrue(row.startswith("│"))
        self.assertTrue(row.endswith("│"))

    def test_startup_panel_uses_professional_turkish_copy(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            print_startup_panel("https://127.0.0.1:8080/", True, "http://192.168.1.25:8080/")
        text = output.getvalue()
        self.assertIn("APK CLEANER STUDIO", text)
        self.assertIn("LOCAL SESSION", text)
        self.assertIn("ENGINE 2.0", text)
        self.assertIn("YEREL MOTOR HAZIR", text)
        self.assertIn("YEREL AĞ ERİŞİMİ", text)
        self.assertIn("http://192.168.1.25:8080/", text)
        self.assertIn("Özel ağlar", text)
        self.assertIn("Tarayıcı açılıyor", text)
        self.assertIn("İŞ AKIŞI", text)
        self.assertIn("01 Paketi seç", text)

    def test_console_uses_requested_110_by_30_layout(self):
        self.assertEqual(CONSOLE_COLUMNS, 110)
        self.assertEqual(CONSOLE_ROWS, 30)
        self.assertLess(CONSOLE_WIDTH, CONSOLE_COLUMNS)
        self.assertEqual(DEFAULT_HOST, "0.0.0.0")

    def test_termux_console_uses_device_width_without_horizontal_overflow(self):
        output = io.StringIO()
        terminal_size = os.terminal_size((44, 30))
        with mock.patch.dict(os.environ, {"TERMUX_VERSION": "0.119"}, clear=False), mock.patch(
            "server.shutil.get_terminal_size", return_value=terminal_size
        ), contextlib.redirect_stdout(output):
            print_startup_panel("https://127.0.0.1:8080/", False, "http://192.168.1.25:8080/")
        lines = [line for line in output.getvalue().splitlines() if line]
        self.assertTrue(lines)
        self.assertTrue(all(len(line) <= 44 for line in lines))
        self.assertIn("YEREL ARAYÜZ", output.getvalue())
        self.assertIn("3  Yerel motoru çalıştır", output.getvalue())

    def test_termux_startup_error_is_compact_and_has_no_desktop_box(self):
        output = io.StringIO()
        terminal_size = os.terminal_size((42, 30))
        error = OSError(98, "Address already in use")
        with mock.patch.dict(os.environ, {"TERMUX_VERSION": "0.119"}, clear=False), mock.patch(
            "server.shutil.get_terminal_size", return_value=terminal_size
        ), contextlib.redirect_stdout(output):
            print_startup_error(8080, error)
        text = output.getvalue()
        lines = [line for line in text.splitlines() if line]
        self.assertTrue(all(len(line) <= 42 for line in lines))
        self.assertIn("BAŞLATILAMADI", text)
        self.assertIn("8080", text)
        self.assertNotIn("╭", text)
        self.assertNotIn("│", text)

    def test_ansi_accents_preserve_visible_row_width(self):
        row = console_row("", "✓  OTURUM HAZIR  ·  https://127.0.0.1:8080/")
        previous = server._ANSI_ENABLED
        try:
            server._ANSI_ENABLED = True
            with mock.patch.dict(os.environ, {}, clear=True):
                styled = colorize_console_line(row)
        finally:
            server._ANSI_ENABLED = previous
        self.assertIn("\033[", styled)
        self.assertEqual(re.sub(r"\033\[[0-9;]*m", "", styled), row)

    def test_console_colors_are_applied_in_one_non_nested_pass(self):
        previous = server._ANSI_ENABLED
        try:
            server._ANSI_ENABLED = True
            with mock.patch.dict(os.environ, {}, clear=True):
                styled = colorize_console_line("✓  OTURUM HAZIR  ·  ENGINE  ·  01  YEREL ARAYÜZ  https://127.0.0.1:8080/")
        finally:
            server._ANSI_ENABLED = previous
        self.assertNotIn("\033[1;38;2;152;167;161mOTURUM", styled)
        self.assertEqual(styled.count("\033[1;38;2;104;195;255m"), 1)
        self.assertEqual(re.sub(r"\033\[[0-9;]*m", "", styled), "✓  OTURUM HAZIR  ·  ENGINE  ·  01  YEREL ARAYÜZ  https://127.0.0.1:8080/")

    def test_request_threads_do_not_keep_the_app_alive(self):
        self.assertTrue(StudioServer.daemon_threads)
        self.assertFalse(StudioServer.block_on_close)

    def test_windows_close_cancels_browser_timer_and_forces_process_exit(self):
        timer = mock.Mock()
        active_server = mock.Mock()
        with mock.patch.object(server, "_BROWSER_TIMER", timer), mock.patch.object(
            server, "_ACTIVE_SERVER", active_server
        ), mock.patch("server.terminate_active_tools") as terminate, mock.patch(
            "server.os._exit", side_effect=SystemExit(0)
        ) as hard_exit:
            with self.assertRaises(SystemExit):
                server._shutdown_windows_runtime()
        timer.cancel.assert_called_once_with()
        terminate.assert_called_once_with()
        active_server.shutdown.assert_called_once_with()
        active_server.server_close.assert_called_once_with()
        hard_exit.assert_called_once_with(0)


if __name__ == "__main__":
    unittest.main()
