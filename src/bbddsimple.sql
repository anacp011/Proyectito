-- Crear la base de datos si no existe
DROP DATABASE if exists bbddsimple;
CREATE DATABASE bbddsimple;

-- Usar la base de datos
USE bbddsimple;

-- Crear la tabla 'productos'
CREATE TABLE Productos (
  ID INT AUTO_INCREMENT PRIMARY KEY,
  Nombre VARCHAR(100) NOT NULL,
  Fecha_vencimiento DATE NOT NULL,
  Cantidad INT NOT NULL
);

-- Crear la tabla 'clientes'
CREATE TABLE Clientes (
  ID INT AUTO_INCREMENT PRIMARY KEY,
  Nombre VARCHAR(100) NOT NULL,
  Apellido VARCHAR(100) NOT NULL,
  Numero_contacto VARCHAR(20) NOT NULL
);

-- Crear la tabla 'compra'
CREATE TABLE Compra (
  ID INT AUTO_INCREMENT PRIMARY KEY,
  ID_cliente INT NOT NULL,
  ID_producto INT NOT NULL,
  Fecha_compra DATE NOT NULL,
  Cantidad INT NOT NULL,
  FOREIGN KEY (ID_cliente) REFERENCES Clientes(ID),
  FOREIGN KEY (ID_producto) REFERENCES Productos(ID)
);

-- Insertar información en la tabla 'clientes'
INSERT INTO clientes (nombre, apellido, numero_contacto) VALUES
  ('Juan', 'Pérez', '1234567890'),
  ('María', 'González', '9876543210'),
  ('Carlos', 'López', '5555555555');

-- Insertar información en la tabla 'productos'
INSERT INTO productos (nombre, fecha_vencimiento, cantidad) VALUES
  ('Leche', '2023-06-30', 10),
  ('Pan', '2023-06-15', 5),
  ('Huevos', '2023-06-20', 12);
  