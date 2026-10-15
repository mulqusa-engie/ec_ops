WITH iso_mapping (mkt, iso, source) AS (
    VALUES
    -- ERCOT (TX)
    ('CCXTGB', 'ERCOT', 'WIND'), ('CCXTGF', 'ERCOT', 'WIND'),
    ('CCXTSB', 'ERCOT', 'SOLAR'), ('CCXTSF', 'ERCOT', 'SOLAR'),
    ('TXCP', 'ERCOT', 'CP'), ('TXCPBH', 'ERCOT', 'CP'), ('TXCPFH', 'ERCOT', 'CP'),
    ('TXGEBH', 'ERCOT', 'WIND'), ('TXGEFH', 'ERCOT', 'WIND'),
    ('TXGSBH', 'ERCOT', 'SOLAR'), ('TXGSFH', 'ERCOT', 'SOLAR'), ('TXGSPY', 'ERCOT', 'SOLAR'),
    ('TXGWBH', 'ERCOT', 'WIND'), ('TXGWFH', 'ERCOT', 'WIND'), ('TXGWPY', 'ERCOT', 'WIND'),
    ('TXNSBH', 'ERCOT', 'SOLAR'), ('TXNSFH', 'ERCOT', 'SOLAR'), ('TXNSPY', 'ERCOT', 'SOLAR'),
    ('TXNWBH', 'ERCOT', 'WIND'), ('TXNWFH', 'ERCOT', 'WIND'), ('TXNWPY', 'ERCOT', 'WIND'),
    ('TXREC', 'ERCOT', 'CP'),
    ('TXRP', 'ERCOT', 'CP'), ('TXRPBH', 'ERCOT', 'CP'), ('TXRPFH', 'ERCOT', 'CP'), ('TXRPPY', 'ERCOT', 'CP'),
    ('TXSABH', 'ERCOT', 'SOLAR'), ('TXSAFH', 'ERCOT', 'SOLAR'),
    ('TXSOBH', 'ERCOT', 'SOLAR'), ('TXSOFH', 'ERCOT', 'SOLAR'),
    ('TXWABH', 'ERCOT', 'WIND'), ('TXWAFH', 'ERCOT', 'WIND'),
    ('TXWIBH', 'ERCOT', 'WIND'), ('TXWIFH', 'ERCOT', 'WIND'),
    ('TXXXGR', 'ERCOT', 'CP'),
    ('TXSRCB', 'ERCOT', 'SOLAR'), ('TXSRCF', 'ERCOT', 'SOLAR'),
    -- NATIONAL (US)
    ('CCXNAR', 'NATIONAL', 'WIND'), ('CCXNBH', 'NATIONAL', 'WIND'), ('CCXNFH', 'NATIONAL', 'WIND'),
    ('CCXNSF', 'NATIONAL', 'SOLAR'), ('CCXNSB', 'NATIONAL', 'SOLAR'),
    ('USHREC', 'NATIONAL', 'HYDRO'),
    ('USHYBH', 'NATIONAL', 'HYDRO'), ('USHYFH', 'NATIONAL', 'HYDRO'),
    ('USSOBH', 'NATIONAL', 'SOLAR'), ('USSOFH', 'NATIONAL', 'SOLAR'),
    ('USGESO', 'NATIONAL', 'SOLAR'),
    ('USWIBH', 'NATIONAL', 'WIND'), ('USWIFH', 'NATIONAL', 'WIND'), ('USWIPY', 'NATIONAL', 'WIND'),
    ('USWREC', 'NATIONAL', 'WIND'),
    ('USWSBH', 'NATIONAL', 'WIND/SOLAR'), ('USWSFH', 'NATIONAL', 'WIND/SOLAR'),
    ('USTXWS', 'NATIONAL', 'WIND/SOLAR'),
    -- MISO
    ('MIWIFH', 'MISO', 'WIND'), ('MIWIBH', 'MISO', 'WIND'),
    -- SPP
    ('SPWIBH', 'SPP', 'WIND'), ('SPWIFH', 'SPP', 'WIND'),
    -- NEPOOL
    ('CCXCT1', 'NEPOOL', 'CP'), ('CCXCT2', 'NEPOOL', 'CP'), ('CCXCT3', 'NEPOOL', 'CP'),
    ('CTC1', 'NEPOOL', 'CP'), ('CTC2', 'NEPOOL', 'CP'), ('CTC3', 'NEPOOL', 'CP'),
    ('CCXMA1', 'NEPOOL', 'CP'), ('CCXMA2', 'NEPOOL', 'CP'), ('CCXMAA', 'NEPOOL', 'CP'),
    ('CCXMAS', 'NEPOOL', 'SOLAR'), ('CCXMAW', 'NEPOOL', 'CP'),
    ('CCXMCE', 'NEPOOL', 'CP'), ('CCXMS2', 'NEPOOL', 'SOLAR'),
    ('MAAPS', 'NEPOOL', 'CP'), ('MACESE', 'NEPOOL', 'CP'), ('MACES', 'NEPOOL', 'CP'),
    ('MACPS', 'NEPOOL', 'CP'),
    ('MARP', 'NEPOOL', 'CP'), ('MARPN', 'NEPOOL', 'CP'), ('MARPW', 'NEPOOL', 'CP'),
    ('MASO', 'NEPOOL', 'SOLAR'), ('MASO2', 'NEPOOL', 'SOLAR'),
    ('CCXME1', 'NEPOOL', 'CP'), ('CCXME2', 'NEPOOL', 'CP'),
    ('ME1A', 'NEPOOL', 'CP'), ('MENWRP', 'NEPOOL', 'CP'), ('MERP', 'NEPOOL', 'CP'),
    ('CCXNEP', 'NEPOOL', 'CP'), ('CCXNEQ', 'NEPOOL', 'CP'),
    ('NEDUAL', 'NEPOOL', 'CP'), ('NEPTRI', 'NEPOOL', 'CP'),
    ('NEQUAD', 'NEPOOL', 'CP'), ('NEQUIN', 'NEPOOL', 'CP'),
    ('CCXNH1', 'NEPOOL', 'CP'), ('CCXNH3', 'NEPOOL', 'CP'),
    ('NHC1', 'NEPOOL', 'CP'), ('NHC1T', 'NEPOOL', 'CP'), ('NHC2', 'NEPOOL', 'CP'),
    ('NHC3', 'NEPOOL', 'CP'), ('NHC4', 'NEPOOL', 'CP'),
    ('CCXRIN', 'NEPOOL', 'CP'), ('RIEX', 'NEPOOL', 'CP'), ('RINEW', 'NEPOOL', 'CP'),
    -- NORTH AMERICA
    ('NAREC', 'NORTH AMERICA', 'HYDRO'),
    -- NYISO
    ('CCXNY1', 'NYISO', 'CP'), ('NYEDP', 'NYISO', 'CP'), ('NYT1', 'NYISO', 'CP'),
    -- PJM
    ('CCXDC1', 'PJM', 'CP'), ('CCXDCS', 'PJM', 'SOLAR'),
    ('CCXMD1', 'PJM', 'CP'), ('CCXMD2', 'PJM', 'CP'), ('CCXMDS', 'PJM', 'SOLAR'),
    ('CCXNJ1', 'PJM', 'CP'), ('CCXNJ2', 'PJM', 'CP'), ('CCXNJS', 'PJM', 'SOLAR'),
    ('CCXOHN', 'PJM', 'CP'), ('CCXOHS', 'PJM', 'SOLAR'),
    ('OHION', 'PJM', 'CP'), ('OHREC', 'PJM', 'CP'), ('OHRECM', 'PJM', 'CP'),
    ('CCXPA1', 'PJM', 'CP'), ('CCXPA2', 'PJM', 'CP'), ('CCXPAS', 'PJM', 'SOLAR'),
    ('CCXPJM', 'PJM', 'CP'),
    ('DCSO', 'PJM', 'SOLAR'), ('DCT1', 'PJM', 'CP'), ('DCT2', 'PJM', 'CP'),
    ('EFECPA', 'PJM', 'CP'),
    ('MDC1', 'PJM', 'CP'), ('MDC2', 'PJM', 'CP'), ('MDSO', 'PJM', 'SOLAR'),
    ('NJC1', 'PJM', 'CP'), ('NJC2', 'PJM', 'CP'), ('NJSO', 'PJM', 'SOLAR'),
    ('PASO', 'PJM', 'SOLAR'), ('PAT1', 'PJM', 'CP'), ('PAT2', 'PJM', 'CP'),
    ('PJMTRI', 'PJM', 'CP'),
    ('VAREC', 'PJM', 'CP'), ('BVREC', 'PJM', 'CP')
),
base AS (
    SELECT 
        CAST(RTRIM(g.comp) AS INTEGER) AS vintage_year,
        COALESCE(m.iso, 'OTHER') AS iso,
        COALESCE(m.source, 'UNKNOWN') AS source,
        g.deltand
    FROM "cdh_eemnapowertradingdata_32020"."greeks_aligne_n_ot" g
    LEFT JOIN iso_mapping m ON RTRIM(g.mkt) = m.mkt
    WHERE g.asofdate = (SELECT MAX(asofdate) FROM "cdh_eemnapowertradingdata_32020"."greeks_aligne_n_ot")
      AND g.active = true
      AND g.sourcesystem = 'Aligne'
      AND g.mrktcattr1 = 'REC'
      AND g.book IN ('HNAT','HNEP','HNYK','HPJR','HREC','TREC','HPHM')  
      AND (g.cpty IS NULL OR (
            UPPER(g.cpty) NOT IN ('IHHM','ITRC','IHRC','IHPS','IHNP','IHNT','IHNY','IHPJ')
            AND UPPER(g.cpty) NOT LIKE 'TEMIT%'
      ))
      AND TRY_CAST(RTRIM(g.comp) AS INTEGER) IS NOT NULL
      AND CAST(RTRIM(g.comp) AS INTEGER) != 2021  
      AND COALESCE(m.source, 'UNKNOWN') != 'CP'   -- SOURCE != CP
)
SELECT 
    COALESCE(iso, 'Total') AS iso,
    SUM(CASE WHEN vintage_year = 2025 THEN deltand ELSE 0 END) AS "2025",
    SUM(CASE WHEN vintage_year = 2026 THEN deltand ELSE 0 END) AS "2026",
    SUM(CASE WHEN vintage_year = 2027 THEN deltand ELSE 0 END) AS "2027",
    SUM(CASE WHEN vintage_year = 2028 THEN deltand ELSE 0 END) AS "2028",
    SUM(CASE WHEN vintage_year = 2029 THEN deltand ELSE 0 END) AS "2029",
    SUM(CASE WHEN vintage_year = 2030 THEN deltand ELSE 0 END) AS "2030",
    SUM(CASE WHEN vintage_year = 2031 THEN deltand ELSE 0 END) AS "2031",
    SUM(CASE WHEN vintage_year = 2032 THEN deltand ELSE 0 END) AS "2032",
    SUM(CASE WHEN vintage_year = 2033 THEN deltand ELSE 0 END) AS "2033",
    SUM(CASE WHEN vintage_year = 2034 THEN deltand ELSE 0 END) AS "2034",
    SUM(CASE WHEN vintage_year = 2035 THEN deltand ELSE 0 END) AS "2035",
    SUM(deltand) AS Total
FROM base
GROUP BY ROLLUP (iso)
ORDER BY 
    CASE 
        WHEN iso IS NULL THEN 99
        WHEN iso = 'ERCOT' THEN 1 
        WHEN iso = 'NATIONAL' THEN 2 
        WHEN iso = 'MISO' THEN 3 
        WHEN iso = 'NEPOOL' THEN 4 
        WHEN iso = 'NYISO' THEN 5 
        WHEN iso = 'PJM' THEN 6 
        WHEN iso = 'SPP' THEN 7 
        WHEN iso = 'NORTH AMERICA' THEN 8 
        ELSE 9 
    END;