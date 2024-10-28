from database import get_db_connection

def fetch_suppliers():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        SELECT DISTINCT Fantasia AS nome
        FROM vw_fabric_produ
        ORDER BY Fantasia ASC
    """
    cursor.execute(query)
    result = cursor.fetchall()

    suppliers = [{'nome': row.nome} for row in result]

    cursor.close()
    connection.close()
    return suppliers

def fetch_product_suppliers(supplier_name):
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
            Des_VenMes0,
            Des_VenMes1,
            Des_VenMes2,
            Des_VenMes3
        FROM vw_fabric_produ
        WHERE Fantasia = ?
        ORDER BY Descricao ASC
    """
    cursor.execute(query, (supplier_name,))
    result = cursor.fetchall()

    products = []
    for row in result:
        products.append({
            'descricao': row.Descricao,
            'unidades_faturadas_mes0': row.Qtd_FatMes0,
            'unidades_faturadas_mes1': row.Qtd_FatMes1,
            'unidades_faturadas_mes2': row.Qtd_FatMes2,
            'unidades_faturadas_mes2': row.Qtd_FatMes3,
            'media_faturada': row.Media_Fat,
            'estoque_minimo': row.Qtd_EstMin,
            'estoque_suprimento': row.Qtd_Ressup,
            'estoque_disponivel': row.Qtd_Dispon,
            'sugestao_compra': row.Qtd_Sugest,
            'valor_compra': row.Prc_UniCom,
            'curva': row.Sta_AbcUniVenFab,
            'mes_labels': {
                'mes0': row.Des_VenMes0,
                'mes1': row.Des_VenMes1,
                'mes2': row.Des_VenMes2,
                'mes3': row.Des_VenMes3,
            }
        })

    cursor.close()
    connection.close()
    return products