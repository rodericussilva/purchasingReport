import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from models import fetch_suppliers, fetch_products_by_supplier, fetch_total_suggestions, fetch_products_and_calculate_rupture, fetch_total_rupture_risk, fetch_items_within_months, fetch_items_below_1_year, fetch_total_items_stopped, fetch_items_stopped_days
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
        supplier_name = request.args.get('supplier_name')
        replacement_days = int(request.args.get('replacement_days', 0))
        supply_days = int(request.args.get('supply_days', 0))

        if not supplier_name:
            return jsonify({'error': 'Fornecedor não especificado'}), 400

        produtos = fetch_products_by_supplier(supplier_name, replacement_days, supply_days)

        return jsonify(produtos), 200
    except Exception as e:
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
    supplier_name = request.args.get('supplier_name')
    days_estimate = int(request.args.get('days_estimate'))

    if not supplier_name or not days_estimate:
        return jsonify({"error": "Parâmetros 'supplier_name' e 'days_estimate' são obrigatórios!"}), 400
    
    try:
        products = fetch_products_and_calculate_rupture(supplier_name, days_estimate)
        
        if not products:
            return jsonify({"message": "Nenhum produto encontrado para o fornecedor especificado!"}), 404

        response_data = []
        for product in products:
            response_data.append({
                "descricao": product['descricao'],
                "estoque_disponivel": product['estoque_disponivel'],
                "estoque_fisico": product['estoque_fisico'],
                "estoque_transito": product['estoque_transito'],
                "estoque_minimo": product['estoque_minimo'],
                "media_diaria_venda": product['media_diaria_venda'],
                "previsao_vendas": product['previsao_vendas'],
                "risco_ruptura": product['risco_ruptura'],
                "curva": product['curva']
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
    
@app.route('/api/items-below-1-year', methods=['GET'])
def get_items_below_1_year():
    try:
        supplier_name = request.args.get('supplier_name')
        if not supplier_name:
            return jsonify({"error": "O fornecedor não foi especificado!"}), 400

        items = fetch_items_below_1_year(supplier_name)
        if not items:
            return jsonify({"message": "Nenhum item abaixo de 1 ano para vencimento encontrado!"}), 404

        return jsonify(items), 200
    except Exception as e:
        print(f"Erro ao buscar itens abaixo de 1 ano para vencimento: {e}")
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
    supplier_name = request.args.get('supplier_name')
    days = request.args.get('days', type=int, default=120)  # default value of 120 days

    if not supplier_name:
        return jsonify({"error": "O nome do fornecedor é obrigatório!"}), 400

    try:
        stagnant_items = fetch_items_stopped_days(supplier_name, days)
        
        if not stagnant_items:
            return jsonify({"message": f"Nenhum item parado há mais de {days} dias encontrado para este fornecedor!"}), 404

        return jsonify(stagnant_items), 200

    except Exception as e:
        print(f"Erro ao buscar itens parados: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    app.run(host=host, port=port, debug=True)