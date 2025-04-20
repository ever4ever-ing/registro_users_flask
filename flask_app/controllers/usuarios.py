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

@app.route('/api/usuarios', methods=['GET', 'POST'])
def api_usuarios():
    if request.method == 'GET':
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
    elif request.method == 'POST':
        try:
            data = request.get_json()  # Obtiene los datos enviados en formato JSON
            if not data or 'nombre' not in data or 'curso' not in data:
                logging.error("Datos incompletos para crear usuario.")
                return jsonify({"success": False, "message": "Datos incompletos"}), 400
            
            usuario_data = {
                "nombre": data['nombre'],
                "curso": data['curso']
            }
            logging.info(f"Datos recibidos para crear usuario: {usuario_data}")
            
            usuario_id = Usuario.save(usuario_data)
            if not usuario_id:
                logging.error("No se pudo guardar el usuario en la base de datos.")
                return jsonify({"success": False, "message": "Error al guardar usuario"}), 500
            
            logging.info(f"Usuario creado con ID: {usuario_id}")
            return jsonify({"success": True, "message": "Usuario creado exitosamente", "id_usuario": usuario_id}), 201
        except Exception as e:
            logging.error(f"Error al crear usuario: {e}")
            return jsonify({"success": False, "message": "Error al crear usuario"}), 500
