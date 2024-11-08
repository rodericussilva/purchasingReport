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
    
    # Logo e nome da empresa
    logo_path = "static/logo-removebg-preview.png"  # Caminho da logo
    logo_width, logo_height = 50, 50  # Ajustar tamanho da logo
    
    c.drawImage(logo_path, 50, height - 100, width=logo_width, height=logo_height)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(120, height - 70, "TS DISTRIBUIDORA")  # Nome da empresa ao lado da logo
    
    # Título do relatório
    c.setFont("Helvetica-Bold", 16)
    c.drawString(300, height - 70, "Tabela de Sugestões de Compras")
    
    # Informações adicionais (na mesma linha)
    c.setFont("Helvetica", 12)
    info_text = f"Fabricante: {supplier}     Dias de Reposição: {replacement_days}     Dias de Suprimento: {supply_days}"
    c.drawString(50, height - 120, info_text)

    table_y = height - 180
    for i, column in enumerate(["Descrição", "Cobertura", "Mês0", "Mês1", "Mês2", "Mês3", "Média Mês", "Estoque Disponível", "Sugestão de Compra", "Valor de Compra", "Curva"]):
        c.drawString(50 + i * 80, table_y, column)

    for row in table_data:
        table_y -= 20
        for i, cell in enumerate(row):
            c.drawString(50 + i * 80, table_y, str(cell))
    
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
    
    # Escrevendo os dados no arquivo CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Cabeçalho com os meses dinâmicos
        headers = ["Descrição", "Cobertura", "Mês0", "Mês1", "Mês2", "Mês3", "Média Mês", "Estoque Disponível", "Sugestão de Compra", "Valor de Compra", "Curva"]
        writer.writerow(headers)
        
        # Adicionando as linhas de dados
        for row in table_data:
            writer.writerow(row)
    
    return f"http://{os.getenv('FLASK_HOST')}:{os.getenv('FLASK_PORT')}/static/reports_files/{os.path.basename(csv_path)}"