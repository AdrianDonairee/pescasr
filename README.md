# 🐟 pescasr - Backend

Proyecto de backend para un e-commerce de artículos de pesca, desarrollado como parte de la carrera de Ingeniería en Informática en la Universidad de Mendoza.

## 📌 Descripción

**pescasr** es un sistema de comercio electrónico orientado a la venta de artículos de pesca. Esta parte del proyecto representa el backend del sistema, encargado de la lógica de negocio, la gestión de datos y la conexión con la base de datos MySQL. Está desarrollado utilizando el framework **Django**, con el objetivo de garantizar una arquitectura robusta, segura y escalable.

## ⚙️ Funcionalidades principales

- Gestión de usuarios y autenticación.
- Administración de productos de pesca (CRUD).
- Manejo de categorías y stock.
- Registro y consulta de transacciones.
- API RESTful para comunicación con el frontend.
- Validación de formularios y seguridad básica integrada.

## 🧰 Tecnologías utilizadas

- **Lenguaje:** Python 3.12
- **Framework:** Django 5.x
- **Base de datos:** MySQL
- **ORM:** Django ORM
- **Control de versiones:** Git + GitHub
- **Entorno de desarrollo:** VS Code
- **Gestión de entorno:** `venv` (entorno virtual de Python)
- **Otros:** Postman (para pruebas de endpoints), DBeaver (gestión de base de datos)

## 🗃️ Estructura del proyecto

```
pescasr/
├── pescasr/               # Configuración principal del proyecto Django
├── tienda/                # Aplicación principal (productos, transacciones, etc.)
├── usuarios/              # Aplicación secundaria para autenticación y usuarios
├── manage.py              # Script de gestión de Django
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Este archivo
```

## 🛠️ Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/usuario/pescasr.git
cd pescasr
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar base de datos

Editar `settings.py` con los datos de conexión MySQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pescasr',
        'USER': 'root',
        'PASSWORD': 'Ecommerce2025$',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 4. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear superusuario

```bash
python manage.py createsuperuser
```

### 6. Iniciar el servidor

```bash
python manage.py runserver
```

Acceder a: [http://localhost:8000](http://localhost:8000)

## 🔌 Endpoints destacados

- `/admin/` – Panel de administración de Django
- `/api/productos/` – API REST para productos
- `/api/usuarios/` – Registro y login de usuarios
- `/api/transacciones/` – Consulta de transacciones

## ✅ Validaciones y seguridad

- Se usan expresiones regulares para validar datos (correos, nombres, precios, etc.).
- Autenticación con tokens (opcional si se integra con DRF).
- Protección CSRF y validaciones integradas de Django.

## 🧪 Pruebas

- Pruebas manuales realizadas con Postman.
- Verificación de endpoints de inserción, actualización y borrado.
- Validación de relaciones entre modelos: productos, usuarios, transacciones.

## 📄 Licencia

Proyecto desarrollado con fines educativos. Licencia libre para revisión académica.
