# 🏗️ Arquitectura y Desarrollo

**HermesApp/**  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 🖼️ **logo.ico** — Icono oficial del ejecutable  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 🐍 **main.py** — Punto de entrada de la aplicación  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 📄 **HermesApp.spec** — Configuración para PyInstaller  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 🔐 **.env** — Configuración de base de datos (No incluido en Git)  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── 📂 **app/**  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── ⚙️ **config/** — Configuración de scrapers y selectores  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 🗄️ **daos/** — Acceso a datos (UserDAO, ProductDAO, CartDAO)  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 🧠 **managers/** — Lógica de negocio (Auth, App, DB, Product, Scraper)  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 📐 **models/** — Contratos y esquemas de datos  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 🕷️ **scrapers/** — Motores de extracción por supermercado  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 🖼️ **gui/** — Interfaz gráfica basada en Tkinter  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;├── 📂 **components/** — Componentes  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;├── 📂 **styles/** — Estilos  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── 🛠️ **utils/** — Utilidades  

## Características técnicas principales

* **Entorno:** Python 3.11.9 (optimizado para PyInstaller)
* **Concurrencia:** Ejecución paralela mediante ThreadPoolExecutor
* **Networking:** Uso de requests.Session con pool de conexiones persistentes
* **Estructura:** Gestión centralizada de rutas y generación estructurada de JSON
* **Seguridad:** Gestión de credenciales mediante crypto_util.py y hashing con bcrypt
* **Interfaz Gráfica:** Desarrollada con CustomTkinter para un acabado moderno y escalable
* **Persistencia:** PostgreSQL alojado en Neon DB con una capa de DAOs para transacciones seguras