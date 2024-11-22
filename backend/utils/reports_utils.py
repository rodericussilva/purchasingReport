from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

REPORTS_DIR = os.path.join(os.getcwd(), 'static', 'reports_files')

def generate_pdf(supplier, replacement_days, supply_days, table_data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join(REPORTS_DIR, f'report_{supplier}_{timestamp}.pdf')
    
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
        c.drawString(300, height - 70, "Tabela de Sugestões de Compras")
        
        c.setFont("Helvetica", 10)
        info_text = f"Fabricante: {supplier}         Dias de Reposição: {replacement_days}         Dias de Suprimento: {supply_days}"
        c.drawString(60, height - 120, info_text)

    def draw_table_header(c, table_y):
        c.setFont("Helvetica-Bold", 7)
        columns = ["Descrição", "Cobertura", "Mês0", "Mês1", "Mês2", "Mês3", "Média Mês", "Estoque Disponível", "Sugestão de Compra", "Valor de Compra", "Curva"]
        
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

    col_widths = [180, 50, 30, 30, 30, 30, 60, 80, 90, 80, 30]
    row_height = 15
    max_rows_per_page = 20

    draw_header(c)
    table_y = height - 150
    draw_table_header(c, table_y)
    table_y -= 25

    rows_on_page = 0
    c.setFont("Helvetica", 7)

    for row in table_data:
        if rows_on_page >= max_rows_per_page:
            c.showPage()
            draw_header(c)
            table_y = height - 150
            draw_table_header(c, table_y)
            table_y -= 25
            rows_on_page = 0

        x_position = 60
        for i, cell in enumerate(row):
            c.drawString(x_position + 5, table_y - 10, str(cell))
            x_position += col_widths[i]

        draw_row_line(c, table_y)
        table_y -= row_height
        rows_on_page += 1

    c.save()
    return f"http://{os.getenv('FLASK_HOST')}:{os.getenv('FLASK_PORT')}/static/reports_files/{os.path.basename(pdf_path)}"


from openpyxl import Workbook

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

def generate_pdf_rupture(supplier, days_estimate, table_data):
    supplier = supplier or "Fornecedor_Desconhecido"
    supplier = ''.join(e for e in supplier if e.isalnum() or e in (' ', '_', '-')).strip()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join(REPORTS_DIR, f'rupture_risk_{supplier}_{timestamp}.pdf')

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
            f"Fornecedor: {supplier}            "
            f"Previsão para os próximos {days_estimate} dias.                   "
            f"*Esse relatório leva em consideração as vendas diárias nos últimos 90 dias."
        )
        c.drawString(70, height - 120, info_text)

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
    max_rows_per_page = 20

    draw_header(c)
    table_y = height - 150
    draw_table_header(c, table_y)
    table_y -= 25

    rows_on_page = 0
    c.setFont("Helvetica", 7)

    for row in table_data:
        if rows_on_page >= max_rows_per_page:
            c.showPage()
            draw_header(c)
            table_y = height - 150
            draw_table_header(c, table_y)
            table_y -= 25
            rows_on_page = 0

        x_position = 70
        for i, cell in enumerate(row):
            c.drawString(x_position + 5, table_y - 10, str(cell))
            x_position += col_widths[i]

        draw_row_line(c, table_y)
        table_y -= row_height
        rows_on_page += 1

    c.save()
    return f"http://{os.getenv('FLASK_HOST')}:{os.getenv('FLASK_PORT')}/static/reports_files/{os.path.basename(pdf_path)}"

def generate_pdf_expiration(supplier, table_data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join(REPORTS_DIR, f'expiration_report_{supplier}_{timestamp}.pdf')

    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    c = canvas.Canvas(pdf_path, pagesize=landscape(A4))
    width, height = landscape(A4)

    def draw_header(c):
        logo_path = "static/logo-removebg-preview.png"
        logo_width, logo_height = 40, 40
        c.drawImage(logo_path, 60, height - 100, width=logo_width, height=logo_height)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(110, height - 85, "TS DISTRIBUIDORA")
        c.drawString(300, height - 70, "Relatório de Vencimentos")
        c.setFont("Helvetica", 10)
        info_text = f"Fornecedor: {supplier}                                   Data de Geração: {datetime.now().strftime('%d/%m/%Y')}"
        c.drawString(60, height - 120, info_text)

    def draw_table_header(c, table_y):
        c.setFont("Helvetica-Bold", 7)
        columns = ["Descrição", "Quantidade em Estoque", "Data do Vencimento", "Curva"]
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

    col_widths = [240, 120, 120, 100]
    row_height = 15
    max_rows_per_page = 20

    draw_header(c)
    table_y = height - 150
    draw_table_header(c, table_y)
    table_y -= 25

    rows_on_page = 0
    c.setFont("Helvetica", 7)

    for row in table_data:
        if rows_on_page >= max_rows_per_page:
            c.showPage()
            draw_header(c)
            table_y = height - 150
            draw_table_header(c, table_y)
            table_y -= 25
            rows_on_page = 0

        x_position = 60
        for i, cell in enumerate(row):
            c.drawString(x_position + 5, table_y - 10, str(cell))
            x_position += col_widths[i]

        draw_row_line(c, table_y)
        table_y -= row_height
        rows_on_page += 1

    c.save()
    return f"http://{os.getenv('FLASK_HOST')}:{os.getenv('FLASK_PORT')}/static/reports_files/{os.path.basename(pdf_path)}"

def generate_excel(supplier, table_data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_path = os.path.join(REPORTS_DIR, f'expiration_report_{supplier}_{timestamp}.xlsx')

    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    workbook = Workbook()
    sheet = workbook.active

    headers = ["Descrição", "Quantidade em Estoque", "Data do Vencimento", "Curva"]
    sheet.append(headers)

    for row in table_data:
        sheet.append(row)

    workbook.save(excel_path)
    return f"http://{os.getenv('FLASK_HOST')}:{os.getenv('FLASK_PORT')}/static/reports_files/{os.path.basename(excel_path)}"

def generate_csv(supplier, table_data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(REPORTS_DIR, f'expiration_report_{supplier}_{timestamp}.csv')

    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        headers = ["Descrição", "Quantidade em Estoque", "Data do Vencimento", "Curva"]
        writer.writerow(headers)

        for row in table_data:
            writer.writerow(row)

    return f"http://{os.getenv('FLASK_HOST')}:{os.getenv('FLASK_PORT')}/static/reports_files/{os.path.basename(csv_path)}"