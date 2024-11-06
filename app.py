from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  shipping_info TEXT,
                  payment_info TEXT,
                  cart_items TEXT)''')
    conn.commit()
    conn.close()

@app.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.json
    shipping_info = str(data['shippingInfo'])
    payment_info = str(data['paymentInfo'])
    cart_items = str(data['cartItems'])

    # Store order in the database
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("INSERT INTO orders (shipping_info, payment_info, cart_items) VALUES (?, ?, ?)",
              (shipping_info, payment_info, cart_items))
    conn.commit()
    order_id = c.lastrowid
    conn.close()

    # Simulate invoice generation and send confirmation response
    return jsonify({'order_id': order_id, 'message': 'Order placed successfully!'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)