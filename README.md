# HermesApp 🛒

**HermesApp** es una aplicación de escritorio diseñada para comparar precios de productos entre distintos supermercados de España de forma automática. La aplicación recopila datos directamente desde las plataformas online, los procesa en paralelo y construye una base de datos unificada.

<div align="center">
  <img src="https://img.shields.io/badge/Estado-Operativo-238636?style=for-the-badge" alt="Operativo">
  <img src="https://img.shields.io/badge/Python-3.11.9-blue?style=for-the-badge&logo=python" alt="Python Version">
</div>

---

## 📖 Documentación Completa

* 🚀 [**Instalación y Descargas**](docs/instalacion.md): Cómo obtener el ejecutable o compilar desde cero.
* ⌨️ [**Guía de Uso y Comandos**](docs/guia_uso.md): Comandos del buscador y sistema de actualizaciones.
* 🏗️ [**Arquitectura y Desarrollo**](docs/arquitectura.md): Estructura del código, tecnologías y lógica interna.
* 🔑 [**Configuración y Logs**](docs/configuracion.md): Variables de entorno (.env) y sistema de depuración.
* 👨‍💻 [**Desarrollo desde cero**](docs/desarrollo.md): Instrucciones para configurar el entorno y compilar.

---

## ¿Qué hace HermesApp?

* **Autenticación:** Sistema de usuarios con contraseñas seguras (bcrypt).
* **Recolección:** Scraping multihilo sincronizado en tiempo real con la nube.
* **Sincronización:** Operaciones masivas (Upsert) en base de datos PostgreSQL (Neon DB).
* **Comparación:** Búsqueda unificada que mezcla y ordena productos de diferentes tiendas por precio.
* **Carrito de compra:** Gestión de listas personalizadas con cálculo de totales por usuario.

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

## 🧠 Roadmap del Proyecto

* ✅ Aplicación auto-actualizable.
* ✅ Base de Datos Cloud (PostgreSQL).
* ✅ Sistema de Usuarios (Auth con bcrypt).
* 🚧 Interfaz Gráfica (GUI) Avanzada (CustomTkinter).
* 🚧 Integración completa de Gadis.

---
**Desarrollado por [BranBP](https://github.com/BranBPDev)**






---

---

---

## 👨‍💻 Desarrollo desde cero (Build Manual)

<details>
<summary><strong>Instrucciones para configurar el entorno y compilar</strong></summary>

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

</details>