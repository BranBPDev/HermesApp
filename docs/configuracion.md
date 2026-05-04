
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

---

## 🔄 Interfaz de Actualización
El componente `Update` gestiona la comunicación visual durante el proceso de actualización:
* **Barra de Progreso:** Visualización en tiempo real del estado de la descarga y sustitución de archivos.
* **Feedback:** Mensajes dinámicos que informan al usuario sobre el paso actual del "Hot-Swap".