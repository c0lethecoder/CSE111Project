DROP TABLE IF EXISTS Cart;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS OrderItem;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS Product;

CREATE TABLE User (
    ROWID INTEGER PRIMARY KEY AUTOINCREMENT,
    id INTEGER UNIQUE NOT NULL,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT 0
);

CREATE TABLE Product (
    ROWID INTEGER PRIMARY KEY AUTOINCREMENT,
    id INTEGER UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
);

CREATE TABLE Cart (
    ROWID INTEGER PRIMARY KEY AUTOINCREMENT,
    id INTEGER UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    size TEXT,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (product_id) REFERENCES Product(id)
);

CREATE TABLE Orders (
    ROWID INTEGER PRIMARY KEY AUTOINCREMENT,
    id INTEGER UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    address TEXT NOT NULL,
    address2 TEXT,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip_code TEXT NOT NULL,
    country TEXT NOT NULL,
    total_amount REAL NOT NULL,
    paid BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES User(id)
);

CREATE TABLE OrderItem (
    ROWID INTEGER PRIMARY KEY AUTOINCREMENT,
    id INTEGER UNIQUE NOT NULL,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    size TEXT,
    FOREIGN KEY (order_id) REFERENCES Orders(id),
    FOREIGN KEY (product_id) REFERENCES Product(id)
);

CREATE TABLE Category (
    ROWID INTEGER PRIMARY KEY AUTOINCREMENT,
    id INTEGER UNIQUE NOT NULL,
    item_id INTEGER NOT NULL,
    item_name TEXT NOT NULL,
    item_price REAL NOT NULL,
    size TEXT,
    item_quantity INTEGER,
    FOREIGN KEY (item_id) REFERENCES Product(id)
);

CREATE TABLE Review (
    ROWID INTEGER PRIMARY KEY AUTOINCREMENT,
    id INTEGER UNIQUE NOT NULL,
    order_id INTEGER NOT NULL,
    quantity INTEGER,
    price REAL,
    product_id INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(id),
    FOREIGN KEY (product_id) REFERENCES Product(id)
);

-- Insert data
INSERT INTO User (id, username, email, password_hash, is_admin) VALUES
(1, 'johndoe', 'johndoe@example.com', 'hashpassword123', 0),
(2, 'adminuser', 'admin@example.com', 'adminpassword', 1);

INSERT INTO Product (id, name, description, price, stock) VALUES
(1, 'Laptop', 'new laptop', 1200.00, 10),
(2, 'Phone', 'new smartphone', 800.00, 20);

INSERT INTO Cart (id, user_id, product_id, size, quantity) VALUES
(1, 1, 1, 'Medium', 1),
(2, 1, 2, 'Large', 2);

INSERT INTO Orders (id, user_id, name, email, address, address2, city, state, zip_code, country, total_amount, paid) VALUES
(1, 1, 'John Doe', 'johndoe@example.com', '123 Main St', NULL, 'Anytown', 'State', '12345', 'Country', 2000.00, 1);

INSERT INTO OrderItem (id, order_id, product_id, quantity, price, size) VALUES
(1, 1, 1, 1, 1200.00, 'Medium'),
(2, 1, 2, 1, 800.00, 'Large');

INSERT INTO Category (id, item_id, item_name, item_price, size, item_quantity) VALUES
(1, 1, 'Laptop', 1200.00, 'Medium', 10),
(2, 2, 'Phone', 800.00, 'Large', 20);

INSERT INTO Review (id, order_id, quantity, price, product_id) VALUES
(1, 1, 1, 1200.00, 1),
(2, 1, 2, 800.00, 2);

-- 2-3 select
SELECT * FROM Product;

SELECT * FROM Orders;


-- 1 update
UPDATE Product
SET stock = stock - 1
WHERE id = 1;

-- 1 delete
DELETE FROM Cart
WHERE id = 1;