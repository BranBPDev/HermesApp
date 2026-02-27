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

| Supermercado | Estado |
| :--- | :--- |
| **Mercadona** | ✅ Operativo |
| **Lidl** | ✅ Operativo |
| **Gadis** | ✅ Operativo |
| **Eroski** | ✅ Operativo |

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

```text
app/  
├── managers/        → Gestión de ejecución paralela (Thread Management)
├── models/          → Clases base y contratos de scrapers
├── scrapers/        → Implementaciones específicas por supermercado
├── utils/           → Utilidades (descarga, JSON, actualización, rutas)
main.py              → Punto de entrada de la aplicación
HermesApp.spec       → Configuración para PyInstaller
pyinstaller_hooks/   → Hooks personalizados para el empaquetado
```

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

```bash
git clone https://github.com/BranBPDev/HermesApp.git
cd HermesApp
py -3.11 -m venv venv
.\venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
pip install certifi requests urllib3 pyinstaller
rmdir /s /q dist build 2>nul
pyinstaller HermesApp.spec
```

---

## 🧠 Estado del Proyecto

HermesApp se encuentra en desarrollo activo.

Próximas metas:

* 🎨 Interfaz de Usuario (GUI)
* ⚖️ Comparador Estructurado
* 🔍 Búsqueda Avanzada
* 🗄️ Persistencia en SQLite

---

## 📜 Licencia

Proyecto en desarrollo. Uso educativo y experimental.