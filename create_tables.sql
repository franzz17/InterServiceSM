-- Script para crear la tabla de clientes si no existe
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

-- Si la tabla de solicitudes no existe, también la creamos
CREATE TABLE IF NOT EXISTS solicitudes (
    id_usuario SERIAL PRIMARY KEY,
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
    instalador VARCHAR(100),
    fecha_instalacion TIMESTAMP WITH TIME ZONE,
    estado VARCHAR(20) DEFAULT 'Pendiente',
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para búsquedas comunes
CREATE INDEX IF NOT EXISTS idx_clientes_cedula ON clientes(cedula);
CREATE INDEX IF NOT EXISTS idx_solicitudes_cedula ON solicitudes(cedula);
CREATE INDEX IF NOT EXISTS idx_solicitudes_estado ON solicitudes(estado);
