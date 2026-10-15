SELECT
    tracrisk.zsup_recs.c12_report_dat as REPORT_DATE,
    tracrisk.zsup_recs.c0_trade_date as TRADE_DATE,
    tracrisk.zsup_recs.c4_book as BOOK,
    tracrisk.zsup_recs.c1_zkey as ZKEY,
    tracrisk.zsup_recs.c3_xref as XREF,
    tracrisk.zsup_recs.c5_b_s as B_S,
    tracrisk.zsup_recs.c8__market as MARKET,
    tracrisk.zsup_recs.c9__component as YEAR,
    tracrisk.zsup_recs.c10__amt as AMOUNT,
    tracrisk.zsup_recs.c11_price_trd as TRADE_PRICE,
    tracrisk.zsup_recs.c15__del_dateend as DEL_DATE
FROM
    tracrisk.zsup_recs
WHERE
    tracrisk.zsup_recs.c4_book = 'TMAC'