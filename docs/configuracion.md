
# 🔑 Configuración de Variables de Entorno

El proyecto utiliza PostgreSQL alojado en [**Neon.tech**](https://neon.com/) para la persistencia de datos en la nube. Para que la aplicación funcione correctamente en desarrollo, debes crear un archivo .env en la raíz del proyecto.

1. Crea el archivo .env:
```bash
touch .env
```

2. Añade tu cadena de conexión (puedes obtenerla en tu consola de Neon):
```text
DATABASE_URL=postgresql://[user]:[password]@[host]/neondb?sslmode=require
```

🛡️ Seguridad: El archivo .env está incluido en el .gitignore para evitar la exposición accidental de credenciales en el repositorio público.

---

## 📁 Sistema de Logs
Para facilitar el mantenimiento, la aplicación genera logs detallados en la carpeta raíz:
`app/logs/hermesApp.log`

* **INFO:** Seguimiento del flujo (Inicios/Finales de scrapers).
* **DEBUG:** Detalles técnicos (URLs procesadas, inyección de cookies).
* **ERROR:** Fallos específicos de red o parseo de datos (ver Tracebacks).