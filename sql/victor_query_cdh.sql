SELECT 
    cpty,
    COUNT(*) AS legs,
    SUM(deltand) AS sum_delta_nd
FROM "cdh_eemnapowertradingdata_32020"."greeks_aligne_n_ot"
WHERE asofdate = TIMESTAMP '2026-05-05 00:00:00'
  AND active = true
  AND book = 'TREC'
  AND mrktcattr1 = 'REC'
  AND sourcesystem = 'Aligne'
  AND TRY_CAST(RTRIM(comp) AS INTEGER) = 2026
GROUP BY cpty
ORDER BY ABS(SUM(deltand)) DESC;