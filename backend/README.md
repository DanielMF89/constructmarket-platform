


# Proyecto Marketplace de Maquinaria de Construcción

Este proyecto es una aplicación web completa de marketplace que permite a los usuarios registrarse para vender o rentar maquinaria de construcción. La plataforma incluye un sistema de comisiones por cada transacción.

## Arquitectura General

La aplicación está construida con una arquitectura de microservicios, con un backend en Flask (Python) y un frontend en React (JavaScript).

- **Backend (Flask):** Proporciona una API RESTful para gestionar usuarios, equipos, transacciones y autenticación.
- **Frontend (React):** Una aplicación de una sola página (SPA) que consume la API del backend para proporcionar una interfaz de usuario interactiva y moderna.
- **Base de Datos:** SQLite para desarrollo y PostgreSQL para producción.
- **Autenticación:** Se utiliza JSON Web Tokens (JWT) para proteger las rutas de la API.




## Instalación y Ejecución

Sigue estos pasos para instalar y ejecutar el proyecto en un entorno de desarrollo local.

### Prerrequisitos

- Python 3.11 o superior
- Node.js 20 o superior
- pnpm (o npm/yarn)

### Backend (Flask)

1. **Navega al directorio del backend:**
   ```bash
   cd marketplace-backend
   ```

2. **Crea y activa un entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecuta la aplicación:**
   ```bash
   python src/main.py
   ```

   El backend se ejecutará en `http://localhost:5000`.

### Frontend (React)

1. **Navega al directorio del frontend:**
   ```bash
   cd marketplace-frontend
   ```

2. **Instala las dependencias:**
   ```bash
   pnpm install
   ```

3. **Ejecuta la aplicación:**
   ```bash
   pnpm run dev
   ```

   El frontend se ejecutará en `http://localhost:5173`.




## Estructura del Proyecto

El proyecto está organizado en dos directorios principales: `marketplace-backend` y `marketplace-frontend`.

### Backend (`marketplace-backend`)

```
marketplace-backend/
├── src/
│   ├── models/       # Modelos de base de datos (SQLAlchemy)
│   ├── routes/       # Rutas de la API (Blueprints de Flask)
│   ├── static/       # Archivos estáticos (para servir el frontend)
│   ├── main.py       # Punto de entrada de la aplicación Flask
│   └── database/
│       └── app.db    # Base de datos SQLite
├── venv/             # Entorno virtual de Python
└── requirements.txt  # Dependencias de Python
```

### Frontend (`marketplace-frontend`)

```
marketplace-frontend/
├── public/           # Archivos públicos
├── src/
│   ├── assets/       # Activos estáticos (imágenes, etc.)
│   ├── components/   # Componentes reutilizables de React
│   ├── contexts/     # Contextos de React (ej. AuthContext)
│   ├── hooks/        # Hooks personalizados de React
│   ├── lib/          # Funciones de utilidad
│   ├── pages/        # Componentes de página (vistas)
│   ├── App.jsx       # Componente principal de la aplicación
│   ├── main.jsx      # Punto de entrada de React
│   └── index.css     # Estilos globales
├── package.json      # Dependencias y scripts de Node.js
└── vite.config.js    # Configuración de Vite
```




## Funcionalidades Principales

- **Sistema de Usuarios:** Registro, login, perfiles de usuario, y sistema de calificaciones.
- **Gestión de Maquinaria:** Publicación de equipos para venta o renta, catálogo con filtros y búsqueda avanzada.
- **Sistema de Transacciones:** Proceso de compra y renta, cálculo automático de comisiones, y contratos digitales.
- **Panel de Administración:** Gestión de usuarios, equipos, y transacciones, con reportes y estadísticas.
- **Sistema de Comisiones:** Configuración de comisiones para ventas y rentas.




## Endpoints de la API

A continuación se describen los principales endpoints de la API del backend.

### Autenticación

- `POST /api/auth/register`: Registrar un nuevo usuario.
- `POST /api/auth/login`: Iniciar sesión y obtener un token JWT.

### Usuarios

- `GET /api/users/profile`: Obtener el perfil del usuario autenticado.
- `PUT /api/users/profile`: Actualizar el perfil del usuario autenticado.
- `GET /api/users/<id>`: Obtener información pública de un usuario.
- `GET /api/users`: Obtener una lista de todos los usuarios (solo admin).

### Equipos

- `GET /api/equipment`: Obtener una lista de equipos con filtros.
- `GET /api/equipment/<id>`: Obtener detalles de un equipo.
- `POST /api/equipment`: Crear un nuevo equipo (requiere autenticación).
- `PUT /api/equipment/<id>`: Actualizar un equipo (propietario o admin).
- `DELETE /api/equipment/<id>`: Eliminar un equipo (propietario o admin).

### Transacciones

- `POST /api/transactions`: Crear una nueva transacción (compra o renta).
- `GET /api/transactions/<id>`: Obtener detalles de una transacción.
- `PUT /api/transactions/<id>/status`: Actualizar el estado de una transacción.
- `GET /api/transactions/my-purchases`: Obtener las compras del usuario.
- `GET /api/transactions/my-sales`: Obtener las ventas del usuario.




## Despliegue

Para desplegar la aplicación en un entorno de producción, sigue estos pasos:

1. **Construye el frontend:**
   ```bash
   cd marketplace-frontend
   pnpm run build
   ```

2. **Copia los archivos del frontend al backend:**
   Copia el contenido del directorio `marketplace-frontend/dist` al directorio `marketplace-backend/src/static`.

3. **Configura el backend para producción:**
   - Utiliza un servidor WSGI como Gunicorn o uWSGI.
   - Configura una base de datos PostgreSQL en lugar de SQLite.
   - Desactiva el modo de depuración en Flask.

4. **Ejecuta el servidor de producción:**
   ```bash
   gunicorn -w 4 'src.main:app'
   ```




## Tecnologías Utilizadas

- **Backend:**
  - Flask
  - SQLAlchemy
  - Flask-CORS
  - PyJWT

- **Frontend:**
  - React
  - Vite
  - Tailwind CSS
  - shadcn/ui
  - Lucide Icons
  - React Router

- **Base de Datos:**
  - SQLite (desarrollo)
  - PostgreSQL (producción)




## Autor

Este proyecto fue desarrollado por Manus, un agente de IA autónomo.


