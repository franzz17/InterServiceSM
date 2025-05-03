"""
Script para crear todas las tablas del sistema de Django en PostgreSQL
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

# SQL para crear todas las tablas necesarias del sistema de Django
CREATE_TABLES_SQL = """
-- Tabla de tipos de contenido (necesaria para permisos y el admin)
CREATE TABLE IF NOT EXISTS django_content_type (
    id SERIAL PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    CONSTRAINT django_content_type_app_label_model_uniq UNIQUE (app_label, model)
);

-- Tabla de permisos (necesaria para el sistema de autenticación)
CREATE TABLE IF NOT EXISTS auth_permission (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL,
    codename VARCHAR(100) NOT NULL,
    CONSTRAINT auth_permission_content_type_id_codename_uniq UNIQUE (content_type_id, codename)
);

-- Añadir la restricción de clave foránea después de que ambas tablas existan
ALTER TABLE auth_permission 
    ADD CONSTRAINT auth_permission_content_type_id_fkey
    FOREIGN KEY (content_type_id) REFERENCES django_content_type(id)
    ON DELETE CASCADE;

-- Tabla de grupos (para gestión de permisos)
CREATE TABLE IF NOT EXISTS auth_group (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
);

-- Tabla de relación entre grupos y permisos
CREATE TABLE IF NOT EXISTS auth_group_permissions (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    CONSTRAINT auth_group_permissions_group_id_permission_id_uniq UNIQUE (group_id, permission_id)
);

-- Añadir las restricciones de clave foránea
ALTER TABLE auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_fkey
    FOREIGN KEY (group_id) REFERENCES auth_group(id)
    ON DELETE CASCADE;

ALTER TABLE auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_permission_id_fkey
    FOREIGN KEY (permission_id) REFERENCES auth_permission(id)
    ON DELETE CASCADE;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS auth_user (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN NOT NULL,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabla de relación entre usuarios y grupos
CREATE TABLE IF NOT EXISTS auth_user_groups (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    CONSTRAINT auth_user_groups_user_id_group_id_uniq UNIQUE (user_id, group_id)
);

-- Añadir las restricciones de clave foránea
ALTER TABLE auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_fkey
    FOREIGN KEY (user_id) REFERENCES auth_user(id)
    ON DELETE CASCADE;

ALTER TABLE auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_fkey
    FOREIGN KEY (group_id) REFERENCES auth_group(id)
    ON DELETE CASCADE;

-- Tabla de relación entre usuarios y permisos
CREATE TABLE IF NOT EXISTS auth_user_user_permissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    CONSTRAINT auth_user_user_permissions_user_id_permission_id_uniq UNIQUE (user_id, permission_id)
);

-- Añadir las restricciones de clave foránea
ALTER TABLE auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_fkey
    FOREIGN KEY (user_id) REFERENCES auth_user(id)
    ON DELETE CASCADE;

ALTER TABLE auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_permission_id_fkey
    FOREIGN KEY (permission_id) REFERENCES auth_permission(id)
    ON DELETE CASCADE;

-- Tabla de sesiones (necesaria para el login)
CREATE TABLE IF NOT EXISTS django_session (
    session_key VARCHAR(40) NOT NULL PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date TIMESTAMP WITH TIME ZONE NOT NULL
);
CREATE INDEX IF NOT EXISTS django_session_expire_date_idx ON django_session(expire_date);

-- Tabla de registro de acciones del admin
CREATE TABLE IF NOT EXISTS django_admin_log (
    id SERIAL PRIMARY KEY,
    action_time TIMESTAMP WITH TIME ZONE NOT NULL,
    object_id TEXT,
    object_repr VARCHAR(200) NOT NULL,
    action_flag SMALLINT NOT NULL,
    change_message TEXT NOT NULL,
    content_type_id INTEGER,
    user_id INTEGER NOT NULL
);

-- Añadir las restricciones de clave foránea
ALTER TABLE django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_fkey
    FOREIGN KEY (content_type_id) REFERENCES django_content_type(id)
    ON DELETE SET NULL;

ALTER TABLE django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_fkey
    FOREIGN KEY (user_id) REFERENCES auth_user(id)
    ON DELETE CASCADE;

-- Tabla de migraciones
CREATE TABLE IF NOT EXISTS django_migrations (
    id SERIAL PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied TIMESTAMP WITH TIME ZONE NOT NULL
);
"""

def main():
    try:
        print("Conectando a la base de datos PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Ejecutar el script SQL completo
        print("Creando todas las tablas del sistema de Django...")
        cursor.execute(CREATE_TABLES_SQL)
        conn.commit()
        print("Tablas creadas exitosamente.")
        
        # Cerrar conexión
        cursor.close()
        conn.close()
        print("Conexión cerrada.")
        
        print("\nPróximos pasos:")
        print("1. Ejecuta 'python manage.py migrate --fake' para registrar las migraciones")
        print("2. Ejecuta 'python manage.py createsuperuser' para crear un superusuario (opcional)")
        print("3. Reinicia el servidor Django con 'python manage.py runserver'")
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
