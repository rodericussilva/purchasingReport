from database import get_db_connection

def fetch_suppliers():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        SELECT DISTINCT Fantasia AS nome
        FROM vw_dados_compras
        ORDER BY Fantasia ASC
    """
    cursor.execute(query)
    result = cursor.fetchall()
    suppliers = [{'nome': row.nome} for row in result]
    cursor.close()
    connection.close()
    return suppliers

def fetch_products_by_supplier(supplier_name, replacement_days, supply_days):
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
            Qtd_Dispon,
            Prc_Venda AS Prc_UniCom,
            Sta_AbcUniVenFab,
            Des_VenMes0,
            Des_VenMes1,
            Des_VenMes2,
            Des_VenMes3
        FROM vw_dados_compras
        WHERE Fantasia = ?
        ORDER BY Descricao ASC
    """
    cursor.execute(query, (supplier_name,))
    result = cursor.fetchall()

    products = []
    for row in result:
        formatted_price = f"R$ {float(row.Prc_UniCom):,.2f}".replace(".", ",")
        formatted_avg = int(row.Media_Fat)

        media_faturamento_diario = row.Media_Fat / 30 if formatted_avg > 0 else 1
        cobertura = int(row.Qtd_Dispon / media_faturamento_diario)

        dias_suprimento_total = replacement_days + supply_days
        sugestao_compra = int((media_faturamento_diario * dias_suprimento_total) - row.Qtd_Dispon)

        products.append({
            'descricao': row.Descricao,
            'unidades_faturadas_mes0': row.Qtd_FatMes0,
            'unidades_faturadas_mes1': row.Qtd_FatMes1,
            'unidades_faturadas_mes2': row.Qtd_FatMes2,
            'unidades_faturadas_mes3': row.Qtd_FatMes3,
            'media_faturada': formatted_avg,
            'estoque_minimo': row.Qtd_EstMin,
            'estoque_disponivel': row.Qtd_Dispon,
            'sugestao_compra': sugestao_compra,
            'valor_compra': formatted_price,
            'curva': row.Sta_AbcUniVenFab,
            'cobertura': cobertura,
            'mes_labels': {
                'mes0': row.Des_VenMes0,
                'mes1': row.Des_VenMes1,
                'mes2': row.Des_VenMes2,
                'mes3': row.Des_VenMes3
            }
        })

    cursor.close()
    connection.close()
    return products