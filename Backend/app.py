from flask import Flask
from flask_cors import CORS

# ===== CONTROLADORES =====
from Backend.Controlador.producto_controller import producto_bp
from Backend.Controlador.inventario_controller import inventario_bp
from Backend.Controlador.usuario_controller import usuario_bp
from Backend.Controlador.ventas_controller import ventas_bp
from Backend.Controlador.ia_controller import ia_bp
from Backend.Controlador.dashboard_controller import dashboard_bp

# ===== APP =====
app = Flask(__name__)
CORS(app)

# ===== REGISTRO DE RUTAS =====
app.register_blueprint(producto_bp)
app.register_blueprint(inventario_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(ventas_bp)
app.register_blueprint(ia_bp)
app.register_blueprint(dashboard_bp)

# ===== INICIO =====
if __name__ == "__main__":
    app.run(debug=True)
