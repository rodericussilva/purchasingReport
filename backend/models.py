from database import get_db_connection

def fetch_suppliers():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        SELECT DISTINCT Fantasia AS nome
        FROM vw_fabri_prod
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
        SELECT Desc_Prod AS descricao
        FROM vw_fabri_prod
        WHERE Fantasia = ?
        ORDER BY descricao ASC
    """
    cursor.execute(query, (supplier_name,))
    result = cursor.fetchall()
    
    products = [{'descricao': row.descricao} for row in result]
    cursor.close()
    connection.close()
    return products