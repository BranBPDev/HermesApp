# HermesApp 🛒

**HermesApp** es una aplicación de escritorio diseñada para comparar precios de productos entre distintos supermercados de España de forma automática. La aplicación recopila datos directamente desde las plataformas online de cada supermercado, los procesa en paralelo y construye una base de datos unificada para su comparación.

---

## 🚀 ¿Qué es HermesApp?

HermesApp automatiza el flujo completo de información:

* **Recolección:** Scraping multihilo desde múltiples supermercados.
* **Normalización:** Estructuración de datos heterogéneos en un esquema único.
* **Persistencia:** Generación de archivos en formato JSON para análisis.
* **Mantenimiento:** Sistema de auto-actualización integrado desde GitHub.
* **Portabilidad:** Distribución como ejecutable `.exe` sin dependencias externas.

El objetivo del proyecto es desarrollar un comparador de precios funcional, preciso y escalable.

---

## 🏪 Supermercados Soportados Actualmente
<div align="center">
  <table style="width: 100%; max-width: 800px; border-collapse: separate; border-spacing: 0; border: 1px solid #30363d; border-radius: 12px; overflow: hidden;">
    <thead>
      <tr style="background-color: #161b22; color: #f0f6fc;">
        <th align="center" valign="middle" style="padding: 15px; border-bottom: 2px solid #30363d;"><b>Supermercado</b></th>
        <th align="center" valign="middle" style="padding: 15px; border-bottom: 2px solid #30363d;"><b>Estado</b></th>
        <th align="center" valign="middle" style="padding: 15px; border-bottom: 2px solid #30363d;"><b>Productos</b></th>
        <th align="center" valign="middle" style="padding: 15px; border-bottom: 2px solid #30363d;"><b>Tiempo</b></th>
      </tr>
    </thead>
    <tbody>
      <tr style="background-color: #0d1117; color: #c9d1d9;">
        <td align="center" valign="middle" style="padding: 20px; border-bottom: 1px solid #21262d;"><b>Mercadona</b></td>
        <td align="center" valign="middle" style="padding: 20px; border-bottom: 1px solid #21262d;">
          <b style="background-color: #238636; color: #ffffff; padding: 4px 12px; border-radius: 4px;">Operativo</b>
        </td>
        <td align="center" valign="middle" style="padding: 20px; border-bottom: 1px solid #21262d;">~4000+</td>
        <td align="center" valign="middle" style="padding: 20px; border-bottom: 1px solid #21262d;">2-4 segundos</td>
      </tr>
      <tr style="background-color: #161b22; color: #c9d1d9;">
        <td align="center" valign="middle" style="padding: 20px; border-bottom: 1px solid #21262d;"><b>Eroski</b></td>
        <td align="center" valign="middle" style="padding: 20px; border-bottom: 1px solid #21262d;">
          <b style="background-color: #d29922; color: #ffffff; padding: 4px 12px; border-radius: 4px;">En Revisión</b>
        </td>
        <td align="center" valign="middle" style="padding: 20px; border-bottom: 1px solid #21262d;">~4000+</td>
        <td align="center" valign="middle" style="padding: 20px; border-bottom: 1px solid #21262d;">15-20 segundos</td>
      </tr>
      <tr style="background-color: #0d1117; color: #c9d1d9;">
        <td align="center" valign="middle" style="padding: 20px;"><b>Gadis</b></td>
        <td align="center" valign="middle" style="padding: 20px;">
          <b style="background-color: #da3633; color: #ffffff; padding: 4px 12px; border-radius: 4px;">En Desarrollo</b>
        </td>
        <td align="center" valign="middle" style="padding: 20px;">-</td>
        <td align="center" valign="middle" style="padding: 20px;">-</td>
      </tr>
    </tbody>
  </table>
</div>

---

## ⬇️ Descarga (IMPORTANTE)

Para utilizar HermesApp debes descargar la aplicación desde la sección de **Releases**:

👉 [**Descargar última versión en Releases**](https://github.com/BranBPDev/HermesApp/releases/latest)

> ⚠️ **No descargues el código fuente (ZIP desde el botón "Code")** para uso normal. La versión de Releases incluye el ejecutable listo para usar y el sistema de auto-actualización.

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
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 🐍 **main.py** — Punto de entrada de la aplicación  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 📄 **HermesApp.spec** — Configuración para PyInstaller  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── 📂 **app/**  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── ⚙️ **managers/** — Gestión de ejecución paralela (*Thread Management*)  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 📐 **models/** — Clases base y contratos de scrapers  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── 🕷️ **scrapers/** — Implementaciones específicas por supermercado  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── 🛠️ **utils/** — Utilidades (descarga, JSON, actualización, rutas)

### Características técnicas principales

* **Entorno:** Python 3.11.9 (optimizado para PyInstaller)
* **Concurrencia:** Ejecución paralela mediante ThreadPoolExecutor
* **Networking:** Uso de requests.Session con pool de conexiones persistentes
* **Estructura:** Gestión centralizada de rutas y generación estructurada de JSON

---

## 💻 Uso del Ejecutable

1. Descarga el `.exe` desde Releases.
2. Copia el archivo a una carpeta vacía para evitar conflictos.
3. Ejecuta el archivo `.exe`.

La aplicación gestionará automáticamente la verificación de versión, el scraping paralelo y la generación de archivos JSON.

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
pip install certifi requests urllib3 pyinstaller httpx h2
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

## 📁 Sistema de Logs
Para facilitar el mantenimiento, la aplicación genera logs detallados en la carpeta raíz:
`logs/hermesApp.log`

* **INFO:** Seguimiento del flujo (Inicios/Finales de scrapers).
* **DEBUG:** Detalles técnicos (URLs procesadas, inyección de cookies).
* **ERROR:** Fallos específicos de red o parseo de datos (ver Tracebacks).

---

## 🧠 Estado del Proyecto

HermesApp se encuentra en desarrollo activo.

Próximas metas:

* 🎨 Interfaz de Usuario (GUI)
* ⚖️ Comparador Estructurado
* 🔍 Búsqueda Avanzada

---

## 📜 Licencia

Proyecto en desarrollo. Uso educativo y experimental.