# Guía de Contribución - ConstructMarket

¡Gracias por tu interés en contribuir a ConstructMarket! Esta guía te ayudará a comenzar.

## 🚀 Cómo Contribuir

### 1. Fork del Repositorio

1. Haz fork del repositorio en GitHub
2. Clona tu fork localmente:
   ```bash
   git clone https://github.com/tu-usuario/constructmarket-platform.git
   cd constructmarket-platform
   ```

### 2. Configuración del Entorno de Desarrollo

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend
```bash
cd frontend
pnpm install
```

### 3. Crear una Rama

```bash
git checkout -b feature/nombre-de-tu-feature
```

### 4. Realizar Cambios

- Sigue las convenciones de código existentes
- Escribe tests para nuevas funcionalidades
- Actualiza la documentación si es necesario

### 5. Commit y Push

```bash
git add .
git commit -m "feat: descripción clara de los cambios"
git push origin feature/nombre-de-tu-feature
```

### 6. Crear Pull Request

1. Ve a GitHub y crea un Pull Request
2. Describe claramente los cambios realizados
3. Referencia cualquier issue relacionado

## 📝 Convenciones de Código

### Python (Backend)
- Sigue PEP 8
- Usa type hints cuando sea posible
- Documenta funciones con docstrings
- Nombres de variables en snake_case

### JavaScript (Frontend)
- Usa ESLint y Prettier
- Componentes en PascalCase
- Variables y funciones en camelCase
- Usa JSDoc para documentar funciones complejas

### Commits
Usa el formato de Conventional Commits:

- `feat:` nueva funcionalidad
- `fix:` corrección de bug
- `docs:` cambios en documentación
- `style:` cambios de formato
- `refactor:` refactorización de código
- `test:` agregar o modificar tests
- `chore:` tareas de mantenimiento

## 🧪 Testing

### Backend
```bash
cd backend
python -m pytest tests/
```

### Frontend
```bash
cd frontend
pnpm test
```

## 📋 Checklist antes de enviar PR

- [ ] El código sigue las convenciones establecidas
- [ ] Se agregaron tests para nuevas funcionalidades
- [ ] Todos los tests pasan
- [ ] La documentación está actualizada
- [ ] El commit message sigue las convenciones
- [ ] No hay conflictos con la rama main

## 🐛 Reportar Bugs

1. Verifica que el bug no haya sido reportado antes
2. Usa el template de issue para bugs
3. Incluye pasos para reproducir el problema
4. Agrega capturas de pantalla si es relevante

## 💡 Sugerir Funcionalidades

1. Verifica que la funcionalidad no exista ya
2. Usa el template de issue para features
3. Describe claramente el problema que resuelve
4. Proporciona ejemplos de uso

## 📞 Contacto

Si tienes preguntas sobre cómo contribuir:

- Abre un issue con la etiqueta "question"
- Contacta a los mantenedores del proyecto

## 🏆 Reconocimientos

Todos los contribuidores serán reconocidos en el README del proyecto.

¡Gracias por hacer que ConstructMarket sea mejor! 🚀

