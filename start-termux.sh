#!/data/data/com.termux/files/usr/bin/bash
set -u

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
PID_FILE="$SCRIPT_DIR/.apk-cleaner-termux.pid"
UPDATE_MANIFEST="$SCRIPT_DIR/.apk-cleaner-update.json"
SERVER_PID=""

stop_server() {
  if [ -n "${SERVER_PID:-}" ] && kill -0 "$SERVER_PID" 2>/dev/null; then
    kill -TERM "$SERVER_PID" 2>/dev/null || true
    for _ in 1 2 3 4 5 6 7 8 9 10; do
      kill -0 "$SERVER_PID" 2>/dev/null || break
      sleep 0.1
    done
    if kill -0 "$SERVER_PID" 2>/dev/null; then
      kill -KILL "$SERVER_PID" 2>/dev/null || true
    fi
    wait "$SERVER_PID" 2>/dev/null || true
  fi
  SERVER_PID=""
  rm -f "$PID_FILE"
}

trap stop_server EXIT
trap 'stop_server; exit 0' HUP INT TERM

if ! command -v python >/dev/null 2>&1; then
  echo "Python eksik. Once install-termux.sh dosyasini calistir."
  exit 1
fi

if [ -f "$PID_FILE" ]; then
  OLD_PID="$(cat "$PID_FILE" 2>/dev/null || true)"
  if [ -n "$OLD_PID" ] && kill -0 "$OLD_PID" 2>/dev/null; then
    OLD_COMMAND="$(tr '\000' ' ' < "/proc/$OLD_PID/cmdline" 2>/dev/null || true)"
    case "$OLD_COMMAND" in
      *studio/server.py*)
        echo "Önceki APK Cleaner Studio oturumu güvenli biçimde kapatılıyor..."
        kill "$OLD_PID" 2>/dev/null || true
        for _ in 1 2 3 4 5 6 7 8 9 10; do
          kill -0 "$OLD_PID" 2>/dev/null || break
          sleep 0.2
        done
        ;;
    esac
  fi
  rm -f "$PID_FILE"
fi

python studio/server.py --host 127.0.0.1 --port 8080 --prefer-http &
SERVER_PID=$!
printf '%s\n' "$SERVER_PID" > "$PID_FILE"

READY=0
for _ in 1 2 3 4 5 6 7 8 9 10; do
  if python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/api/status', timeout=1)" >/dev/null 2>&1; then
    READY=1
    break
  fi
  kill -0 "$SERVER_PID" 2>/dev/null || break
  sleep 0.4
done

if [ "$READY" -ne 1 ]; then
  wait "$SERVER_PID" 2>/dev/null || true
  SERVER_PID=""
  echo "APK Cleaner Studio başlatılamadı. Yukarıdaki açıklamayı kontrol et."
  exit 1
fi

if command -v termux-open-url >/dev/null 2>&1; then
  termux-open-url http://127.0.0.1:8080/
else
  am start -a android.intent.action.VIEW -d http://127.0.0.1:8080/ >/dev/null 2>&1 || true
  echo "Tarayıcıda http://127.0.0.1:8080/ adresini aç."
fi

wait "$SERVER_PID" || true
SERVER_PID=""
rm -f "$PID_FILE"

if [ -f "$UPDATE_MANIFEST" ]; then
  echo "GitHub güncellemesi doğrulanıyor ve uygulanıyor..."
  if python studio/apply_termux_update.py "$UPDATE_MANIFEST"; then
    echo "Güncelleme tamamlandı; APK Cleaner Studio yeniden başlatılıyor."
    exec bash "$SCRIPT_DIR/start-termux.sh"
  fi
  echo "Güncelleme uygulanamadı. Mevcut sürüm korunarak oturum kapatıldı."
  exit 1
fi
