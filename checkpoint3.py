import sqlite3
from sqlite3 import Error

def openConnection(dbFile):
    print("Connecting to database:", dbFile)
    try:
        conn = sqlite3.connect(dbFile)
        print("Connection successful.")
        return conn
    except Error as e:
        print(e)
        return None

def closeConnection(conn, dbFile):
    print("Closing connection to database:", dbFile)
    try:
        conn.close()
        print("Connection closed successfully.")
    except Error as e:
        print(e)

def showMenu():
    print("\nInteractive Menu")
    print("1. View all products")
    print("2. Add product to cart")
    print("3. View cart")
    print("4. Place an order")
    print("5. Update product stock")
    print("6. Delete a product from the cart")
    print("7. Exit")
    return input("Choose an option: ")

def viewProducts(conn):
    print("\nAvailable Products:")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description, price, stock FROM Product;")
        products = cursor.fetchall()
        for product in products:
            print(f"ID: {product[0]}, Name: {product[1]}, Price: {product[3]}, Stock: {product[4]}")
    except Error as e:
        print(e)

def addToCart(conn):
    try:
        user_id = input("Enter your user ID: ")
        product_id = input("Enter the product ID: ")
        size = input("Enter the size: ")
        quantity = int(input("Enter the quantity: "))
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Cart (user_id, product_id, size, quantity)
            VALUES (?, ?, ?, ?);
        """, (user_id, product_id, size, quantity))
        conn.commit()
        print("Product added to cart successfully.")
    except Error as e:
        print(e)

def viewCart(conn):
    try:
        user_id = input("Enter your user ID: ")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.name, c.size, c.quantity 
            FROM Cart c 
            JOIN Product p ON c.product_id = p.id 
            WHERE c.user_id = ?;
        """, (user_id,))
        cart_items = cursor.fetchall()
        if cart_items:
            print("\nYour Cart:")
            for item in cart_items:
                print(f"Product: {item[0]}, Size: {item[1]}, Quantity: {item[2]}")
        else:
            print("Your cart is empty.")
    except Error as e:
        print(e)

def placeOrder(conn):
    try:
        user_id = input("Enter your user ID: ")
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        address = input("Enter your address: ")
        city = input("Enter your city: ")
        state = input("Enter your state: ")
        zip_code = input("Enter your zip code: ")
        country = input("Enter your country: ")
        cursor = conn.cursor()
        
        #  calculate amounts
        cursor.execute("""
            SELECT SUM(p.price * c.quantity)
            FROM Cart c
            JOIN Product p ON c.product_id = p.id
            WHERE c.user_id = ?;
        """, (user_id,))
        total_amount = cursor.fetchone()[0]
        if not total_amount:
            print("Your cart is empty.")
            return
        
        # put order in
        cursor.execute("""
            INSERT INTO Orders (user_id, name, email, address, city, state, zip_code, country, total_amount, paid)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0);
        """, (user_id, name, email, address, city, state, zip_code, country, total_amount))
        order_id = cursor.lastrowid
        
        # add items to the order item
        cursor.execute("""
            SELECT product_id, quantity, size
            FROM Cart
            WHERE user_id = ?;
        """, (user_id,))
        cart_items = cursor.fetchall()
        for item in cart_items:
            product_id, quantity, size = item
            cursor.execute("""
                INSERT INTO OrderItem (order_id, product_id, quantity, price, size)
                SELECT ?, id, ?, price, ?
                FROM Product
                WHERE id = ?;
            """, (order_id, quantity, size, product_id))
        
        cursor.execute("DELETE FROM Cart WHERE user_id = ?;", (user_id,))
        conn.commit()
        print("Order placed successfully.")
    except Error as e:
        print(e)

def updateProductStock(conn):
    try:
        product_id = input("Enter the product ID: ")
        new_stock = int(input("Enter the new stock quantity: "))
        cursor = conn.cursor()
        cursor.execute("UPDATE Product SET stock = ? WHERE id = ?;", (new_stock, product_id))
        conn.commit()
        print("Product stock updated successfully.")
    except Error as e:
        print(e)

def deleteFromCart(conn):
    try:
        cart_id = input("Enter the cart item ID to delete: ")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Cart WHERE id = ?;", (cart_id,))
        conn.commit()
        print("Item removed from cart.")
    except Error as e:
        print(e)

def main():
    dbFile = "checkpoint2-dbase-1.sqlite3"
    conn = openConnection(dbFile)
    if conn:
        while True:
            option = showMenu()
            if option == "1":
                viewProducts(conn)
            elif option == "2":
                addToCart(conn)
            elif option == "3":
                viewCart(conn)
            elif option == "4":
                placeOrder(conn)
            elif option == "5":
                updateProductStock(conn)
            elif option == "6":
                deleteFromCart(conn)
            elif option == "7":
                break
            else:
                print("Invalid option. Please try again.")
        closeConnection(conn, dbFile)

if __name__ == "__main__":
    main()