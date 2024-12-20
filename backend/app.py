import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from models import fetch_suppliers, fetch_products_by_suppliers, fetch_total_suggestions, fetch_products_and_calculate_rupture, fetch_total_rupture_risk, fetch_items_within_months, fetch_items_close_to_expiration, fetch_total_items_stopped, fetch_items_stopped_days
from routes.reports import report
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'reports_files')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.register_blueprint(report, url_prefix='/api')

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
        suppliers = request.args.getlist('supplier_name[]')
        replacement_days = int(request.args.get('replacement_days', 0))
        supply_days = int(request.args.get('supply_days', 0))

        if not suppliers:
            return jsonify({'error': 'Nenhum fornecedor especificado'}), 400

        products = fetch_products_by_suppliers(suppliers, replacement_days, supply_days)

        return jsonify(products), 200
    except Exception as e:
        print(f"Erro ao buscar produtos: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/static/reports_files/<path:filename>')
def serve_report(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/total-suggestions', methods=['GET'])
def get_total_suggestions():
    try:
        total_suggestions = fetch_total_suggestions()
        return jsonify({'total_suggestions': total_suggestions}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rupture-risk', methods=['GET'])
def rupture_risk():
    supplier_names = request.args.getlist('supplier_name[]')
    days_estimate = request.args.get('days_estimate')

    if not supplier_names or not days_estimate:
        return jsonify({"error": "Parâmetros 'supplier_name[]' e 'days_estimate' são obrigatórios!"}), 400
    
    try:
        days_estimate = int(days_estimate)
        products_by_supplier = fetch_products_and_calculate_rupture(supplier_names, days_estimate)
        
        if not products_by_supplier:
            return jsonify({"message": "Nenhum produto encontrado com risco de ruptura para os fornecedores especificados!"}), 404

        response_data = []
        for fornecedor, products in products_by_supplier.items():
            response_data.append({
                "fornecedor": fornecedor,
                "produtos": products
            })

        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/rupture-risk-count', methods=['GET'])
def get_rupture_risk_count():
    days_estimate = int(request.args.get('days_estimate', 30))  # default value of 30 days
    total_risk_items = fetch_total_rupture_risk(days_estimate)
    return jsonify({"total_risk_items": total_risk_items})

@app.route('/api/maturity-items-count', methods=['GET'])
def get_items_within_months():
    try:
        months = int(request.args.get('months', 12))  # Default to 12 months

        total_within_months = fetch_items_within_months(months)
        
        return jsonify({"total_within_months": total_within_months}), 200
    except Exception as e:
        print(f"Erro ao buscar itens dentro de {months} meses: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/items-close-expiration', methods=['GET'])
def get_items_close_to_expiration():
    supplier_names = request.args.getlist('supplier_name[]')
    months = request.args.get('months', type=int, default=12)

    if not supplier_names:
        return jsonify({"error": "Os nomes dos fornecedores são obrigatórios!"}), 400

    try:
        items_by_supplier = fetch_items_close_to_expiration(supplier_names, months)

        if not items_by_supplier:
            return jsonify({"message": f"Nenhum item próximo ao vencimento em até {months} meses encontrado para os fornecedores especificados!"}), 404

        response_data = [
            {"fornecedor": supplier, "produtos": produtos}
            for supplier, produtos in items_by_supplier.items()
        ]

        return jsonify(response_data), 200

    except Exception as e:
        print(f"Erro ao buscar itens próximos ao vencimento: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/items-stopped', methods=['GET'])
def get_items_stopped():
    try:
        days = int(request.args.get('days', 120))  # default value of 120 days
        total_stopped_items = fetch_total_items_stopped(days)
        return jsonify({"total_stopped_items": total_stopped_items}), 200
    except Exception as e:
        print(f"Erro ao buscar itens parados a mais de {days} dias: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/stagnant-items', methods=['GET'])
def get_stagnant_items():
    supplier_names = request.args.getlist('supplier_name[]')
    days = request.args.get('days', type=int, default=120)  # default value of 120 days

    if not supplier_names:
        return jsonify({"error": "Os nomes dos fornecedores são obrigatórios!"}), 400

    try:
        stagnant_items = fetch_items_stopped_days(supplier_names, days)

        if not stagnant_items:
            return jsonify({"message": f"Nenhum item parado há mais de {days} dias encontrado para os fornecedores especificados!"}), 404

        response_data = [
            {"fornecedor": supplier, "produtos": produtos}
            for supplier, produtos in stagnant_items.items()
        ]

        return jsonify(response_data), 200

    except Exception as e:
        print(f"Erro ao buscar itens parados: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    app.run(host=host, port=port, debug=True)