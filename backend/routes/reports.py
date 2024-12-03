from flask import Blueprint, request, jsonify
from utils.reports_utils import generate_pdf, generate_excel, generate_csv, generate_pdf_rupture, generate_pdf_expiration, generate_pdf_stagnant
import threading

report = Blueprint('report', __name__)

lock = threading.Lock()

@report.route('/generate_report', methods=['POST'])
def generate_report():
    if not lock.acquire(blocking=False):
        return jsonify({"error": "Um relatório já está sendo gerado"}), 429

    try:
        data = request.get_json()

        suppliers = data['suppliers']
        replacement_days = data['replacement_days']
        supply_days = data['supply_days']
        table_data = data['table_data']
        file_format = data.get('file_format', 'pdf')

        if not suppliers or not table_data:
            return jsonify({"error": "Dados de fornecedor ou tabela estão vazios"}), 400

        supplier_data_list = []
        
        for supplier in suppliers:
            supplier_data = {
                'supplier': supplier,
                'replacement_days': replacement_days,
                'supply_days': supply_days,
                'produtos': []
            }
            
            for supplier_entry in table_data:
                if supplier in supplier_entry['fornecedor']:
                    supplier_data['produtos'] = supplier_entry['produtos']

            supplier_data_list.append(supplier_data)

        if file_format == 'pdf':
            file_path = generate_pdf(supplier_data_list)
        elif file_format == 'excel':
            file_path = generate_excel(table_data)
        elif file_format == 'csv':
            file_path = generate_csv(suppliers, table_data)
        else:
            return jsonify({"error": "Formato de arquivo inválido"}), 400

        return jsonify({
            "message": "Relatório gerado com sucesso",
            "file_path": file_path
        })

    except Exception as e:
        print(f"Erro ao gerar relatório: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        lock.release()


@report.route('/generate_rupture_report', methods=['POST'])
def generate_rupture_report():
    if not lock.acquire(blocking=False):
        return jsonify({"error": "Um relatório já está sendo gerado"}), 429

    try:
        data = request.get_json()
        suppliers = data.get('suppliers', [])
        days_estimate = data.get('days_estimate')
        table_data = data.get('table_data')
        file_format = data.get('file_format', 'pdf')

        if not suppliers or not days_estimate or not table_data:
            return jsonify({"error": "Todos os campos são obrigatórios!"}), 400

        if file_format == 'pdf':
            file_path = generate_pdf_rupture(suppliers, days_estimate, table_data)
        elif file_format == 'excel':
            file_path = generate_excel(suppliers, days_estimate, table_data)
        elif file_format == 'csv':
            file_path = generate_csv(suppliers, table_data)
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

@report.route('/generate_expiration_report', methods=['POST'])
def generate_expiration_report():
    try:
        data = request.get_json()
        supplier = data.get('supplier_name', 'Fornecedor_Desconhecido')
        table_data = data.get('table_data', [])
        file_format = data.get('file_format', 'pdf')
        months = data.get('months', 12)

        if file_format == 'pdf':
            file_path = generate_pdf_expiration(supplier, table_data, months)
        elif file_format == 'excel':
            file_path = generate_excel(supplier, table_data)
        elif file_format == 'csv':
            file_path = generate_csv(supplier, table_data)
        else:
            return jsonify({"error": "Formato de arquivo inválido"}), 400

        return jsonify({
            "message": "Relatório gerado com sucesso",
            "file_path": file_path
        }), 200
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
        return jsonify({"error": str(e)}), 500
    
@report.route('/generate-stagnant-report', methods=['POST'])
def generate_stagnant_report():
    if not lock.acquire(blocking=False):
        return jsonify({"error": "Um relatório já está sendo gerado"}), 429

    try:
        data = request.get_json()
        supplier = data.get('supplier_name', 'Fornecedor_Desconhecido')
        table_data = data.get('table_data', [])
        file_format = data.get('file_format', 'pdf')
        days = data.get('days', 120)

        if not table_data:
            return jsonify({"error": "Nenhum dado encontrado para geração do relatório."}), 400

        if file_format == 'pdf':
            file_path = generate_pdf_stagnant(supplier, table_data, days)
        elif file_format == 'excel':
            file_path = generate_excel(supplier, table_data)
        elif file_format == 'csv':
            file_path = generate_csv(supplier, table_data)
        else:
            return jsonify({"error": "Formato de arquivo inválido"}), 400

        return jsonify({
            "message": "Relatório gerado com sucesso.",
            "file_path": file_path
        })
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        lock.release()