-- Crear la tabla clientes si no existe
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
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crear índices para mejorar el rendimiento de las consultas
CREATE INDEX IF NOT EXISTS idx_clientes_cedula ON clientes(cedula);
CREATE INDEX IF NOT EXISTS idx_clientes_correo ON clientes(correo);
