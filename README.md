# ConstructMarket - Marketplace de Maquinaria de Construcción

![ConstructMarket](https://img.shields.io/badge/ConstructMarket-v1.0.0-orange)
![Flask](https://img.shields.io/badge/Flask-2.3.3-blue)
![React](https://img.shields.io/badge/React-19.1.0-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![Node.js](https://img.shields.io/badge/Node.js-20+-green)

Una plataforma web completa de marketplace que permite a los usuarios registrarse para comprar, vender o rentar maquinaria de construcción. La plataforma incluye un sistema de comisiones automático por cada transacción realizada.

## 🚀 Características Principales

- **Sistema de Usuarios Completo**: Registro, autenticación JWT, perfiles y calificaciones
- **Catálogo de Equipos**: Búsqueda avanzada, filtros por categoría, ubicación y precio
- **Transacciones Seguras**: Sistema de compra y renta con cálculo automático de comisiones
- **Panel de Administración**: Gestión de usuarios, equipos y reportes financieros
- **Diseño Responsivo**: Interfaz moderna y adaptable a dispositivos móviles
- **API RESTful**: Backend robusto con documentación completa

## 🏗️ Arquitectura

```
constructmarket-platform/
├── backend/          # API Flask (Python)
├── frontend/         # Aplicación React (JavaScript)
├── docs/            # Documentación adicional
└── README.md        # Este archivo
```

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask** - Framework web de Python
- **SQLAlchemy** - ORM para base de datos
- **JWT** - Autenticación segura
- **Flask-CORS** - Manejo de CORS
- **SQLite/PostgreSQL** - Base de datos

### Frontend
- **React 19** - Biblioteca de interfaz de usuario
- **Vite** - Herramienta de construcción rápida
- **Tailwind CSS** - Framework de CSS utilitario
- **shadcn/ui** - Componentes de UI modernos
- **React Router** - Enrutamiento del lado del cliente

## 🚀 Instalación Rápida

### Prerrequisitos
- Python 3.11+
- Node.js 20+
- pnpm (recomendado) o npm

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/constructmarket-platform.git
cd constructmarket-platform
```

### 2. Configurar el Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

### 3. Configurar el Frontend
```bash
cd frontend
pnpm install
pnpm run dev
```

### 4. Acceder a la aplicación
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

## 📱 Capturas de Pantalla

### Página Principal
![Página Principal](docs/screenshots/home.png)

### Panel de Usuario
![Dashboard](docs/screenshots/dashboard.png)

### Catálogo de Equipos
![Catálogo](docs/screenshots/catalog.png)

## 🔧 Configuración de Desarrollo

### Variables de Entorno

Crea un archivo `.env` en el directorio `backend/`:

```env
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=sqlite:///database/app.db
JWT_SECRET_KEY=tu-jwt-secret-aqui
```

### Base de Datos

La aplicación creará automáticamente las tablas necesarias al ejecutarse por primera vez.

## 🚀 Despliegue en Producción

### Opción 1: Despliegue Tradicional

1. **Construir el frontend:**
   ```bash
   cd frontend
   pnpm run build
   ```

2. **Configurar el backend para producción:**
   ```bash
   cd backend
   pip install gunicorn
   gunicorn -w 4 'src.main:app'
   ```

### Opción 2: Docker (Próximamente)

```bash
docker-compose up -d
```

## 📚 Documentación de la API

### Endpoints Principales

#### Autenticación
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/login` - Iniciar sesión

#### Equipos
- `GET /api/equipment` - Listar equipos
- `POST /api/equipment` - Crear equipo
- `GET /api/equipment/{id}` - Obtener equipo específico

#### Transacciones
- `POST /api/transactions` - Crear transacción
- `GET /api/transactions/my-purchases` - Mis compras
- `GET /api/transactions/my-sales` - Mis ventas

Para documentación completa de la API, consulta [backend/README.md](backend/README.md).

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Equipo

- **Desarrollador Principal**: Manus AI Agent
- **Arquitectura**: Full-stack con Flask + React
- **Diseño**: Interfaz moderna con Tailwind CSS

## 📞 Soporte

Si tienes preguntas o necesitas ayuda:

- 📧 Email: support@constructmarket.com
- 🐛 Issues: [GitHub Issues](https://github.com/tu-usuario/constructmarket-platform/issues)
- 📖 Documentación: [Wiki del proyecto](https://github.com/tu-usuario/constructmarket-platform/wiki)

## 🎯 Roadmap

- [ ] Sistema de mensajería entre usuarios
- [ ] Integración con pasarelas de pago
- [ ] Aplicación móvil (React Native)
- [ ] Sistema de geolocalización avanzado
- [ ] Integración con APIs de logística
- [ ] Dashboard de analytics avanzado

---

⭐ **¡Si te gusta este proyecto, dale una estrella en GitHub!** ⭐

