
-- Crear la tabla 'productos'
CREATE TABLE IF NOT EXISTS producto (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  fecha_vencimiento DATE NOT NULL,
  cantidad INT NOT NULL
);

-- Crear la tabla 'clientes'
CREATE TABLE IF NOT EXISTS cliente (
  ID INT AUTO_INCREMENT PRIMARY KEY,
  Nombre VARCHAR(100) NOT NULL,
  Apellido VARCHAR(100) NOT NULL,
  Numero_contacto VARCHAR(20) NOT NULL
);

-- Crear la tabla 'compra'
CREATE TABLE IF NOT EXISTS compra (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_cliente INT NOT NULL,
  id_producto INT NOT NULL,
  fecha_compra DATE NOT NULL,
  cantidad INT NOT NULL,
  FOREIGN KEY (id_cliente) REFERENCES clientes(id),
  FOREIGN KEY (id_producto) REFERENCES productos(id)
);
