from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

REPORTS_DIR = os.path.join(os.getcwd(), 'static', 'reports_files')

def generate_pdf(supplier_data_list):
    if not isinstance(supplier_data_list, list) or len(supplier_data_list) == 0:
        raise ValueError("Os dados dos fornecedores estão vazios ou têm formato inválido.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join(REPORTS_DIR, f'report_{timestamp}.pdf')

    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    c = canvas.Canvas(pdf_path, pagesize=landscape(A4))
    width, height = landscape(A4)

    margin_bottom = 50
    margin_top = 50
    margin_left = 60
    margin_right = 60

    def draw_header():
        logo_path = "static/logo-removebg-preview.png"
        logo_width, logo_height = 40, 40
        c.drawImage(logo_path, margin_left, height - margin_top - 40, width=logo_width, height=logo_height)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(margin_left + 45, height - margin_top - 25, "TS DISTRIBUIDORA")
        c.drawString(margin_left + 240, height - margin_top - 10, "Tabela de Sugestões de Compras")

    def draw_supplier_info(supplier, replacement_days, supply_days, table_y):
        c.setFont("Helvetica", 10)
        info_text = f"Fabricante: {supplier}      Dias de Reposição: {replacement_days}      Dias de Suprimento: {supply_days}"
        c.drawString(margin_left, table_y, info_text)
        c.line(margin_left, table_y - 5, width - margin_right, table_y - 5)
        return table_y - 20

    def draw_table_header(table_y, col_positions):
        c.setFont("Helvetica-Bold", 7)
        headers = [
            "Descrição", "Cobertura", " ", " ", 
            " ", " ", "Média Mês", 
            "Estoque Disponível", "Sugestão de Compra", "Valor de Compra", "Curva"
        ]
        for i, header in enumerate(headers):
            c.drawString(col_positions[i] + 5, table_y - 10, header)
        return table_y - 25

    def draw_row_line(table_y, col_positions):
        c.line(margin_left, table_y, col_positions[-1] + 30, table_y)

    row_height = 12
    max_rows_per_page = 20

    def new_page():
        c.showPage()
        draw_header()
        c.setFont("Helvetica", 7)
        return height - margin_top - 80

    draw_header()
    c.setFont("Helvetica", 7)
    table_y = height - margin_top - 80

    col_positions = [margin_left, margin_left + 180, margin_left + 230, margin_left + 270, margin_left + 310, margin_left + 350, margin_left + 400, margin_left + 440, margin_left + 520, margin_left + 610, margin_left + 695]
    headers = [
        "descricao", "cobertura", "unidades_faturadas_mes3", "unidades_faturadas_mes2", 
        "unidades_faturadas_mes1", "unidades_faturadas_mes0", "media_faturada", 
        "estoque_disponivel", "sugestao_compra", "valor_venda", "curva"
    ]

    for supplier_data in supplier_data_list:
        supplier = supplier_data.get("supplier", "Desconhecido")
        replacement_days = supplier_data.get("replacement_days", "N/A")
        supply_days = supplier_data.get("supply_days", "N/A")
        produtos = supplier_data.get("produtos", [])

        if not isinstance(produtos, list):
            raise ValueError("A chave 'produtos' deve ser uma lista.")

        if table_y - margin_bottom < 150:
            table_y = new_page()

        table_y = draw_supplier_info(supplier, replacement_days, supply_days, table_y)
        table_y = draw_table_header(table_y, col_positions)
        rows_on_page = 0

        for product in produtos:
            if rows_on_page >= max_rows_per_page or table_y - row_height < margin_bottom:
                table_y = new_page()
                table_y = draw_supplier_info(supplier, replacement_days, supply_days, table_y)
                table_y = draw_table_header(table_y, col_positions)
                rows_on_page = 0

            c.setFont("Helvetica", 7)
            for i, col_position in enumerate(col_positions):
                c.drawString(col_position + 5, table_y - 10, str(product.get(headers[i], 'N/A')))

            draw_row_line(table_y, col_positions)
            table_y -= row_height
            rows_on_page += 1

        if table_y - margin_bottom < 150:
            table_y = new_page()

        table_y -= 20

    c.save()
    return f"http://{os.getenv('FLASK_HOST')}:{os.getenv('FLASK_PORT')}/static/reports_files/{os.path.basename(pdf_path)}"

def generate_excel(supplier, replacement_days, supply_days, table_data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_path = os.path.join(REPORTS_DIR, f'report_{supplier}_{timestamp}.pdf')
    
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    workbook = Workbook()
    sheet = workbook.active

    headers = ["Descrição", "Cobertura", "Mês0", "Mês1", "Mês2", "Mês3", "Média Mês", "Estoque Disponível", "Sugestão de Compra", "Valor de Compra", "Curva"]
    sheet.append(headers)

    for row in table_data:
        sheet.append(row)

    workbook.save(excel_path)
    return f"http://{os.getenv('FLASK_HOST')}:{os.getenv('FLASK_PORT')}/static/reports_files/{os.path.basename(excel_path)}"

import csv

def generate_csv(supplier, table_data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(REPORTS_DIR, f'report_{supplier}_{timestamp}.csv')
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        headers = ["Descrição", "Cobertura", "Mês0", "Mês1", "Mês2", "Mês3", "Média Mês", "Estoque Disponível", "Sugestão de Compra", "Valor de Compra", "Curva"]
        writer.writerow(headers)
        
        for row in table_data:
            writer.writerow(row)
    
    return f"http://{os.getenv('FLASK_HOST')}:{os.getenv('FLASK_PORT')}/static/reports_files/{os.path.basename(csv_path)}"

def generate_pdf_rupture(suppliers, days_estimate, table_data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join(REPORTS_DIR, f'rupture_risk_{timestamp}.pdf')

    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    c = canvas.Canvas(pdf_path, pagesize=landscape(A4))
    width, height = landscape(A4)

    def draw_header(c):
        logo_path = "static/logo-removebg-preview.png"
        logo_width, logo_height = 40, 40
        c.drawImage(logo_path, 70, height - 100, width=logo_width, height=logo_height)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(115, height - 85, "TS DISTRIBUIDORA")
        c.drawString(300, height - 70, "Tabela de Risco de Ruptura")
        c.setFont("Helvetica", 10)
        info_text = (
            f"Previsão para os próximos {days_estimate} dias.                                                                  "
            f"*Esse relatório leva em consideração as vendas diárias nos últimos 90 dias."
        )
        c.drawString(70, height - 120, info_text)

    def draw_supplier_info(c, supplier, table_y):
        c.setFont("Helvetica", 10)
        info_text = f"Fornecedor: {supplier}"
        c.drawString(70, table_y, info_text)
        c.line(70, table_y - 5, width - 70, table_y - 5)
        return table_y - 20

    def draw_table_header(c, table_y):
        c.setFont("Helvetica-Bold", 7)
        columns = ["Descrição", "Estoque Disponível", "Estoque Mínimo", "Em Trânsito", "Média Diária", "Curva"]
        x_position = 70

        for i, column in enumerate(columns):
            c.drawString(x_position + 5, table_y - 10, column)
            x_position += col_widths[i]

        table_width = sum(col_widths)
        c.rect(70, table_y - 20, table_width, 20, stroke=1, fill=0)

        x_position = 70
        for width in col_widths:
            c.line(x_position, table_y, x_position, table_y - 20)
            x_position += width

    def draw_row_line(c, table_y):
        table_width = sum(col_widths)
        c.line(70, table_y, 70 + table_width, table_y)

    col_widths = [200, 100, 100, 100, 100, 80]
    row_height = 15
    max_rows_per_page = 25
    margin_bottom = 25

    draw_header(c)
    table_y = height - 150

    for supplier_data in table_data:
        supplier = supplier_data.get("fornecedor", "Desconhecido")
        produtos = supplier_data.get("produtos", [])

        if not isinstance(produtos, list):
            raise ValueError("A chave 'produtos' deve ser uma lista.")

        if table_y - margin_bottom < 150:
            c.showPage()
            draw_header(c)
            table_y = height - 150

        table_y = draw_supplier_info(c, supplier, table_y)
        draw_table_header(c, table_y)
        table_y -= 25

        rows_on_page = 0
        c.setFont("Helvetica", 7)

        for product in produtos:
            if rows_on_page >= max_rows_per_page or table_y - row_height < margin_bottom:
                c.showPage()
                draw_header(c)
                table_y = height - 150
                table_y = draw_supplier_info(c, supplier, table_y)
                draw_table_header(c, table_y)
                table_y -= 25
                rows_on_page = 0

            x_position = 70
            for i, col in enumerate(["descricao", "estoque_disponivel", "estoque_minimo", "estoque_transito", "media_diaria_venda", "curva"]):
                c.drawString(x_position + 5, table_y - 10, str(product.get(col, 'N/A')))
                x_position += col_widths[i]

            draw_row_line(c, table_y)
            table_y -= row_height
            rows_on_page += 1

        table_y -= 15

    c.save()
    return f"http://{os.getenv('FLASK_HOST')}:{os.getenv('FLASK_PORT')}/static/reports_files/{os.path.basename(pdf_path)}"

def generate_pdf_expiration(supplier_data_list, months):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join(REPORTS_DIR, f'expiration_report_{timestamp}.pdf')

    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    c = canvas.Canvas(pdf_path, pagesize=landscape(A4))
    width, height = landscape(A4)

    margin_bottom = 50
    margin_top = 50
    margin_left = 60
    margin_right = 60
    row_height = 15

    def draw_header():
        logo_path = "static/logo-removebg-preview.png"
        logo_width, logo_height = 40, 40
        c.drawImage(logo_path, margin_left, height - margin_top - 40, width=logo_width, height=logo_height)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(margin_left + 45, height - margin_top - 35, "TS DISTRIBUIDORA")
        c.drawString(margin_left + 180, height - margin_top - 10, f"Relatório de Itens Próximos ao Vencimento ({months} meses)")

    def draw_supplier_info(supplier, table_y):
        c.setFont("Helvetica", 10)
        info_text = f"Fornecedor: {supplier}                                   Data de Geração: {datetime.now().strftime('%d/%m/%Y')}"
        c.drawString(margin_left, table_y, info_text)
        c.line(margin_left, table_y - 5, width - margin_right, table_y - 5)
        return table_y - 20

    def draw_table_header(table_y):
        c.setFont("Helvetica-Bold", 7)
        columns = ["Descrição", "Quantidade em Estoque", "Data do Vencimento", "Curva"]
        x_position = margin_left
        for i, column in enumerate(columns):
            c.drawString(x_position + 5, table_y - 10, column)
            x_position += col_widths[i]
        
        table_width = sum(col_widths)
        c.rect(margin_left, table_y - 20, table_width, 20, stroke=1, fill=0)

        x_position = margin_left
        for width in col_widths:
            c.line(x_position, table_y, x_position, table_y - 20)
            x_position += width

    def draw_table_content(table_data, table_y):
        rows_on_page = 0

        for row in table_data:
            if rows_on_page >= max_rows_per_page or table_y - row_height < margin_bottom:
                table_y = new_page()
                draw_table_header(table_y)
                rows_on_page = 0

            x_position = margin_left
            for i, cell in enumerate(row):
                c.setFont("Helvetica", 8)
                c.drawString(x_position + 5, table_y - 10, str(cell))
                x_position += col_widths[i]

            draw_row_line(table_y)
            table_y -= row_height
            rows_on_page += 1

        return table_y

    def draw_row_line(table_y):
        table_width = sum(col_widths)
        c.line(margin_left, table_y, margin_left + table_width, table_y)

    def new_page():
        c.showPage()
        draw_header()
        return height - margin_top - 80

    col_widths = [300, 150, 150, 120]
    max_rows_per_page = 20

    draw_header()
    table_y = height - margin_top - 80

    for supplier_data in supplier_data_list:
        supplier = supplier_data.get("supplier_name", "Desconhecido")
        table_data = supplier_data.get("table_data", [])

        if not isinstance(table_data, list):
            raise ValueError("A chave 'table_data' deve ser uma lista.")

        if table_y - margin_bottom < 150:
            table_y = new_page()

        table_y = draw_supplier_info(supplier, table_y)
        draw_table_header(table_y)
        table_y -= 25

        table_y = draw_table_content(table_data, table_y)

    c.save()
    return f"http://{os.getenv('FLASK_HOST')}:{os.getenv('FLASK_PORT')}/static/reports_files/{os.path.basename(pdf_path)}"

def generate_pdf_stagnant(suppliers, table_data, days):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join(REPORTS_DIR, f'stagnant_items_{timestamp}.pdf')

    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    c = canvas.Canvas(pdf_path, pagesize=landscape(A4))
    width, height = landscape(A4)

    def draw_header(c):
        logo_path = "static/logo-removebg-preview.png"
        logo_width, logo_height = 40, 40
        c.drawImage(logo_path, 60, height - 100, width=logo_width, height=logo_height)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(105, height - 85, "TS DISTRIBUIDORA")
        c.drawString(300, height - 70, f"Itens Parados a Mais de {days} Dias")
        c.setFont("Helvetica", 10)
        c.drawString(60, height - 120, f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y')}")

    def draw_supplier_info(c, supplier, table_y):
        c.setFont("Helvetica", 10)
        info_text = f"Fornecedor: {supplier}"
        c.drawString(60, table_y, info_text)
        c.line(60, table_y - 5, width - 60, table_y - 5)
        return table_y - 20

    def draw_table_header(c, table_y):
        c.setFont("Helvetica-Bold", 8)
        columns = ["Descrição", "Quantidade em Estoque", "Data da Última Venda", "Curva"]
        x_position = 60

        for i, column in enumerate(columns):
            c.drawString(x_position + 5, table_y - 10, column)
            x_position += col_widths[i]

        table_width = sum(col_widths)
        c.rect(60, table_y - 20, table_width, 20, stroke=1, fill=0)

        x_position = 60
        for width in col_widths:
            c.line(x_position, table_y, x_position, table_y - 20)
            x_position += width

    def draw_row_line(c, table_y):
        table_width = sum(col_widths)
        c.line(60, table_y, 60 + table_width, table_y)

    col_widths = [270, 150, 200, 100]
    row_height = 20
    max_rows_per_page = 20
    margin_bottom = 25

    draw_header(c)
    table_y = height - 160

    for supplier_data in table_data:
        supplier = supplier_data.get("fornecedor", "Desconhecido")
        produtos = supplier_data.get("produtos", [])

        if not isinstance(produtos, list):
            raise ValueError("A chave 'produtos' deve ser uma lista.")

        if table_y - margin_bottom < 150:
            c.showPage()
            draw_header(c)
            table_y = height - 160

        table_y = draw_supplier_info(c, supplier, table_y)
        draw_table_header(c, table_y)
        table_y -= 25

        rows_on_page = 0
        c.setFont("Helvetica", 8)

        for product in produtos:
            if rows_on_page >= max_rows_per_page or table_y - row_height < margin_bottom:
                c.showPage()
                draw_header(c)
                table_y = height - 160
                table_y = draw_supplier_info(c, supplier, table_y)
                draw_table_header(c, table_y)
                table_y -= 25
                rows_on_page = 0

            x_position = 60
            for i, col in enumerate(["descricao", "quantidade_estoque", "ultima_venda", "curva"]):
                c.drawString(x_position + 5, table_y - 10, str(product.get(col, 'N/A')))
                x_position += col_widths[i]

            draw_row_line(c, table_y)
            table_y -= row_height
            rows_on_page += 1

        table_y -= 15

    c.save()
    return f"http://{os.getenv('FLASK_HOST')}:{os.getenv('FLASK_PORT')}/static/reports_files/{os.path.basename(pdf_path)}"