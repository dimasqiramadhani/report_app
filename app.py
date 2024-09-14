from flask import Flask, request, jsonify
import psycopg2
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="cashier_db",
    user="postgres",
    password="281101",
    host="localhost"
)
cur = conn.cursor()

@app.route('/products', methods=['GET'])
def get_products():
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    return jsonify(rows)

@app.route('/product', methods=['POST'])
def add_product():
    data = request.json
    cur.execute("INSERT INTO products (name, price) VALUES (%s, %s) RETURNING id", (data['name'], data['price']))
    conn.commit()
    return jsonify({'id': cur.fetchone()[0]})

@app.route('/sales', methods=['GET'])
def get_sales():
    cur.execute("SELECT s.id, p.name, s.quantity, s.total_price, s.sale_date FROM sales s JOIN products p ON s.product_id = p.id")
    rows = cur.fetchall()
    return jsonify(rows)

@app.route('/sale', methods=['POST'])
def add_sale():
    data = request.json
    cur.execute("INSERT INTO sales (product_id, quantity, total_price) VALUES (%s, %s, %s) RETURNING id",
                (data['product_id'], data['quantity'], data['total_price']))
    conn.commit()
    return jsonify({'id': cur.fetchone()[0]})

@app.route('/report', methods=['GET'])
def get_report():
    cur.execute("""
        SELECT p.name, SUM(s.quantity) AS total_quantity, SUM(s.total_price) AS total_sales
        FROM sales s
        JOIN products p ON s.product_id = p.id
        GROUP BY p.name
        ORDER BY total_sales DESC
    """)
    rows = cur.fetchall()
    return jsonify(rows)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
