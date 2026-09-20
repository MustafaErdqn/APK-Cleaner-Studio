"""Exercise the Android Python entry point with a real disposable HTTP listener."""
import importlib.util
import os
import socket
import tempfile
import types
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch


class AndroidLifecycleTests(unittest.TestCase):
    def test_start_stop_and_lost_listener_recover_without_duplicate_server(self):
        path = Path(__file__).resolve().parents[1] / 'android/app/src/main/python/android_entry.py'
        spec = importlib.util.spec_from_file_location('entry_under_test', path)
        entry = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(entry)
        fake = types.ModuleType('server')
        fake._ACTIVE_SERVER = None
        fake.terminate_active_tools = lambda: None
        starts = []

        def serve(host, port, *_):
            with ThreadingHTTPServer((host, port), BaseHTTPRequestHandler) as server:
                fake._ACTIVE_SERVER = server
                starts.append(server)
                try:
                    server.serve_forever(poll_interval=0.02)
                finally:
                    fake._ACTIVE_SERVER = None

        fake.serve = serve
        with socket.socket() as probe:
            probe.bind(('127.0.0.1', 0))
            port = probe.getsockname()[1]
        old_temp = tempfile.tempdir
        try:
            with tempfile.TemporaryDirectory() as root, patch.dict(os.environ), patch.dict('sys.modules', server=fake):
                try:
                    self.assertTrue(entry.start(root, port))
                    first_thread = entry._thread
                    self.assertTrue(entry.start(root, port))
                    self.assertIs(entry._thread, first_thread)
                    self.assertEqual(len(starts), 1)
                    entry.stop()
                    self.assertFalse(first_thread.is_alive())
                    self.assertTrue(entry.start(root, port))
                    lost_thread = entry._thread
                    fake._ACTIVE_SERVER.shutdown()
                    lost_thread.join(timeout=2)
                    self.assertFalse(lost_thread.is_alive())
                    self.assertTrue(entry.start(root, port))
                    self.assertEqual(len(starts), 3)
                finally:
                    entry.stop()
        finally:
            tempfile.tempdir = old_temp
