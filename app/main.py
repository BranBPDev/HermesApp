from app.utils.update_util import is_latest_version, perform_update

def main():
    if not is_latest_version():
        perform_update()
    print("App iniciada correctamente")

if __name__ == "__main__":
    main()