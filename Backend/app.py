from flask import Flask
from flask_cors import CORS
from Backend.Controlador.producto_controller import producto_bp
from Backend.Controlador.inventario_controller import inventario_bp
from Backend.Controlador.usuario_controller import usuario_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(producto_bp)
app.register_blueprint(inventario_bp)
app.register_blueprint(usuario_bp)

if __name__ == "__main__":
    app.run(debug=True)
