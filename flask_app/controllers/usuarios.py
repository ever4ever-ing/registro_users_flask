import logging
from flask import render_template, request, redirect, session, flash, jsonify
from flask_app import app, bcrypt
from flask_app.models.usuario import Usuario
from datetime import date
from functools import wraps




@app.route("/")
def index():
    Usuarios = Usuario.get_all()
    logging.info(f"Usuarios obtenidos: {Usuarios}")
    for usuario in Usuarios:
        logging.info(f"Usuario: {usuario.nombre}, Curso: {usuario.curso}")    
    if not Usuarios:  # Verifica si la lista está vacía
        logging.info("No hay usuarios registrados.")
        return render_template("index.html", Usuarios=None)
    else:
        logging.info(f"Usuarios: {Usuarios}")
        return render_template("index.html", Usuarios=Usuarios)

@app.route('/register', methods=['POST'])
def crear_usuario():
    data = {
        'nombre': request.form['nombre'],
        'curso': request.form['curso']
    }
    logging.info(f"Datos enviados al modelo Usuario.save: {data}")
    usuario_id = Usuario.save(data)
    if not usuario_id:
        flash("No se pudo crear el usuario.", "error")
        logging.error("El usuario no se guardó en la base de datos.")
        return redirect('/')
    else:
        logging.info(f"Usuario creado con ID: {usuario_id}")
        session['usuario_id'] = usuario_id
    return redirect('/')

@app.route('/api/usuarios', methods=['GET'])
def api_get_usuarios():
    try:
        usuarios = Usuario.get_all()
        # Convertir los objetos Usuario a diccionarios
        usuarios_json = [
            {
                "id_usuario": usuario.id_usuario,
                "nombre": usuario.nombre,
                "curso": usuario.curso
            }
            for usuario in usuarios
        ]
        return jsonify({"success": True, "usuarios": usuarios_json}), 200
    except Exception as e:
        logging.error(f"Error al obtener usuarios: {e}")
        return jsonify({"success": False, "message": "Error al obtener usuarios"}), 500
