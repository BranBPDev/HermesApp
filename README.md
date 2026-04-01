# HermesApp 🛒

**HermesApp** es una aplicación de escritorio diseñada para comparar precios de productos entre distintos supermercados de España de forma automática. La aplicación recopila datos directamente desde las plataformas online de cada supermercado, los procesa en paralelo y construye una base de datos unificada para su comparación.

---

## 🚀 ¿Qué es HermesApp?

HermesApp automatiza el flujo completo de información:

* **Autenticación:** Sistema de usuarios con contraseñas seguras (bcrypt).
* **Recolección:** Scraping multihilo sincronizado en tiempo real con la nube.
* **Sincronización:** Operaciones masivas (Upsert) en base de datos PostgreSQL (Neon DB).
* **Comparación:** Búsqueda unificada que mezcla y ordena productos de diferentes tiendas por precio.
* **Carrito de compra:** Gestión de listas personalizadas con cálculo de totales por usuario.

El objetivo del proyecto es desarrollar un comparador de precios funcional, preciso y escalable.

---

## 🏪 Supermercados Soportados Actualmente
<div align="center">
  <table style="width: 100%; max-width: 800px;">
    <thead>
      <tr>
        <th align="center" valign="middle">Supermercado</th>
        <th align="center" valign="middle">Estado</th>
        <th align="center" valign="middle">Productos</th>
        <th align="center" valign="middle">Tiempo</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td align="center" valign="middle">Mercadona</td>
        <td align="center" valign="middle">
          <img src="https://img.shields.io/badge/Estado-Operativo-238636?style=flat" alt="Operativo">
        </td>
        <td align="center" valign="middle">~4000+</td>
        <td align="center" valign="middle">2-4 segundos</td>
      </tr>
      <tr>
        <td align="center" valign="middle">Eroski</td>
        <td align="center" valign="middle">
          <img src="https://img.shields.io/badge/Estado-En_Revisión-d29922?style=flat" alt="En Revisión">
        </td>
        <td align="center" valign="middle">~4000+</td>
        <td align="center" valign="middle">15-20 segundos</td>
      </tr>
      <tr>
        <td align="center" valign="middle">Gadis</td>
        <td align="center" valign="middle">
          <img src="https://img.shields.io/badge/Estado-En_Desarrollo-da3633?style=flat" alt="En Desarrollo">
        </td>
        <td align="center" valign="middle">-</td>
        <td align="center" valign="middle">-</td>
      </tr>
    </tbody>
  </table>
</div>

---

## ⬇️ Descarga (IMPORTANTE)

Para utilizar HermesApp debes descargar la aplicación desde la sección de **Releases**:

👉 [**Descargar última versión en Releases**](https://github.com/BranBPDev/HermesApp/releases/latest/download/HermesApp.zip)

> ⚠️ **No descargues el código fuente (ZIP desde el botón "Code")** para uso normal. La versión de Releases incluye el ejecutable listo para usar y el sistema de auto-actualización.

---

## 💻 Uso del Ejecutable

1. Descarga el `.zip` desde Releases.
2. Descomprime el contenido en una carpeta vacía para evitar conflictos.
3. Ejecuta el archivo `.exe`.

La aplicación gestionará automáticamente la verificación de versión, el scraping paralelo y la generación de archivos JSON.

---

## ⌨️ Comandos de la Aplicación

Una vez iniciada la sesión, puedes usar los siguientes comandos en el buscador:
* `carrito`: Visualiza tus productos guardados y el total estimado.
* `vaciar`: Limpia por completo tu lista de la compra.
* `+`: Carga los siguientes 10 resultados de la última búsqueda.
* `salir` / `exit` / `q`: Cierra la aplicación de forma segura.
* `[Número]`: Al ver resultados, escribe el ID del producto para añadirlo al carrito.

---

## 🔄 Sistema de Auto-Actualización

HermesApp incorpora un sistema automático de actualización completamente transparente:

1. **Comprobación:** Verifica la versión local contra la última disponible en GitHub.
2. **Descarga:** Si detecta una versión superior, descarga el paquete actualizado.
3. **Hot-Swap:** Sustituye los archivos antiguos y reinicia la aplicación automáticamente.

---

## 🏗 Arquitectura Técnica

**HermesApp/**  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── ⚓ **pyinstaller_hooks/** — Hooks personalizados para el empaquetado  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 🖼️ **logo.ico** — Icono oficial del ejecutable  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 🐍 **main.py** — Punto de entrada de la aplicación  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 📄 **HermesApp.spec** — Configuración para PyInstaller  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 🔐 **.env** — Configuración de base de datos (No incluido en Git)  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── 📂 **app/**  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 🗄️ **daos/** — Acceso a datos (UserDAO, ProductDAO, CartDAO)  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── ⚙️ **managers/** — Lógica de negocio (Auth, App, DB, Product, Scraper)  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 📐 **models/** — Contratos y esquemas de datos  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 🕷️ **scrapers/** — Motores de extracción por supermercado  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── 🛠️ **utils/** — SSL Patches, Logs, Rutas y Actualización  

### Características técnicas principales

* **Entorno:** Python 3.11.9 (optimizado para PyInstaller)
* **Concurrencia:** Ejecución paralela mediante ThreadPoolExecutor
* **Networking:** Uso de requests.Session con pool de conexiones persistentes
* **Estructura:** Gestión centralizada de rutas y generación estructurada de JSON

---

## 👨‍💻 Desarrollo desde cero (Build Manual)

### Clonar el repositorio
```bash
git clone https://github.com/BranBPDev/HermesApp.git
```

### Moverse a la carpeta del proyecto
```bash
cd HermesApp
```

### Crear entorno virtual (Python 3.11.9)
```bash
py -3.11 -m venv venv
```

### Activar entorno virtual
```bash
.\venv\Scripts\activate
```

### Actualizar herramientas de Python
```bash
python -m pip install --upgrade pip setuptools wheel
```

### Instalar dependencias necesarias
```bash
pip install certifi requests urllib3 pyinstaller httpx h2 psycopg2-binary bcrypt python-dotenv customtkinter Pillow
```

### Limpiar compilaciones previas
```bash
rmdir /s /q dist build 2>nul
```

### Generar ejecutable con PyInstaller
```bash
pyinstaller HermesApp.spec
```

### Salir del entorno virtual
```bash
deactivate
```  

> ⚠️ Es importante que el `.exe` use el archivo `app/data/version.json` correspondiente, pero no junto con el código fuente, para evitar conflictos.

```text
{
    "name": "HermesApp",
    "description": "La forma más rápida e inteligente de comparar precios entre supermercados en España y ahorrar en cada compra.",
    "version": "0.0.0",
    "releaseDate": "2026-02-20",
    "author": "BranBP",
    "repository": "https://github.com/BranBPDev/HermesApp"
}
```

---

## 🔑 Configuración de Variables de Entorno
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

## 🧠 Estado del Proyecto

HermesApp se encuentra en desarrollo activo.

Metas del proyecto:
* ✅ Aplicación auto-actualizable.
* ✅ Base de Datos Cloud: PostgreSQL integrado.
* ✅ Sistema de Usuarios: Login y registro funcional.
* ✅ Carrito Multi-tienda: Comparación y suma de productos de distintas fuentes.
* 🚧 Interfaz de Usuario (GUI): En planificación.
* 🚧 Gadis: Scraper en fase de re-estructuración.

---

## 📜 Licencia

Proyecto en desarrollo. Uso educativo y experimental.