import logging
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cargar un archivo .env específico
# Busca el .env en el mismo directorio que este archivo
env_file = os.path.join(os.path.dirname(__file__), 'config.env')
load_dotenv(dotenv_path=env_file)

# Asegurarse de que las variables de entorno estén configuradas
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DATABASE')
DB_PORT = os.getenv('DB_PORT')
logging.info(f"Variables de entorno: {DB_HOST}, {DB_USER}, {DB_PASSWORD}, {DATABASE}")

if not all([DB_HOST, DB_USER, DB_PASSWORD, DATABASE]):
    raise EnvironmentError(
        "Faltan variables de entorno necesarias para la configuración de la base de datos.")

# URL de conexión para pruebas

#postgresql://postgres:cJneJIiXUYBKtsWCrjAYWvtavXFVZtYj@hopper.proxy.rlwy.net:11148/railway
#TEST_DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DATABASE}"
# Crear la URL de conexión
TEST_DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DATABASE}"


# Probar conexión a la base de datos
try:
    logging.info("Probando conexión a la base de datos...")
    test_connection = psycopg2.connect(TEST_DB_URL)
    logging.info("Conexión exitosa a la base de datos.")
    test_connection.close()
except Exception as e:
    logging.error(f"Error al conectar a la base de datos: {e}")


class PostgreSQLConnection:
    def __init__(self, db):
        try:
            self.connection = psycopg2.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                port=DB_PORT,
                database=db
            )
            self.connection.autocommit = True
            logging.info(f"Conexión establecida con la base de datos: {db}")
        except Exception as e:
            logging.error(f"Error al conectar con la base de datos {db}: {e}")
            raise

    def query_db(self, query, data=None):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute(query, data)
                if query.strip().lower().startswith("insert"):
                    logging.info("Inserting...")
                    logging.debug(f"query: {query}")
                    return cursor.fetchone()  # Devuelve toda la fila en lugar de asumir 'id'
                elif query.strip().lower().startswith("select"):
                    logging.info("Selecting...")
                    return cursor.fetchall()
                else:
                    logging.warning("Query None.")
                    return None
            except Exception as e:
                logging.error(f"Something went wrong: {e}")
                return False
            finally:
                self.connection.close()


def connectToPostgreSQL(db):
    logging.info("Conectando a PostgreSQL...")
    logging.debug(PostgreSQLConnection(db))
    return PostgreSQLConnection(db)
