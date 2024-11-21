from database import get_db_connection
from datetime import datetime

def fetch_suppliers():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        SELECT DISTINCT Fantasia AS nome
        FROM vw_dados_compras
        WHERE Fantasia NOT IN (
            '3M', 
            'CANNONE', 
            'CALUETE E PINHO LTDA', 
            'CABEPEL', 
            'C&M FARDAMENTOS', 
            'C ROLIM', 
            'C B DIAS ME', 
            'C & M FARDAMENTOS', 
            'CARMEHIL',
		    'ARTE NATIVA',
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
            det.Qtd_SldCalPra,
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
        JOIN V_PRSLD_DET det ON p.Codigo = det.Cod_Produt
        WHERE f.Fantasia = ?
        AND f.Fantasia NOT IN (
            '3M', 
            'CANNONE', 
            'CALUETE E PINHO LTDA', 
            'CABEPEL', 
            'C&M FARDAMENTOS', 
            'C ROLIM', 
            'C B DIAS ME', 
            'C & M FARDAMENTOS', 
            'CARMEHIL',
		    'ARTE NATIVA',
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
        GROUP BY 
	        f.Fantasia,
            p.Descricao,
            p.Codigo,
            pr.Sta_AbcUniVenFab,
            pr.Sta_AbcValFatFab,
            pr.Prc_Venda,
            pr.Qtd_Dispon,
            det.Qtd_SldCalPra,
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

        media_faturamento_diario = formatted_avg / 30 if formatted_avg > 0 else 0.0000000001
        cobertura = int(formatted_avg / media_faturamento_diario)

        dias_suprimento_total = replacement_days + supply_days
        sugestao_compra = int((media_faturamento_diario * dias_suprimento_total) - row.Qtd_SldCalPra)
        if row.Qtd_SldCalPra == 0 and sugestao_compra == 0 and row.Qtd_EstMin > 0:
            sugestao_compra = row.Qtd_EstMin
        
        products.append({
            'descricao': row.Descricao,
            'unidades_faturadas_mes0': row.Qtd_FatMes0,
            'unidades_faturadas_mes1': row.Qtd_FatMes1,
            'unidades_faturadas_mes2': row.Qtd_FatMes2,
            'unidades_faturadas_mes3': row.Qtd_FatMes3,
            'media_faturada': formatted_avg,
            'estoque_minimo': row.Qtd_EstMin,
            'estoque_disponivel': row.Qtd_SldCalPra,
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
		    'ARTE NATIVA',
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
        det.Qtd_SldCalPra,
        pr.Qtd_Fisico,
        pr.Qtd_Transi,
        pr.Qtd_EstMin,
        v.idproduto,
        v.idfabricante,
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
            ) AS media_diaria_venda  -- Média diária de vendas (último trimestre)
    FROM 
        fVENDAS v
    JOIN 
        PRODU p ON v.IDPRODUTO = p.Codigo
    JOIN 
        FABRI f ON p.Cod_Fabricante = f.Codigo
    JOIN 
        PRXES pr ON pr.Cod_Produt = p.Codigo
    JOIN 
    	V_PRSLD_DET det ON p.Codigo = det.Cod_Produt
    WHERE
        f.Fantasia = ?
        AND f.Fantasia NOT IN (
            '3M', 
            'CANNONE', 
            'CALUETE E PINHO LTDA', 
            'CABEPEL', 
            'C&M FARDAMENTOS', 
            'C ROLIM', 
            'C B DIAS ME', 
            'C & M FARDAMENTOS', 
            'CARMEHIL',
		    'ARTE NATIVA',
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
    GROUP BY 
        f.Fantasia, 
        p.Descricao, 
        p.Codigo, 
        pr.Sta_AbcUniVenFab, 
        pr.Sta_AbcValFatFab, 
        pr.Qtd_Dispon, 
        det.Qtd_SldCalPra,
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
        estoque_disponivel = row.Qtd_SldCalPra
        estoque_fisico = row.Qtd_Fisico
        estoque_transito = row.Qtd_Transi
        media_diaria_venda = row.media_diaria_venda
        estoque_minimo = row.Qtd_EstMin,
        curva = row.Sta_AbcUniVenFab,
        total_estoque = estoque_disponivel + estoque_transito
        
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

def fetch_total_rupture_risk(days_estimate):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            p.Codigo,
            pr.Qtd_Dispon,
            det.Qtd_SldCalPra,
            pr.Qtd_Transi,
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
        	V_PRSLD_DET det ON p.Codigo = det.Cod_Produt
        GROUP BY 
            p.Codigo,
            pr.Qtd_Dispon,
            det.Qtd_SldCalPra,
            pr.Qtd_Transi,
            pr.Qtd_EstMin;
    """

    cursor.execute(query)
    result = cursor.fetchall()

    total_risk_items = 0

    for row in result:
        total_stock = row.Qtd_SldCalPra + row.Qtd_Transi 
        predicted_sales = row.Media_Diaria_Trimestre * days_estimate
        rupture_risk = (total_stock - predicted_sales) - total_stock if total_stock > 0 else -1

        if rupture_risk < 0:
            total_risk_items += 1

    cursor.close()
    connection.close()

    return total_risk_items

def fetch_items_within_1_year():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT 
            p.Codigo,
            det.Qtd_SldCalPra,
            pr.Dat_PrxVctLot,
            MAX(ba.Dat_VctLot) AS Dat_VctLot_Mais_Recente
        FROM 
            PRODU p
        JOIN 
            PRXES pr ON pr.Cod_Produt = p.Codigo
        JOIN 
            V_PRSLD_DET det ON p.Codigo = det.Cod_Produt
        LEFT JOIN 
            BALIT ba ON p.Codigo = ba.Cod_Produt
        GROUP BY 
            p.Codigo, 
            det.Qtd_SldCalPra, 
            pr.Dat_PrxVctLot;
    """

    cursor.execute(query)
    result = cursor.fetchall()

    total_within_1_year = 0

    for row in result:
        dat_prx_vct_lot = row.Dat_PrxVctLot
        dat_vct_lot_mais_recente = row.Dat_VctLot_Mais_Recente

        # Determina a data de vencimento final
        if dat_prx_vct_lot:
            data_vencimento = dat_prx_vct_lot.date() if isinstance(dat_prx_vct_lot, datetime) else dat_prx_vct_lot
        elif dat_vct_lot_mais_recente:
            data_vencimento = dat_vct_lot_mais_recente.date() if isinstance(dat_vct_lot_mais_recente, datetime) else dat_vct_lot_mais_recente
        else:
            continue  # Ignora produtos sem datas válidas

        # Calcula os dias para vencimento
        dias_para_vencimento = (data_vencimento - datetime.now().date()).days

        # Conta produtos com vencimento dentro de 1 ano
        if 0 <= dias_para_vencimento <= 365:
            total_within_1_year += 1

    cursor.close()
    connection.close()

    return total_within_1_year