# routes/reports.py
from flask import Blueprint, request, jsonify
from utils.reports_utils import generate_pdf, generate_excel, generate_csv
import threading

report = Blueprint('report', __name__)

lock = threading.Lock()

@report.route('/generate_report', methods=['POST'])
def generate_report():
    if not lock.acquire(blocking=False):
        return jsonify({"error": "Um relatório já está sedo gerado"}), 429

    try:
        data = request.get_json()
        supplier = data['supplier']
        replacement_days = data['replacement_days']
        supply_days = data['supply_days']
        table_data = data['table_data']
        file_format = data.get('file_format', 'pdf')  # Adiciona verificação do formato do arquivo

        # Geração condicional do arquivo solicitado
        if file_format == 'pdf':
            file_path = generate_pdf(supplier, replacement_days, supply_days, table_data)
        elif file_format == 'excel':
            file_path = generate_excel(table_data)
        elif file_format == 'csv':
            file_path = generate_csv(supplier, table_data)
        else:
            return jsonify({"error": "Formato de arquivo inválido"}), 400

        return jsonify({
            "message": "Relatório gerado com sucesso",
            "file_path": file_path
        })
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        lock.release()