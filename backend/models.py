from database import get_db_connection
from datetime import datetime
import calendar

def fetch_suppliers():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        SELECT DISTINCT Fantasia AS nome
        FROM vw_fabric_produto
        ORDER BY Fantasia ASC
    """
    cursor.execute(query)
    result = cursor.fetchall()

    suppliers = [{'nome': row.nome} for row in result]

    cursor.close()
    connection.close()
    return suppliers

def fetch_products_by_supplier(supplier_name):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT  
            Descricao,
            Qtd_FatMes0,
            Qtd_FatMes1,
            Qtd_FatMes2,
            Qtd_FatMes3,
            Media_Fat,
            Qtd_EstMin,
            Qtd_Ressup,
            Qtd_Dispon,
            Qtd_Sugest,
            Prc_UniCom,
            Sta_AbcUniVenFab,
            mes0 AS Des_VenMes0,
            mes1 AS Des_VenMes1,
            mes2 AS Des_VenMes2,
            mes3 AS Des_VenMes3
        FROM vw_fabric_produto
        WHERE Fantasia = ?
        ORDER BY Descricao ASC
    """
    cursor.execute(query, (supplier_name,))
    result = cursor.fetchall()

    last_four_months = get_last_four_months()

    products = []
    for row in result:

        formatted_value = f"R$ {float(row.Prc_UniCom):,.2f}".replace(".", ",")
        products.append({
            'descricao': row.Descricao,
            'unidades_faturadas_mes0': row.Qtd_FatMes0,
            'unidades_faturadas_mes1': row.Qtd_FatMes1,
            'unidades_faturadas_mes2': row.Qtd_FatMes2,
            'unidades_faturadas_mes3': row.Qtd_FatMes3,
            'media_faturada': row.Media_Fat,
            'estoque_minimo': row.Qtd_EstMin,
            'estoque_suprimento': row.Qtd_Ressup,
            'estoque_disponivel': row.Qtd_Dispon,
            'sugestao_compra': row.Qtd_Sugest,
            'valor_compra': formatted_value,
            'curva': row.Sta_AbcUniVenFab,
            'mes_labels': {
                'mes0': last_four_months[3],
                'mes1': last_four_months[2],
                'mes2': last_four_months[1],
                'mes3': last_four_months[0],
            }
        })

    cursor.close()
    connection.close()
    return products

def get_last_four_months():
    current_month = datetime.now().month
    current_year = datetime.now().year

    months = []
    for i in range(4):
        month_index = (current_month - i - 1) % 12 + 1
        month_abbr = calendar.month_abbr[month_index].upper()
        
        month_abbr_pt = {
            "JAN": "JAN", "FEB": "FEV", "MAR": "MAR", "APR": "ABR",
            "MAY": "MAI", "JUN": "JUN", "JUL": "JUL", "AUG": "AGO",
            "SEP": "SET", "OCT": "OUT", "NOV": "NOV", "DEC": "DEZ"
        }
        
        months.append(month_abbr_pt.get(month_abbr, month_abbr))
    
    return months[::-1]