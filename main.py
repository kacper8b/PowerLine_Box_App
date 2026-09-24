"""Entry point used both for local runs and PyInstaller packaging."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from powerline_box.app import run

if __name__ == "__main__":
    run()
