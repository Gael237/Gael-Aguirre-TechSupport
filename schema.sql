CREATE DATABASE IF NOT EXISTS soporte_db;
USE soporte_db;

-- Tabla de clientes
CREATE TABLE IF NOT EXISTS clientes (
id INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
email VARCHAR(100) NOT NULL,
creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de técnicos
CREATE TABLE IF NOT EXISTS tecnicos (
id INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
especialidad VARCHAR(100),
creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de tickets
CREATE TABLE IF NOT EXISTS tickets (
id INT AUTO_INCREMENT PRIMARY KEY,
cliente_id INT,
tecnico_id INT,
titulo VARCHAR(200) NOT NULL,
descripcion TEXT,
prioridad ENUM('baja', 'media', 'alta') NOT NULL,
estado ENUM('abierto', 'en_progreso', 'resuelto') DEFAULT 'abierto',
creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

FOREIGN KEY (cliente_id) REFERENCES clientes(id),
FOREIGN KEY (tecnico_id) REFERENCES tecnicos(id)

);
