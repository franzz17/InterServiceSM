"""
Script para solucionar el error de la tabla django_session
Este script crea la tabla django_session en PostgreSQL.
"""
import psycopg2
import os
import sys

# Configuración de la conexión a la base de datos
DB_CONFIG = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'n5rNZneopwuKZiDd',
    'host': 'confidently-nifty-skylark.data-1.use1.tembo.io',
    'port': '5432',
    'sslmode': 'require'
}

# SQL para crear la tabla django_session
CREATE_SESSION_TABLE = """
CREATE TABLE IF NOT EXISTS django_session (
    session_key VARCHAR(40) NOT NULL PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date TIMESTAMP WITH TIME ZONE NOT NULL
);
CREATE INDEX IF NOT EXISTS django_session_expire_date_idx ON django_session(expire_date);
"""

def main():
    try:
        print("Conectando a la base de datos PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Verificar si la tabla ya existe
        cursor.execute("SELECT to_regclass('django_session');")
        result = cursor.fetchone()[0]
        
        if result:
            print("La tabla django_session ya existe.")
        else:
            # Crear la tabla django_session
            print("Creando tabla django_session...")
            cursor.execute(CREATE_SESSION_TABLE)
            conn.commit()
            print("Tabla django_session creada exitosamente.")
        
        # Cerrar conexión
        cursor.close()
        conn.close()
        print("Conexión cerrada.")
        
        print("\nPróximos pasos:")
        print("1. Ejecuta 'python manage.py migrate --fake-initial' para registrar las migraciones")
        print("2. Reinicia el servidor Django con 'python manage.py runserver'")
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
