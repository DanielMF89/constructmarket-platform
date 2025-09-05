import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db, User
from src.routes.user import user_bp
from src.routes.equipment import equipment_bp
from src.routes.transaction import transaction_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'marketplace_secret_key_2024_construction_equipment'

# Configurar CORS para permitir acceso desde cualquier origen
CORS(app, origins="*", allow_headers=["Content-Type", "Authorization"])

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(equipment_bp, url_prefix='/api')
app.register_blueprint(transaction_bp, url_prefix='/api')

# Configuración de base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Crear tablas y usuario admin por defecto
with app.app_context():
    db.create_all()
    
    # Crear usuario administrador por defecto si no existe
    admin_user = User.query.filter_by(email='admin@marketplace.com').first()
    if not admin_user:
        admin_user = User(
            email='admin@marketplace.com',
            name='Administrador',
            user_type='both',
            is_admin=True,
            verification_status='verified'
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()
        print("Usuario administrador creado: admin@marketplace.com / admin123")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

# Ruta de estado de la API
@app.route('/api/health', methods=['GET'])
def health_check():
    return {
        'status': 'OK',
        'message': 'Marketplace API funcionando correctamente',
        'version': '1.0.0'
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
