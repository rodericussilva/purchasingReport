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
        c.drawImage(logo_path, 50, height - 100, width=logo_width, height=logo_height)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(95, height - 85, "TS DISTRIBUIDORA")
        c.drawString(300, height - 70, "Tabela de Sugestões de Compras")
        
        c.setFont("Helvetica", 10)
        info_text = f"Fabricante: {supplier}         Dias de Reposição: {replacement_days}         Dias de Suprimento: {supply_days}"
        c.drawString(50, height - 120, info_text)

    def draw_table_header(c, table_y):
        c.setFont("Helvetica-Bold", 7)
        columns = ["Descrição", "Cobertura", "Mês0", "Mês1", "Mês2", "Mês3", "Média Mês", "Estoque Disp.", "Sugestão Compra", "Valor Compra", "Curva"]
        
        x_position = 50
        for i, column in enumerate(columns):
            c.drawString(x_position, table_y, column)
            x_position += col_widths[i] + 1

    col_widths = [180, 50, 30, 30, 30, 30, 60, 80, 90, 80, 30]

    draw_header(c)
    
    table_y = height - 150 
    draw_table_header(c, table_y)

    table_y -= 20 
  
    row_height = 15
    max_rows_per_page = 20 
    rows_on_page = 0

    c.setFont("Helvetica", 7)
    
    for row in table_data:
        if rows_on_page >= max_rows_per_page:
            c.showPage()
            draw_header(c)
            table_y = height - 150 
            draw_table_header(c, table_y)
            table_y -= 20
            rows_on_page = 0

        x_position = 50
        for i, cell in enumerate(row):
            c.drawString(x_position, table_y, str(cell))
            x_position += col_widths[i] + 1
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