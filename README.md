# PowerLine Box App

Aplikacja desktopowa (Windows, Python + Tkinter) do sterowania i diagnostyki urządzenia PowerLine Box po porcie szeregowym (UART/COM). Jest interfejsem operatorskim komplementarnym do firmware [PowerLine_Box_STM8](../PowerLine_Box_STM8).

## Funkcje

- Nawigacja: Home, Control Panel, Settings, About
- Konfigurowalny panel przycisków (siatka 6x10) z edycją etykiet i komend w runtime
- Stałe przyciski operacyjne: SEND, INIT, ON, OFF, DPC
- Połączenie z urządzeniem przez port szeregowy (domyślnie COM4, konfigurowalny w `config.json`)
- Terminal diagnostyczny z podglądem komunikacji na żywo (timestamp, kierunek `-->`/`<--`)
- Automatyczne tworzenie plików konfiguracyjnych w `Documents\PowerLine Box` przy pierwszym uruchomieniu

## Wymagania

- Python 3
- Zależności: `pyserial` (`tkinter` i `json` są częścią standardowej biblioteki)

## Uruchomienie ze źródeł

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pyserial
python powerline-box.py
```

## Budowanie pliku .exe

Proces budowy jest zautomatyzowany w skrypcie `build.ps1`:

```powershell
.\build.ps1
```

Jeśli PowerShell zablokuje uruchomienie skryptu (`running scripts is disabled on this system`), uruchom jednorazowo:

```powershell
powershell -ExecutionPolicy Bypass -File .\build.ps1
```

Gotowy plik `powerline-box.exe` wraz z plikami konfiguracyjnymi pojawi się w katalogu `dist\`.

## Struktura projektu

- `powerline-box.py` — punkt wejścia GUI (`WindowManager`)
- `config.py`, `config.json`, `panel_buttons.json` — konfiguracja layoutu i domyślne ustawienia użytkownika
- `gui.py` — generyczne helpery Tkinter (przyciski, etykiety, pola tekstowe)
- `windows/` — ekrany aplikacji (sidebar, home, panel, settings, about, terminal)
- `panel/` — logika panelu sterowania (przyciski stałe, konfigurowalne, edycja)
- `uart/` — warstwa komunikacji szeregowej (`uart.py`, `terminal.py`, `power_line.py`)
- `gui_terminal/` — logowanie komunikacji do okna terminala
- `powerline-box.spec`, `powerline-box.ico`, `build.ps1` — zasoby i automatyzacja budowy PyInstaller

## Konfiguracja

Pliki konfiguracyjne użytkownika znajdują się w `%USERPROFILE%\Documents\PowerLine Box\` (kopiowane automatycznie z katalogu aplikacji przy pierwszym uruchomieniu). Aby przywrócić ustawienia domyślne, usuń pliki `config.json` / `panel_buttons.json` z tego katalogu i uruchom aplikację ponownie.

## Powiązany projekt

Komendy wysyłane z aplikacji (`pwr`, `safepwr`, `init`, `ppc`, `cali_a`, `cali_d`) odpowiadają parserowi komend `Command.c` w firmware `PowerLine_Box_STM8`.
