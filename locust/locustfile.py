"""
Prueba de rendimiento de PostgreSQL usando Locust
"""
import time
import random
from locust import User, task, between, events
import psycopg2
from psycopg2 import pool

# Configuración de la conexión a PostgreSQL
DB_HOST = "postgres"  # Nombre del contenedor PostgreSQL
DB_PORT = 5432
DB_NAME = "testdb"
DB_USER = "testuser"
DB_PASSWORD = "testpass"

# Configuración del pool de conexiones
MIN_CONNECTIONS = 5
MAX_CONNECTIONS = 20

class PostgresClient:
    """Cliente personalizado para interactuar con PostgreSQL"""
    
    def __init__(self):
        """Inicializa el pool de conexiones"""
        self.conn_pool = psycopg2.pool.ThreadedConnectionPool(
            MIN_CONNECTIONS,
            MAX_CONNECTIONS,
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
    def execute_query(self, query, params=None, name=None):
        """Ejecuta una consulta y mide el tiempo"""
        start_time = time.time()
        conn = None
        cursor = None
        error = None
        result = None
        
        try:
            conn = self.conn_pool.getconn()
            cursor = conn.cursor()
            
            cursor.execute(query, params)
            result = cursor.fetchall()
            
            # Si es una operación de escritura, commit
            if not query.strip().upper().startswith("SELECT"):
                conn.commit()
                
        except Exception as e:
            error = e
            if conn:
                conn.rollback()
        finally:
            if cursor:
                cursor.close()
            if conn:
                self.conn_pool.putconn(conn)
        
        # Calcular tiempo de respuesta
        total_time = (time.time() - start_time) * 1000  # en milisegundos
        
        # Registrar evento para Locust
        if name:
            if error:
                # Modo compatible con Locust 2.15+
                events.request.fire(
                    request_type="SQL",
                    name=name,
                    response_time=total_time,
                    response_length=0,
                    exception=error,
                    context={},
                    url=DB_HOST,
                )
            else:
                # Modo compatible con Locust 2.15+
                events.request.fire(
                    request_type="SQL",
                    name=name,
                    response_time=total_time,
                    response_length=len(result) if result else 0,
                    exception=None,
                    context={},
                    url=DB_HOST,
                )
        
        if error:
            raise error
            
        return result
    
    def close(self):
        """Cierra el pool de conexiones"""
        if self.conn_pool:
            self.conn_pool.closeall()

class PostgresUser(User):
    """Usuario de Locust que realiza consultas a PostgreSQL"""
    
    # Tiempo de espera entre tareas (entre 1 y 3 segundos)
    wait_time = between(0.05, 0.1)
    
    def on_start(self):
        """Método que se ejecuta cuando el usuario inicia"""
        self.client = PostgresClient()
    
    def on_stop(self):
        """Método que se ejecuta cuando el usuario termina"""
        self.client.close()
    
    @task(5)
    def select_all_users(self):
        """Consulta SELECT para obtener todos los usuarios"""
        self.client.execute_query(
            "SELECT * FROM users",
            name="select_all_users"
        )
    
    @task(10)
    def select_user_by_id(self):
        """Consulta SELECT para obtener un usuario por ID"""
        # ID aleatorio entre 1 y 100 (para cuando tengamos más registros)
        user_id = random.randint(1, 100)
        self.client.execute_query(
            "SELECT * FROM users WHERE id = %s",
            params=(user_id,),
            name="select_user_by_id"
        )
    
    @task(2)
    def insert_new_user(self):
        """Inserta un nuevo usuario con nombre aleatorio"""
        # Lista de nombres para variedad
        first_names = ["Alex", "Jamie", "Taylor", "Morgan", "Casey", "Riley", 
                       "Jordan", "Avery", "Quinn", "Blake", "Reese", "Dakota", 
                       "Cameron", "Hayden", "Drew", "Parker", "Skyler", "Rowan"]
        
        last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", 
                      "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", 
                      "Jackson", "White", "Harris", "Martin", "Garcia", "Martinez"]
        
        # Generar nombre aleatorio
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        
        self.client.execute_query(
            "INSERT INTO users (name) VALUES (%s) RETURNING id",
            params=(name,),
            name="insert_user"
        )