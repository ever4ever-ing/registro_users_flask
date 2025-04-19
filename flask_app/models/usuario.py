import logging
from flask_app.config.dbconnection import connectToPostgreSQL
from flask import flash
import re
import os

from dotenv import load_dotenv
env_file = os.getenv('ENV_FILE', 'config.env')  # Por defecto, carga .env
load_dotenv(dotenv_path=env_file)

# Asegurarse de que las variables de entorno estén configuradas
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DATABASE')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NOMBRE_REGEX = re.compile(r'^[a-zA-Z\s]+$')


class Usuario:
    def __init__(self, data):
        self.id_usuario = data['id_usuario']
        self.nombre = data['nombre']
        self.curso = data['curso']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        resultados = connectToPostgreSQL(DATABASE).query_db(query)
        if not resultados:  # Si no hay resultados, devuelve una lista vacía
            return []
        usuarios = []
        for usuario in resultados:
            usuarios.append(cls(usuario))
        return usuarios

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO usuarios (nombre, curso)
        VALUES (%(nombre)s, %(curso)s) RETURNING id_usuario;
        """ 
        
        logging.info(f"Datos enviados para guardar usuario: {data}")
        try:
            resultado = connectToPostgreSQL(DATABASE).query_db(query, data)
            logging.info(f"Resultado de la consulta: {resultado}")
            return resultado
        except Exception as e:
            logging.error(f"Error al guardar usuario: {e}")
            return None
