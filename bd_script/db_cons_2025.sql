-- Crear base de datos
-- Integrar aspectos ambiente en sec_workspace

CREATE TABLE rol (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    id_rol INT NOT NULL,
    CONSTRAINT fk_user_rol FOREIGN KEY (id_rol) REFERENCES rol(id) ON DELETE CASCADE
);

INSERT INTO rol (name) VALUES ('admin');


INSERT INTO usuario (name, email, password, id_rol) VALUES 
('admin', 'admin@example.com', '123456', 1),
('admin1', 'admin1@example.com', '1234567', 1),
('admin2', 'admin2@example.com', '12345678', 1),
('admin3', 'admin3@example.com', '123456789', 1),
('admin4', 'admin4@example.com', '1234567890', 1);


CREATE TABLE producto (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    estado BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO producto (nombre, descripcion, precio, stock, estado) VALUES 
('Laptop', 'Laptop gamer con 16GB RAM', 1500.00, 10, TRUE),
('Mouse', 'Mouse inalámbrico', 25.99, 50, TRUE),
('Teclado', 'Teclado mecánico RGB', 60.00, 30, TRUE);
