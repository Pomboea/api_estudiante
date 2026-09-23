import logging
from app.core.database import Database
from app.models.estudiante import Estudiante

# Configuración básica de logging para registrar los errores
logger = logging.getLogger(__name__)

class EstudianteRepository:
    def __init__(self):
        # Composición: El repositorio instancia su propia conexión
        self.db = Database()

    def obtener_todos(self):
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM estudiantes ORDER BY id ASC;")
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error al obtener todos los estudiantes: {e}")
            raise e
        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, estudiante_id: int):
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM estudiantes WHERE id = %s;", (estudiante_id,))
            return cursor.fetchone()
        except Exception as e:
            logger.error(f"Error al obtener el estudiante con ID {estudiante_id}: {e}")
            raise e
        finally:
            if conn:
                conn.close()

    def crear(self, estudiante: Estudiante):
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO estudiantes (nombre, grado, promedio) 
                VALUES (%s, %s, %s) RETURNING id;
            """
            cursor.execute(query, (estudiante.nombre, estudiante.grado, estudiante.promedio))
            resultado = cursor.fetchone()
            
            # Validación por si fetchone() retorna None
            if not resultado:
                raise Exception("No se obtuvo el ID del estudiante creado.")

            # Si el cursor devuelve una tupla o un dict dependiendo del conector:
            nuevo_id = resultado['id'] if isinstance(resultado, dict) else resultado[0]

            conn.commit()
            return nuevo_id
        except Exception as e:
            if conn:
                conn.rollback()  # Revierte la transacción en caso de error
            logger.error(f"Error al crear estudiante: {e}")
            raise e
        finally:
            if conn:
                conn.close()

    def eliminar(self, estudiante_id: int) -> bool:
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM estudiantes WHERE id = %s RETURNING id;", (estudiante_id,))
            eliminado = cursor.fetchone()
            conn.commit()
            return eliminado is not None
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error al eliminar estudiante con ID {estudiante_id}: {e}")
            raise e
        finally:
            if conn:
                conn.close()

    def actualizar(self, estudiante_id: int, estudiante: Estudiante) -> bool:
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            query = """
                UPDATE estudiantes
                SET nombre = %s, grado = %s, promedio = %s
                WHERE id = %s
                RETURNING id;
            """
            cursor.execute(query, (estudiante.nombre, estudiante.grado, estudiante.promedio, estudiante_id))
            actualizado = cursor.fetchone()
            conn.commit()
            return actualizado is not None
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error al actualizar estudiante con ID {estudiante_id}: {e}")
            raise e
        finally:
            if conn:
                conn.close()