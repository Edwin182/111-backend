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


# GET http://127.0.0.1:5000/api/products    -> return all products 
@app.get("/api/products")
def get_products():

    connection = sqlite3.connect(DB_NAME)   # Open the connection to the D.B
    connection.row_factory = sqlite3.Row    # makes each row behaves like a dictionary
    cursor = connection.cursor()            # execute sql syntax
    cursor.execute("SELECT * FROM products")    
    products_db = cursor.fetchall()         # retrieves all rows from the result of the query
    connection.close()

    products = []                   # list will store each product a a dictionary 
    for product in products_db:
        print(dict(product))        # convert the row object into a dictionary and print it
        products.append(dict(product))  # 

    return jsonify({
        "success": True,
        "message": "Products retrieved successfully",
        "data": products
        }), 200

# GET http://127.0.0.1:5000/api/products/2  -> get a product by id
@app.get("/api/products/<int:product_id>")
def get_product_by_id(product_id):
    #logic here
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products WHERE id =?", (product_id,))
    product_db = cursor.fetchone()

    if not product_db:
        connection.close()
        return jsonify({
            "success": False,
            "message": "product not found"
        }), 404
    
    connection.close()
    print(dict(product_db))
    product = dict(product_db)

    return jsonify({
        "success": True,
        "message": "product retrieved successfully",
        "data": product
    }), 200


# ---------- COUPONS ---------------
@app.post("/api/coupons")
def create_coupon():
    # get the coupon from thunder client
    new_coupon = request.get_json()
    print(new_coupon)

    # create variables for coupon fields (code, discount)
    code = new_coupon["code"]
    discount = new_coupon["discount"]
        
    
    connection = sqlite3.connect(DB_NAME)    # opening the connection to the D.B
    cursor = connection.cursor()    # cursor/tool help us to execute sql syntax (INSERT< SELECT.....) to the D.B 
    cursor.execute("INSERT INTO coupons (code, discount) VALUES (?, ?)",(code, discount)    #execute sql (INSERT INTO)
    )
    
    connection.commit() # Save the changes to the D.B
    connection.close()  # Close the connection to the D.B
    
    return jsonify({
        "success": True,
        "message": "coupon created successfully"
    }), 201

#MINI-Challenge
#GET http://127.0.0.1:5000/api/coupons -> return all the coupons 
@app.get("/api/coupons")
def get_coupons():

    connection = sqlite3.connect(DB_NAME)   # Open the connection to the D.B
    connection.row_factory = sqlite3.Row    # makes each row behaves like a dictionary
    cursor = connection.cursor()            # execute sql syntax
    cursor.execute("SELECT * FROM coupons")    
    coupons_db = cursor.fetchall()         # retrieves all rows from the result of the query
    connection.close()

    coupons = []                   # list will store each product a a dictionary 
    for coupon in coupons_db:
        print(dict(coupon))        # convert the row object into a dictionary and print it
        coupons.append(dict(coupon))  # 

    return jsonify({
        "success": True,
        "message": "coupons retrieved successfully",
        "data": coupons
        }), 200

# GET http://127.0.0.1:5000/api/coupons/2
@app.get("/api/coupons/<int:coupon_id>")
def get_coupon_by_id(coupon_id):
    #logic here
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM coupons WHERE id =?", (coupon_id,))
    coupon_db = cursor.fetchone()

    if not coupon_db:
        connection.close()
        return jsonify({
            "success": False,
            "message": "coupon not found"
        }), 404
    
    connection.close()
    print(dict(coupon_db))
    coupon = dict(coupon_db)

    return jsonify({
        "success": True,
        "message": "coupon retrieved successfully",
        "data": coupon
    }), 200


init_db()
app.run(debug=True)