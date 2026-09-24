# PowerLine Box App

Aplikacja desktopowa (Windows, Python + Tkinter) do sterowania i diagnostyki urządzenia PowerLine Box po porcie szeregowym (UART/COM). Jest interfejsem operatorskim komplementarnym do firmware [PowerLine_Box_STM8](../PowerLine_Box_STM8).

## Funkcje

- Nawigacja: Home, Control Panel, Settings, About
- Konfigurowalny panel przycisków (siatka 6x10) z edycją etykiet i komend w runtime
- Stałe przyciski operacyjne: SEND, INIT, ON, OFF, DPC
- Połączenie z urządzeniem przez port szeregowy (domyślnie COM4, konfigurowalny w `config/config.json`)
- Terminal diagnostyczny z podglądem komunikacji na żywo (timestamp, kierunek `-->`/`<--`)
- Automatyczne tworzenie plików konfiguracyjnych w `Documents\PowerLine Box` przy pierwszym uruchomieniu

## Wymagania

- Python 3
- Zależności wykonawcze: `requirements.txt` (`pyserial`; `tkinter` i `json` są częścią standardowej biblioteki)
- Zależności deweloperskie (budowa `.exe`, testy): `requirements-dev.txt` (`pyinstaller`, `pytest`)

## Uruchomienie ze źródeł

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
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

```
PowerLine_Box_App/
├── main.py                     # punkt wejścia (dev run + PyInstaller)
├── build.ps1                   # automatyzacja budowy .exe
├── config/                     # domyślne szablony konfiguracji
│   ├── config.json
│   └── panel_buttons.json
├── packaging/                  # zasoby i specyfikacja PyInstaller
│   ├── powerline-box.spec
│   ├── powerline-box.ico
│   └── how to build exe.txt
└── src/powerline_box/           # kod źródłowy aplikacji (pakiet Python)
    ├── app.py                  # `WindowManager`, pętla główna
    ├── config.py               # layout, ścieżki, inicjalizacja configu użytkownika
    ├── gui.py                  # generyczne helpery Tkinter
    ├── terminal_log.py         # logowanie komunikacji do okna terminala
    ├── panel/                  # logika panelu sterowania
    │   ├── controller.py       # orkiestracja komend/sekwencji (INIT, DPC)
    │   ├── buttons.py          # konfigurowalna siatka przycisków
    │   ├── edit.py             # panel edycji przycisku
    │   └── main_panel.py       # stałe przyciski operacyjne
    ├── uart/                   # warstwa komunikacji szeregowej
    │   ├── serial_port.py      # wrapper na pyserial
    │   ├── manager.py          # menedżer wielu portów
    │   └── power_line.py       # protokół domenowy PowerLine Box
    └── windows/                # ekrany aplikacji
        ├── sidebar.py, home.py, settings.py, about.py
        ├── panel_view.py
        └── terminal_view.py
```

## Konfiguracja

Pliki konfiguracyjne użytkownika znajdują się w `%USERPROFILE%\Documents\PowerLine Box\` (kopiowane automatycznie z katalogu aplikacji przy pierwszym uruchomieniu). Aby przywrócić ustawienia domyślne, usuń pliki `config.json` / `panel_buttons.json` z tego katalogu i uruchom aplikację ponownie.

## Powiązany projekt

Komendy wysyłane z aplikacji (`pwr`, `safepwr`, `init`, `ppc`, `cali_a`, `cali_d`) odpowiadają parserowi komend `Command.c` w firmware `PowerLine_Box_STM8`.
