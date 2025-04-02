from flask import Flask, render_template, request, jsonify
import csv
import os

app = Flask(__name__)

# Routes for rendering pages
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/farmers')
def farmers():
    farmers_list = []
    with open('farmers.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            farmers_list.append(row)
    return render_template('farmers.html', farmers=farmers_list)

# API for adding new farmers
@app.route('/add_farmer', methods=['POST'])
def add_farmer():
    data = request.form
    new_farmer = [data['name'], data['location'], data['product']]
    with open('farmers.csv', mode='a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(new_farmer)
    return jsonify({'message': 'Farmer added successfully!'})

@app.route('/products')
def products():
    products_list = []
    with open('products.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            products_list.append(row)
    return render_template('products.html', products=products_list)

@app.route('/order', methods=['POST'])
def order():
    data = request.form
    new_order = [data['consumer_name'], data['product_name'], data['quantity']]
    
    # Save the order to a file
    if not os.path.exists('orders.csv'):
        with open('orders.csv', mode='w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['Consumer Name', 'Product', 'Quantity'])  # Header row
    
    with open('orders.csv', mode='a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(new_order)
    
    return jsonify('Order placed successfully!')

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True)
