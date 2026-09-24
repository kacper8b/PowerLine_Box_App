<#
.SYNOPSIS
    Automatyzuje budowe pliku wykonywalnego PowerLine_Box_App (PyInstaller).
.DESCRIPTION
    Tworzy/aktywuje wirtualne srodowisko, instaluje zaleznosci, czysci stare
    artefakty budowy, uruchamia PyInstaller wg powerline-box.spec i kopiuje
    pliki konfiguracyjne oraz ikone do katalogu dist.
.PARAMETER SkipVenv
    Pomija tworzenie/aktywacje wirtualnego srodowiska (uzywa aktualnie
    aktywnego interpretera Pythona).
#>
param(
    [switch]$SkipVenv
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not $SkipVenv) {
    if (-not (Test-Path ".venv")) {
        Write-Host "Tworzenie wirtualnego srodowiska .venv..." -ForegroundColor Cyan
        python -m venv .venv
    }
    Write-Host "Aktywacja .venv..." -ForegroundColor Cyan
    . .\.venv\Scripts\Activate.ps1
}

Write-Host "Instalacja/aktualizacja zaleznosci..." -ForegroundColor Cyan
python -m pip install --upgrade pip
pip install pyserial pyinstaller

Write-Host "Czyszczenie poprzednich artefaktow build/dist..." -ForegroundColor Cyan
Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue

Write-Host "Budowanie aplikacji (PyInstaller)..." -ForegroundColor Cyan
pyinstaller powerline-box.spec

Write-Host "Kopiowanie plikow konfiguracyjnych i ikony do dist..." -ForegroundColor Cyan
Copy-Item "powerline-box.ico" "dist\powerline-box.ico" -Force
Copy-Item "config.json" "dist\config.json" -Force
Copy-Item "panel_buttons.json" "dist\panel_buttons.json" -Force

Write-Host "Build zakonczony. Plik wykonywalny: dist\powerline-box.exe" -ForegroundColor Green
