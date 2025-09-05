from flask import Blueprint, jsonify, request, current_app
from src.models.user import User, Equipment, Transaction, Review, db
from src.routes.user import token_required, admin_required
from datetime import datetime, timedelta
from sqlalchemy import or_, and_

transaction_bp = Blueprint('transaction', __name__)

# Configuración de comisiones
COMMISSION_RATES = {
    'sale': 0.05,  # 5% para ventas
    'rent': 0.10   # 10% para rentas
}

def calculate_commission(amount, transaction_type):
    """Calcular comisión basada en el tipo de transacción"""
    rate = COMMISSION_RATES.get(transaction_type, 0.05)
    commission_amount = amount * rate
    return rate, commission_amount

@transaction_bp.route('/transactions', methods=['POST'])
@token_required
def create_transaction(current_user):
    try:
        data = request.json
        
        # Validar datos requeridos
        required_fields = ['equipment_id', 'transaction_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'Campo {field} es requerido'}), 400
        
        equipment_id = data['equipment_id']
        transaction_type = data['transaction_type']
        
        # Validar tipo de transacción
        if transaction_type not in ['sale', 'rent']:
            return jsonify({'message': 'Tipo de transacción inválido'}), 400
        
        # Obtener equipo
        equipment = Equipment.query.get_or_404(equipment_id)
        
        # Verificar que el equipo esté disponible
        if equipment.availability_status != 'available':
            return jsonify({'message': 'El equipo no está disponible'}), 400
        
        # Verificar que el usuario no sea el propietario
        if equipment.owner_id == current_user.id:
            return jsonify({'message': 'No puedes comprar/rentar tu propio equipo'}), 400
        
        # Validar que el equipo esté disponible para el tipo de transacción
        if transaction_type == 'sale' and not equipment.is_for_sale:
            return jsonify({'message': 'Este equipo no está disponible para venta'}), 400
        
        if transaction_type == 'rent' and not equipment.is_for_rent:
            return jsonify({'message': 'Este equipo no está disponible para renta'}), 400
        
        # Calcular monto según tipo de transacción
        if transaction_type == 'sale':
            if not equipment.price_sale:
                return jsonify({'message': 'Precio de venta no definido'}), 400
            amount = equipment.price_sale
            start_date = None
            end_date = None
        else:  # rent
            rent_type = data.get('rent_type', 'daily')  # daily, weekly
            duration = data.get('duration', 1)  # número de días/semanas
            
            if not data.get('start_date'):
                return jsonify({'message': 'Fecha de inicio es requerida para rentas'}), 400
            
            start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
            
            if rent_type == 'daily':
                if not equipment.price_rent_daily:
                    return jsonify({'message': 'Precio de renta diaria no definido'}), 400
                amount = equipment.price_rent_daily * duration
                end_date = start_date + timedelta(days=duration)
            elif rent_type == 'weekly':
                if not equipment.price_rent_weekly:
                    return jsonify({'message': 'Precio de renta semanal no definido'}), 400
                amount = equipment.price_rent_weekly * duration
                end_date = start_date + timedelta(weeks=duration)
            else:
                return jsonify({'message': 'Tipo de renta inválido'}), 400
        
        # Calcular comisión
        commission_rate, commission_amount = calculate_commission(amount, transaction_type)
        
        # Crear transacción
        transaction = Transaction(
            equipment_id=equipment_id,
            buyer_id=current_user.id,
            seller_id=equipment.owner_id,
            transaction_type=transaction_type,
            amount=amount,
            commission_rate=commission_rate,
            commission_amount=commission_amount,
            start_date=start_date,
            end_date=end_date,
            status='pending'
        )
        
        db.session.add(transaction)
        
        # Actualizar estado del equipo si es venta
        if transaction_type == 'sale':
            equipment.availability_status = 'sold'
        else:
            equipment.availability_status = 'rented'
        
        equipment.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Transacción creada exitosamente',
            'transaction': transaction.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al crear transacción: {str(e)}'}), 500

@transaction_bp.route('/transactions/<int:transaction_id>', methods=['GET'])
@token_required
def get_transaction(current_user, transaction_id):
    try:
        transaction = Transaction.query.get_or_404(transaction_id)
        
        # Verificar que el usuario sea parte de la transacción o admin
        if (transaction.buyer_id != current_user.id and 
            transaction.seller_id != current_user.id and 
            not current_user.is_admin):
            return jsonify({'message': 'No tienes permisos para ver esta transacción'}), 403
        
        return jsonify(transaction.to_dict()), 200
        
    except Exception as e:
        return jsonify({'message': f'Error al obtener transacción: {str(e)}'}), 500

@transaction_bp.route('/transactions/<int:transaction_id>/status', methods=['PUT'])
@token_required
def update_transaction_status(current_user, transaction_id):
    try:
        transaction = Transaction.query.get_or_404(transaction_id)
        data = request.json
        new_status = data.get('status')
        
        # Validar estados permitidos
        valid_statuses = ['pending', 'confirmed', 'completed', 'cancelled']
        if new_status not in valid_statuses:
            return jsonify({'message': 'Estado de transacción inválido'}), 400
        
        # Verificar permisos según el estado
        if new_status == 'confirmed':
            # Solo el vendedor puede confirmar
            if transaction.seller_id != current_user.id and not current_user.is_admin:
                return jsonify({'message': 'Solo el vendedor puede confirmar la transacción'}), 403
        elif new_status == 'completed':
            # Solo el comprador puede marcar como completada
            if transaction.buyer_id != current_user.id and not current_user.is_admin:
                return jsonify({'message': 'Solo el comprador puede completar la transacción'}), 403
        elif new_status == 'cancelled':
            # Ambas partes pueden cancelar
            if (transaction.buyer_id != current_user.id and 
                transaction.seller_id != current_user.id and 
                not current_user.is_admin):
                return jsonify({'message': 'No tienes permisos para cancelar esta transacción'}), 403
        
        # Actualizar estado
        old_status = transaction.status
        transaction.status = new_status
        transaction.updated_at = datetime.utcnow()
        
        # Actualizar estado del equipo según el nuevo estado de la transacción
        equipment = transaction.equipment
        if new_status == 'cancelled':
            equipment.availability_status = 'available'
        elif new_status == 'completed' and transaction.transaction_type == 'rent':
            equipment.availability_status = 'available'
        
        equipment.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': f'Estado de transacción actualizado a {new_status}',
            'transaction': transaction.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al actualizar estado: {str(e)}'}), 500

@transaction_bp.route('/transactions/my-purchases', methods=['GET'])
@token_required
def get_my_purchases(current_user):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        
        query = Transaction.query.filter_by(buyer_id=current_user.id)
        
        if status:
            query = query.filter_by(status=status)
        
        transactions = query.order_by(Transaction.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'transactions': [t.to_dict() for t in transactions.items],
            'total': transactions.total,
            'pages': transactions.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error al obtener compras: {str(e)}'}), 500

@transaction_bp.route('/transactions/my-sales', methods=['GET'])
@token_required
def get_my_sales(current_user):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        
        query = Transaction.query.filter_by(seller_id=current_user.id)
        
        if status:
            query = query.filter_by(status=status)
        
        transactions = query.order_by(Transaction.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'transactions': [t.to_dict() for t in transactions.items],
            'total': transactions.total,
            'pages': transactions.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error al obtener ventas: {str(e)}'}), 500

@transaction_bp.route('/transactions', methods=['GET'])
@token_required
@admin_required
def get_all_transactions(current_user):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        transaction_type = request.args.get('type')
        
        query = Transaction.query
        
        if status:
            query = query.filter_by(status=status)
        
        if transaction_type:
            query = query.filter_by(transaction_type=transaction_type)
        
        transactions = query.order_by(Transaction.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'transactions': [t.to_dict() for t in transactions.items],
            'total': transactions.total,
            'pages': transactions.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error al obtener transacciones: {str(e)}'}), 500

@transaction_bp.route('/transactions/commission-report', methods=['GET'])
@token_required
@admin_required
def get_commission_report(current_user):
    try:
        # Parámetros de fecha
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Transaction.query.filter_by(status='completed')
        
        if start_date:
            start = datetime.fromisoformat(start_date)
            query = query.filter(Transaction.created_at >= start)
        
        if end_date:
            end = datetime.fromisoformat(end_date)
            query = query.filter(Transaction.created_at <= end)
        
        transactions = query.all()
        
        # Calcular estadísticas
        total_transactions = len(transactions)
        total_sales_amount = sum(t.amount for t in transactions if t.transaction_type == 'sale')
        total_rent_amount = sum(t.amount for t in transactions if t.transaction_type == 'rent')
        total_commission = sum(t.commission_amount for t in transactions)
        
        sales_count = len([t for t in transactions if t.transaction_type == 'sale'])
        rent_count = len([t for t in transactions if t.transaction_type == 'rent'])
        
        return jsonify({
            'summary': {
                'total_transactions': total_transactions,
                'sales_count': sales_count,
                'rent_count': rent_count,
                'total_sales_amount': total_sales_amount,
                'total_rent_amount': total_rent_amount,
                'total_amount': total_sales_amount + total_rent_amount,
                'total_commission': total_commission
            },
            'commission_rates': COMMISSION_RATES,
            'transactions': [t.to_dict() for t in transactions]
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error al generar reporte: {str(e)}'}), 500

@transaction_bp.route('/transactions/<int:transaction_id>/review', methods=['POST'])
@token_required
def create_review(current_user, transaction_id):
    try:
        transaction = Transaction.query.get_or_404(transaction_id)
        
        # Verificar que la transacción esté completada
        if transaction.status != 'completed':
            return jsonify({'message': 'Solo se pueden reseñar transacciones completadas'}), 400
        
        # Verificar que el usuario sea parte de la transacción
        if transaction.buyer_id != current_user.id and transaction.seller_id != current_user.id:
            return jsonify({'message': 'No tienes permisos para reseñar esta transacción'}), 403
        
        # Determinar quién está siendo reseñado
        if transaction.buyer_id == current_user.id:
            reviewed_id = transaction.seller_id
        else:
            reviewed_id = transaction.buyer_id
        
        # Verificar que no haya reseña previa del mismo usuario
        existing_review = Review.query.filter_by(
            transaction_id=transaction_id,
            reviewer_id=current_user.id
        ).first()
        
        if existing_review:
            return jsonify({'message': 'Ya has reseñado esta transacción'}), 400
        
        data = request.json
        
        # Validar datos
        if not data.get('rating') or data['rating'] < 1 or data['rating'] > 5:
            return jsonify({'message': 'Calificación debe ser entre 1 y 5'}), 400
        
        # Crear reseña
        review = Review(
            transaction_id=transaction_id,
            reviewer_id=current_user.id,
            reviewed_id=reviewed_id,
            rating=data['rating'],
            comment=data.get('comment')
        )
        
        db.session.add(review)
        
        # Actualizar rating promedio del usuario reseñado
        user_reviews = Review.query.filter_by(reviewed_id=reviewed_id).all()
        if user_reviews:
            avg_rating = sum(r.rating for r in user_reviews) / len(user_reviews)
            reviewed_user = User.query.get(reviewed_id)
            reviewed_user.rating = round(avg_rating, 2)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Reseña creada exitosamente',
            'review': review.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al crear reseña: {str(e)}'}), 500

