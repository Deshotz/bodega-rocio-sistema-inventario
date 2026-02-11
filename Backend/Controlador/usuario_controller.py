from flask import Blueprint, request, jsonify
from Backend.Modelo.usuario_model import UsuarioModel

usuario_bp = Blueprint("usuario_bp", __name__)

# HU05 - Listar usuarios
@usuario_bp.route("/usuarios", methods=["GET"])
def listar_usuarios():
    usuarios = UsuarioModel.obtener_todos()
    return jsonify(usuarios)

# HU05 - Crear usuario
@usuario_bp.route("/usuarios", methods=["POST"])
def crear_usuario():
    data = request.json

    UsuarioModel.crear(
        data["nombre"],
        data["correo"],
        data["password"],
        data.get("rol", "usuario")
    )

    return jsonify({"mensaje": "Usuario creado correctamente"})

# HU05 - Eliminar usuario
@usuario_bp.route("/usuarios/<int:id>", methods=["DELETE"])
def eliminar_usuario(id):
    UsuarioModel.eliminar(id)
    return jsonify({"mensaje": "Usuario eliminado"})

# ✅ NUEVO – LOGIN
@usuario_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    usuario = UsuarioModel.login(
        data["correo"],
        data["password"]
    )

    if not usuario:
        return jsonify({"error": "Credenciales incorrectas"}), 401

    return jsonify(usuario)
