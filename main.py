import sys
import ctypes
from app.managers.app_manager import AppManager

def main():
    if sys.platform == "win32":
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('HermesApp')
        except Exception:
            pass
    AppManager().start()

if __name__ == "__main__":
    main()