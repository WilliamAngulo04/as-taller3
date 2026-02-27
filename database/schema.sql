-- TODO: Definir las tablas del sistema

-- Tabla de usuarios
CREATE TABLE users (
    -- TODO: Agregar campos para id, username, email, password_hash, created_at
    id_user INT PRIMARY KEY NOT NULL,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de productos  
CREATE TABLE products (
    -- TODO: Agregar campos para id, name, description, price, stock, image_url, created_at
    id_product INT PRIMARY KEY NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de carritos
CREATE TABLE carts (
    -- TODO: Agregar campos para id, user_id, created_at, updated_at
    id_cart INT PRIMARY KEY NOT NULL,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de items del carrito
CREATE TABLE cart_items (
    -- TODO: Agregar campos para id, cart_id, product_id, quantity, added_at
    id_cart_item INT PRIMARY KEY NOT NULL,
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TODO: Agregar índices y restricciones de clave foránea
ALTER TABLE carts ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id_user);
ALTER TABLE cart_items ADD CONSTRAINT fk_cart_id FOREIGN KEY (cart_id) REFERENCES carts(id_cart);
ALTER TABLE cart_items ADD CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES products(id_product);

-- TODO: Insertar datos de prueba
INSERT INTO users (id_user, username, email, password_hash) VALUES
(1, 'john_doe', 'john@example.com', 'hashed_password_123');

INSERT INTO products (id_product, name, description, price, stock) VALUES
(1, 'Laptop', 'A high-performance laptop', 999.99, 10),
(2, 'Smartphone', 'A latest model smartphone', 499.99, 20);

INSERT INTO carts (id_cart, user_id) VALUES
(1, 1);

INSERT INTO cart_items (id_cart_item, cart_id, product_id, quantity) VALUES
(1, 1, 1, 1),
(2, 1, 2, 2);
