from flask import Blueprint, jsonify, request, current_app
from src.models.user import User, Equipment, Transaction, Review, db
import jwt
from datetime import datetime, timedelta
from functools import wraps

user_bp = Blueprint('user', __name__)

# Decorador para verificar JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token faltante'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'message': 'Usuario no encontrado'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

# Decorador para verificar admin
def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if not current_user.is_admin:
            return jsonify({'message': 'Acceso denegado. Se requieren permisos de administrador'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

# Rutas de autenticación
@user_bp.route('/auth/register', methods=['POST'])
def register():
    try:
        data = request.json
        
        # Validar datos requeridos
        required_fields = ['email', 'password', 'name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'Campo {field} es requerido'}), 400
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'El email ya está registrado'}), 400
        
        # Crear nuevo usuario
        user = User(
            email=data['email'],
            name=data['name'],
            phone=data.get('phone'),
            user_type=data.get('user_type', 'both')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuario registrado exitosamente',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al registrar usuario: {str(e)}'}), 500

@user_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.json
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Email y contraseña son requeridos'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'message': 'Credenciales inválidas'}), 401
        
        # Generar token JWT
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=7)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'message': 'Login exitoso',
            'token': token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error en login: {str(e)}'}), 500

# Rutas de usuario
@user_bp.route('/users/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    return jsonify(current_user.to_dict()), 200

@user_bp.route('/users/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    try:
        data = request.json
        
        # Actualizar campos permitidos
        if 'name' in data:
            current_user.name = data['name']
        if 'phone' in data:
            current_user.phone = data['phone']
        if 'user_type' in data:
            current_user.user_type = data['user_type']
        
        current_user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Perfil actualizado exitosamente',
            'user': current_user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al actualizar perfil: {str(e)}'}), 500

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user_public(current_user, user_id):
    user = User.query.get_or_404(user_id)
    
    # Información pública del usuario
    public_info = {
        'id': user.id,
        'name': user.name,
        'user_type': user.user_type,
        'verification_status': user.verification_status,
        'rating': user.rating,
        'created_at': user.created_at.isoformat() if user.created_at else None
    }
    
    return jsonify(public_info), 200

@user_bp.route('/users', methods=['GET'])
@token_required
@admin_required
def get_all_users(current_user):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        users = User.query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'users': [user.to_dict() for user in users.items],
            'total': users.total,
            'pages': users.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error al obtener usuarios: {str(e)}'}), 500

@user_bp.route('/users/<int:user_id>/verify', methods=['PUT'])
@token_required
@admin_required
def verify_user(current_user, user_id):
    try:
        user = User.query.get_or_404(user_id)
        data = request.json
        
        status = data.get('verification_status')
        if status not in ['verified', 'rejected']:
            return jsonify({'message': 'Estado de verificación inválido'}), 400
        
        user.verification_status = status
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': f'Usuario {status} exitosamente',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al verificar usuario: {str(e)}'}), 500

@user_bp.route('/users/<int:user_id>/reviews', methods=['GET'])
@token_required
def get_user_reviews(current_user, user_id):
    try:
        user = User.query.get_or_404(user_id)
        reviews = Review.query.filter_by(reviewed_id=user_id).all()
        
        return jsonify({
            'reviews': [review.to_dict() for review in reviews],
            'average_rating': user.rating,
            'total_reviews': len(reviews)
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error al obtener reseñas: {str(e)}'}), 500
