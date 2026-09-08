from flask import Flask, jsonify
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
    connection.commit() # Save the changes to the D.B
    connection.close()  # Close the connection to the D.B 


@app.get("/api/health")
def health_check():
    return jsonify({"status": "ok"}), 200

init_db()
app.run(debug=True)