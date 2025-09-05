from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    user_type = db.Column(db.String(20), nullable=False, default='both')  # owner, renter, both
    verification_status = db.Column(db.String(20), nullable=False, default='pending')  # pending, verified, rejected
    rating = db.Column(db.Float, nullable=True, default=0.0)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    equipment = db.relationship('Equipment', backref='owner', lazy=True, cascade='all, delete-orphan')
    transactions_as_buyer = db.relationship('Transaction', foreign_keys='Transaction.buyer_id', backref='buyer', lazy=True)
    transactions_as_seller = db.relationship('Transaction', foreign_keys='Transaction.seller_id', backref='seller', lazy=True)
    reviews_given = db.relationship('Review', foreign_keys='Review.reviewer_id', backref='reviewer', lazy=True)
    reviews_received = db.relationship('Review', foreign_keys='Review.reviewed_id', backref='reviewed', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'user_type': self.user_type,
            'verification_status': self.verification_status,
            'rating': self.rating,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=False)
    price_sale = db.Column(db.Float, nullable=True)
    price_rent_daily = db.Column(db.Float, nullable=True)
    price_rent_weekly = db.Column(db.Float, nullable=True)
    availability_status = db.Column(db.String(20), nullable=False, default='available')  # available, rented, sold, maintenance
    location = db.Column(db.String(200), nullable=True)
    specifications = db.Column(db.Text, nullable=True)  # JSON string
    images = db.Column(db.Text, nullable=True)  # JSON string with image URLs
    is_for_sale = db.Column(db.Boolean, nullable=False, default=True)
    is_for_rent = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    transactions = db.relationship('Transaction', backref='equipment', lazy=True)

    def get_specifications(self):
        if self.specifications:
            try:
                return json.loads(self.specifications)
            except:
                return {}
        return {}

    def set_specifications(self, specs_dict):
        self.specifications = json.dumps(specs_dict)

    def get_images(self):
        if self.images:
            try:
                return json.loads(self.images)
            except:
                return []
        return []

    def set_images(self, images_list):
        self.images = json.dumps(images_list)

    def __repr__(self):
        return f'<Equipment {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'owner_name': self.owner.name if self.owner else None,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'price_sale': self.price_sale,
            'price_rent_daily': self.price_rent_daily,
            'price_rent_weekly': self.price_rent_weekly,
            'availability_status': self.availability_status,
            'location': self.location,
            'specifications': self.get_specifications(),
            'images': self.get_images(),
            'is_for_sale': self.is_for_sale,
            'is_for_rent': self.is_for_rent,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # sale, rent
    amount = db.Column(db.Float, nullable=False)
    commission_rate = db.Column(db.Float, nullable=False)  # Porcentaje de comisión
    commission_amount = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, nullable=True)  # Para rentas
    end_date = db.Column(db.DateTime, nullable=True)  # Para rentas
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, confirmed, completed, cancelled
    payment_status = db.Column(db.String(20), nullable=False, default='pending')  # pending, paid, refunded
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    reviews = db.relationship('Review', backref='transaction', lazy=True)

    def __repr__(self):
        return f'<Transaction {self.id} - {self.transaction_type}>'

    def to_dict(self):
        return {
            'id': self.id,
            'equipment_id': self.equipment_id,
            'equipment_title': self.equipment.title if self.equipment else None,
            'buyer_id': self.buyer_id,
            'buyer_name': self.buyer.name if self.buyer else None,
            'seller_id': self.seller_id,
            'seller_name': self.seller.name if self.seller else None,
            'transaction_type': self.transaction_type,
            'amount': self.amount,
            'commission_rate': self.commission_rate,
            'commission_amount': self.commission_amount,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'payment_status': self.payment_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviewed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 estrellas
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Review {self.id} - {self.rating} stars>'

    def to_dict(self):
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'reviewer_id': self.reviewer_id,
            'reviewer_name': self.reviewer.name if self.reviewer else None,
            'reviewed_id': self.reviewed_id,
            'reviewed_name': self.reviewed.name if self.reviewed else None,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
