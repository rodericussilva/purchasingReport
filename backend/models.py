from database import get_db_connection
from datetime import datetime
from decimal import Decimal

def fetch_suppliers():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        SELECT DISTINCT
            f.Fantasia AS nome
        FROM V_PRCPL AS vpr
        JOIN PRODU AS p ON p.Codigo = vpr.Codigo
        JOIN FABRI AS f ON p.Cod_Fabricante = f.Codigo
        WHERE f.Fantasia NOT IN (
            '3M', 
            'CANNONE', 
            'CALUETE E PINHO LTDA', 
            'CABEPEL', 
            'C&M FARDAMENTOS', 
            'C ROLIM', 
            'C B DIAS ME', 
            'C & M FARDAMENTOS', 
            'CARMEHIL',
		    'BISCOITOS BRIEJER CONFEIT',
		    'AGATEK',
		    'AGIS',
		    'AILDA MARIA',
		    'AILEC',
		    'AKUA',
		    'ANDREA FIRMINO',
		    'APIGUANA',
		    'ASA SUL',
		    'ATACADÃO DAS BEBIDAS',
		    'AVENPAR',
		    'BASALL',
		    'BLOCKBIT TECNOLOGIA LTDA',
		    'BRASIL PC',
		    'CANONNE',
		    'CARAUBAS',
		    'CARMEHIL COMERCIAL',
		    'CARONE',
		    'CASA DA CONSTRUÇÃO',
		    'CASAS BAHIA',
		    'CASA MAGALHAES',
		    'CEARA DISTRIBUIDORA',
		    'CECOMIL',
		    'CEFIS',
		    'CELTA',
		    'CENTER AÇO',
		    'CENTRO DO TIJOLO',
		    'CEQUIP',
		    'CHINA CEPREI (SICHUAN)',
		    'CHRON EPIGEN',
		    'CIA DOS NOVOS',
		    'CLARUS',
		    'CLAUDIA LUCIA ARAUJO SARA',
		    'CLEANTECH',
		    'COCO BAMBU',
		    'COLGATE',
		    'COLOPLAST',
		    'COMERCIAL MAB',
		    'COMPUCARD',
		    'CONTRULOPES',
		    'CONVATEC',
		    'CRISTIANO MOTOS',
		    'CSL BEHRING AG',
		    'D M F L JR PRODUTOS DE LI',
		    'DANILO',
		    'DANONE',
		    'DB RIBEIRO',
		    'DELL',
		    'DELLA VIDA',
		    'DINDIN DA REH',
		    'DISPAFILM',
		    'DISTRIMEDICA COMERCIO DE',
		    'DIVERSOS',
		    'DUFRIO',
		    'DYNAMOVA',
		    'E N C OLIVEIRA SERV DE PR',
		    'EDITORA PREMIUS LTDA',
		    'EDIZIO JOAQUIM DOS SANTOS',
		    'ELENMARK',
		    'ELETRONICA AMOR',
		    'ELETRONICA APOLO',
		    'FAMI',
		    'FERCOL',
		    'FILIP´S DISTRIBUIDORA LTD',
		    'FJESUS',
		    'FLATEX',
		    'FLEXOR',
		    'FLEXPELL',
		    'FORCA DIGITAL',
		    'FORT FLEX',
		    'FORTE ESTRUTURAS',
		    'FQM',
		    'FRANCISCO DE ASSIS',
		    'FRANCISCO PEREIRA',
		    'FRANCISCO ROMULO DE LIMA',
		    'FRANCO RODRIGUES',
		    'FREITAS VAREJO',
		    'FRIGELAR',
		    'FRIOPEÇAS',
		    'GELOTECH',
		    'GIFT MAIS',
		    'GLAXOSMITHKLINE',
		    'GLOBAL',
		    'GRAN MAREIRO',
		    'GRIFOLS BRASIL',
		    'G-TECH',
		    'HARTE INSTRUMENTOS CIRURG',
		    'HC PNEUS',
		    'HENHIQUE PEREIRA GAPAZI',
		    'HIDROLIGHT',
		    'HIDROLIGHT 2',
		    'IBYTE',
		    'IMPERIAL',
		    'INGRAM',
		    'INSTITUTO PROTEGE',
		    'INTRACORP',
		    'ISDIN PROD FARMACEUTICOS',
		    'IU-A HOTEL',
		    'JAGF COMERCIO VAREJISTA D',
		    'JAGUAR',
		    'JALLES MACHADO S.A',
		    'JC',
		    'JL PLACAS',
		    'JM COMERCIO DE GAS',
		    'JMARTINS',
		    'JMM',
		    'JMX',
		    'JNA',
		    'JOHNSON & JOHNSON',
		    'JOSE IVANILDO MIRANDA MAT',
		    'JPS ELETRONICA LTDA ME',
		    'KALUNGA',
		    'KASMED',
		    'KEDRION BRASIL DISTRIBUID',
		    'KELLDRIN',
		    'KODAK',
		    'L N L COMERCIAL MOVIS',
		    'LA ROCHE POSAY',
		    'LAIANA JUVENAL DE ALMEIDA',
		    'LATINOFARMA',
		    'LENOVO',
		    'LEROY',
		    'LFB',
		    'LIMPIDA',
		    'LINEA',
		    'LM CAMPOS',
		    'LOCAWARE',
		    'LOJAO DOS ESPORTES',
		    'LOREAL',
		    'LOVE YOUR SKIN',
		    'LUBEKA',
		    'LUDAN INDUSTRIA E COMERCI',
		    'LUNDBECK',
		    'LUSTRAR',
		    'M4 DISTRIBUIDORA LTDA',
		    'MACAVI',
		    'MADEIREIRA GEOVANE LTDA M',
		    'MADEREIRA RIO BRANCO',
		    'MADESERPA',
		    'MAGAZINE LUIZA',
		    'MAPPEL',
		    'MARCIO GOMERS',
		    'MARIOL',
		    'MASTERFIX',
		    'MB TEXTIL LTDA',
		    'MDR SAUDE',
		    'MDR SAUDE',
		    'METAL KING',
		    'MG',
		    'MIDFARMA',
		    'MIL COMERCIO DE EMBALAGEN',
		    'MIL PLAST',
		    'MILLET ROUX',
		    'MINASREY',
		    'MM ETIQUETAS',
		    'MONTSERRAT',
		    'MUNDIPHARMA',
		    'N TAPETES',
		    'NAGEM',
		    'NAGEM IGUATEMI',
		    'NATCOFARMA BRASIL',
		    'NATHY',
		    'NESTLE',
		    'NEWSEDAN COM DE VEICULOS',
		    'NILKO',
		    'NORDESTE DISTRIBUIDORA',
		    'NORMATEL',
		    'NOVO NORDISK',
		    'NYCOMED',
		    'OCTAPHARMA',
		    'OFFICER',
		    'OFTALMOPHARMA',
		    'OPÇÃO',
		    'OSORIO DE MORAES',
		    'OXIGEL',
		    'PARDAL',
		    'PEREIRA DIESEL',
		    'PERFIL',
		    'PIAUI PLASTICOS',
		    'PIERRE FABRE',
		    'PLENA FRALDAS',
		    'POINT CENTER',
		    'PROGRAMA OFFFICE',
		    'PROHOSPITAL',
		    'QUEIJOS E VINHOS',
		    'R BAIAO',
		    'R7 INFORMATICA',
		    'RAIMUNDO CICERO ARAUJO',
		    'RAMALHO TEXTIL',
		    'RANGEL',
		    'RAPHAEL MARQUES OLIVEIRA',
		    'RAPIGEN',
		    'RAVA',
		    'RAYSSA BRITO',
		    'RC CONFECÇÃO',
		    'RECAMONDE COUROS LTDA',
		    'REDE EXPRESS',
		    'REDE MAQUINAS',
		    'REGENCE VEICULOS LTDA',
		    'RMC',
		    'RMDESC',
		    'ROC',
		    'RVT',
		    'SAFTI',
		    'SANSUNG',
		    'SAO LUIZ',
		    'SAO ROQUE ARTEFATOS',
		    'SATURNO SISTEMAS INTEGRAD',
		    'SCHIWAY',
		    'SEM FABRICANTE',
		    'SERIKAKU',
		    'SERILOS COMERCIO LTDA',
		    'SERVIS ELETRONICA',
		    'SEVEN CARE',
		    'SHIRE',
		    'SHOPPING DA LIMPEZA',
		    'SILICONTECH',
		    'SILVESTRE LABS',
		    'SL COM DE COMB E DERIV',
		    'SND',
		    'SODINE',
		    'SOS CONDOMINIO',
		    'SOUL GOURMET',
		    'SUNDOWN NATURALS',
		    'SUPRI',
		    'SV COMERCIO DE MATERIAL',
		    'TALIMPO',
		    'TARCILENE',
		    'TERRA DA LUZ',
		    'THIAGO HENRIQUE',
		    'TILIBRA',
		    'TIM',
		    'TOK PEL',
		    'TOK&STOK',
		    'TOPLINE',
		    'TRANSPORTE',
		    'TRUEREAD',
		    'TVC COM DE DERIV DE ÇET',
		    'UNENTEL',
		    'UNISPEED GRAFICA E EDITOR',
		    'UNITED MEDICAL LTDA.',
		    'UNIVERSAL DISTRIBUIDORA',
		    'VERTICAL EMPILHADEIRAS',
		    'VIA SUL',
		    'VIDFARMA',
		    'VITA MEDICAL',
		    'VOLKSVAGEN',
		    'WESTCON',
		    'WS IND DE GRANITO',
		    'YESO MED',
		    'ZENIR',
		    'ZEST',
		    'ZHALINGER',
		    'ZODIAC',
		    'ZULU',
		    'FACCHINI',
		    'FABIO GONÇALVES',
		    'EXTINFOGO',
		    'EXACTA',
		    'FALO SPORT'
        )
        ORDER BY Fantasia ASC
    """
    cursor.execute(query)
    result = cursor.fetchall()
    
    suppliers = [{'nome': row.nome} for row in result]
    
    cursor.close()
    connection.close()
    
    return suppliers

def fetch_products_by_suppliers(supplier_names, replacement_days, supply_days):
    connection = get_db_connection()
    cursor = connection.cursor()

    placeholders = ', '.join(['?'] * len(supplier_names))

    query = f"""
        SELECT
            f.Fantasia AS fornecedor,
            p.Descricao,
            p.Codigo,
            pr.Sta_AbcUniVenFab,
            pr.Prc_Venda,
            ROUND(nfe.Prc_UniFat, 2) AS Prc_Compra,
            COALESCE(pul.C_QtdPulmao, 0) AS C_QtdPulmao,
            COALESCE(pr.Qtd_Dispon, 0) AS Qtd_Dispon,
            COALESCE(pr.Qtd_EstMin, 0) AS Qtd_EstMin,
            SUM(COALESCE(CASE WHEN MONTH(v.DATA) = MONTH(GETDATE()) AND YEAR(v.DATA) = YEAR(GETDATE()) THEN v.QUANTIDADE ELSE 0 END, 0)) AS Qtd_FatMes0,
            LEFT(CASE MONTH(GETDATE())
                WHEN 1 THEN 'JAN' WHEN 2 THEN 'FEV' WHEN 3 THEN 'MAR' WHEN 4 THEN 'ABR'
                WHEN 5 THEN 'MAI' WHEN 6 THEN 'JUN' WHEN 7 THEN 'JUL' WHEN 8 THEN 'AGO'
                WHEN 9 THEN 'SET' WHEN 10 THEN 'OUT' WHEN 11 THEN 'NOV' WHEN 12 THEN 'DEZ'
                END, 3) AS Des_VenMes0,
            SUM(COALESCE(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -1, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -1, GETDATE())) THEN v.QUANTIDADE ELSE 0 END, 0)) AS Qtd_FatMes1,
            LEFT(CASE MONTH(DATEADD(MONTH, -1, GETDATE()))
                WHEN 1 THEN 'JAN' WHEN 2 THEN 'FEV' WHEN 3 THEN 'MAR' WHEN 4 THEN 'ABR'
                WHEN 5 THEN 'MAI' WHEN 6 THEN 'JUN' WHEN 7 THEN 'JUL' WHEN 8 THEN 'AGO'
                WHEN 9 THEN 'SET' WHEN 10 THEN 'OUT' WHEN 11 THEN 'NOV' WHEN 12 THEN 'DEZ'
                END, 3) AS Des_VenMes1,
            SUM(COALESCE(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -2, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -2, GETDATE())) THEN v.QUANTIDADE ELSE 0 END, 0)) AS Qtd_FatMes2,
            LEFT(CASE MONTH(DATEADD(MONTH, -2, GETDATE()))
                WHEN 1 THEN 'JAN' WHEN 2 THEN 'FEV' WHEN 3 THEN 'MAR' WHEN 4 THEN 'ABR'
                WHEN 5 THEN 'MAI' WHEN 6 THEN 'JUN' WHEN 7 THEN 'JUL' WHEN 8 THEN 'AGO'
                WHEN 9 THEN 'SET' WHEN 10 THEN 'OUT' WHEN 11 THEN 'NOV' WHEN 12 THEN 'DEZ'
                END, 3) AS Des_VenMes2,
            SUM(COALESCE(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -3, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -3, GETDATE())) THEN v.QUANTIDADE ELSE 0 END, 0)) AS Qtd_FatMes3,
            LEFT(CASE MONTH(DATEADD(MONTH, -3, GETDATE()))
                WHEN 1 THEN 'JAN' WHEN 2 THEN 'FEV' WHEN 3 THEN 'MAR' WHEN 4 THEN 'ABR'
                WHEN 5 THEN 'MAI' WHEN 6 THEN 'JUN' WHEN 7 THEN 'JUL' WHEN 8 THEN 'AGO'
                WHEN 9 THEN 'SET' WHEN 10 THEN 'OUT' WHEN 11 THEN 'NOV' WHEN 12 THEN 'DEZ'
                END, 3) AS Des_VenMes3,
            ROUND((SUM(COALESCE(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -1, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -1, GETDATE())) THEN v.QUANTIDADE ELSE 0 END, 0)) +
            SUM(COALESCE(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -2, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -2, GETDATE())) THEN v.QUANTIDADE ELSE 0 END, 0)) +
            SUM(COALESCE(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -3, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -3, GETDATE())) THEN v.QUANTIDADE ELSE 0 END, 0))) / 3.0, 2) AS Media_Fat
        FROM 
            fVENDAS v
        JOIN 
            PRODU p ON v.IDPRODUTO = p.Codigo
        JOIN
            FABRI f ON p.Cod_Fabricante = f.Codigo
        JOIN
            PRXES pr ON p.Codigo = pr.Cod_Produt
        JOIN (
            SELECT 
                Cod_Produto, 
                Prc_UniFat,
                ROW_NUMBER() OVER (PARTITION BY Cod_Produto ORDER BY Dat_Movimento DESC) AS rn
            FROM NFEIT
        ) nfe ON nfe.Cod_Produto = p.Codigo AND nfe.rn = 1
        LEFT JOIN 
            V_PULMAO AS pul ON v.IDPRODUTO = pul.Cod_Produto
        WHERE f.Fantasia IN ({placeholders})
        GROUP BY 
            f.Fantasia,
            p.Descricao,
            p.Codigo,
            pr.Sta_AbcUniVenFab,
            pr.Prc_Venda,
            nfe.Prc_UniFat,
            pul.C_QtdPulmao,
            pr.Qtd_Dispon,
            pr.Qtd_EstMin
        ORDER BY 
            p.Descricao ASC;
    """
    cursor.execute(query, supplier_names)
    result = cursor.fetchall()

    suppliers = {}
    sugestao_compra = {}
    supplier_totals = {}

    for row in result:
        formatted_buy_price = f"R$ {float(row.Prc_Compra):,.2f}".replace(".", ",")
        formatted_sale_price = f"R$ {float(row.Prc_Venda):,.2f}".replace(".", ",")
        formatted_avg = int(row.Media_Fat)
        fornecedor = row.fornecedor
        total_stock = row.Qtd_Dispon + row.C_QtdPulmao

        demanda_media_diaria = row.Media_Fat / 30 if formatted_avg > 0 else Decimal('0.000000001')

        dias_cobertura = replacement_days + supply_days

        sugestao = (demanda_media_diaria * dias_cobertura) - total_stock
        if total_stock == 0 and sugestao == 0 and row.Qtd_EstMin > 0:
            sugestao = row.Qtd_EstMin
        sugestao = round(sugestao, 2)

        cobertura = total_stock / demanda_media_diaria if demanda_media_diaria > 0 else 0.000000001
        cobertura = round(cobertura)

        sugestao_compra[row.Codigo] = sugestao


        if fornecedor not in supplier_totals:
            supplier_totals[fornecedor] = {
                "total_vendas_mes0": Decimal(0),
                "total_vendas_mes1": Decimal(0),
                "total_vendas_mes2": Decimal(0),
                "total_vendas_mes3": Decimal(0),
                "total_disponivel": Decimal(0),
                "total_preco_compra": Decimal(0),
                "total_preco_compra_mes0": Decimal(0),
                "total_preco_compra_mes1": Decimal(0),
                "total_preco_compra_mes2": Decimal(0),
                "total_preco_compra_mes3": Decimal(0),
                "total_preco_venda": Decimal(0),
                "total_preco_venda_mes0": Decimal(0),
                "total_preco_venda_mes1": Decimal(0),
                "total_preco_venda_mes2": Decimal(0),
                "total_preco_venda_mes3": Decimal(0),
                "total_unidades_sugeridas": int(0),
                "total_sugestao_compra_valor": Decimal(0),
                "total_sugestao_venda_valor": Decimal(0)
            }

        preco_unitario = Decimal(row.Prc_Compra or "0")
        preco_venda = Decimal(row.Prc_Venda or "0")
        quantidade_disponivel = int(row.Qtd_Dispon or "0")

        supplier_totals[fornecedor]["total_vendas_mes0"] += row.Qtd_FatMes0
        supplier_totals[fornecedor]["total_vendas_mes1"] += row.Qtd_FatMes1
        supplier_totals[fornecedor]["total_vendas_mes2"] += row.Qtd_FatMes2
        supplier_totals[fornecedor]["total_vendas_mes3"] += row.Qtd_FatMes3
        supplier_totals[fornecedor]["total_disponivel"] += quantidade_disponivel
        supplier_totals[fornecedor]["total_preco_compra"] += preco_unitario * quantidade_disponivel
        supplier_totals[fornecedor]["total_preco_compra_mes0"] += preco_unitario * Decimal(row.Qtd_FatMes0)
        supplier_totals[fornecedor]["total_preco_compra_mes1"] += preco_unitario * Decimal(row.Qtd_FatMes1)
        supplier_totals[fornecedor]["total_preco_compra_mes2"] += preco_unitario * Decimal(row.Qtd_FatMes2)
        supplier_totals[fornecedor]["total_preco_compra_mes3"] += preco_unitario * Decimal(row.Qtd_FatMes3)
        supplier_totals[fornecedor]["total_preco_venda"] += preco_venda * (Decimal(row.Qtd_FatMes0) + Decimal(row.Qtd_FatMes1) + Decimal(row.Qtd_FatMes2) + Decimal(row.Qtd_FatMes3))
        supplier_totals[fornecedor]["total_preco_venda_mes0"] += preco_venda * Decimal(row.Qtd_FatMes0)
        supplier_totals[fornecedor]["total_preco_venda_mes1"] += preco_venda * Decimal(row.Qtd_FatMes1)
        supplier_totals[fornecedor]["total_preco_venda_mes2"] += preco_venda * Decimal(row.Qtd_FatMes2)
        supplier_totals[fornecedor]["total_preco_venda_mes3"] += preco_venda * Decimal(row.Qtd_FatMes3)

        if isinstance(sugestao_compra, dict) and row.Codigo in sugestao_compra:
            sugestao = sugestao_compra[row.Codigo]
            if sugestao > 0:
                supplier_totals[fornecedor]["total_unidades_sugeridas"] += int(sugestao)
                supplier_totals[fornecedor]["total_sugestao_compra_valor"] += sugestao * preco_unitario
                supplier_totals[fornecedor]["total_sugestao_venda_valor"] += sugestao * preco_venda

        product = {
            'codigo': row.Codigo,
            "fornecedor": fornecedor,
            'descricao': row.Descricao,
            "preco_unitario": formatted_buy_price,
            'unidades_faturadas_mes0': row.Qtd_FatMes0,
            'unidades_faturadas_mes1': row.Qtd_FatMes1,
            'unidades_faturadas_mes2': row.Qtd_FatMes2,
            'unidades_faturadas_mes3': row.Qtd_FatMes3,
            'media_faturada': formatted_avg,
            'estoque_minimo': row.Qtd_EstMin,
            'estoque_disponivel': row.Qtd_Dispon,
            'transito': row.C_QtdPulmao or 0,
            'sugestao_compra': sugestao,
            'valor_compra': formatted_buy_price,
            'valor_venda': formatted_sale_price,
            'curva': row.Sta_AbcUniVenFab,
            'cobertura': cobertura,
            "total_faturado_mes0": round(float(row.Qtd_FatMes0), 2),
            "total_faturado_mes1": round(float(row.Qtd_FatMes1), 2),
            "total_faturado_mes2": round(float(row.Qtd_FatMes2), 2),
            "total_faturado_mes3": round(float(row.Qtd_FatMes3), 2),
            "soma_total": round(float(row.Qtd_FatMes0 + row.Qtd_FatMes1 + row.Qtd_FatMes2 + row.Qtd_FatMes3), 2),
            "media_faturada_mensal": round((float(row.Qtd_FatMes0 + row.Qtd_FatMes1 + row.Qtd_FatMes2 + row.Qtd_FatMes3)) / 4, 2),
            "total_disponivel": round(float(row.Qtd_Dispon), 2),
            'mes_labels': {
                'mes0': row.Des_VenMes0,
                'mes1': row.Des_VenMes1,
                'mes2': row.Des_VenMes2,
                'mes3': row.Des_VenMes3
            }
        }

        if row.fornecedor not in suppliers: 
            suppliers[row.fornecedor] = []

        if not any(prod['codigo'] == product['codigo'] for prod in suppliers[row.fornecedor]):
            suppliers[row.fornecedor].append(product)
    
    for fornecedor, totals in supplier_totals.items():
        totals["media_vendas_mensal"] = round(
            (totals["total_vendas_mes0"] + totals["total_vendas_mes1"] + totals["total_vendas_mes2"] + totals["total_vendas_mes3"]) / 4, 2
        )
        totals["media_compras_mensal"] = round(
            (totals["total_preco_compra_mes0"] + totals["total_preco_compra_mes1"] + totals["total_preco_compra_mes2"] + totals["total_preco_compra_mes3"]) / 4, 2
        )
        totals["total_preco_compra"] = round(totals["total_preco_compra"], 2)
        totals["total_preco_compra_mes0"] = round(totals["total_preco_compra_mes0"], 2)
        totals["total_preco_compra_mes1"] = round(totals["total_preco_compra_mes1"], 2)
        totals["total_preco_compra_mes2"] = round(totals["total_preco_compra_mes2"], 2)
        totals["total_preco_compra_mes3"] = round(totals["total_preco_compra_mes3"], 2)
        totals["total_preco_venda"] = round(totals["total_preco_venda"], 2)
        totals["total_preco_venda_mes0"] = round(totals["total_preco_venda_mes0"], 2)
        totals["total_preco_venda_mes1"] = round(totals["total_preco_venda_mes1"], 2)
        totals["total_preco_venda_mes2"] = round(totals["total_preco_venda_mes2"], 2)
        totals["total_preco_venda_mes3"] = round(totals["total_preco_venda_mes3"], 2)

    cursor.close()
    connection.close()
    
    return {
        "suppliers": [{"fornecedor": key, "produtos": value} for key, value in suppliers.items()],
        "totals": supplier_totals
    }

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
			    SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -3, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -3, GETDATE())) THEN v.QUANTIDADE ELSE 0 END)) / 4.0, 0) AS media_faturada,
                
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
            GROUP BY p.Codigo, f.Fantasia, pr.Qtd_Dispon
        ) AS subquery
        WHERE sugestao_compra > 0;
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    total_suggestions = int(result[0][0]) if result else 0

    cursor.close()
    connection.close()
    return total_suggestions

def fetch_products_and_calculate_rupture(supplier_names, days_estimate):
    if not supplier_names:
        raise ValueError("Nenhum fornecedor fornecido.")

    connection = get_db_connection()
    cursor = connection.cursor()

    placeholders = ', '.join(['?'] * len(supplier_names))

    query = f"""
    SELECT 
        f.Fantasia,
        p.Descricao,
        p.Codigo,
        pr.Sta_AbcUniVenFab,
        pr.Qtd_Dispon,
        pr.Qtd_EstMin,
        pul.C_QtdPulmao,
        pr.Qtd_Fisico,
        
        (SUM(CASE WHEN MONTH(v.DATA) = MONTH(GETDATE()) AND YEAR(v.DATA) = YEAR(GETDATE()) THEN v.QUANTIDADE ELSE 0 END) +
        SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -1, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -1, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) +
        SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -2, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -2, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) +
        SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -3, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -3, GETDATE())) THEN v.QUANTIDADE ELSE 0 END)) AS Total_Ult_4_meses,

        ROUND(
                (
                    SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -1, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -1, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) +
                    SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -2, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -2, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) +
                    SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -3, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -3, GETDATE())) THEN v.QUANTIDADE ELSE 0 END)
                ) / 90.0, 2
            ) AS media_diaria_venda  -- Média diária de vendas
    FROM 
        fVENDAS v
    JOIN 
        PRODU p ON v.IDPRODUTO = p.Codigo
    JOIN 
        FABRI f ON p.Cod_Fabricante = f.Codigo
    JOIN 
        PRXES pr ON pr.Cod_Produt = p.Codigo
    LEFT JOIN 
        V_PULMAO pul ON p.Codigo = pul.Cod_Produto
    WHERE
        f.Fantasia IN ({placeholders})
    GROUP BY 
        f.Fantasia, 
        p.Descricao, 
        p.Codigo, 
        pr.Sta_AbcUniVenFab,  
        pr.Qtd_Dispon, 
        pr.Qtd_EstMin,
        pul.C_QtdPulmao,
        pr.Qtd_Fisico
    ORDER BY
		p.Descricao ASC;
    """
    
    cursor.execute(query, supplier_names)
    result = cursor.fetchall()

    products_by_supplier = {}

    for row in result:
        descricao = row.Descricao
        estoque_disponivel = row.Qtd_Dispon
        estoque_fisico = row.Qtd_Fisico
        estoque_transito = row.C_QtdPulmao
        estoque_minimo = row.Qtd_EstMin
        media_diaria_venda = row.media_diaria_venda
        curva = row.Sta_AbcUniVenFab

        previsao_vendas = media_diaria_venda * days_estimate
        risco_ruptura = estoque_disponivel - previsao_vendas

        if row.Fantasia not in products_by_supplier:
            products_by_supplier[row.Fantasia] = []

        if risco_ruptura < 0:
            products_by_supplier[row.Fantasia].append({
                'codigo': row.Codigo,
                'descricao': descricao,
                'estoque_disponivel': estoque_disponivel,
                'estoque_fisico': estoque_fisico,
                'estoque_transito': estoque_transito or 0,
                'estoque_minimo': estoque_minimo,
                'media_diaria_venda': media_diaria_venda,
                'previsao_vendas': previsao_vendas,
                'risco_ruptura': risco_ruptura,
                'curva': curva
            })

    cursor.close()
    connection.close()

    return products_by_supplier

def fetch_total_rupture_risk(days_estimate):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            p.Codigo,
            pr.Qtd_Dispon,
            pul.C_QtdPulmao,
            pr.Qtd_EstMin,
            ROUND(
                (
                    SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -1, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -1, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) +
                    SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -2, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -2, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) +
                    SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -3, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -3, GETDATE())) THEN v.QUANTIDADE ELSE 0 END)
                ) / 90.0, 2
            ) AS Media_Diaria_Trimestre
        FROM 
            fVENDAS v
        JOIN 
            PRODU p ON v.IDPRODUTO = p.Codigo
        JOIN 
            PRXES pr ON pr.Cod_Produt = p.Codigo
        JOIN 
        	FABRI f ON p.Cod_Fabricante = f.Codigo
        LEFT JOIN
			V_PULMAO pul ON p.Codigo = pul.Cod_Produto
        GROUP BY 
            p.Codigo,
            pr.Qtd_Dispon,
            pul.C_QtdPulmao,
            pr.Qtd_EstMin;
    """

    cursor.execute(query)
    result = cursor.fetchall()

    total_risk_items = 0

    for row in result:
        estoque_disponivel = row.Qtd_Dispon
        estoque_transito = row.C_QtdPulmao or 0
        media_diaria_trimestre = row.Media_Diaria_Trimestre

        if estoque_transito > 0:
            continue

        previsao_vendas = media_diaria_trimestre * days_estimate
        risco_ruptura = estoque_disponivel - previsao_vendas

        if risco_ruptura < 0:
            total_risk_items += 1

    cursor.close()
    connection.close()

    return total_risk_items

def fetch_items_within_months(months):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT 
            f.Fantasia,
            p.Codigo,
            p.Descricao,
            pr.Qtd_Dispon,
            nfe.Dat_Vencim,
            nfe.Cod_Lote
        FROM 
            PRODU p
        JOIN 
            FABRI f ON p.Cod_Fabricante = f.Codigo
        JOIN 
            PRXES pr ON pr.Cod_Produt = p.Codigo
        LEFT JOIN 
            NFEIT nfe ON p.Codigo = nfe.Cod_Produto
        GROUP BY 
            f.Fantasia,
            p.Codigo, 
            p.Descricao,
            pr.Qtd_Dispon, 
            nfe.Dat_Vencim,
            nfe.Cod_Lote;
    """

    cursor.execute(query)
    result = cursor.fetchall()

    total_within_months = 0

    for row in result:
        if row.Qtd_Dispon == 0:
            continue

        dat_prx_vct_lot = row.Dat_Vencim

        if dat_prx_vct_lot:
            data_vencimento = dat_prx_vct_lot.date() if isinstance(dat_prx_vct_lot, datetime) else dat_prx_vct_lot
        else:
            continue

        dias_para_vencimento = (data_vencimento - datetime.now().date()).days

        if 0 <= dias_para_vencimento <= (months * 30):
            total_within_months += 1

    cursor.close()
    connection.close()

    return total_within_months

def fetch_items_close_to_expiration(supplier_names, months):
    if not supplier_names:
        raise ValueError("Nenhum fornecedor fornecido.")

    connection = get_db_connection()
    cursor = connection.cursor()

    placeholders = ', '.join(['?'] * len(supplier_names))

    query = f"""
    SELECT 
        f.Fantasia,
        p.Codigo,
        p.Descricao,
        pr.Qtd_Dispon,
        pr.Sta_AbcUniVenFab,
        nfe.Dat_Vencim,
        nfe.Cod_Lote
    FROM 
        PRODU p
    JOIN 
        FABRI f ON p.Cod_Fabricante = f.Codigo
    JOIN 
        PRXES pr ON pr.Cod_Produt = p.Codigo
    LEFT JOIN 
        NFEIT nfe ON p.Codigo = nfe.Cod_Produto
    WHERE 
        f.Fantasia IN ({placeholders})
    GROUP BY 
        f.Fantasia, p.Codigo, p.Descricao, pr.Qtd_Dispon, pr.Sta_AbcUniVenFab, nfe.Dat_Vencim, nfe.Cod_Lote
    HAVING 
        MAX(nfe.Dat_Vencim) <= DATEADD(MONTH, ?, GETDATE())
    ORDER BY 
        f.Fantasia, p.Descricao;
    """

    cursor.execute(query, (*supplier_names, months))
    results = cursor.fetchall()

    items_by_supplier = {}

    for row in results:

        if row.Qtd_Dispon == 0:
            continue
        
        data_vencimento = row.Dat_Vencim
        if data_vencimento:
            data_vencimento = data_vencimento.strftime('%d-%m-%Y') if isinstance(data_vencimento, datetime) else data_vencimento

        item = {
            "codigo": row.Codigo,
            "descricao": row.Descricao,
            "quantidade_estoque": row.Qtd_Dispon,
            "data_vencimento": data_vencimento,
            "lote": row.Cod_Lote,
            "curva": row.Sta_AbcUniVenFab,
        }

        if row.Fantasia not in items_by_supplier:
            items_by_supplier[row.Fantasia] = []

        items_by_supplier[row.Fantasia].append(item)

    cursor.close()
    connection.close()

    return items_by_supplier

def fetch_total_items_stopped(days):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT 
            p.Codigo, 
            f.Fantasia, 
            p.Descricao, 
            pr.Qtd_Dispon AS Quantidade_Estoque, 
            (SELECT MAX(v.DATA) 
             FROM fVENDAS v 
             WHERE v.IDPRODUTO = p.Codigo) AS Ultima_Venda, 
            pr.Sta_AbcUniVenFab AS Curva, 
            (SELECT MAX(nfe.Dat_Movimento) 
             FROM NFEIT nfe 
             WHERE nfe.Cod_Produto = p.Codigo) AS Ultima_Entrada
        FROM 
            PRODU p
        JOIN 
            FABRI f ON p.Cod_Fabricante = f.Codigo
        LEFT JOIN 
            PRXES pr ON pr.Cod_Produt = p.Codigo
        LEFT JOIN 
            NFEIT nfe ON p.Codigo = nfe.Cod_Produto
        GROUP BY 
            p.Codigo, 
            p.Descricao, 
            f.Fantasia, 
            pr.Qtd_Dispon, 
            pr.Sta_AbcUniVenFab
        HAVING 
            (SELECT MAX(v.DATA) 
             FROM fVENDAS v 
             WHERE v.IDPRODUTO = p.Codigo) IS NULL 
            OR (SELECT MAX(v.DATA) 
                FROM fVENDAS v 
                WHERE v.IDPRODUTO = p.Codigo) < DATEADD(DAY, -?, GETDATE())
            AND (SELECT MAX(nfe.Dat_Movimento) 
                 FROM NFEIT nfe 
                 WHERE nfe.Cod_Produto = p.Codigo) < DATEADD(DAY, -30, GETDATE())
    """

    cursor.execute(query, (days,))
    results = cursor.fetchall()

    total_stopped_items = 0

    for row in results:
        if row.Quantidade_Estoque == 0:
            continue
        total_stopped_items += 1

    cursor.close()
    connection.close()

    return total_stopped_items

def fetch_items_stopped_days(supplier_names, days):
    if not supplier_names:
        raise ValueError("Nenhum fornecedor fornecido.")

    connection = get_db_connection()
    cursor = connection.cursor()

    placeholders = ", ".join("?" for _ in supplier_names)

    query = f"""
        SELECT 
            p.Codigo, 
            f.Fantasia, 
            p.Descricao, 
            pr.Qtd_Dispon AS Quantidade_Estoque, 
            (SELECT MAX(v.DATA) 
             FROM fVENDAS v 
             WHERE v.IDPRODUTO = p.Codigo) AS Ultima_Venda, 
            pr.Sta_AbcUniVenFab AS Curva, 
            (SELECT MAX(nfe.Dat_Movimento) 
             FROM NFEIT nfe 
             WHERE nfe.Cod_Produto = p.Codigo) AS Ultima_Entrada
        FROM 
            PRODU p
        JOIN 
            FABRI f ON p.Cod_Fabricante = f.Codigo
        LEFT JOIN 
            PRXES pr ON pr.Cod_Produt = p.Codigo
        LEFT JOIN 
            NFEIT nfe ON p.Codigo = nfe.Cod_Produto
        WHERE 
            f.Fantasia IN ({placeholders})
        GROUP BY 
            p.Codigo, 
            p.Descricao, 
            f.Fantasia, 
            pr.Qtd_Dispon, 
            pr.Sta_AbcUniVenFab
        HAVING 
            (SELECT MAX(v.DATA) 
             FROM fVENDAS v 
             WHERE v.IDPRODUTO = p.Codigo) IS NULL 
            OR (SELECT MAX(v.DATA) 
                FROM fVENDAS v 
                WHERE v.IDPRODUTO = p.Codigo) < DATEADD(DAY, -?, GETDATE())
            AND (SELECT MAX(nfe.Dat_Movimento) 
                 FROM NFEIT nfe 
                 WHERE nfe.Cod_Produto = p.Codigo) < DATEADD(DAY, -30, GETDATE())
    """

    cursor.execute(query, (*supplier_names, days))
    results = cursor.fetchall()

    stagnant_items_by_supplier = {}
    for row in results:
        if row.Quantidade_Estoque == 0:
            continue

        ultima_venda = row.Ultima_Venda.strftime('%d-%m-%Y') if row.Ultima_Venda else 'Sem registro'
        ultima_entrada = row.Ultima_Entrada.strftime('%d-%m-%Y') if row.Ultima_Entrada else 'Sem registro'
        item = {
            "codigo": row.Codigo,
            "descricao": row.Descricao,
            "quantidade_estoque": row.Quantidade_Estoque,
            "ultima_venda": ultima_venda,
            "ultima_entrada": ultima_entrada,
            "curva": row.Curva,
        }

        if row.Fantasia not in stagnant_items_by_supplier:
            stagnant_items_by_supplier[row.Fantasia] = []

        stagnant_items_by_supplier[row.Fantasia].append(item)

    cursor.close()
    connection.close()

    return stagnant_items_by_supplier