from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from dotenv import load_dotenv
import os

load_dotenv()

REPORTS_DIR = os.path.join(os.getcwd(), 'static', 'reports_files')

def generate_pdf(supplier, replacement_days, supply_days, table_data):
    pdf_path = os.path.join(REPORTS_DIR, f'report_{supplier}.pdf')
    
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    c.drawImage("static/logo-removebg-preview.png", 50, height - 100, width=50, height=50)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(150, height - 70, "Tabela de Sugestões de Compras")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 120, f"Fabricante: {supplier}")
    c.drawString(50, height - 140, f"Dias de Reposição: {replacement_days}")
    c.drawString(50, height - 160, f"Dias de Suprimento: {supply_days}")

    table_y = height - 200
    for i, column in enumerate(["Descrição", "Cobertura", "Mês0", "Mês1", "Mês2", "Mês3", "Média Mês", "Estoque Disponível", "Sugestão de Compra", "Valor de Compra", "Curva"]):
        c.drawString(50 + i * 80, table_y, column)

    for row in table_data:
        table_y -= 20
        for i, cell in enumerate(row):
            c.drawString(50 + i * 80, table_y, str(cell))
    
    c.save()

    return f"http://{os.getenv('FLASK_HOST')}:{os.getenv('FLASK_PORT')}/static/reports_files/{os.path.basename(pdf_path)}"


from openpyxl import Workbook

def generate_excel(table_data):
    excel_path = os.path.join(REPORTS_DIR, 'report.xlsx')
    
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

def generate_csv(table_data):
    csv_path = os.path.join(REPORTS_DIR, 'report.csv')
    
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)
    
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        headers = ["Descrição", "Cobertura", "Mês0", "Mês1", "Mês2", "Mês3", "Média Mês", "Estoque Disponível", "Sugestão de Compra", "Valor de Compra", "Curva"]
        writer.writerow(headers)
        
        writer.writerows(table_data)

    return f"http://{os.getenv('FLASK_HOST')}:{os.getenv('FLASK_PORT')}/static/reports_files/{os.path.basename(csv_path)}"