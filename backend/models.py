from database import get_db_connection

def fetch_suppliers():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        SELECT DISTINCT Fantasia AS nome
        FROM vw_fabri_produ
        ORDER BY Fantasia ASC
    """
    cursor.execute(query)
    result = cursor.fetchall()

    suppliers = [{'nome': row.nome} for row in result]

    cursor.close()
    connection.close()
    return suppliers

def fetch_product_supplires(supplier_name):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT DISTINCT
            Desc_Prod AS descricao,
            Qtd_VenMes0,
            Qtd_VenMes1,
            Qtd_VenMes2,
            Sta_AbcUniVenFab
        FROM vw_fabri_produt
        WHERE Fantasia = ?
        ORDER BY descricao ASC
    """
    cursor.execute(query, (supplier_name,))
    result = cursor.fetchall()

    products = []
    for row in result:
        products.append({
            'descricao': row.descricao,
            'unidades_faturadas_mes1': row.Qtd_VenMes0,
            'unidades_faturadas_mes2': row.Qtd_VenMes1,
            'unidades_faturadas_mes3': row.Qtd_VenMes2,
            'curva': row.Sta_AbcUniVenFab,
        })

    cursor.close()
    connection.close()
    return products

def fetch_month_abbreviations():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    query = """
        SELECT 
            Des_VenMes2 AS mes3,
            Des_VenMes1 AS mes2,
            Des_VenMes0 AS mes1
        FROM vw_fabri_produt
    """
    
    cursor.execute(query)
    result = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    return {
        'mes3': result.mes3,
        'mes2': result.mes2,
        'mes1': result.mes1
    }