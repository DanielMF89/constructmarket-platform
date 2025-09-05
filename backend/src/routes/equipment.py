from flask import Blueprint, jsonify, request, current_app
from src.models.user import User, Equipment, Transaction, db
from src.routes.user import token_required, admin_required
from datetime import datetime
from sqlalchemy import or_, and_

equipment_bp = Blueprint('equipment', __name__)

@equipment_bp.route('/equipment', methods=['GET'])
def get_equipment():
    try:
        # Parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Parámetros de filtrado
        category = request.args.get('category')
        location = request.args.get('location')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        availability = request.args.get('availability', 'available')
        transaction_type = request.args.get('type')  # sale, rent
        search = request.args.get('search')
        
        # Construir query base
        query = Equipment.query.filter_by(availability_status=availability)
        
        # Aplicar filtros
        if category:
            query = query.filter(Equipment.category == category)
        
        if location:
            query = query.filter(Equipment.location.ilike(f'%{location}%'))
        
        if search:
            query = query.filter(
                or_(
                    Equipment.title.ilike(f'%{search}%'),
                    Equipment.description.ilike(f'%{search}%')
                )
            )
        
        # Filtrar por tipo de transacción y precio
        if transaction_type == 'sale':
            query = query.filter(Equipment.is_for_sale == True)
            if min_price:
                query = query.filter(Equipment.price_sale >= min_price)
            if max_price:
                query = query.filter(Equipment.price_sale <= max_price)
        elif transaction_type == 'rent':
            query = query.filter(Equipment.is_for_rent == True)
            if min_price:
                query = query.filter(
                    or_(
                        Equipment.price_rent_daily >= min_price,
                        Equipment.price_rent_weekly >= min_price
                    )
                )
            if max_price:
                query = query.filter(
                    or_(
                        Equipment.price_rent_daily <= max_price,
                        Equipment.price_rent_weekly <= max_price
                    )
                )
        
        # Ordenar por fecha de creación (más recientes primero)
        query = query.order_by(Equipment.created_at.desc())
        
        # Paginar resultados
        equipment_list = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'equipment': [eq.to_dict() for eq in equipment_list.items],
            'total': equipment_list.total,
            'pages': equipment_list.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error al obtener equipos: {str(e)}'}), 500

@equipment_bp.route('/equipment/<int:equipment_id>', methods=['GET'])
def get_equipment_detail(equipment_id):
    try:
        equipment = Equipment.query.get_or_404(equipment_id)
        return jsonify(equipment.to_dict()), 200
    except Exception as e:
        return jsonify({'message': f'Error al obtener equipo: {str(e)}'}), 500

@equipment_bp.route('/equipment', methods=['POST'])
@token_required
def create_equipment(current_user):
    try:
        data = request.json
        
        # Validar datos requeridos
        required_fields = ['title', 'category']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'Campo {field} es requerido'}), 400
        
        # Validar que al menos un tipo de transacción esté habilitado
        is_for_sale = data.get('is_for_sale', False)
        is_for_rent = data.get('is_for_rent', False)
        
        if not is_for_sale and not is_for_rent:
            return jsonify({'message': 'El equipo debe estar disponible para venta o renta'}), 400
        
        # Validar precios según tipo de transacción
        if is_for_sale and not data.get('price_sale'):
            return jsonify({'message': 'Precio de venta es requerido'}), 400
        
        if is_for_rent and not (data.get('price_rent_daily') or data.get('price_rent_weekly')):
            return jsonify({'message': 'Al menos un precio de renta es requerido'}), 400
        
        # Crear nuevo equipo
        equipment = Equipment(
            owner_id=current_user.id,
            title=data['title'],
            description=data.get('description'),
            category=data['category'],
            price_sale=data.get('price_sale'),
            price_rent_daily=data.get('price_rent_daily'),
            price_rent_weekly=data.get('price_rent_weekly'),
            location=data.get('location'),
            is_for_sale=is_for_sale,
            is_for_rent=is_for_rent
        )
        
        # Agregar especificaciones si se proporcionan
        if data.get('specifications'):
            equipment.set_specifications(data['specifications'])
        
        # Agregar imágenes si se proporcionan
        if data.get('images'):
            equipment.set_images(data['images'])
        
        db.session.add(equipment)
        db.session.commit()
        
        return jsonify({
            'message': 'Equipo creado exitosamente',
            'equipment': equipment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al crear equipo: {str(e)}'}), 500

@equipment_bp.route('/equipment/<int:equipment_id>', methods=['PUT'])
@token_required
def update_equipment(current_user, equipment_id):
    try:
        equipment = Equipment.query.get_or_404(equipment_id)
        
        # Verificar que el usuario sea el propietario o admin
        if equipment.owner_id != current_user.id and not current_user.is_admin:
            return jsonify({'message': 'No tienes permisos para editar este equipo'}), 403
        
        data = request.json
        
        # Actualizar campos permitidos
        updatable_fields = [
            'title', 'description', 'category', 'price_sale', 
            'price_rent_daily', 'price_rent_weekly', 'location',
            'availability_status', 'is_for_sale', 'is_for_rent'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(equipment, field, data[field])
        
        # Actualizar especificaciones
        if 'specifications' in data:
            equipment.set_specifications(data['specifications'])
        
        # Actualizar imágenes
        if 'images' in data:
            equipment.set_images(data['images'])
        
        equipment.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Equipo actualizado exitosamente',
            'equipment': equipment.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al actualizar equipo: {str(e)}'}), 500

@equipment_bp.route('/equipment/<int:equipment_id>', methods=['DELETE'])
@token_required
def delete_equipment(current_user, equipment_id):
    try:
        equipment = Equipment.query.get_or_404(equipment_id)
        
        # Verificar que el usuario sea el propietario o admin
        if equipment.owner_id != current_user.id and not current_user.is_admin:
            return jsonify({'message': 'No tienes permisos para eliminar este equipo'}), 403
        
        # Verificar que no tenga transacciones activas
        active_transactions = Transaction.query.filter(
            and_(
                Transaction.equipment_id == equipment_id,
                Transaction.status.in_(['pending', 'confirmed'])
            )
        ).first()
        
        if active_transactions:
            return jsonify({'message': 'No se puede eliminar equipo con transacciones activas'}), 400
        
        db.session.delete(equipment)
        db.session.commit()
        
        return jsonify({'message': 'Equipo eliminado exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al eliminar equipo: {str(e)}'}), 500

@equipment_bp.route('/equipment/my-equipment', methods=['GET'])
@token_required
def get_my_equipment(current_user):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        equipment_list = Equipment.query.filter_by(owner_id=current_user.id)\
            .order_by(Equipment.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'equipment': [eq.to_dict() for eq in equipment_list.items],
            'total': equipment_list.total,
            'pages': equipment_list.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error al obtener mis equipos: {str(e)}'}), 500

@equipment_bp.route('/equipment/categories', methods=['GET'])
def get_categories():
    try:
        # Obtener categorías únicas de la base de datos
        categories = db.session.query(Equipment.category.distinct()).all()
        category_list = [cat[0] for cat in categories if cat[0]]
        
        # Agregar categorías predefinidas si no existen
        predefined_categories = [
            'Excavadoras', 'Bulldozers', 'Grúas', 'Cargadores', 'Compactadores',
            'Martillos Neumáticos', 'Generadores', 'Andamios', 'Herramientas Eléctricas',
            'Camiones', 'Mezcladoras', 'Bombas', 'Otros'
        ]
        
        all_categories = list(set(category_list + predefined_categories))
        all_categories.sort()
        
        return jsonify({'categories': all_categories}), 200
        
    except Exception as e:
        return jsonify({'message': f'Error al obtener categorías: {str(e)}'}), 500

@equipment_bp.route('/equipment/<int:equipment_id>/availability', methods=['PUT'])
@token_required
def update_availability(current_user, equipment_id):
    try:
        equipment = Equipment.query.get_or_404(equipment_id)
        
        # Verificar que el usuario sea el propietario o admin
        if equipment.owner_id != current_user.id and not current_user.is_admin:
            return jsonify({'message': 'No tienes permisos para modificar este equipo'}), 403
        
        data = request.json
        status = data.get('availability_status')
        
        valid_statuses = ['available', 'rented', 'sold', 'maintenance']
        if status not in valid_statuses:
            return jsonify({'message': 'Estado de disponibilidad inválido'}), 400
        
        equipment.availability_status = status
        equipment.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Disponibilidad actualizada exitosamente',
            'equipment': equipment.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al actualizar disponibilidad: {str(e)}'}), 500

