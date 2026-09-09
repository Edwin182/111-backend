from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)   # Instance of Flask 


DB_NAME = "online-store.db"


def init_db():
    connection = sqlite3.connect(DB_NAME)   # Open the connection to the D.B file named 'online-store.db'
    cursor = connection.cursor()    # Creates a cursor/tool that lets us send command (SELECT, INSERT,...) to the D.B
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coupons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL,
        discount INTEGER NOT NULL      
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        price REAL NOT NULL,
        category TEXT NOT NULL,
        image TEXT NOT NULL    
    )    
    """)


    connection.commit() # Save the changes to the D.B
    connection.close()  # Close the connection to the D.B 


@app.get("/api/health")
def health_check():
    return jsonify({"status": "ok"}), 200



# ----------- PRODUCTS -------------

# POST /api/products -> creation of a product to the DB
@app.post("/api/products")
def create_product():
    # logic here
    new_product = request.get_json()
    print(new_product)

    name = new_product["name"]
    price = new_product["price"]
    category = new_product["category"]
    image = new_product["image"]

    connection = sqlite3.connect(DB_NAME)    # opening the connection to the D.B
    cursor = connection.cursor()    # cursor/tool help us to execute sql syntax (INSERT< SELCT.....) to the D.B 
    cursor.execute("INSERT INTO products (name, price, category, image) VALUES (?, ?, ?, ?)",(name, price, category, image)
)

    connection.commit() # Save the changes to the D.B
    connection.close()  # Close the connection to the D.B

    return jsonify({
        "success": True,
        "message": "product created successfully"
    }), 201


# ---------- COUPONS ---------------
@app.post("/api/coupons")
def create_coupon():
    # logic here
    new_coupon = request.get_json()
    print(new_coupon)
    
    code = new_coupon["code"]
    discount = new_coupon["discount"]
        
    
    connection = sqlite3.connect(DB_NAME)    # opening the connection to the D.B
    cursor = connection.cursor()    # cursor/tool help us to execute sql syntax (INSERT< SELCT.....) to the D.B 
    cursor.execute("INSERT INTO coupons (code, discount) VALUES (?, ?)",(code,discount)
    )
    
    connection.commit() # Save the changes to the D.B
    connection.close()  # Close the connection to the D.B
    
    return jsonify({
        "success": True,
        "message": "coupon created successfully"
    }), 201


init_db()
app.run(debug=True)