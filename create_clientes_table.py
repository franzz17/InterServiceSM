"""
Script para crear la tabla 'clientes' en PostgreSQL
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

# SQL para crear la tabla de clientes
CREATE_CLIENTES_TABLE = """
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    correo VARCHAR(254) NOT NULL,
    barrio VARCHAR(100) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    plan_seleccionado VARCHAR(50) NOT NULL,
    preferencia_horario VARCHAR(50) NOT NULL,
    url_cedula VARCHAR(500) NOT NULL,
    url_recibo VARCHAR(500) NOT NULL,
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices para búsquedas comunes
CREATE INDEX IF NOT EXISTS idx_clientes_cedula ON clientes(cedula);
"""

def main():
    try:
        print("Conectando a la base de datos PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Verificar si la tabla ya existe
        cursor.execute("SELECT to_regclass('clientes');")
        result = cursor.fetchone()[0]
        
        if result:
            print("La tabla clientes ya existe.")
            
            # Verificar la estructura de la tabla
            cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'clientes'
            ORDER BY ordinal_position;
            """)
            columns = [row[0] for row in cursor.fetchall()]
            print("Columnas existentes:", ", ".join(columns))
            
            # Verificar si falta la columna id_cliente
            if 'id_cliente' not in columns:
                print("Añadiendo columna id_cliente a la tabla existente...")
                cursor.execute("""
                ALTER TABLE clientes
                ADD COLUMN id_cliente SERIAL PRIMARY KEY;
                """)
                conn.commit()
                print("Columna id_cliente añadida exitosamente.")
        else:
            # Crear la tabla completa
            print("Creando tabla clientes...")
            cursor.execute(CREATE_CLIENTES_TABLE)
            conn.commit()
            print("Tabla clientes creada exitosamente.")
            
            # Insertar un cliente de ejemplo para probar
            cursor.execute("""
            INSERT INTO clientes (
                nombre, apellido, cedula, telefono, correo,
                barrio, direccion, plan_seleccionado, preferencia_horario,
                url_cedula, url_recibo
            ) VALUES (
                'Cliente', 'Ejemplo', '123456789', '3001234567', 'cliente@example.com',
                'Centro', 'Calle Principal 123', 'Internet 100MB', 'Mañana (8:00-12:00)',
                'https://storage.googleapis.com/interservicesm/Cedulas/ejemplo.jpg',
                'https://storage.googleapis.com/interservicesm/Factura_sp/ejemplo.jpg'
            );
            """)
            conn.commit()
            print("Cliente de ejemplo insertado para probar la vista.")
        
        # Cerrar conexión
        cursor.close()
        conn.close()
        print("Conexión cerrada.")
        
        print("\nPróximos pasos:")
        print("1. Reinicia el servidor Django con 'python manage.py runserver'")
        print("2. Accede a la vista de clientes completados: http://127.0.0.1:8000/admin-panel/completadas/")
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
