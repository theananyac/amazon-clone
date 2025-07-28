from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

# Configuration
app.config['STATIC_FOLDER'] = 'static'
app.config['TEMPLATES_FOLDER'] = 'templates'

# Sample product data
products = [
    {"id": 1, "name": "iPhone 14", "price": "$799", "image": "iphone.jpg"},
    {"id": 2, "name": "Samsung Galaxy S22", "price": "$699", "image": "samsung.jpg"},
    {"id": 3, "name": "OnePlus 11", "price": "$599", "image": "oneplus.jpg"},
    # Add more products as needed
]

# API endpoint for products
@app.route('/api/products')
def api_products():
    return {
        'status': 'success',
        'products': products
    }

# Main routes
@app.route('/')
def home():
    return render_template('index.html', products=products)

@app.route('/search')
def search():
    query = request.args.get('q', '').strip().lower()
    if not query:
        return render_template('index.html', products=products)
    
    filtered_products = [
        p for p in products 
        if query in p["name"].lower() or 
           query in p["price"].lower()
    ]
    return render_template('index.html', products=filtered_products, query=query)

# Static file serving
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        app.config['STATIC_FOLDER'],
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

if __name__ == '__main__':
    # Create necessary directories if they don't exist
    os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)
    os.makedirs(app.config['TEMPLATES_FOLDER'], exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)