from database import get_db_connection
from datetime import datetime
from decimal import Decimal
import re
import unicodedata

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

def fetch_sellers():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """       
        SELECT DISTINCT
            vendedor.Codigo,
            vendedor.Nome_Guerra
        FROM (
            SELECT
                COD_VENDEDOR = cb.Cod_Vendedor
            FROM NFSCB cb
            JOIN NFSIT it
            ON cb.Cod_Estabe = it.Cod_Estabe
            AND cb.Ser_Nota   = it.Ser_Nota
            AND cb.Num_Nota   = it.Num_Nota
            JOIN POCOM pc
            ON it.Id_PolCom = pc.Id_PolCom
            WHERE cb.Status    = 'F'
            AND cb.Tip_Saida = 'V'
            GROUP BY cb.Cod_Vendedor
        ) AS ven
        JOIN V_VENDE AS vendedor
        ON ven.COD_VENDEDOR = vendedor.Codigo
        WHERE vendedor.Codigo IN (
            84, 98, 117, 119, 129, 130, 131, 137,
            143, 144, 145, 148, 149, 155, 156, 172, 192
        )
        ORDER BY vendedor.Nome_Guerra ASC;
    """

    cursor.execute(query)
    result = cursor.fetchall()

    sellers = [
        {
            'codigo': row.Codigo,
            'nome': row.Nome_Guerra
        }
        for row in result
    ]

    cursor.close()
    connection.close()

    return sellers

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
            pr.Qtd_Transi,
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
            ROUND(
                (SUM(CASE WHEN MONTH(v.DATA) = MONTH(GETDATE()) AND YEAR(v.DATA) = YEAR(GETDATE()) THEN v.QUANTIDADE ELSE 0 END) +
                SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -1, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -1, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) +
                SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -2, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -2, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) +
                SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -3, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -3, GETDATE())) THEN v.QUANTIDADE ELSE 0 END)) /
                NULLIF(
                    (CASE WHEN SUM(CASE WHEN MONTH(v.DATA) = MONTH(GETDATE()) AND YEAR(v.DATA) = YEAR(GETDATE()) THEN v.QUANTIDADE ELSE 0 END) > 0 THEN 1 ELSE 0 END +
                    CASE WHEN SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -1, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -1, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) > 0 THEN 1 ELSE 0 END +
                    CASE WHEN SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -2, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -2, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) > 0 THEN 1 ELSE 0 END +
                    CASE WHEN SUM(CASE WHEN MONTH(v.DATA) = MONTH(DATEADD(MONTH, -3, GETDATE())) AND YEAR(v.DATA) = YEAR(DATEADD(MONTH, -3, GETDATE())) THEN v.QUANTIDADE ELSE 0 END) > 0 THEN 1 ELSE 0 END), 0), 2) AS Media_Fat
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
            pr.Qtd_Transi,
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
        formatted_buy_price = f"R$ {Decimal(row.Prc_Compra):,.2f}".replace(".", ",")
        formatted_sale_price = f"R$ {Decimal(row.Prc_Venda):,.2f}".replace(".", ",")
        fornecedor = row.fornecedor
        total_stock = Decimal(row.Qtd_Dispon or 0) + Decimal(row.C_QtdPulmao or 0)

        media_fat = Decimal(row.Media_Fat or 0)
        demanda_media_diaria = media_fat / 30 if media_fat > 0 else Decimal(0)
        dias_cobertura = total_stock / demanda_media_diaria if demanda_media_diaria > 0 else Decimal(0)

        sugestao = demanda_media_diaria * supply_days

        if total_stock == 0 and sugestao == 0 and row.Qtd_EstMin > 0:
            sugestao = Decimal(row.Qtd_EstMin)
        sugestao = round(sugestao, 2)

        cobertura = round(dias_cobertura)

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
        quantidade_disponivel = Decimal(row.Qtd_Dispon or 0)

        supplier_totals[fornecedor]["total_vendas_mes0"] += Decimal(row.Qtd_FatMes0 or 0)
        supplier_totals[fornecedor]["total_vendas_mes1"] += Decimal(row.Qtd_FatMes1 or 0)
        supplier_totals[fornecedor]["total_vendas_mes2"] += Decimal(row.Qtd_FatMes2 or 0)
        supplier_totals[fornecedor]["total_vendas_mes3"] += Decimal(row.Qtd_FatMes3 or 0)
        supplier_totals[fornecedor]["total_disponivel"] += quantidade_disponivel
        supplier_totals[fornecedor]["total_preco_compra"] += preco_unitario * quantidade_disponivel
        supplier_totals[fornecedor]["total_preco_compra_mes0"] += preco_unitario * Decimal(row.Qtd_FatMes0 or 0)
        supplier_totals[fornecedor]["total_preco_compra_mes1"] += preco_unitario * Decimal(row.Qtd_FatMes1 or 0)
        supplier_totals[fornecedor]["total_preco_compra_mes2"] += preco_unitario * Decimal(row.Qtd_FatMes2 or 0)
        supplier_totals[fornecedor]["total_preco_compra_mes3"] += preco_unitario * Decimal(row.Qtd_FatMes3 or 0)
        supplier_totals[fornecedor]["total_preco_venda"] += preco_venda * (Decimal(row.Qtd_FatMes0 or 0) + Decimal(row.Qtd_FatMes1 or 0) + Decimal(row.Qtd_FatMes2 or 0) + Decimal(row.Qtd_FatMes3 or 0))
        supplier_totals[fornecedor]["total_preco_venda_mes0"] += preco_venda * Decimal(row.Qtd_FatMes0 or 0)
        supplier_totals[fornecedor]["total_preco_venda_mes1"] += preco_venda * Decimal(row.Qtd_FatMes1 or 0)
        supplier_totals[fornecedor]["total_preco_venda_mes2"] += preco_venda * Decimal(row.Qtd_FatMes2 or 0)
        supplier_totals[fornecedor]["total_preco_venda_mes3"] += preco_venda * Decimal(row.Qtd_FatMes3 or 0)

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
            'unidades_faturadas_mes0': Decimal(row.Qtd_FatMes0 or 0),
            'unidades_faturadas_mes1': Decimal(row.Qtd_FatMes1 or 0),
            'unidades_faturadas_mes2': Decimal(row.Qtd_FatMes2 or 0),
            'unidades_faturadas_mes3': Decimal(row.Qtd_FatMes3 or 0),
            'media_faturada': Decimal(row.Media_Fat or 0),
            'estoque_minimo': Decimal(row.Qtd_EstMin or 0),
            'estoque_disponivel': Decimal(row.Qtd_Dispon or 0),
            'transito': Decimal(row.Qtd_Transi or 0),
            'sugestao_compra': sugestao,
            'valor_compra': formatted_buy_price,
            'valor_venda': formatted_sale_price,
            'curva': row.Sta_AbcUniVenFab,
            'cobertura': cobertura,
            "total_faturado_mes0": round(float(row.Qtd_FatMes0 or 0), 2),
            "total_faturado_mes1": round(float(row.Qtd_FatMes1 or 0), 2),
            "total_faturado_mes2": round(float(row.Qtd_FatMes2 or 0), 2),
            "total_faturado_mes3": round(float(row.Qtd_FatMes3 or 0), 2),
            "soma_total": round(float((row.Qtd_FatMes0 or 0) + (row.Qtd_FatMes1 or 0) + (row.Qtd_FatMes2 or 0) + (row.Qtd_FatMes3 or 0)), 2),
            "media_faturada_mensal": round((float((row.Qtd_FatMes0 or 0) + (row.Qtd_FatMes1 or 0) + (row.Qtd_FatMes2 or 0) + (row.Qtd_FatMes3 or 0))) / 4, 2),
            "total_disponivel": round(float(row.Qtd_Dispon or 0), 2),
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
        total_vendas = totals["total_vendas_mes0"] + totals["total_vendas_mes1"] + totals["total_vendas_mes2"] + totals["total_vendas_mes3"]
        meses_com_vendas = sum(1 for x in [totals["total_vendas_mes0"], totals["total_vendas_mes1"], totals["total_vendas_mes2"], totals["total_vendas_mes3"]] if x > 0)
        media_vendas_mensal = total_vendas / meses_com_vendas if meses_com_vendas > 0 else 0

        totals["media_vendas_mensal"] = round(media_vendas_mensal, 2)
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

    replacement_days = 15  # default value to help with the sum
    supply_days = 45  # default value to help with the sum
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

            FROM  V_PRCPL vpr
            JOIN fVENDAS v ON v.IDPRODUTO = vpr.Codigo
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
        pr.Qtd_Quaren,
        pr.Qtd_EstMin,
        pr.Qtd_Transi,
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
        pr.Qtd_Quaren,
        pr.Qtd_EstMin,
        pr.Qtd_Transi,
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
        estoque_disponivel = row.Qtd_Dispon - row.Qtd_Quaren
        estoque_fisico = row.Qtd_Fisico
        estoque_transito = row.Qtd_Transi
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
            pr.Qtd_Transi,
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
            pr.Qtd_Transi,
            pul.C_QtdPulmao,
            pr.Qtd_EstMin;
    """

    cursor.execute(query)
    result = cursor.fetchall()

    total_risk_items = 0

    for row in result:
        estoque_disponivel = row.Qtd_Dispon
        estoque_transito = row.Qtd_Transi or 0
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

#CONTAGEM
def fetch_items_within_months(months=12):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            f.Fantasia,
            p.Codigo,
            p.Descricao,
            pr.Qtd_Dispon,
            pl.Dat_Vencim,
            pl.Cod_Lote,
            pl.Qtd_SldPra,
            vpr.Codigo
        FROM
            PRODU p
        JOIN
            FABRI f ON p.Cod_Fabricante = f.Codigo
        JOIN
            PRXES pr ON pr.Cod_Produt = p.Codigo
        JOIN
            PRLTL pl ON p.Codigo = pl.Cod_Produt
        JOIN
            V_PRCPL vpr ON p.Codigo = vpr.Codigo
        WHERE
            pl.Dat_Vencim > GETDATE() AND pl.Dat_Vencim <= DATEADD(MONTH, ?, GETDATE())
        AND f.Fantasia IN (
            'ABL',
            'ACCUMED PRO MED',
            'AGPMED',
            'AIRELA IND. FARMACEUTICA',
            'AMERICA',
            'AMERICAN',
            'APOLO',
            'ARTE NATIVA',
            'AUROBINDO',
            'AVVIO',
            'BE CARE',
            'BEKER',
            'BELFAR',
            'BELFAR GEN',
            'BIOCHIMICO',
            'BIOLAB',
            'BIONATUS',
            'BLAU',
            'BLOWTEX',
            'BRASTERAPICA',
            'BRAVIR',
            'BUBA',
            'CAZI',
            'CBEMED',
            'CCM',
            'CELLERA FARMA',
            'CIFARMA',
            'CLINMED',
            'CREMER',
            'CRISTALIA',
            'DELLAMED S.A.',
            'DELTA',
            'DESCARBOX',
            'DESCARPACK',
            'DISTRIMEDICA COMERCIO DE',
            'E M S',
            'EMS',
            'EMS GENERICO',
            'EQUIPLEX',
            'EUGIA PHARMA INDUSTRIA FA',
            'EUROFARMA',
            'EUROFARMA GENERICO',
            'FAMI',
            'FARMACE',
            'FARMAX',
            'FLEXPELL',
            'FORT FLEX',
            'FORTSAN',
            'FRESENIUS',
            'FZ MED',
            'GENOM',
            'GEOLAB',
            'GERMED',
            'GLOBO',
            'GREEN PHARMA',
            'GSK',
            'G-TECH',
            'HALEX ISTAR',
            'HEALTHY DO BRASIL',
            'HIDROLIGHT',
            'HIPOLABOR',
            'HIPOLABOR GENERICO',
            'HISAMITSU',
            'HYPOFARMA',
            'HYPOFARMA GENERICO',
            'IFAL',
            'INCOTERM',
            'INDALABOR INDAIA LABORATO',
            'ISOFARMA',
            'J.PROLAB',
            'JANSSEN',
            'JOSE IVANILDO MIRANDA MAT',
            'KASMED',
            'KEDRION BRASIL DISTRIBUID',
            'LABOR IMPORT IMP EXP LTDA',
            'LABOTRAT',
            'LALAN',
            'LAPON',
            'LEGRAND',
            'LEMGRUBER',
            'LOCAWARE',
            'LUDAN INDUSTRIA E COMERCI',
            'MARK MED',
            'MAXINUTRI',
            'MDA',
            'MDR SAUDE',
            'MEDEVICE DO BRASIL COMERC',
            'MEDI COMPANY',
            'MEDIX',
            'MEDIX BRASIL',
            'MEDQUIMICA',
            'MEDSONDA',
            'MEDTEX',
            'MEM CIRURGICA LTDA',
            'MERCUR',
            'MG',
            'MISSNER',
            'MULTILAB',
            'MUNILA COSMETICOS LTDA',
            'NATCOFARMA BRASIL',
            'NATHY',
            'NATIVITA',
            'NATULAB',
            'NATURELIFE',
            'NEVOARN INDUSTRIA TEXTIL',
            'NOVAFARMA GENERICO',
            'NOVAQUIMICA',
            'NOVARTIS',
            'NUTRIEX',
            'OCTAPHARMA',
            'OMRON',
            'OSORIO DE MORAES',
            'PHARLAB',
            'PHARMASCIENCE',
            'PLUMAX',
            'POLAR FIX',
            'PRATI',
            'PRATI GENERICO',
            'PROHOSPITAL',
            'RANBAXY',
            'RANGEL',
            'RAPHAEL MARQUES OLIVEIRA',
            'RIOQUIMICA',
            'SANDOZ',
            'SANFARMA',
            'SANOFI AVENTIS',
            'SANTISA',
            'SHALON FIOS CIRUGICOS',
            'SOLIDOR',
            'SR',
            'SUBURBAN',
            'SUN PHARMA',
            'TEUTO',
            'TKL',
            'UNIAO QUIMICA',
            'UNIAO QUIMICA GENERICO',
            'UNICHEM FARMACEUTICA',
            'UNIPHAR',
            'UNITED MEDICAL LTDA.',
            'VIC PHARMA',
            'VITAMEDIC',
            'VMG FARMACEUTICA',
            'WASSER FARMA',
            'ZHALINGER',
            'ZYDUS'
        )
        GROUP BY
            f.Fantasia,
            p.Codigo,
            p.Descricao,
            pr.Qtd_Dispon,
            pl.Dat_Vencim,
            pl.Cod_Lote,
            pl.Qtd_SldPra,
            vpr.Codigo;
    """

    cursor.execute(query, (months,))
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
            pr.Sta_AbcUniVenFab,
            pl.Cod_Lote,
            pl.Qtd_SldPra,
            pl.Dat_Vencim
        FROM PRODU p
        JOIN
            FABRI f ON p.Cod_Fabricante = f.Codigo
        JOIN
            PRXES pr ON pr.Cod_Produt = p.Codigo
        JOIN
            PRLTL pl ON p.Codigo = pl.Cod_Produt
        WHERE f.Fantasia IN ({placeholders})
        AND pl.Dat_Vencim > GETDATE()
        AND pl.Dat_Vencim <= DATEADD(MONTH, ?, GETDATE())
        ORDER BY f.Fantasia, p.Descricao;
    """

    cursor.execute(query, (*supplier_names, months))
    results = cursor.fetchall()

    items_by_supplier = {}

    for row in results:
        if row.Qtd_SldPra == 0:
            continue

        data_vencimento = row.Dat_Vencim
        if data_vencimento:
            data_vencimento = data_vencimento.strftime('%d-%m-%Y') if isinstance(data_vencimento, datetime) else data_vencimento

        item = {
            "codigo": row.Codigo,
            "descricao": row.Descricao,
            "quantidade_estoque": row.Qtd_SldPra,
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

def fetch_months_years_by_sellers(seller_codes):
    connection = get_db_connection()
    cursor = connection.cursor()

    placeholders = ','.join(['?'] * len(seller_codes))

    query = f"""        
        SELECT DISTINCT
            vvend.MES,
            vvend.ANO
        FROM (
            SELECT
                ANO = YEAR(cb.Dat_Emissao),
                MES = MONTH(cb.Dat_Emissao),
                COD_VENDEDOR = cb.Cod_Vendedor
            FROM NFSCB cb
            JOIN NFSIT it
            ON cb.Cod_Estabe = it.Cod_Estabe
            AND cb.Ser_Nota   = it.Ser_Nota
            AND cb.Num_Nota   = it.Num_Nota
            JOIN POCOM pc
            ON it.Id_PolCom = pc.Id_PolCom
            WHERE cb.Status    = 'F'
            AND cb.Tip_Saida = 'V' 
            GROUP BY
                YEAR(cb.Dat_Emissao),
                MONTH(cb.Dat_Emissao),
                cb.Cod_Vendedor
        ) AS vvend
        WHERE vvend.COD_VENDEDOR IN ({placeholders})
        ORDER BY vvend.ANO DESC, vvend.MES ASC;
    """

    cursor.execute(query, seller_codes)
    result = cursor.fetchall()

    data = [
        {
            'mes': row.MES,
            'ano': row.ANO
        }
        for row in result
    ]

    cursor.close()
    connection.close()

    return data


def normalize_policy_name(s: str) -> str:
    """Normaliza nome de política para comparação: remove acentos, lowercase, colapsa espaços."""
    if s is None:
        return ""
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ascii', 'ignore').decode('ascii') 
    s = s.strip().lower()
    s = re.sub(r'\s+', ' ', s) 
    return s

RAW_POLICIES_PERCENT = {
    117: {
        "ARTE NATIVA ABRIL 2026": 2.0,
        "ARTE NATIVA MAIO 2026": 2.0,
        "ARTE NATIVA MAIO BON 2026": 2.0,
        "ARTE NATIVA ABR BON 2026": 2.0,
        "BELLAPHITUS": 2.0,
        "BELLAPHITUS OL": 1.0,
        "BIOLAB GEN COMBATE": 1.0,
        "CASADINHA QUENTE E FRIO": 2.0,
        "CONECTADOS GEOLAB MARC": 1.0,
        "CCM PROMOÇÃO": 2.0,
        "COTAÇÃO FARMA": 1.0,
        "COMBO BELFAR": 2.0,
        "COMBO BELFAR 2": 2.0,
        "COMBO FECHAMENTO 1": 2.0,
        "COMBO INVERNO": 2.0,
        "COMBO PARAC + DIPIMED": 2.0,
        "COMBO MULTI": 1.0,
        "DIA D ARTE NATIVA BRINDES": 2.0,
        "DIA D LABOTRAT": 2.0,
        "DIA D MERCUR": 2.0,
        "FARMA 01 INTERIOR": 5.0,
        "FARMA 02 INTERIOR": 4.0,
        "FARMA 01": 4.5,
        "FARMA 02": 3.5,
        "FARMA 03": 3.0,
        "FARMA 03 INTERIOR": 3.0,
        "FECHA MES MERCUR": 2.0,
        "GEOLAB OL MARÇO": 1.0,
        "GEOLAB OL ABRIL": 1.0,
        "HOSPITAL LOCAL": 2.0,
        "LUPA DE LEITURA": 2.0,
        "MAXINUTRI": 10.0,
        "MERCUR 5": 5.0,
        "MERCUR 7": 7.0,
        "MULTI + ESPAÇADOR": 2.0,
        "NEGOCIAÇÃO OL FARMA": 1.0,
        "OFERTAS UNIPHAR ABRIL": 2.0,
        "ORTOPEDICOS": 5.0,
        "PED ELETRONICO - GD REDES": 3.0,
        "PRE VENCIDOS - FARMA": 2.0,
        "PROMOÇÃO DO DIA": 2.0,
        "RANBAXY OPORTUNIDADE": 1.0,
        "RANBAXY TS": 3.0,
        "RANBAXY OL": 1.0,
        "RANBAXY PROMO": 2.0,
        "SUPER COMBO RILEX": 2.0,
        "SUPER COMBO RILEX 2": 2.0,
    },
    137: {
        "ARTE NATIVA ABRIL 2026": 2.0,
        "ARTE NATIVA MAIO 2026": 2.0,
        "ARTE NATIVA MAIO BON 2026": 2.0,
        "ARTE NATIVA ABR BON 2026": 2.0,
        "BELLAPHITUS": 2.0,
        "BELLAPHITUS OL": 1.0,
        "BIOLAB GEN COMBATE": 1.0,
        "CASADINHA QUENTE E FRIO": 2.0,
        "CONECTADOS GEOLAB MARC": 1.0,
        "CCM PROMOÇÃO": 2.0,
        "COTAÇÃO FARMA": 1.0,
        "COMBO BELFAR": 2.0,
        "COMBO BELFAR 2": 2.0,
        "COMBO FECHAMENTO 1": 2.0,
        "COMBO INVERNO": 2.0,
        "COMBO MULTI": 1.0,
        "COMBO PARAC + DIPIMED": 2.0,
        "DIA D ARTE NATIVA BRINDES": 2.0,
        "DIA D LABOTRAT": 2.0,
        "DIA D MERCUR": 2.0,
        "FARMA 01": 4.5,
        "FARMA 02": 3.5,
        "FARMA 03": 2.5,
        "FARMA 03 INTERIOR": 3.0,
        "FECHA MES MERCUR": 2.0,
        "GEOLAB OL MARÇO": 1.0,
        "GEOLAB OL ABRIL": 1.0,
        "HOSPITAL LOCAL": 2.0,
        "LUPA DE LEITURA": 2.0,
        "MAXINUTRI": 10.0,
        "MERCUR 5": 5.0,
        "MERCUR 7": 7.0,
        "MULTI + ESPAÇADOR": 2.0,
        "NEGOCIAÇÃO OL FARMA": 1.0,
        "OFERTAS UNIPHAR ABRIL": 2.0,
        "ORTOPEDICOS": 5.0,
        "PED ELETRONICO - GD REDES": 3.0,
        "PRE VENCIDOS - FARMA": 2.0,
        "PROMOÇÃO DO DIA": 2.0,
        "RANBAXY OPORTUNIDADE": 1.0,
        "RANBAXY TS": 3.0,
        "RANBAXY OL": 1.0,
        "RANBAXY PROMO": 2.0,
        "SUPER COMBO RILEX": 2.0,
        "SUPER COMBO RILEX 2": 2.0,
    },
    84: {
        "ARTE NATIVA ABRIL 2026": 2.0,
        "ARTE NATIVA MAIO 2026": 2.0,
        "ARTE NATIVA MAIO BON 2026": 2.0,
        "ARTE NATIVA ABR BON 2026": 2.0,
        "BELLAPHITUS": 2.0,
        "BELLAPHITUS OL": 1.0,
        "BIOLAB GEN COMBATE": 1.0,
        "CASADINHA QUENTE E FRIO": 2.0,
        "CONECTADOS GEOLAB MARC": 1.0,
        "CCM PROMOÇÃO": 2.0,
        "COTAÇÃO FARMA": 1.0,
        "COMBO BELFAR": 2.0,
        "COMBO BELFAR 2": 2.0,
        "COMBO FECHAMENTO 1": 2.0,
        "COMBO INVERNO": 2.0,
        "COMBO PARAC + DIPIMED": 2.0,
        "COMBO MULTI": 1.0,
        "DIA D ARTE NATIVA BRINDES": 2.0,
        "DIA D LABOTRAT": 2.0,
        "DIA D MERCUR": 2.0,
        "FARMA 01": 4.5,
        "FARMA 02": 3.5,
        "FARMA 03": 2.5,
        "FARMA 03 INTERIOR": 3.0,
        "FECHA MES MERCUR": 2.0,
        "GEOLAB OL MARÇO": 1.0,
        "GEOLAB OL ABRIL": 1.0,
        "HOSPITAL LOCAL": 2.0,
        "LUPA DE LEITURA": 2.0,
        "MAXINUTRI": 10.0,
        "MERCUR 5": 5.0,
        "MERCUR 7": 7.0,
        "MULTI + ESPAÇADOR": 2.0,
        "NEGOCIAÇÃO OL FARMA": 1.0,
        "OFERTAS UNIPHAR ABRIL": 2.0,
        "ORTOPEDICOS": 5.0,
        "PED ELETRONICO - GD REDES": 3.0,
        "PRE VENCIDOS - FARMA": 2.0,
        "PROMOÇÃO DO DIA": 2.0,
        "RANBAXY OPORTUNIDADE": 1.0,
        "RANBAXY TS": 3.0,
        "RANBAXY OL": 1.0,
        "RANBAXY PROMO": 2.0,
        "SUPER COMBO RILEX": 2.0,
        "SUPER COMBO RILEX 2": 2.0,
    },
    172: {
        "ARTE NATIVA ABRIL 2026": 2.0,
        "ARTE NATIVA MAIO 2026": 2.0,
        "ARTE NATIVA MAIO BON 2026": 2.0,
        "ARTE NATIVA ABR BON 2026": 2.0,
        "BELLAPHITUS": 2.0,
        "BELLAPHITUS OL": 1.0,
        "BIOLAB GEN COMBATE": 1.0,
        "CASADINHA QUENTE E FRIO": 2.0,
        "CONECTADOS GEOLAB MARC": 1.0,
        "CCM PROMOÇÃO": 2.0,
        "COTAÇÃO FARMA": 1.0,
        "COMBO BELFAR": 2.0,
        "COMBO BELFAR 2": 2.0,
        "COMBO FECHAMENTO 1": 2.0,
        "COMBO INVERNO": 2.0,
        "COMBO PARAC + DIPIMED": 2.0,
        "COMBO MULTI": 1.0,
        "DIA D ARTE NATIVA BRINDES": 2.0,
        "DIA D LABOTRAT": 2.0,
        "DIA D MERCUR": 2.0,
        "FARMA 01": 4.5,
        "FARMA 02": 3.5,
        "FARMA 03": 2.5,
        "FARMA 03 INTERIOR": 3.0,
        "FECHA MES MERCUR": 2.0,
        "GEOLAB OL MARÇO": 1.0,
        "GEOLAB OL ABRIL": 1.0,
        "HOSPITAL LOCAL": 2.0,
        "LUPA DE LEITURA": 2.0,
        "MAXINUTRI": 10.0,
        "MERCUR 5": 5.0,
        "MERCUR 7": 7.0,
        "MULTI + ESPAÇADOR": 2.0,
        "NEGOCIAÇÃO OL FARMA": 1.0,
        "OFERTAS UNIPHAR ABRIL": 2.0,
        "ORTOPEDICOS": 5.0,
        "PED ELETRONICO - GD REDES": 3.0,
        "PRE VENCIDOS - FARMA": 2.0,
        "PROMOÇÃO DO DIA": 2.0,
        "RANBAXY OPORTUNIDADE": 1.0,
        "RANBAXY TS": 3.0,
        "RANBAXY OL": 1.0,
        "RANBAXY PROMO": 2.0,
        "SUPER COMBO RILEX": 2.0,
        "SUPER COMBO RILEX 2": 2.0,
    },
    145: {
        "ARTE NATIVA ABRIL 2026": 2.0,
        "ARTE NATIVA MAIO 2026": 2.0,
        "ARTE NATIVA MAIO BON 2026": 2.0,
        "ARTE NATIVA ABR BON 2026": 2.0,
        "BELLAPHITUS": 2.0,
        "BELLAPHITUS OL": 1.0,
        "BIOLAB GEN COMBATE": 1.0,
        "CASADINHA QUENTE E FRIO": 2.0,
        "CONECTADOS GEOLAB MARC": 1.0,
        "CCM PROMOÇÃO": 2.0,
        "COTAÇÃO FARMA": 1.0,
        "COMBO BELFAR": 2.0,
        "COMBO BELFAR 2": 2.0,
        "COMBO FECHAMENTO 1": 2.0,
        "COMBO INVERNO": 2.0,
        "COMBO PARAC + DIPIMED": 2.0,
        "COMBO MULTI": 1.0,
        "DIA D ARTE NATIVA BRINDES": 2.0,
        "DIA D LABOTRAT": 2.0,
        "DIA D MERCUR": 2.0,
        "FARMA 01": 4.5,
        "FARMA 02": 3.5,
        "FARMA 03": 2.5,
        "FARMA 03 INTERIOR": 2.5,
        "FECHA MES MERCUR": 2.0,
        "GEOLAB OL MARÇO": 1.0,
        "GEOLAB OL ABRIL": 1.0,
        "HOSPITAL LOCAL": 2.0,
        "LUPA DE LEITURA": 2.0,
        "MAXINUTRI": 10.0,
        "MERCUR 5": 5.0,
        "MERCUR 7": 7.0,
        "MULTI + ESPAÇADOR": 2.0,
        "NEGOCIAÇÃO OL FARMA": 1.0,
        "OFERTAS UNIPHAR ABRIL": 2.0,
        "ORTOPEDICOS": 5.0,
        "PED ELETRONICO - GD REDES": 3.0,
        "PRE VENCIDOS - FARMA": 2.0,
        "PROMOÇÃO DO DIA": 2.0,
        "RANBAXY OPORTUNIDADE": 1.0,
        "RANBAXY TS": 3.0,
        "RANBAXY OL": 1.0,
        "RANBAXY PROMO": 2.0,
        "SUPER COMBO RILEX": 2.0,
        "SUPER COMBO RILEX 2": 2.0,
    },
    98: {
        "ARTE NATIVA ABRIL 2026": 2.0,
        "ARTE NATIVA MAIO 2026": 2.0,
        "ARTE NATIVA MAIO BON 2026": 2.0,
        "ARTE NATIVA ABR BON 2026": 2.0,
        "BELLAPHITUS": 2.0,
        "BELLAPHITUS OL": 1.0,
        "BIOLAB GEN COMBATE": 1.0,
        "CASADINHA QUENTE E FRIO": 2.0,
        "CONECTADOS GEOLAB MARC": 1.0,
        "CCM PROMOÇÃO": 2.0,
        "COTAÇÃO FARMA": 1.0,
        "COMBO BELFAR": 2.0,
        "COMBO BELFAR 2": 2.0,
        "COMBO FECHAMENTO 1": 2.0,
        "COMBO INVERNO": 2.0,
        "COMBO PARAC + DIPIMED": 2.0,
        "COMBO MULTI": 1.0,
        "DIA D ARTE NATIVA BRINDES": 2.0,
        "DIA D LABOTRAT": 2.0,
        "DIA D MERCUR": 2.0,
        "FARMA 01 INTERIOR": 5.0,
        "FARMA 02 INTERIOR": 4.0,
        "FARMA 01": 4.5,
        "FARMA 02": 3.5,
        "FARMA 03": 3.0,
        "FARMA 03 INTERIOR": 3.0,
        "FECHA MES MERCUR": 2.0,
        "GEOLAB OL MARÇO": 1.0,
        "GEOLAB OL ABRIL": 1.0,
        "HOSPITAL LOCAL": 2.0,
        "LUPA DE LEITURA": 2.0,
        "MAXINUTRI": 10.0,
        "MERCUR 5": 5.0,
        "MERCUR 7": 7.0,
        "MULTI + ESPAÇADOR": 2.0,
        "NEGOCIAÇÃO OL FARMA": 1.0,
        "OFERTAS UNIPHAR ABRIL": 2.0,
        "ORTOPEDICOS": 5.0,
        "PED ELETRONICO - GD REDES": 3.0,
        "PRE VENCIDOS - FARMA": 2.0,
        "PROMOÇÃO DO DIA": 2.0,
        "RANBAXY OPORTUNIDADE": 1.0,
        "RANBAXY TS": 3.0,
        "RANBAXY OL": 1.0,
        "RANBAXY PROMO": 2.0,
        "SUPER COMBO RILEX": 2.0,
        "SUPER COMBO RILEX 2": 2.0,
    },
    149: {
        "ARTE NATIVA ABRIL 2026": 2.0,
        "ARTE NATIVA MAIO 2026": 2.0,
        "ARTE NATIVA MAIO BON 2026": 2.0,
        "ARTE NATIVA ABR BON 2026": 2.0,
        "BELLAPHITUS": 2.0,
        "BELLAPHITUS OL": 1.0,
        "BIOLAB GEN COMBATE": 1.0,
        "CASADINHA QUENTE E FRIO": 2.0,
        "CONECTADOS GEOLAB MARC": 1.0,
        "CCM PROMOÇÃO": 2.0,
        "COTAÇÃO FARMA": 1.0,
        "COMBO BELFAR": 2.0,
        "COMBO BELFAR 2": 2.0,
        "COMBO FECHAMENTO 1": 2.0,
        "COMBO INVERNO": 2.0,
        "COMBO PARAC + DIPIMED": 2.0,
        "COMBO MULTI": 1.0,
        "DIA D ARTE NATIVA BRINDES": 2.0,
        "DIA D LABOTRAT": 2.0,
        "DIA D MERCUR": 2.0,
        "FARMA 01 INTERIOR": 5.0,
        "FARMA 02 INTERIOR": 4.0,
        "FARMA 01": 4.5,
        "FARMA 02": 3.5,
        "FARMA 03": 3.0,
        "FARMA 03 INTERIOR": 3.0,
        "FECHA MES MERCUR": 2.0,
        "GEOLAB OL MARÇO": 1.0,
        "GEOLAB OL ABRIL": 1.0,
        "HOSPITAL LOCAL": 2.0,
        "LUPA DE LEITURA": 2.0,
        "MAXINUTRI": 10.0,
        "MERCUR 5": 5.0,
        "MERCUR 7": 7.0,
        "MULTI + ESPAÇADOR": 2.0,
        "NEGOCIAÇÃO OL FARMA": 1.0,
        "OFERTAS UNIPHAR ABRIL": 2.0,
        "ORTOPEDICOS": 5.0,
        "PED ELETRONICO - GD REDES": 3.0,
        "PRE VENCIDOS - FARMA": 2.0,
        "PROMOÇÃO DO DIA": 2.0,
        "RANBAXY OPORTUNIDADE": 1.0,
        "RANBAXY TS": 3.0,
        "RANBAXY OL": 1.0,
        "RANBAXY PROMO": 2.0,
        "SUPER COMBO RILEX": 2.0,
        "SUPER COMBO RILEX 2": 2.0,
    },
    156: {
        "ARTE NATIVA ABRIL 2026": 2.0,
        "ARTE NATIVA MAIO 2026": 2.0,
        "ARTE NATIVA MAIO BON 2026": 2.0,
        "ARTE NATIVA ABR BON 2026": 2.0,
        "BELLAPHITUS": 2.0,
        "BELLAPHITUS OL": 1.0,
        "BIOLAB GEN COMBATE": 1.0,
        "CASADINHA QUENTE E FRIO": 2.0,
        "CONECTADOS GEOLAB MARC": 1.0,
        "CCM PROMOÇÃO": 2.0,
        "COTAÇÃO FARMA": 1.0,
        "COMBO BELFAR": 2.0,
        "COMBO BELFAR 2": 2.0,
        "COMBO FECHAMENTO 1": 2.0,
        "COMBO INVERNO": 2.0,
        "COMBO PARAC + DIPIMED": 2.0,
        "COMBO MULTI": 1.0,
        "DIA D ARTE NATIVA BRINDES": 2.0,
        "DIA D LABOTRAT": 2.0,
        "DIA D MERCUR": 2.0,
        "FARMA 01 INTERIOR": 5.0,
        "FARMA 02 INTERIOR": 4.0,
        "FARMA 01": 4.5,
        "FARMA 02": 3.5,
        "FARMA 03": 3.0,
        "FARMA 03 INTERIOR": 3.0,
        "FECHA MES MERCUR": 2.0,
        "GEOLAB OL MARÇO": 1.0,
        "GEOLAB OL ABRIL": 1.0,
        "HOSPITAL LOCAL": 2.0,
        "LUPA DE LEITURA": 2.0,
        "MAXINUTRI": 10.0,
        "MERCUR 5": 5.0,
        "MERCUR 7": 7.0,
        "MULTI + ESPAÇADOR": 2.0,
        "NEGOCIAÇÃO OL FARMA": 1.0,
        "OFERTAS UNIPHAR ABRIL": 2.0,
        "ORTOPEDICOS": 5.0,
        "PED ELETRONICO - GD REDES": 3.0,
        "PRE VENCIDOS - FARMA": 2.0,
        "PROMOÇÃO DO DIA": 2.0,
        "RANBAXY OPORTUNIDADE": 1.0,
        "RANBAXY TS": 3.0,
        "RANBAXY OL": 1.0,
        "RANBAXY PROMO": 2.0,
        "SUPER COMBO RILEX": 2.0,
        "SUPER COMBO RILEX 2": 2.0,
    },
    131: {
        "ARTE NATIVA ABRIL 2026": 2.0,
        "ARTE NATIVA MAIO 2026": 2.0,
        "ARTE NATIVA MAIO BON 2026": 2.0,
        "ARTE NATIVA ABR BON 2026": 2.0,
        "BELLAPHITUS": 2.0,
        "BELLAPHITUS OL": 1.0,
        "BIOLAB GEN COMBATE": 1.0,
        "CASADINHA QUENTE E FRIO": 2.0,
        "CONECTADOS GEOLAB MARC": 1.0,
        "CCM PROMOÇÃO": 2.0,
        "COTAÇÃO FARMA": 1.0,
        "COMBO BELFAR": 2.0,
        "COMBO BELFAR 2": 2.0,
        "COMBO FECHAMENTO 1": 2.0,
        "COMBO INVERNO": 2.0,
        "COMBO PARAC + DIPIMED": 2.0,
        "COMBO MULTI": 1.0,
        "DIA D ARTE NATIVA BRINDES": 2.0,
        "DIA D LABOTRAT": 2.0,
        "DIA D MERCUR": 2.0,
        "FARMA 01 INTERIOR": 5.0,
        "FARMA 02 INTERIOR": 4.0,
        "FARMA 01": 4.5,
        "FARMA 02": 3.5,
        "FARMA 03": 3.0,
        "FARMA 03 INTERIOR": 3.0,
        "FECHA MES MERCUR": 2.0,
        "GEOLAB OL MARÇO": 1.0,
        "GEOLAB OL ABRIL": 1.0,
        "HOSPITAL LOCAL": 2.0,
        "LUPA DE LEITURA": 2.0,
        "MAXINUTRI": 10.0,
        "MERCUR 5": 5.0,
        "MERCUR 7": 7.0,
        "MULTI + ESPAÇADOR": 2.0,
        "NEGOCIAÇÃO OL FARMA": 1.0,
        "OFERTAS UNIPHAR ABRIL": 2.0,
        "ORTOPEDICOS": 5.0,
        "PED ELETRONICO - GD REDES": 3.0,
        "PRE VENCIDOS - FARMA": 2.0,
        "PROMOÇÃO DO DIA": 2.0,
        "RANBAXY OPORTUNIDADE": 1.0,
        "RANBAXY TS": 3.0,
        "RANBAXY OL": 1.0,
        "RANBAXY PROMO": 2.0,
        "SUPER COMBO RILEX": 2.0,
        "SUPER COMBO RILEX 2": 2.0,
    },
    143: {
        "ARTE NATIVA ABRIL 2026": 2.0,
        "ARTE NATIVA MAIO 2026": 2.0,
        "ARTE NATIVA MAIO BON 2026": 2.0,
        "ARTE NATIVA ABR BON 2026": 2.0,
        "BELLAPHITUS": 2.0,
        "BELLAPHITUS OL": 1.0,
        "BIOLAB GEN COMBATE": 1.0,
        "CASADINHA QUENTE E FRIO": 2.0,
        "CONECTADOS GEOLAB MARC": 1.0,
        "CCM PROMOÇÃO": 2.0,
        "COTAÇÃO FARMA": 1.0,
        "COMBO BELFAR": 2.0,
        "COMBO BELFAR 2": 2.0,
        "COMBO FECHAMENTO 1": 2.0,
        "COMBO INVERNO": 2.0,
        "COMBO PARAC + DIPIMED": 2.0,
        "COMBO MULTI": 1.0,
        "DIA D ARTE NATIVA BRINDES": 2.0,
        "DIA D LABOTRAT": 2.0,
        "DIA D MERCUR": 2.0,
        "FARMA 01 INTERIOR": 5.0,
        "FARMA 02 INTERIOR": 4.0,
        "FARMA 01": 4.5,
        "FARMA 02": 3.5,
        "FARMA 03": 3.0,
        "FARMA 03 INTERIOR": 3.0,
        "FECHA MES MERCUR": 2.0,
        "GEOLAB OL MARÇO": 1.0,
        "GEOLAB OL ABRIL": 1.0,
        "HOSPITAL LOCAL": 2.0,
        "LUPA DE LEITURA": 2.0,
        "MAXINUTRI": 10.0,
        "MERCUR 5": 5.0,
        "MERCUR 7": 7.0,
        "MULTI + ESPAÇADOR": 2.0,
        "NEGOCIAÇÃO OL FARMA": 1.0,
        "OFERTAS UNIPHAR ABRIL": 2.0,
        "ORTOPEDICOS": 5.0,
        "PED ELETRONICO - GD REDES": 3.0,
        "PRE VENCIDOS - FARMA": 2.0,
        "PROMOÇÃO DO DIA": 2.0,
        "RANBAXY OPORTUNIDADE": 1.0,
        "RANBAXY TS": 3.0,
        "RANBAXY OL": 1.0,
        "RANBAXY PROMO": 2.0,
        "SUPER COMBO RILEX": 2.0,
        "SUPER COMBO RILEX 2": 2.0,
    },
    155: {
        "ARTE NATIVA ABRIL 2026": 2.0,
        "ARTE NATIVA MAIO 2026": 2.0,
        "ARTE NATIVA MAIO BON 2026": 2.0,
        "ARTE NATIVA ABR BON 2026": 2.0,
        "BELLAPHITUS": 2.0,
        "BELLAPHITUS OL": 1.0,
        "BIOLAB GEN COMBATE": 1.0,
        "CASADINHA QUENTE E FRIO": 2.0,
        "CONECTADOS GEOLAB MARC": 1.0,
        "CCM PROMOÇÃO": 2.0,
        "COTAÇÃO FARMA": 1.0,
        "COMBO FECHAMENTO 1": 2.0,
        "COMBO BELFAR": 2.0,
        "COMBO BELFAR 2": 2.0,
        "COMBO INVERNO": 2.0,
        "COMBO PARAC + DIPIMED": 2.0,
        "COMBO MULTI": 1.0,
        "DIA D ARTE NATIVA BRINDES": 2.0,
        "DIA D LABOTRAT": 2.0,
        "DIA D MERCUR": 2.0,
        "FARMA 01 INTERIOR": 5.0,
        "FARMA 02 INTERIOR": 4.0,
        "FARMA 01": 4.5,
        "FARMA 02": 3.5,
        "FARMA 03": 3.0,
        "FARMA 03 INTERIOR": 3.0,
        "FECHA MES MERCUR": 2.0,
        "GEOLAB OL MARÇO": 1.0,
        "GEOLAB OL ABRIL": 1.0,
        "HOSPITAL LOCAL": 2.0,
        "LUPA DE LEITURA": 2.0,
        "MAXINUTRI": 10.0,
        "MERCUR 5": 5.0,
        "MERCUR 7": 7.0,
        "MULTI + ESPAÇADOR": 2.0,
        "NEGOCIAÇÃO OL FARMA": 1.0,
        "OFERTAS UNIPHAR ABRIL": 2.0,
        "ORTOPEDICOS": 5.0,
        "PED ELETRONICO - GD REDES": 3.0,
        "PRE VENCIDOS - FARMA": 2.0,
        "PROMOÇÃO DO DIA": 2.0,
        "RANBAXY OPORTUNIDADE": 1.0,
        "RANBAXY TS": 3.0,
        "RANBAXY OL": 1.0,
        "RANBAXY PROMO": 2.0,
        "SUPER COMBO RILEX": 2.0,
        "SUPER COMBO RILEX 2": 2.0,
    },
    129: {
        "ARTE NATIVA ABRIL 2026": 2.0,
        "ARTE NATIVA MAIO 2026": 2.0,
        "ARTE NATIVA MAIO BON 2026": 2.0,
        "ARTE NATIVA ABR BON 2026": 2.0,
        "BELLAPHITUS": 2.0,
        "BELLAPHITUS OL": 1.0,
        "BIOLAB GEN COMBATE": 1.0,
        "CASADINHA QUENTE E FRIO": 2.0,
        "CONECTADOS GEOLAB MARC": 1.0,
        "CCM PROMOÇÃO": 2.0,
        "COTAÇÃO FARMA": 1.0,
        "COMBO BELFAR": 2.0,
        "COMBO BELFAR 2": 2.0,
        "COMBO FECHAMENTO 1": 2.0,
        "COMBO INVERNO": 2.0,
        "COMBO PARAC + DIPIMED": 2.0,
        "COMBO MULTI": 1.0,
        "DIA D ARTE NATIVA BRINDES": 2.0,
        "DIA D LABOTRAT": 2.0,
        "DIA D MERCUR": 2.0,
        "FARMA 01 INTERIOR": 5.0,
        "FARMA 02 INTERIOR": 4.0,
        "FARMA 01": 4.5,
        "FARMA 02": 3.5,
        "FARMA 03": 3.0,
        "FARMA 03 INTERIOR": 3.0,
        "FECHA MES MERCUR": 2.0,
        "GEOLAB OL MARÇO": 1.0,
        "GEOLAB OL ABRIL": 1.0,
        "HOSPITAL LOCAL": 2.0,
        "LUPA DE LEITURA": 2.0,
        "MAXINUTRI": 10.0,
        "MERCUR 5": 5.0,
        "MERCUR 7": 7.0,
        "MULTI + ESPAÇADOR": 2.0,
        "NEGOCIAÇÃO OL FARMA": 1.0,
        "OFERTAS UNIPHAR ABRIL": 2.0,
        "ORTOPEDICOS": 5.0,
        "PED ELETRONICO - GD REDES": 3.0,
        "PRE VENCIDOS - FARMA": 2.0,
        "PROMOÇÃO DO DIA": 2.0,
        "RANBAXY OPORTUNIDADE": 1.0,
        "RANBAXY TS": 3.0,
        "RANBAXY OL": 1.0,
        "RANBAXY PROMO": 2.0,
        "SUPER COMBO RILEX": 2.0,
        "SUPER COMBO RILEX 2": 2.0,
    },
    119: {
        "ARTE NATIVA ABRIL 2026": 2.0,
        "ARTE NATIVA MAIO 2026": 2.0,
        "ARTE NATIVA MAIO BON 2026": 2.0,
        "ARTE NATIVA ABR BON 2026": 2.0,
        "BELLAPHITUS": 2.0,
        "BELLAPHITUS OL": 1.0,
        "BIOLAB GEN COMBATE": 1.0,
        "CASADINHA QUENTE E FRIO": 2.0,
        "CONECTADOS GEOLAB MARC": 1.0,
        "CCM PROMOÇÃO": 2.0,
        "COTAÇÃO FARMA": 1.0,
        "COMBO BELFAR": 2.0,
        "COMBO BELFAR 2": 2.0,
        "COMBO FECHAMENTO 1": 2.0,
        "COMBO INVERNO": 2.0,
        "COMBO PARAC + DIPIMED": 2.0,
        "COMBO MULTI": 1.0,
        "DIA D ARTE NATIVA BRINDES": 2.0,
        "DIA D LABOTRAT": 2.0,
        "DIA D MERCUR": 2.0,
        "FARMA 01 INTERIOR": 5.0,
        "FARMA 02 INTERIOR": 4.0,
        "FARMA 01": 4.5,
        "FARMA 02": 3.5,
        "FARMA 03": 3.0,
        "FARMA 03 INTERIOR": 3.0,
        "FECHA MES MERCUR": 2.0,
        "GEOLAB OL MARÇO": 1.0,
        "GEOLAB OL ABRIL": 1.0,
        "HOSPITAL LOCAL": 2.0,
        "LUPA DE LEITURA": 2.0,
        "MAXINUTRI": 10.0,
        "MERCUR 5": 5.0,
        "MERCUR 7": 7.0,
        "MULTI + ESPAÇADOR": 2.0,
        "NEGOCIAÇÃO OL FARMA": 1.0,
        "OFERTAS UNIPHAR ABRIL": 2.0,
        "ORTOPEDICOS": 5.0,
        "PED ELETRONICO - GD REDES": 3.0,
        "PRE VENCIDOS - FARMA": 2.0,
        "PROMOÇÃO DO DIA": 2.0,
        "RANBAXY OPORTUNIDADE": 1.0,
        "RANBAXY TS": 3.0,
        "RANBAXY OL": 1.0,
        "RANBAXY PROMO": 2.0,
        "SUPER COMBO RILEX": 2.0,
        "SUPER COMBO RILEX 2": 2.0,
    },
    192: {
        "ARTE NATIVA ABRIL 2026": 2.0,
        "ARTE NATIVA MAIO 2026": 2.0,
        "ARTE NATIVA MAIO BON 2026": 2.0,
        "ARTE NATIVA ABR BON 2026": 2.0,
        "BELLAPHITUS": 2.0,
        "BELLAPHITUS OL": 1.0,
        "BIOLAB GEN COMBATE": 1.0,
        "CASADINHA QUENTE E FRIO": 2.0,
        "CONECTADOS GEOLAB MARC": 1.0,
        "CCM PROMOÇÃO": 2.0,
        "COTAÇÃO FARMA": 1.0,
        "COMBO BELFAR": 2.0,
        "COMBO BELFAR 2": 2.0,
        "COMBO FECHAMENTO 1": 2.0,
        "COMBO INVERNO": 2.0,
        "COMBO PARAC + DIPIMED": 2.0,
        "COMBO MULTI": 1.0,
        "DIA D ARTE NATIVA BRINDES": 2.0,
        "DIA D LABOTRAT": 2.0,
        "DIA D MERCUR": 2.0,
        "FARMA 01 INTERIOR": 5.0,
        "FARMA 02 INTERIOR": 4.0,
        "FARMA 01": 4.5,
        "FARMA 02": 3.5,
        "FARMA 03": 3.0,
        "FARMA 03 INTERIOR": 3.0,
        "FECHA MES MERCUR": 2.0,
        "GEOLAB OL MARÇO": 1.0,
        "GEOLAB OL ABRIL": 1.0,
        "HOSPITAL LOCAL": 2.0,
        "LUPA DE LEITURA": 2.0,
        "MAXINUTRI": 10.0,
        "MERCUR 5": 5.0,
        "MERCUR 7": 7.0,
        "MULTI + ESPAÇADOR": 2.0,
        "NEGOCIAÇÃO OL FARMA": 1.0,
        "OFERTAS UNIPHAR ABRIL": 2.0,
        "ORTOPEDICOS": 5.0,
        "PED ELETRONICO - GD REDES": 3.0,
        "PRE VENCIDOS - FARMA": 2.0,
        "PROMOÇÃO DO DIA": 2.0,
        "RANBAXY OPORTUNIDADE": 1.0,
        "RANBAXY TS": 3.0,
        "RANBAXY OL": 1.0,
        "RANBAXY PROMO": 2.0,
        "SUPER COMBO RILEX": 2.0,
        "SUPER COMBO RILEX 2": 2.0,
    },
    148: {
        "ARTE NATIVA ABRIL 2026": 2.0,
        "ARTE NATIVA MAIO 2026": 2.0,
        "ARTE NATIVA MAIO BON 2026": 2.0,
        "ARTE NATIVA ABR BON 2026": 2.0,
        "BELLAPHITUS": 2.0,
        "BELLAPHITUS OL": 1.0,
        "BIOLAB GEN COMBATE": 1.0,
        "CASADINHA QUENTE E FRIO": 2.0,
        "CONECTADOS GEOLAB MARC": 1.0,
        "CCM PROMOÇÃO": 2.0,
        "COTAÇÃO FARMA": 1.0,
        "COMBO BELFAR": 2.0,
        "COMBO BELFAR 2": 2.0,
        "COMBO FECHAMENTO 1": 2.0,
        "COMBO INVERNO": 2.0,
        "COMBO PARAC + DIPIMED": 2.0,
        "COMBO MULTI": 1.0,
        "DIA D ARTE NATIVA BRINDES": 2.0,
        "DIA D LABOTRAT": 2.0,
        "DIA D MERCUR": 2.0,
        "FARMA 01 INTERIOR": 5.0,
        "FARMA 02 INTERIOR": 4.0,
        "FARMA 01": 4.5,
        "FARMA 02": 3.5,
        "FARMA 03": 3.0,
        "FARMA 03 INTERIOR": 3.0,
        "FECHA MES MERCUR": 2.0,
        "GEOLAB OL MARÇO": 1.0,
        "GEOLAB OL ABRIL": 1.0,
        "HOSPITAL LOCAL": 2.0,
        "LUPA DE LEITURA": 2.0,
        "MAXINUTRI": 10.0,
        "MERCUR 5": 5.0,
        "MERCUR 7": 7.0,
        "MULTI + ESPAÇADOR": 2.0,
        "NEGOCIAÇÃO OL FARMA": 1.0,
        "OFERTAS UNIPHAR ABRIL": 2.0,
        "ORTOPEDICOS": 5.0,
        "PED ELETRONICO - GD REDES": 3.0,
        "PRE VENCIDOS - FARMA": 2.0,
        "PROMOÇÃO DO DIA": 2.0,
        "RANBAXY OPORTUNIDADE": 1.0,
        "RANBAXY TS": 3.0,
        "RANBAXY OL": 1.0,
        "RANBAXY PROMO": 2.0,
        "SUPER COMBO RILEX": 2.0,
        "SUPER COMBO RILEX 2": 2.0,
    },
    130: {
        "ARTE NATIVA ABRIL 2026": 2.0,
        "ARTE NATIVA MAIO 2026": 2.0,
        "ARTE NATIVA MAIO BON 2026": 2.0,
        "ARTE NATIVA ABR BON 2026": 2.0,
        "BELLAPHITUS": 2.0,
        "BELLAPHITUS OL": 1.0,
        "BIOLAB GEN COMBATE": 1.0,
        "CASADINHA QUENTE E FRIO": 2.0,
        "CONECTADOS GEOLAB MARC": 1.0,
        "CCM PROMOÇÃO": 2.0,
        "COTAÇÃO FARMA": 1.0,
        "COMBO BELFAR": 2.0,
        "COMBO BELFAR 2": 2.0,
        "COMBO INVERNO": 2.0,
        "COMBO FECHAMENTO 1": 2.0,
        "COMBO PARAC + DIPIMED": 2.0,
        "COMBO MULTI": 1.0,
        "DIA D ARTE NATIVA BRINDES": 2.0,
        "DIA D LABOTRAT": 2.0,
        "DIA D MERCUR": 2.0,
        "FARMA 01 INTERIOR": 5.0,
        "FARMA 02 INTERIOR": 4.0,
        "FARMA 01": 4.5,
        "FARMA 02": 3.5,
        "FARMA 03": 3.0,
        "FARMA 03 INTERIOR": 3.0,
        "FECHA MES MERCUR": 2.0,
        "GEOLAB OL MARÇO": 1.0,
        "GEOLAB OL ABRIL": 1.0,
        "HOSPITAL LOCAL": 2.0,
        "LUPA DE LEITURA": 2.0,
        "MAXINUTRI": 10.0,
        "MERCUR 5": 5.0,
        "MERCUR 7": 7.0,
        "MULTI + ESPAÇADOR": 2.0,
        "NEGOCIAÇÃO OL FARMA": 1.0,
        "OFERTAS UNIPHAR ABRIL": 2.0,
        "ORTOPEDICOS": 5.0,
        "PED ELETRONICO - GD REDES": 3.0,
        "PRE VENCIDOS - FARMA": 2.0,
        "PROMOÇÃO DO DIA": 2.0,
        "RANBAXY OPORTUNIDADE": 1.0,
        "RANBAXY TS": 3.0,
        "RANBAXY OL": 1.0,
        "RANBAXY PROMO": 2.0,
        "SUPER COMBO RILEX": 2.0,
        "SUPER COMBO RILEX 2": 2.0,
    },
    144: {
        "ARTE NATIVA ABRIL 2026": 2.0,
        "ARTE NATIVA MAIO 2026": 2.0,
        "ARTE NATIVA MAIO BON 2026": 2.0,
        "ARTE NATIVA ABR BON 2026": 2.0,
        "BELLAPHITUS": 2.0,
        "BELLAPHITUS OL": 1.0,
        "BIOLAB GEN COMBATE": 1.0,
        "CASADINHA QUENTE E FRIO": 2.0,
        "CONECTADOS GEOLAB MARC": 1.0,
        "CCM PROMOÇÃO": 2.0,
        "COTAÇÃO FARMA": 1.0,
        "COMBO BELFAR": 2.0,
        "COMBO BELFAR 2": 2.0,
        "COMBO FECHAMENTO 1": 2.0,
        "COMBO INVERNO": 2.0,
        "COMBO PARAC + DIPIMED": 2.0,
        "COMBO MULTI": 1.0,
        "DIA D ARTE NATIVA BRINDES": 2.0,
        "DIA D LABOTRAT": 2.0,
        "DIA D MERCUR": 2.0,
        "FARMA 01 INTERIOR": 5.0,
        "FARMA 02 INTERIOR": 4.0,
        "FARMA 01": 4.5,
        "FARMA 02": 3.5,
        "FARMA 03": 3.0,
        "FARMA 03 INTERIOR": 3.0,
        "FECHA MES MERCUR": 2.0,
        "GEOLAB OL MARÇO": 1.0,
        "GEOLAB OL ABRIL": 1.0,
        "HOSPITAL LOCAL": 2.0,
        "LUPA DE LEITURA": 2.0,
        "MAXINUTRI": 10.0,
        "MERCUR 5": 5.0,
        "MERCUR 7": 7.0,
        "MULTI + ESPAÇADOR": 2.0,
        "NEGOCIAÇÃO OL FARMA": 1.0,
        "OFERTAS UNIPHAR ABRIL": 2.0,
        "ORTOPEDICOS": 5.0,
        "PED ELETRONICO - GD REDES": 3.0,
        "PRE VENCIDOS - FARMA": 2.0,
        "PROMOÇÃO DO DIA": 2.0,
        "RANBAXY OPORTUNIDADE": 1.0,
        "RANBAXY TS": 3.0,
        "RANBAXY OL": 1.0,
        "RANBAXY PROMO": 2.0,
        "SUPER COMBO RILEX": 2.0,
        "SUPER COMBO RILEX 2": 2.0,
    },
}

POLICY_PERCENT = {
    seller: {normalize_policy_name(pname): pct for pname, pct in policies.items()}
    for seller, policies in RAW_POLICIES_PERCENT.items()
}

def fetch_political_detail_by_sellers(seller_codes, month, year):
    if not seller_codes:
        return []

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        placeholders = ",".join("?" for _ in seller_codes)

        query = f"""
        SELECT 
            vvend.COD_VENDEDOR,
            vend.Nome_Guerra,
            vvend.COD_POLITICA,
            vvend.VALOR_VENDA
        FROM (
            SELECT 
                ANO           = YEAR(cb.Dat_Emissao),
                MES           = MONTH(cb.Dat_Emissao),
                COD_VENDEDOR  = cb.Cod_Vendedor, 
                COD_POLITICA  = pc.Cod_PolCom,
                VALOR_VENDA   = ROUND(
                    SUM(it.Vlr_LiqItem
                        - it.Vlr_SubsTrib
                        - it.Vlr_SbtRes
                        - it.Vlr_RecSbt
                        - it.Vlr_SubsTribEmb
                        - it.Vlr_DespRateada
                        - ISNULL(it.Vlr_DspExt, 0)), 2)
            FROM NFSCB cb 
            JOIN NFSIT it
              ON cb.Cod_Estabe = it.Cod_Estabe
             AND cb.Ser_Nota   = it.Ser_Nota
             AND cb.Num_Nota   = it.Num_Nota
            JOIN POCOM pc
              ON it.Id_PolCom = pc.Id_PolCom
            WHERE cb.Status    = 'F'
              AND cb.Tip_Saida = 'V'
              AND cb.Dat_Emissao >= DATEFROMPARTS(?, ?, 1)
              AND cb.Dat_Emissao <  DATEADD(MONTH, 1, DATEFROMPARTS(?, ?, 1))
            GROUP BY cb.Cod_Vendedor, pc.Cod_PolCom, YEAR(cb.Dat_Emissao), MONTH(cb.Dat_Emissao)
        ) AS vvend
        JOIN V_VENDE AS vend
          ON vvend.COD_VENDEDOR = vend.Codigo
        WHERE vvend.COD_VENDEDOR IN ({placeholders})
        ORDER BY vvend.COD_VENDEDOR, vvend.COD_POLITICA;
        """

        params = [int(year), int(month), int(year), int(month), *[int(c) for c in seller_codes]]
        cursor.execute(query, params)
        rows = cursor.fetchall()

        if not rows:
            return []

        sellers_data = {}
        unknown = [] 

        for row in rows:
            try:
                seller_id = int(row.COD_VENDEDOR)
                seller_name = row.Nome_Guerra
                policy_label = str(row.COD_POLITICA or "").strip()
                liquid_sale = float(row.VALOR_VENDA or 0.0)
            except AttributeError:
                seller_id = int(row[0]); seller_name = row[1]
                policy_label = str(row[2] or "").strip()
                liquid_sale = float(row[3] or 0.0)

            if seller_id not in sellers_data:
                sellers_data[seller_id] = {
                    "codigo_vendedor": seller_id,
                    "vendedor": seller_name,
                    "dados": [],
                    "total_venda_liquida": 0.0,
                    "total_valor": 0.0
                }

            pct = POLICY_PERCENT.get(seller_id, {}).get(normalize_policy_name(policy_label))
            if pct is None:
                unknown.append((seller_id, policy_label))
                pct = 0.0

            valor = liquid_sale * (pct / 100.0)

            sellers_data[seller_id]["dados"].append({
                "politica": policy_label,
                "venda_liquida": round(liquid_sale, 2),
                "percentual": pct,
                "valor": round(valor, 2)
            })
            sellers_data[seller_id]["total_venda_liquida"] += liquid_sale
            sellers_data[seller_id]["total_valor"] += valor

        for s in sellers_data.values():
            s["total_venda_liquida"] = round(s["total_venda_liquida"], 2)
            s["total_valor"] = round(s["total_valor"], 2)

        if unknown:
            seen = set()
            print("[WARN] Politicas sem mapeamento (vendedor, politica):")
            for v, p in unknown:
                key = (v, p.lower())
                if key not in seen:
                    seen.add(key)
                    print(f"  - {v}: {p}")

        result = list(sellers_data.values())
        result.sort(key=lambda x: x["vendedor"]) 
        return result

    except Exception as e:
        print(f"Erro ao buscar comissões: {e}")
        return []


# def fetch_commissions(seller_codes, month, year):
#     connection = get_db_connection()
#     cursor = connection.cursor()

#     placeholders = ",".join(["?"] * len(seller_codes))

#     query = f"""
#         SELECT 
#             vend.Nome_Guerra AS vendedor,
#             dfab.FABRICANTE AS fabricante,
#             vob.Val_Cota AS valor_cota,
#             vob.Val_Realiz AS valor_realizado,
#             vob.Val_Devol AS valor_devolucao,
#             vob.Per_Cobert AS percentual_cobertura
#         FROM dFABRICANTE AS dfab
#         JOIN V_OBFAB AS vob
#             ON dfab.IDFABRICANTE = vob.Cod_Fabricante
#         JOIN V_VENDE AS vend
#             ON vob.Cod_Vendedor = vend.Codigo
#         WHERE vob.Ano_Ref = ?
#           AND vob.Mes_Ref = ?
#           AND vob.Cod_Vendedor IN ({placeholders})
#         ORDER BY vend.Nome_Guerra ASC
#     """

#     params = [int(year), int(month)] + [int(c) for c in seller_codes]

#     cursor.execute(query, params)
#     rows = cursor.fetchall()

#     sellers = {}

#     for row in rows:

#         vendedor = row.vendedor

#         if vendedor not in sellers:
#             sellers[vendedor] = {
#                 "vendedor": vendedor,
#                 "dados": [],
#                 "total_realizado": 0,
#                 "total_devolucao": 0,
#                 "total_premiacao": 0
#             }

#         realizado = float(row.valor_realizado or 0) / 100
#         devolucao = float(row.valor_devolucao or 0) / 100
#         valor_cota = float(row.valor_cota or 0) / 100
#         cobertura = float(row.percentual_cobertura or 0)
#         fabricante = row.fabricante

#         # 🔥 REGRAS DE PREMIAÇÃO
#         if 100 <= cobertura <= 119:
#             percentual_premio = 0.01
#         elif 120 <= cobertura <= 149:
#             percentual_premio = 0.02
#         elif cobertura >= 150:
#             percentual_premio = 0.03
#         else:
#             percentual_premio = 0

#         venda_liquida = realizado - devolucao
#         premiacao = venda_liquida * percentual_premio

#         sellers[vendedor]["dados"].append({
#             "fabricante": fabricante,
#             "valor_cota": valor_cota,
#             "valor_realizado": realizado,
#             "percentual_cobertura": cobertura,
#             "valor_devolucao": devolucao,
#             "venda_liquida": venda_liquida,
#             "percentual_premio": percentual_premio * 100,
#             "valor_premiacao": premiacao
#         })

#         sellers[vendedor]["total_realizado"] += realizado
#         sellers[vendedor]["total_devolucao"] += devolucao
#         sellers[vendedor]["total_premiacao"] += premiacao

#     connection.close()

#     return list(sellers.values())

def fetch_commissions(seller_codes, month, year):
    connection = get_db_connection()
    cursor = connection.cursor()

    placeholders = ",".join(["?"] * len(seller_codes))

    query = f""" 
        SELECT 
            vend.Nome_Guerra AS vendedor,
            vob.Cod_Vendedor AS codigo_vendedor,
            dfab.FABRICANTE  AS fabricante,
            vob.Val_Cota     AS valor_cota,
            vob.Val_Realiz   AS valor_realizado,
            vob.Val_Devol    AS valor_devolucao,
            vob.Per_Cobert   AS percentual_cobertura
        FROM dFABRICANTE AS dfab
        JOIN (
            SELECT 
                ct.Cod_Estabe,
                ct.Cod_Vendedor,
                ct.Cod_Fabricante,
                Val_Cota   = ISNULL(ct.Vlr_Cota, 0) * 100, 
                Val_Realiz = ISNULL(v.VlrLiq, 0),  
                Val_Devol  = ISNULL(d.VlrDev, 0),  
                Per_Cobert = CASE 
                                WHEN ISNULL(ct.Vlr_Cota, 0) > 0
                                THEN (ISNULL(v.VlrLiq, 0) - ISNULL(d.VlrDev, 0)) / ct.Vlr_Cota 
                                ELSE 0 
                              END,
                ct.Ano_Ref,
                ct.Mes_Ref
            FROM VECOT ct
            INNER JOIN VENDE ve 
                ON ct.Cod_Vendedor = ve.Codigo
            LEFT JOIN (
                SELECT 
                    cb.Cod_Estabe, 
                    cb.Cod_Vendedor, 
                    pr.Cod_Fabricante,
                    SUM(
                        it.Vlr_LiqItem
                      - it.Vlr_SubsTrib
                      - it.Vlr_SbtRes
                      - it.Vlr_RecSbt
                      - it.Vlr_SubsTribEmb
                    ) * 100 AS VlrLiq,
                    SUM(it.Qtd_Produto + it.Qtd_Bonificacao) AS UndVen
                FROM NFSCB cb
                INNER JOIN NFSIT it 
                    ON cb.Cod_Estabe = it.Cod_Estabe 
                   AND cb.Ser_Nota   = it.Ser_Nota 
                   AND cb.Num_Nota   = it.Num_Nota
                INNER JOIN VENDE vd 
                    ON cb.Cod_Vendedor = vd.Codigo
                INNER JOIN PRODU pr 
                    ON it.Cod_Produto = pr.Codigo
                WHERE YEAR(cb.Dat_Emissao) = ?
                  AND MONTH(cb.Dat_Emissao) = ?
                  AND cb.Status = 'F'
                  AND cb.Tip_Saida = 'V'
                  AND vd.Flg_Export = 1
                GROUP BY cb.Cod_Estabe, cb.Cod_Vendedor, pr.Cod_Fabricante
            ) v 
                ON ct.Cod_Estabe   = v.Cod_Estabe
               AND ct.Cod_Vendedor = v.Cod_Vendedor
               AND ct.Cod_Fabricante = v.Cod_Fabricante
            LEFT JOIN (
                SELECT 
                    cb.Cod_Estabe, 
                    cb.Cod_Vendedor, 
                    pr.Cod_Fabricante,
                    SUM(
                        it.Vlr_LiqIte
                      - it.Vlr_SubsTrib
                      - it.Vlr_DifTri
                      - it.Vlr_DespRateada
                      - it.Vlr_SbtRes
                    ) * 100 AS VlrDev,
                    SUM(it.Qtd_Pedido + it.Qtd_Bonificacao) AS UndDev
                FROM NFECB cb
                INNER JOIN NFEIT it 
                    ON cb.Cod_Estabe = it.Cod_Estabe 
                   AND cb.Protocolo  = it.Protocolo
                INNER JOIN VENDE vd 
                    ON cb.Cod_Vendedor = vd.Codigo
                INNER JOIN PRODU pr 
                    ON it.Cod_Produto = pr.Codigo
                WHERE YEAR(cb.Dat_Movimento) = ?
                  AND MONTH(cb.Dat_Movimento) = ?
                  AND cb.Status = 'F'
                  AND cb.Tip_NF = 'D'
                  AND vd.Flg_Export = 1
                GROUP BY cb.Cod_Estabe, cb.Cod_Vendedor, pr.Cod_Fabricante
            ) d 
                ON ct.Cod_Estabe   = d.Cod_Estabe
               AND ct.Cod_Vendedor = d.Cod_Vendedor
               AND ct.Cod_Fabricante = d.Cod_Fabricante
            WHERE ve.Flg_Export = 1
        ) AS vob
            ON dfab.IDFABRICANTE = vob.Cod_Fabricante
        JOIN V_VENDE AS vend
            ON vob.Cod_Vendedor = vend.Codigo
        WHERE vob.Ano_Ref = ?
          AND vob.Mes_Ref = ?
          AND vob.Cod_Vendedor IN ({placeholders})
        ORDER BY vend.Nome_Guerra ASC;
    """

    params = [
        int(year), int(month),
        int(year), int(month),
        int(year), int(month),
        *[int(c) for c in seller_codes] 
    ]

    cursor.execute(query, params)
    rows = cursor.fetchall()

    sellers = {}

    for row in rows:
        vendedor = row.vendedor
        codigo_vendedor = row.codigo_vendedor

        if vendedor not in sellers:
            sellers[vendedor] = {
                "vendedor": vendedor,
                "codigo_vendedor": codigo_vendedor,
                "dados": [],
                "total_realizado": 0.0,
                "total_devolucao": 0.0,
                "total_premiacao": 0.0,
                "total_realizado_geral": 0.0,
                "objetivo_geral": 0.0,
                "cobertura": 0.0
            }

        realizado   = float(row.valor_realizado or 0) / 100.0
        devolucao   = float(row.valor_devolucao or 0) / 100.0
        valor_cota  = float(row.valor_cota or 0) / 100.0
        cobertura   = float(row.percentual_cobertura or 0)
        fabricante  = row.fabricante

        if 100 <= cobertura <= 119:
            percentual_premio = 0.01
        elif 120 <= cobertura <= 149:
            percentual_premio = 0.02
        elif cobertura >= 150:
            percentual_premio = 0.03
        else:
            percentual_premio = 0.0

        venda_liquida = realizado - devolucao
        premiacao = venda_liquida * percentual_premio

        sellers[vendedor]["dados"].append({
            "fabricante": fabricante,
            "valor_cota": valor_cota,
            "valor_realizado": realizado,
            "percentual_cobertura": cobertura,
            "valor_devolucao": devolucao,
            "venda_liquida": venda_liquida,
            "percentual_premio": percentual_premio * 100,
            "valor_premiacao": premiacao
        })

        sellers[vendedor]["total_realizado"] += realizado
        sellers[vendedor]["total_devolucao"] += devolucao
        sellers[vendedor]["total_premiacao"] += premiacao

    query_totals = f"""
        SELECT
            v.Cod_Vendedor,
            v.Total_Vendas,
            ISNULL(o.Obj_Geral, 0) AS Obj_Geral
        FROM (
            SELECT 
                cb.Cod_Vendedor,
                ISNULL(ROUND(SUM(
                    it.Vlr_LiqItem
                  - it.Vlr_SubsTrib
                  - it.Vlr_SbtRes
                  - it.Vlr_RecSbt
                  - it.Vlr_SubsTribEmb
                  - it.Vlr_DespRateada
                  - ISNULL(it.Vlr_DspExt, 0)
                ), 2), 0) AS Total_Vendas
            FROM NFSCB cb
            INNER JOIN NFSIT it
                ON cb.Cod_Estabe = it.Cod_Estabe
               AND cb.Ser_Nota   = it.Ser_Nota
               AND cb.Num_Nota   = it.Num_Nota
            INNER JOIN POCOM pc
                ON it.Id_PolCom = pc.Id_PolCom
            WHERE cb.Status    = 'F'
              AND cb.Tip_Saida = 'V'
              AND cb.Dat_Emissao >= DATEFROMPARTS(?, ?, 1)
              AND cb.Dat_Emissao <  DATEADD(MONTH, 1, DATEFROMPARTS(?, ?, 1))
              AND cb.Cod_Vendedor IN ({placeholders})
            GROUP BY cb.Cod_Vendedor
        ) v
        LEFT JOIN (
            SELECT 
                idvendedor,
                MAX(obj.[VLR OBJETIVO]]]) AS Obj_Geral
            FROM dbo.dOBJETIVO obj
            WHERE obj.Mes = ?  -- (N+1) Mes
              AND obj.Ano = ?  -- (N+2) Ano
            GROUP BY idvendedor
        ) o
          ON o.idvendedor = v.Cod_Vendedor
    """

    params_totals = [
        int(year), int(month),
        int(year), int(month),
        *[int(c) for c in seller_codes],
        int(month), int(year)
    ]

    cursor.execute(query_totals, params_totals)
    totals_rows = cursor.fetchall()

    for row in totals_rows:
        try:
            codigo = row.Cod_Vendedor
            total_realizado_geral = float(row.Total_Vendas or 0)
            objetivo_geral = float(row.Obj_Geral or 0)
        except AttributeError:
            codigo = row[0]
            total_realizado_geral = float(row[1] or 0)
            objetivo_geral = float(row[2] or 0)

        for vend_data in sellers.values():
            if vend_data["codigo_vendedor"] == codigo:
                vend_data["total_realizado_geral"] = total_realizado_geral
                vend_data["objetivo_geral"] = objetivo_geral
                vend_data["cobertura"] = (total_realizado_geral / objetivo_geral) * 100 if objetivo_geral > 0 else 0.0

    connection.close()
    return list(sellers.values())
    
def fetch_general_results(seller_codes, month, year):
    connection = get_db_connection()
    cursor = connection.cursor()

    placeholders = ",".join(["?"] * len(seller_codes))

    query = f"""
        SELECT 
            SUM(ven.VALOR_VENDA) AS total_realizado,
            SUM(obj.OBJETIVO)    AS objetivo_geral
        FROM (
            SELECT
                YEAR(cb.Dat_Emissao)  AS ANO,
                MONTH(cb.Dat_Emissao) AS MES,
                cb.Cod_Vendedor       AS COD_VENDEDOR,
                ROUND(
                    SUM(
                        it.Vlr_LiqItem
                        - it.Vlr_SubsTrib
                        - it.Vlr_SbtRes
                        - it.Vlr_RecSbt
                        - it.Vlr_SubsTribEmb
                        - it.Vlr_DespRateada
                        - ISNULL(it.Vlr_DspExt, 0)
                    ),
                2) AS VALOR_VENDA
            FROM NFSCB cb
            INNER JOIN NFSIT it
            ON cb.Cod_Estabe = it.Cod_Estabe
            AND cb.Ser_Nota   = it.Ser_Nota
            AND cb.Num_Nota   = it.Num_Nota
            INNER JOIN POCOM pc
            ON it.Id_PolCom = pc.Id_PolCom
            WHERE cb.Status    = 'F'
            AND cb.Tip_Saida = 'V'
            AND cb.Dat_Emissao >= DATEFROMPARTS(?, ?, 1)
            AND cb.Dat_Emissao <  DATEADD(MONTH, 1, DATEFROMPARTS(?, ?, 1))
            GROUP BY
                YEAR(cb.Dat_Emissao),
                MONTH(cb.Dat_Emissao),
                cb.Cod_Vendedor
        ) AS ven
        LEFT JOIN (
            SELECT
                obj.idvendedor,
                obj.Mes,
                obj.Ano,
                MAX(obj.[VLR OBJETIVO]]]) AS OBJETIVO
            FROM dbo.dOBJETIVO obj
            GROUP BY obj.idvendedor, obj.Mes, obj.Ano
        ) AS obj
        ON obj.idvendedor = ven.COD_VENDEDOR
        AND obj.Mes        = ven.MES
        AND obj.Ano        = ven.ANO
        WHERE ven.COD_VENDEDOR IN ({placeholders})
        AND ven.MES = ? 
        AND ven.ANO = ?;
    """

    params = [int(c) for c in seller_codes] + [int(month), int(year)]

    cursor.execute(query, params)
    row = cursor.fetchone()

    total_realizado = float(row.total_realizado or 0)
    objetivo_geral = float(row.objetivo_geral or 0)

    cobertura = 0
    if objetivo_geral > 0:
        cobertura = (total_realizado / objetivo_geral) * 100

    connection.close()

    return {
        "total_realizado": total_realizado,
        "objetivo_geral": objetivo_geral,
        "cobertura": cobertura
    }
