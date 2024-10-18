from database import get_db_connection

def fetch_suppliers():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = 'SELECT DISTINCT Fantasia AS nome FROM vw_infos'
    cursor.execute(query)
    result = cursor.fetchall()

    suppliers = [{'nome': row.nome} for row in result]

    cursor.close()
    connection.close()
    return suppliers