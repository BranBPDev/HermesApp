from app.managers.app_manager import AppManager

def main():
    # La instancia se encarga de todo el ciclo de vida
    app = AppManager()
    app.start()

if __name__ == "__main__":
    main()