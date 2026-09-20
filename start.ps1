$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $projectRoot

$portableExe = Join-Path $projectRoot "APK-Cleaner-Studio.exe"
if (Test-Path -LiteralPath $portableExe) {
    Write-Host "APK Cleaner Studio baslatiliyor..." -ForegroundColor Green
    & $portableExe --open
    exit $LASTEXITCODE
}

$pythonCommand = Get-Command py, python, python3 -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $pythonCommand) {
    Write-Host "Python 3 bulunamadi." -ForegroundColor Red
    Write-Host "Once https://www.python.org/downloads/ adresinden Python 3 kurup bu dosyayi yeniden ac." -ForegroundColor Yellow
    Read-Host "Kapatmak icin Enter"
    exit 1
}

Write-Host "APK Cleaner Studio Python ile baslatiliyor..." -ForegroundColor Green
if ($pythonCommand.Name -eq "py.exe" -or $pythonCommand.Name -eq "py") {
    & $pythonCommand.Source -3 "$projectRoot\studio\server.py" --open
} else {
    & $pythonCommand.Source "$projectRoot\studio\server.py" --open
}
