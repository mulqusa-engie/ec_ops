WITH iso_mapping (mkt, iso) AS (
    VALUES
    -- ERCOT (TX)
    ('CCXTGB', 'ERCOT'), ('CCXTGF', 'ERCOT'), ('CCXTSB', 'ERCOT'), ('CCXTSF', 'ERCOT'),
    ('TXCP', 'ERCOT'), ('TXCPBH', 'ERCOT'), ('TXCPFH', 'ERCOT'),
    ('TXGEBH', 'ERCOT'), ('TXGEFH', 'ERCOT'), ('TXGSBH', 'ERCOT'), ('TXGSFH', 'ERCOT'),
    ('TXGSPY', 'ERCOT'), ('TXGWBH', 'ERCOT'), ('TXGWFH', 'ERCOT'),
    ('TXNSBH', 'ERCOT'), ('TXNSFH', 'ERCOT'), ('TXNSPY', 'ERCOT'),
    ('TXNWBH', 'ERCOT'), ('TXNWFH', 'ERCOT'), ('TXNWPY', 'ERCOT'),
    ('TXREC', 'ERCOT'), ('TXRP', 'ERCOT'), ('TXGWPY', 'ERCOT'),
    ('TXRPBH', 'ERCOT'), ('TXRPFH', 'ERCOT'), ('TXRPPY', 'ERCOT'),
    ('TXSABH', 'ERCOT'), ('TXSAFH', 'ERCOT'), ('TXSOBH', 'ERCOT'), ('TXSOFH', 'ERCOT'),
    ('TXWABH', 'ERCOT'), ('TXWAFH', 'ERCOT'), ('TXWIBH', 'ERCOT'), ('TXWIFH', 'ERCOT'),
    ('TXXXGR', 'ERCOT'), ('TXSRCB', 'ERCOT'), ('TXSRCF', 'ERCOT'),
    -- NATIONAL (US)
    ('CCXNAR', 'NATIONAL'), ('CCXNBH', 'NATIONAL'), ('CCXNFH', 'NATIONAL'),
    ('CCXNSF', 'NATIONAL'), ('CCXNSB', 'NATIONAL'),
    ('USHREC', 'NATIONAL'), ('USHYBH', 'NATIONAL'), ('USHYFH', 'NATIONAL'),
    ('USSOBH', 'NATIONAL'), ('USSOFH', 'NATIONAL'), ('USGESO', 'NATIONAL'),
    ('USWIBH', 'NATIONAL'), ('USWIFH', 'NATIONAL'), ('USWIPY', 'NATIONAL'),
    ('USWREC', 'NATIONAL'), ('USWSBH', 'NATIONAL'), ('USWSFH', 'NATIONAL'),
    ('USTXWS', 'NATIONAL'),
    
    
    
    
    
    
    
    
    -- MISO
    ('MIWIFH', 'MISO'), ('MIWIBH', 'MISO'),
    -- SPP
    ('SPWIBH', 'SPP'), ('SPWIFH', 'SPP'),
    -- NEPOOL
    ('CCXCT1', 'NEPOOL'), ('CCXCT2', 'NEPOOL'), ('CCXCT3', 'NEPOOL'),
    ('CTC1', 'NEPOOL'), ('CTC2', 'NEPOOL'), ('CTC3', 'NEPOOL'),
    ('CCXMA1', 'NEPOOL'), ('CCXMA2', 'NEPOOL'), ('CCXMAA', 'NEPOOL'),
    ('CCXMAS', 'NEPOOL'), ('CCXMAW', 'NEPOOL'), ('CCXMCE', 'NEPOOL'), ('CCXMS2', 'NEPOOL'),
    ('MAAPS', 'NEPOOL'), ('MACESE', 'NEPOOL'), ('MACES', 'NEPOOL'), ('MACPS', 'NEPOOL'),
    ('MARP', 'NEPOOL'), ('MARPN', 'NEPOOL'), ('MARPW', 'NEPOOL'),
    ('MASO', 'NEPOOL'), ('MASO2', 'NEPOOL'),
    ('CCXME1', 'NEPOOL'), ('CCXME2', 'NEPOOL'),
    ('ME1A', 'NEPOOL'), ('MENWRP', 'NEPOOL'), ('MERP', 'NEPOOL'),
    ('CCXNEP', 'NEPOOL'), ('CCXNEQ', 'NEPOOL'),
    ('NEDUAL', 'NEPOOL'), ('NEPTRI', 'NEPOOL'), ('NEQUAD', 'NEPOOL'), ('NEQUIN', 'NEPOOL'),
    ('CCXNH1', 'NEPOOL'), ('CCXNH3', 'NEPOOL'),
    ('NHC1', 'NEPOOL'), ('NHC1T', 'NEPOOL'), ('NHC2', 'NEPOOL'),
    ('NHC3', 'NEPOOL'), ('NHC4', 'NEPOOL'),
    ('CCXRIN', 'NEPOOL'), ('RIEX', 'NEPOOL'), ('RINEW', 'NEPOOL'),
    -- NORTH AMERICA
    ('NAREC', 'NORTH AMERICA'),
    -- NYISO
    ('CCXNY1', 'NYISO'), ('NYEDP', 'NYISO'), ('NYT1', 'NYISO'),
    -- PJM
    ('CCXDC1', 'PJM'), ('CCXDCS', 'PJM'),
    ('CCXMD1', 'PJM'), ('CCXMD2', 'PJM'), ('CCXMDS', 'PJM'),
    ('CCXNJ1', 'PJM'), ('CCXNJ2', 'PJM'), ('CCXNJS', 'PJM'),
    ('CCXOHN', 'PJM'), ('CCXOHS', 'PJM'),
    ('OHION', 'PJM'), ('OHREC', 'PJM'), ('OHRECM', 'PJM'),
    ('CCXPA1', 'PJM'), ('CCXPA2', 'PJM'), ('CCXPAS', 'PJM'),
    ('CCXPJM', 'PJM'),
    ('DCSO', 'PJM'), ('DCT1', 'PJM'), ('DCT2', 'PJM'),
    ('EFECPA', 'PJM'),
    ('MDC1', 'PJM'), ('MDC2', 'PJM'), ('MDSO', 'PJM'),
    ('NJC1', 'PJM'), ('NJC2', 'PJM'), ('NJSO', 'PJM'),
    ('PASO', 'PJM'), ('PAT1', 'PJM'), ('PAT2', 'PJM'),
    ('PJMTRI', 'PJM'),
    ('VAREC', 'PJM'), ('BVREC', 'PJM')
),
base AS (
    SELECT 
        CAST(RTRIM(g.comp) AS INTEGER) AS vintage_year,
        COALESCE(m.iso, 'OTHER') AS iso,
        g.deltand
    FROM "cdh_eemnapowertradingdata_32020"."greeks_aligne_n_ot" g
    LEFT JOIN iso_mapping m ON RTRIM(g.mkt) = m.mkt
    WHERE g.asofdate = (SELECT MAX(asofdate) FROM "cdh_eemnapowertradingdata_32020"."greeks_aligne_n_ot")
      AND g.active = true
      AND g.sourcesystem = 'Aligne'
      AND g.mrktcattr1 = 'REC'
    --   AND g.book IN (
    --       'HMMK','HPBW','RRHY','HPHM','HREC','REWL','TREC','GREC','HPDS',
    --       'HPLO','HPPD','HPPS','TPPS','HPTN','HPIS','RPWR','ROWN','TMAC',
    --       'HNAT','HNEP','HNYK','HPJR','HPLK','HSPL','HAVW','HPSV','RHDG',
    --       'HPSB','HPLU'
    --   )
      
        AND g.book IN (
          'HPHM','HREC','TREC',
          'HNAT','HNEP','HNYK','HPJR'
         
      )
      
      
      AND (g.cpty IS NULL OR (
            UPPER(g.cpty) NOT IN ('IHHM','ITRC','IHRC','IHPS','IHNP','IHNT','IHNY','IHPJ')
            AND UPPER(g.cpty) NOT LIKE 'TEMIT%'
      ))
      AND TRY_CAST(RTRIM(g.comp) AS INTEGER) IS NOT NULL
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
