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
    
    # Função para desenhar cabeçalho do relatório
    def draw_header(c):
        logo_path = "static/logo-removebg-preview.png"
        logo_width, logo_height = 40, 40
        c.drawImage(logo_path, 50, height - 100, width=logo_width, height=logo_height)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(95, height - 85, "TS DISTRIBUIDORA")
        c.drawString(300, height - 70, "Tabela de Sugestões de Compras")
        
        # Informações adicionais (na mesma linha)
        c.setFont("Helvetica", 10)
        info_text = f"Fabricante: {supplier}         Dias de Reposição: {replacement_days}         Dias de Suprimento: {supply_days}"
        c.drawString(50, height - 120, info_text)

    # Função para desenhar o cabeçalho da tabela
    def draw_table_header(c, table_y):
        c.setFont("Helvetica-Bold", 7)  # Cabeçalho em negrito
        columns = ["Descrição", "Cobertura", "Mês0", "Mês1", "Mês2", "Mês3", "Média Mês", "Estoque Disp.", "Sugestão Compra", "Valor Compra", "Curva"]
        
        x_position = 50
        for i, column in enumerate(columns):
            c.drawString(x_position, table_y, column)
            x_position += col_widths[i] + 1  # Adiciona margem entre colunas

    # Coloca a largura das colunas em uma variável para garantir acesso fora da função
    col_widths = [180, 50, 30, 30, 30, 30, 60, 80, 90, 80, 30]

    # Desenha o cabeçalho
    draw_header(c)
    
    # Ajusta a posição do Y para garantir que a primeira linha da tabela não sobreponha o cabeçalho
    table_y = height - 150  # Ajusta a posição para a primeira linha da tabela
    draw_table_header(c, table_y)
    
    # Adiciona um espaço extra após o cabeçalho da tabela antes da primeira linha de conteúdo
    table_y -= 20  # Espaço extra entre o cabeçalho da tabela e a primeira linha de conteúdo
    
    # Margem entre linhas para o conteúdo da tabela
    row_height = 15
    max_rows_per_page = 20  # Número máximo de linhas por página
    rows_on_page = 0

    # Define a fonte para o conteúdo da tabela (agora está normal, não negrito)
    c.setFont("Helvetica", 7)  # Fonte normal (sem negrito) para o conteúdo da tabela
    
    # Itera sobre o conteúdo da tabela e adiciona novas páginas conforme necessário
    for row in table_data:
        # Checa se é preciso criar uma nova página
        if rows_on_page >= max_rows_per_page:
            c.showPage()  # Cria nova página
            draw_header(c)  # Desenha o cabeçalho novamente
            table_y = height - 150  # Reseta a posição Y para a nova página
            draw_table_header(c, table_y)  # Desenha o cabeçalho da tabela novamente
            table_y -= 20  # Espaço extra após o cabeçalho para a primeira linha de conteúdo
            rows_on_page = 0  # Reseta a contagem de linhas na nova página

        # Adiciona cada célula da linha atual
        x_position = 50
        for i, cell in enumerate(row):
            c.drawString(x_position, table_y, str(cell))
            x_position += col_widths[i] + 1  # Atualiza a posição X para a próxima célula
        table_y -= row_height  # Atualiza a posição Y para a próxima linha
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