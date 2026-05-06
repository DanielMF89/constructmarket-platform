# ConstructMarket — Marketplace de Maquinaria de Construcción

![Flask](https://img.shields.io/badge/Flask-3.1-blue?logo=flask)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)
![Python](https://img.shields.io/badge/Python-3.11+-green?logo=python)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

Plataforma web full-stack para la compra, venta y renta de maquinaria de construcción. Incluye autenticación JWT, catálogo con filtros avanzados, sistema de transacciones con comisiones automáticas y panel de administración.

---

## ✨ Características

- **Autenticación JWT** — registro, login y gestión de sesiones segura
- **Catálogo de equipos** — búsqueda y filtros por categoría, ubicación y precio
- **Compra y renta** — sistema de transacciones con cálculo automático de comisiones
- **Panel de administración** — gestión de usuarios, equipos y reportes financieros
- **API RESTful** — backend documentado con Flask y SQLAlchemy
- **Diseño responsivo** — interfaz moderna con Tailwind CSS y shadcn/ui

---

## 🏗️ Arquitectura

```
constructmarket-platform/
├── backend/              # API REST (Python + Flask)
│   ├── src/
│   │   ├── models/       # Modelos SQLAlchemy
│   │   ├── routes/       # Endpoints de la API
│   │   └── main.py       # Punto de entrada
│   └── requirements.txt
├── frontend/             # SPA (React + Vite)
│   └── src/
│       ├── components/
│       └── pages/
└── docs/
    └── API.md            # Documentación de la API
```

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| Frontend | React 19, Vite, Tailwind CSS, shadcn/ui |
| Backend | Python 3.11, Flask 3.1, SQLAlchemy |
| Auth | JWT (PyJWT) |
| API | REST + Flask-CORS |
| Base de datos | SQLite (dev) / PostgreSQL (prod) |

---

## 🚀 Instalación

### Prerrequisitos
- Python 3.11+
- Node.js 20+
- pnpm

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

### Frontend
```bash
cd frontend
pnpm install
pnpm run dev
```

La aplicación estará disponible en:
- **Frontend:** http://localhost:5173
- **API:** http://localhost:5000

### Variables de entorno

Crea `backend/.env`:
```env
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta
DATABASE_URL=sqlite:///database/app.db
JWT_SECRET_KEY=tu-jwt-secret
```

---

## 📡 API — Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/auth/register` | Registrar usuario |
| POST | `/api/auth/login` | Iniciar sesión |
| GET | `/api/equipment` | Listar equipos |
| POST | `/api/equipment` | Publicar equipo |
| GET | `/api/equipment/{id}` | Detalle de equipo |
| POST | `/api/transactions` | Crear transacción |
| GET | `/api/transactions/my-purchases` | Mis compras |
| GET | `/api/transactions/my-sales` | Mis ventas |

Documentación completa en [`docs/API.md`](docs/API.md).

---

## 📄 Licencia

MIT — ver [LICENSE](LICENSE).
