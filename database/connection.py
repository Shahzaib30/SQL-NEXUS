import psycopg2
from core.config import settings

def init_db_connection():
    """Initialize a connection to the PostgreSQL database."""
    try:
        with psycopg2.connect(settings.DATABASE_URL) as connection:
            with connection.cursor() as cursor:
                print("Dropping Old Tables...")
                cursor.execute("""
                               DROP TABLE IF EXISTS order_items CASCADE;
                               DROP TABLE IF EXISTS orders CASCADE;
                               DROP TABLE IF EXISTS inventory CASCADE;
                               DROP TABLE IF EXISTS warehouses CASCADE;
                               DROP TABLE IF EXISTS products CASCADE;
                               DROP TABLE IF EXISTS users CASCADE;
                               """)
                
                print("Create enterprice schema...")
                cursor.execute("""
                               --1. Users Table
                               CREATE TABLE users (
                                    id SERIAL PRIMARY KEY,
                                    first_name VARCHAR(50) NOT NULL,
                                    last_name VARCHAR(50) NOT NULL,
                                    email VARCHAR(255) UNIQUE NOT NULL,
                                    role VARCHAR(20) DEFAULT 'customer',
                                    signup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                );
                               
                               --2. Products Table
                               CREATE TABLE products (
                                    id SERIAL PRIMARY KEY,
                                    name VARCHAR(255) NOT NULL,
                                    description TEXT,
                                    price DECIMAL(10, 2) NOT NULL,
                                    stock INT NOT NULL,
                                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                );
                               
                               --3. Warehouses Table
                               CREATE TABLE warehouses (
                                    id SERIAL PRIMARY KEY,
                                    name VARCHAR(255) NOT NULL,
                                    location VARCHAR(255) NOT NULL,
                                    capacity INT NOT NULL,
                                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                );
                               
                               --4. Inventory Table
                               CREATE TABLE inventory (
                                    id SERIAL PRIMARY KEY,
                                    product_id INT REFERENCES products(id) ON DELETE CASCADE,
                                    warehouse_id INT REFERENCES warehouses(id) ON DELETE CASCADE,
                                    quantity INT NOT NULL,
                                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                );
                               
                               --5. Orders Table
                               CREATE TABLE orders (
                                    id SERIAL PRIMARY KEY,
                                    user_id INT REFERENCES users(id) ON DELETE CASCADE,
                                    total_amount DECIMAL(10, 2) NOT NULL,
                                    status VARCHAR(20) DEFAULT 'pending',
                                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                );
                               
                               --6. Order Items Table
                               CREATE TABLE order_items (
                                    id SERIAL PRIMARY KEY,
                                    order_id INT REFERENCES orders(id) ON DELETE CASCADE,
                                    product_id INT REFERENCES products(id) ON DELETE CASCADE,
                                    quantity INT NOT NULL,
                                    price DECIMAL(10, 2) NOT NULL
                                );
                               """)
                
                print("Database schema created successfully.")
                print("Inserting sample data...")
                cursor.execute("""
                               -- Insert sample users
                               INSERT INTO users (first_name, last_name, email, role) VALUES
                                    ('John', 'Doe', 'john.doe@example.com', 'customer'),
                                    ('shahzaib', 'shafique', 'shahzaibshafique.dev@example.com', 'admin');
                               
                               -- Insert sample products
                                 INSERT INTO products (name, description, price, stock) VALUES
                                        ('Laptop', 'High performance laptop', 999.99, 50),
                                        ('Smartphone', 'Latest model smartphone', 499.99, 100);
                               -- Insert sample warehouses
                               INSERT INTO warehouses (name, location, capacity) VALUES
                                    ('Warehouse A', 'Location A', 1000),
                                    ('Warehouse B', 'Location B', 1500);
                               -- Insert sample inventory
                               INSERT INTO inventory (product_id, warehouse_id, quantity) VALUES
                                    (1, 1, 30),
                                    (1, 2, 20),
                                    (2, 1, 50),
                                    (2, 2, 50);
                                 -- Insert sample orders
                                 INSERT INTO orders (user_id, total_amount, status) VALUES
                                        (1, 1499.98, 'pending');
                                 -- Insert sample order items
                                 INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
                                        (1, 1, 1, 999.99),
                                        (1, 2, 1, 499.99);
                               """)
                connection.commit()
        print("Database connection initialized successfully.")
    except Exception as e:
        print(f"Error initializing the database connection: {e}")

if __name__ == "__main__":
    init_db_connection()