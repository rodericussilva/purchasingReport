from database import get_db_connection

def fetch_suppliers():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        SELECT Fantasia AS nome, Descricao AS categoria
        FROM vw_fabri_cat
        WHERE Descricao LIKE '%Farma%'
    """
    cursor.execute(query)
    result = cursor.fetchall()

    suppliers = [{'nome': row.nome, 'categoria': row.categoria} for row in result]

    cursor.close()
    connection.close()
    return suppliers