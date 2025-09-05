# Documentación de la API - ConstructMarket

Esta documentación describe todos los endpoints disponibles en la API de ConstructMarket.

## Base URL

```
http://localhost:5000/api
```

## Autenticación

La API utiliza JSON Web Tokens (JWT) para la autenticación. Incluye el token en el header `Authorization`:

```
Authorization: Bearer <tu-jwt-token>
```

## Endpoints

### Autenticación

#### POST /auth/register
Registra un nuevo usuario en la plataforma.

**Request Body:**
```json
{
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "password": "password123",
  "phone": "+1234567890",
  "user_type": "both"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Usuario registrado exitosamente",
  "user": {
    "id": 1,
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "user_type": "both"
  }
}
```

#### POST /auth/login
Inicia sesión y obtiene un token JWT.

**Request Body:**
```json
{
  "email": "juan@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login exitoso",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "user_type": "both"
  }
}
```

### Usuarios

#### GET /users/profile
Obtiene el perfil del usuario autenticado.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "phone": "+1234567890",
    "user_type": "both",
    "verification_status": "verified",
    "rating": 4.5,
    "created_at": "2025-01-01T00:00:00Z"
  }
}
```

#### PUT /users/profile
Actualiza el perfil del usuario autenticado.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "name": "Juan Carlos Pérez",
  "phone": "+1234567891"
}
```

### Equipos

#### GET /equipment
Obtiene una lista de equipos con filtros opcionales.

**Query Parameters:**
- `search` (string): Búsqueda por título o descripción
- `category` (string): Filtrar por categoría
- `location` (string): Filtrar por ubicación
- `type` (string): "sale", "rent", o vacío para ambos
- `min_price` (number): Precio mínimo
- `max_price` (number): Precio máximo
- `page` (number): Número de página (default: 1)
- `per_page` (number): Elementos por página (default: 20)

**Response:**
```json
{
  "success": true,
  "data": {
    "equipment": [
      {
        "id": 1,
        "title": "Excavadora CAT 320",
        "description": "Excavadora en excelente estado",
        "category": "Excavadoras",
        "location": "Ciudad de México",
        "is_for_sale": true,
        "is_for_rent": true,
        "price_sale": 250000,
        "price_rent_daily": 1500,
        "price_rent_weekly": 9000,
        "availability_status": "available",
        "owner_name": "Juan Pérez",
        "images": ["url1.jpg", "url2.jpg"]
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 1,
      "pages": 1
    }
  }
}
```

#### GET /equipment/{id}
Obtiene los detalles de un equipo específico.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Excavadora CAT 320",
    "description": "Excavadora en excelente estado con mantenimiento al día",
    "category": "Excavadoras",
    "location": "Ciudad de México",
    "is_for_sale": true,
    "is_for_rent": true,
    "price_sale": 250000,
    "price_rent_daily": 1500,
    "price_rent_weekly": 9000,
    "availability_status": "available",
    "owner_id": 1,
    "owner_name": "Juan Pérez",
    "images": ["url1.jpg", "url2.jpg"],
    "specifications": {
      "año": "2020",
      "horas": "1500",
      "peso": "20 toneladas"
    },
    "created_at": "2025-01-01T00:00:00Z"
  }
}
```

#### POST /equipment
Crea un nuevo equipo (requiere autenticación).

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "title": "Excavadora CAT 320",
  "description": "Excavadora en excelente estado",
  "category": "Excavadoras",
  "location": "Ciudad de México",
  "is_for_sale": true,
  "is_for_rent": true,
  "price_sale": 250000,
  "price_rent_daily": 1500,
  "price_rent_weekly": 9000,
  "specifications": {
    "año": "2020",
    "horas": "1500"
  }
}
```

### Transacciones

#### POST /transactions
Crea una nueva transacción.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "equipment_id": 1,
  "transaction_type": "sale",
  "amount": 250000,
  "start_date": "2025-01-15",
  "end_date": null
}
```

**Response:**
```json
{
  "success": true,
  "message": "Transacción creada exitosamente",
  "transaction": {
    "id": 1,
    "equipment_id": 1,
    "buyer_id": 2,
    "seller_id": 1,
    "transaction_type": "sale",
    "amount": 250000,
    "commission": 12500,
    "status": "pending",
    "created_at": "2025-01-01T00:00:00Z"
  }
}
```

#### GET /transactions/my-purchases
Obtiene las compras del usuario autenticado.

#### GET /transactions/my-sales
Obtiene las ventas del usuario autenticado.

## Códigos de Estado HTTP

- `200` - OK
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## Manejo de Errores

Todas las respuestas de error siguen este formato:

```json
{
  "success": false,
  "message": "Descripción del error",
  "error_code": "ERROR_CODE"
}
```

