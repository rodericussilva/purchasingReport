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
	        f.Fantasia,
            p.Descricao,
            p.Codigo,
            pr.Sta_AbcUniVenFab,
            pr.Sta_AbcValFatFab,
            ROUND(pr.Prc_Venda, 2) AS Prc_Venda,
            pr.Qtd_Dispon,
            pr.Qtd_Fisico,
            pr.Qtd_Transi,
            pr.Qtd_EstMin,
            pr.Dat_UltVen,

                SUM(CASE WHEN MONTH(v.DATA) = MONTH(GETDATE()) AND YEAR(v.DATA) = YEAR(GETDATE()) THEN v.QUANTIDADE ELSE 0 END) AS Qtd_FatMes0,
		        LEFT(CASE MONTH(GETDATE())
			        WHEN 1 THEN 'JAN' WHEN 2 THEN 'FEV' WHEN 3 THEN 'MAR' WHEN 4 THEN 'ABR'
			        WHEN 5 THEN 'MAI' WHEN 6 THEN 'JUN' WHEN 7 THEN 'JUL' WHEN 8 THEN 'AGO'
			        WHEN 9 THEN 'SET' WHEN 10 THEN 'OUT' WHEN 11 THEN 'NOV' WHEN 12 THEN 'DEZ'
			        END, 3) AS Des_VenMes0,

		        SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -1, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -1, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) AS Qtd_FatMes1,
		        LEFT(CASE MONTH(DATEADD(MONTH, -1, GETDATE()))
			        WHEN 1 THEN 'JAN' WHEN 2 THEN 'FEV' WHEN 3 THEN 'MAR' WHEN 4 THEN 'ABR'
			        WHEN 5 THEN 'MAI' WHEN 6 THEN 'JUN' WHEN 7 THEN 'JUL' WHEN 8 THEN 'AGO'
			        WHEN 9 THEN 'SET' WHEN 10 THEN 'OUT' WHEN 11 THEN 'NOV' WHEN 12 THEN 'DEZ'
			        END, 3) AS Des_VenMes1,

		        SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -2, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -2, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) AS Qtd_FatMes2,
		        LEFT(CASE MONTH(DATEADD(MONTH, -2, GETDATE()))
			        WHEN 1 THEN 'JAN' WHEN 2 THEN 'FEV' WHEN 3 THEN 'MAR' WHEN 4 THEN 'ABR'
			        WHEN 5 THEN 'MAI' WHEN 6 THEN 'JUN' WHEN 7 THEN 'JUL' WHEN 8 THEN 'AGO'
			        WHEN 9 THEN 'SET' WHEN 10 THEN 'OUT' WHEN 11 THEN 'NOV' WHEN 12 THEN 'DEZ'
			        END, 3) AS Des_VenMes2,

		        SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -3, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -3, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) AS Qtd_FatMes3,
		        LEFT(CASE MONTH(DATEADD(MONTH, -3, GETDATE()))
			        WHEN 1 THEN 'JAN' WHEN 2 THEN 'FEV' WHEN 3 THEN 'MAR' WHEN 4 THEN 'ABR'
			        WHEN 5 THEN 'MAI' WHEN 6 THEN 'JUN' WHEN 7 THEN 'JUL' WHEN 8 THEN 'AGO'
			        WHEN 9 THEN 'SET' WHEN 10 THEN 'OUT' WHEN 11 THEN 'NOV' WHEN 12 THEN 'DEZ'
			        END, 3) AS Des_VenMes3,

		        ROUND((SUM(CASE WHEN MONTH(v.DATA) = MONTH(GETDATE()) AND YEAR(v.DATA) = YEAR(GETDATE()) THEN v.QUANTIDADE ELSE 0 END) +
		        SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -1, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -1, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) +
		        SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -2, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -2, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) +
		        SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -3, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -3, GETDATE())) THEN v.QUANTIDADE ELSE 0 END)) / 4.0, 2) AS Media_Fat,

		        ROUND((SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -1, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -1, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) +
		        SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -2, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -2, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) +
		        SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -3, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -3, GETDATE())) THEN v.QUANTIDADE ELSE 0 END)) / 90.0, 2) AS Media_Diaria_Trimestre
        FROM 
            fVENDAS v
        JOIN 
            PRODU p ON v.IDPRODUTO = p.Codigo
        JOIN
	        FABRI f ON p.Cod_Fabricante = f.Codigo
        JOIN PRXES pr ON pr.Cod_Produt = p.Codigo
        WHERE f.Fantasia = ?
        GROUP BY 
	        f.Fantasia,
            p.Descricao,
            p.Codigo,
            pr.Sta_AbcUniVenFab,
            pr.Sta_AbcValFatFab,
            pr.Prc_Venda,
            pr.Qtd_Dispon,
            pr.Qtd_Fisico,
            pr.Qtd_Transi,
            pr.Qtd_EstMin,
            pr.Dat_UltVen
        ORDER BY p.Descricao ASC
    """
    cursor.execute(query, (supplier_name,))
    result = cursor.fetchall()

    products = []

    for row in result:
        formatted_price = f"R$ {float(row.Prc_Venda):,.2f}".replace(".", ",")
        formatted_avg = int(row.Media_Fat)

        media_faturamento_diario = row.Media_Fat / 30 if formatted_avg > 0 else 1
        cobertura = int(formatted_avg / media_faturamento_diario)

        dias_suprimento_total = replacement_days + supply_days
        sugestao_compra = int((media_faturamento_diario or 0 * dias_suprimento_total) - row.Qtd_Dispon)

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
            'valor_venda': formatted_price,
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

def fetch_total_suggestions():
    connection = get_db_connection()
    cursor = connection.cursor()

    replacement_days = 7  # default value to help with the sum
    supply_days = 14  # default value to help with the sum
    dias_suprimento_total = replacement_days + supply_days

    query = f"""
        SELECT COUNT(*) AS total
        FROM (
            SELECT 
                ROUND((SUM(CASE WHEN MONTH(v.DATA) = MONTH(GETDATE()) AND YEAR(v.DATA) = YEAR(GETDATE()) THEN v.QUANTIDADE ELSE 0 END) +
			    SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -1, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -1, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) +
			    SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -2, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -2, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) +
			    SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -3, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -3, GETDATE())) THEN v.QUANTIDADE ELSE 0 END)) / 4.0, 2) AS media_faturada,
                
                pr.Qtd_Dispon,

                -- Calcula sugestao_compra com media_faturada calculada dentro do SELECT
                ROUND(((SUM(CASE WHEN MONTH(v.DATA) = MONTH(GETDATE()) AND YEAR(v.DATA) = YEAR(GETDATE()) THEN v.QUANTIDADE ELSE 0 END) +
			    SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -1, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -1, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) +
			    SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -2, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -2, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) +
			    SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -3, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -3, GETDATE())) THEN v.QUANTIDADE ELSE 0 END)) / 4.0 * {dias_suprimento_total}) - pr.Qtd_Dispon, 2) AS sugestao_compra

            FROM fVENDAS v
            JOIN PRODU p ON v.IDPRODUTO = p.Codigo
            JOIN FABRI f ON p.Cod_Fabricante = f.Codigo
            JOIN PRXES pr ON pr.Cod_Produt = p.Codigo
            GROUP BY p.Codigo, pr.Qtd_Dispon
        ) AS subquery
        WHERE sugestao_compra > 0;
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    total_suggestions = int(result[0][0]) if result else 0

    cursor.close()
    connection.close()
    return total_suggestions

def fetch_products_and_calculate_rupture(supplier_name, days_estimate):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    SELECT 
        f.Fantasia,
        p.Descricao,
        p.Codigo,
        pr.Sta_AbcUniVenFab,
        pr.Sta_AbcValFatFab,
        pr.Qtd_Dispon,
        pr.Qtd_Fisico,
        pr.Qtd_Transi,
        pr.Qtd_EstMin,
        v.idproduto,
        v.idfabricante,
        (SUM(CASE WHEN MONTH(v.DATA) = MONTH(GETDATE()) AND YEAR(v.DATA) = YEAR(GETDATE()) THEN v.QUANTIDADE ELSE 0 END) +
        SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -1, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -1, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) +
        SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -2, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -2, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) +
        SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -3, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -3, GETDATE())) THEN v.QUANTIDADE ELSE 0 END)) AS Total_Ult_4_meses,

        ROUND(SUM(v.QUANTIDADE) / 90.0, 2) AS media_diaria_venda  -- Média diária de vendas (último trimestre)
    FROM 
        fVENDAS v
    JOIN 
        PRODU p ON v.IDPRODUTO = p.Codigo
    JOIN 
        FABRI f ON p.Cod_Fabricante = f.Codigo
    JOIN 
        PRXES pr ON pr.Cod_Produt = p.Codigo
    WHERE
        f.Fantasia = ?  -- Filtro para o nome do fornecedor
        AND v.DATA >= DATEADD(MONTH, -3, GETDATE())  -- Filtra vendas no último trimestre (últimos 3 meses)
    GROUP BY 
        f.Fantasia, 
        p.Descricao, 
        p.Codigo, 
        pr.Sta_AbcUniVenFab, 
        pr.Sta_AbcValFatFab, 
        pr.Qtd_Dispon, 
        pr.Qtd_Fisico, 
        pr.Qtd_Transi, 
        pr.Qtd_EstMin, 
        v.idproduto, 
        v.idfabricante
    ORDER BY 
        p.Descricao ASC;
    """
    
    cursor.execute(query, (supplier_name,))
    result = cursor.fetchall()
    
    products = []
    
    for row in result:
        descricao = row.Descricao
        estoque_disponivel = row.Qtd_Dispon
        estoque_fisico = row.Qtd_Fisico
        estoque_transito = row.Qtd_Transi
        media_diaria_venda = row.media_diaria_venda
        estoque_minimo = row.Qtd_EstMin,
        curva = row.Sta_AbcUniVenFab,
        total_estoque = estoque_disponivel + estoque_fisico + estoque_transito
        
        previsao_vendas = media_diaria_venda * days_estimate
        risco_ruptura = total_estoque - previsao_vendas
        
        products.append({
            'descricao': descricao,
            'estoque_fisico': estoque_fisico,
            'estoque_disponivel': estoque_disponivel,
            'estoque_transito': estoque_transito,
            'estoque_minimo': estoque_minimo,
            'curva': curva,
            'media_diaria_venda': media_diaria_venda,
            'previsao_vendas': previsao_vendas,
            'risco_ruptura': risco_ruptura
        })
    
    cursor.close()
    connection.close()
    
    return products