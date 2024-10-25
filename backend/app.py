import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import fetch_suppliers, fetch_product_supplires, fetch_month_abbreviations
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    try:
        suppliers = fetch_suppliers()
        return jsonify(suppliers), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        supplier_name = request.args.get('supplier_name')
        if not supplier_name:
            return jsonify({'error': 'Fornecedor não especificado'}), 400
        
        produtos = fetch_product_supplires(supplier_name)
        return jsonify(produtos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/month-abbreviations', methods=['GET'])
def get_month_abbreviations():
    month_abbreviations = fetch_month_abbreviations()
    return jsonify(month_abbreviations)

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    app.run(host=host, port=port, debug=True)