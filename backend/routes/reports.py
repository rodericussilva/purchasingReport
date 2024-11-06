from flask import Blueprint, request, jsonify
from utils.reports_utils import generate_pdf, generate_excel, generate_csv

report = Blueprint('report', __name__)

@report.route('/generate_report', methods=['POST'])
def generate_report():
    try:
        data = request.get_json()
        supplier = data['supplier']
        replacement_days = data['replacement_days']
        supply_days = data['supply_days']
        table_data = data['table_data']

        pdf_path = generate_pdf(supplier, replacement_days, supply_days, table_data)
        excel_path = generate_excel(table_data)
        csv_path = generate_csv(table_data)

        return jsonify({
            "message": "Relatório gerado com sucesso",
            "pdf": pdf_path,
            "excel": excel_path,
            "csv": csv_path
        })
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
        return jsonify({'error': str(e)}), 500