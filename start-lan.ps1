$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $projectRoot

$lanIp = Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
    Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*" } |
    Select-Object -ExpandProperty IPAddress -First 1

Write-Host "APK Cleaner Studio LAN modunda baslatiliyor..." -ForegroundColor Green
if ($lanIp) {
    Write-Host "Diger cihazlardan: http://${lanIp}:8080/" -ForegroundColor Cyan
}
Write-Host "Yalnizca guvendigin ozel aglarda kullan. Kapatmak icin Ctrl+C." -ForegroundColor Yellow
Start-Process "http://127.0.0.1:8080/"

$portableExe = Join-Path $projectRoot "APK-Cleaner-Studio.exe"
if (Test-Path -LiteralPath $portableExe) {
    & $portableExe --host 0.0.0.0
    exit $LASTEXITCODE
}

$pythonCommand = Get-Command py, python, python3 -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $pythonCommand) {
    Write-Host "Python 3 bulunamadi ve tasinabilir EXE pakette yok." -ForegroundColor Red
    Read-Host "Kapatmak icin Enter"
    exit 1
}

if ($pythonCommand.Name -eq "py.exe" -or $pythonCommand.Name -eq "py") {
    & $pythonCommand.Source -3 "$projectRoot\studio\server.py" --host 0.0.0.0
} else {
    & $pythonCommand.Source "$projectRoot\studio\server.py" --host 0.0.0.0
}
