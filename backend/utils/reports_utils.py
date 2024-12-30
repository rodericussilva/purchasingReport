from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

REPORTS_DIR = os.path.join(os.getcwd(), 'static', 'reports_files')

def generate_pdf(supplier_data_list):
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
    row_height = 15

    def draw_header():
        logo_path = "static/logo-removebg-preview.png"
        logo_width, logo_height = 40, 40
        c.drawImage(logo_path, margin_left, height - margin_top - 40, width=logo_width, height=logo_height)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(margin_left + 45, height - margin_top - 35, "TS DISTRIBUIDORA")
        c.drawString(margin_left + 180, height - margin_top - 10, "Relatório de Produtos")

    def draw_supplier_info(supplier, table_y):
        c.setFont("Helvetica", 10)
        info_text = f"Fornecedor: {supplier}                                   Data de Geração: {datetime.now().strftime('%d/%m/%Y')}"
        c.drawString(margin_left, table_y, info_text)
        c.line(margin_left, table_y - 5, width - margin_right, table_y - 5)
        return table_y - 20

    def draw_table_header(table_y):
        c.setFont("Helvetica-Bold", 7)
        columns = ["Código", "Descrição", "Cobertura", "Unidades Faturadas Mês 3", "Unidades Faturadas Mês 2", "Unidades Faturadas Mês 1", "Unidades Faturadas Mês 0", "Méd. Mês", "Est. Disponível", "Est. Minimo", "Trânsito", "Sugestão de Compra", "Valor de Compra", "Curva"]
        x_position = margin_left
        for column in columns:
            c.drawString(x_position + 5, table_y - 10, column)
            x_position += col_widths[columns.index(column)]
        
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
            for i, cell in enumerate(row.values()):
                c.setFont("Helvetica", 8)
                c.drawString(x_position + 5, table_y - 10, str(cell))
                x_position += col_widths[i]

            draw_row_line(table_y)
            table_y -= row_height
            rows_on_page += 1

        return table_y

    def draw_summary_table_header(table_y, mes_labels):
        c.setFont("Helvetica-Bold", 7)
        columns = ["-", mes_labels['mes0'], mes_labels['mes1'], mes_labels['mes2'], mes_labels['mes3'], "Média Mês", "Total Disponível", "Sugestão"]
        x_position = margin_left
        for i, column in enumerate(columns):
            c.drawString(x_position + 5, table_y - 10, column)
            x_position += col_widths_summary[i]
        
        table_width = sum(col_widths_summary)
        c.rect(margin_left, table_y - 20, table_width, 20, stroke=1, fill=0)

        x_position = margin_left
        for width in col_widths_summary:
            c.line(x_position, table_y, x_position, table_y - 20)
            x_position += width

    def draw_summary_table_content(summary_data, table_y):
        rows_on_page = 0

        for row in summary_data:
            if rows_on_page >= max_rows_per_page or table_y - row_height < margin_bottom:
                table_y = new_page()
                draw_summary_table_header(table_y, row['mes_labels'])
                rows_on_page = 0

            x_position = margin_left
            for i, cell in enumerate(row.values()):
                c.setFont("Helvetica", 8)
                c.drawString(x_position + 5, table_y - 10, str(cell))
                x_position += col_widths_summary[i]

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

    col_widths = [50, 150, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
    col_widths_summary = [50, 50, 50, 50, 50, 50, 50, 50]
    max_rows_per_page = 20

    draw_header()
    table_y = height - margin_top - 80

    for supplier_data in supplier_data_list:
        supplier = supplier_data.get("supplier", "Desconhecido")
        table_data = supplier_data.get("produtos", [])
        summary_data = supplier_data.get("summary", [])

        if not isinstance(table_data, list):
            raise ValueError("A chave 'produtos' deve ser uma lista.")

        if table_y - margin_bottom < 150:
            table_y = new_page()

        table_y = draw_supplier_info(supplier, table_y)
        draw_table_header(table_y)
        table_y -= 25

        table_y = draw_table_content(table_data, table_y)

        if table_y - margin_bottom < 150:
            table_y = new_page()

        draw_summary_table_header(table_y, table_data[0]['mes_labels'])
        table_y -= 25

        table_y = draw_summary_table_content(summary_data, table_y)

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
        columns = ["Código", "Descrição", "Estoque Disponível", "Estoque Mínimo", "Em Trânsito", "Média Diária", "Curva"]
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

    col_widths = [80, 200, 100, 100, 100, 100, 80]
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
            for i, col in enumerate(["codigo", "descricao", "estoque_disponivel", "estoque_minimo", "estoque_transito", "media_diaria_venda", "curva"]):
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
        columns = ["Código", "Descrição", "Quantidade em Estoque", "Data do Vencimento", "Lote", "Curva"]
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

    col_widths = [80, 250, 100, 100, 100, 120]
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
        columns = ["Código", "Descrição", "Quantidade em Estoque", "Data da Última Venda", "Última Entrada", "Curva"]
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

    col_widths = [50, 270, 100, 110, 110, 80]
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
            for i, col in enumerate(["codigo", "descricao", "quantidade_estoque", "ultima_venda", "ultima_entrada", "curva"]):
                c.drawString(x_position + 5, table_y - 10, str(product.get(col, 'N/A')))
                x_position += col_widths[i]

            draw_row_line(c, table_y)
            table_y -= row_height
            rows_on_page += 1

        table_y -= 15

    c.save()
    return f"http://{os.getenv('FLASK_HOST')}:{os.getenv('FLASK_PORT')}/static/reports_files/{os.path.basename(pdf_path)}"