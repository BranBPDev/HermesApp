from app.utils.update_util import is_latest_version, perform_update

def main():
    if not is_latest_version():
        print("[SISTEMA] Nueva versión detectada. Actualizando...")
        perform_update()
        
    print("App iniciada correctamente")
    # Pausa para que el usuario vea el mensaje si se ejecuta desde consola
    input("Presiona ENTER para salir...")

if __name__ == "__main__":
    main()