# 📚 Sistema de Gestión de Biblioteca – Grupo A

Aplicación de escritorio para gestionar una biblioteca, desarrollada en **Python** con la librería **[Flet](https://flet.dev/)**. Permite registrar clientes, libros, gestionar préstamos y devoluciones, con una interfaz moderna, búsqueda inteligente y persistencia de datos local.

---

##  Integrantes
- Keytlen Mata 
- Brayan Abrego
- Georgina Hanna
- Iván Rodríguez
- Edgar García

---

## ✨ Características Implementadas

- 👤 **Gestión de clientes**:  
  - Registro, búsqueda, edición y eliminación.
  - Validación de datos (solo letras en nombre/apellido, cédula única).
- 📖 **Inventario de libros**:  
  - Registro, búsqueda, edición y eliminación.
  - Estados: *Disponible* / *Prestado*.
- 🔄 **Préstamos y devoluciones**:  
  - Asignación de libros a clientes con plazo personalizable.
  - Validación: no se prestan libros no disponibles ni a clientes inexistentes.
- 🔍 **Búsqueda inteligente**:  
  - Filtra por nombre, apellido, título, autor o ISBN (ignora acentos y mayúsculas).
- 🔤 **Orden alfabético**:  
  - Clientes ordenados por apellido → nombre.
  - Libros ordenados por título.
- 🌙 **Interfaz moderna en modo oscuro**:  
  - Diseño limpio, colores coherentes, íconos intuitivos.
- 💾 **Persistencia local**:  
  - Todos los datos se guardan automáticamente en archivos JSON (`data/`).

---

## 🛠️ Requisitos

- Python 3.9 o superior
- Git (para clonar el repositorio)

---

## 🚀 Cómo ejecutar la aplicación

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/KeytlenMata/BibliotecaFlet.git
   cd BibliotecaFlet

2. **Crea y activa un entorno virtual**
   python -m venv venv
   # En Windows (Git Bash):
   source venv/Scripts/activate

4. **Instala las dependencias**
   pip install flet==0.24.1 python-dotenv==1.0.1

5. **Ejecuta la aplicación**
   cd ProyectoFinal
   python main.py
   
