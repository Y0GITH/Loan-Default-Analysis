-- since it's monthly status history at the bureau account level (SK_ID_BUREAU), and we need to first summarize per account, then roll that up to per customer — but raw_bureau_balance doesn't have SK_ID_CURR on it directly, so we need to join through raw_bureau to get there.

DROP VIEW IF EXISTS dbo.fact_bureau_balance_summary;
GO

CREATE VIEW dbo.fact_bureau_balance_summary AS
WITH account_level AS (
    SELECT
        bb.SK_ID_BUREAU,
        COUNT(*)                                                          AS months_on_record,
        SUM(CASE WHEN bb.STATUS = 'C' THEN 1 ELSE 0 END)                  AS months_closed,
        SUM(CASE WHEN bb.STATUS = '0' THEN 1 ELSE 0 END)                  AS months_no_dpd,
        SUM(CASE WHEN bb.STATUS IN ('1','2','3','4','5') THEN 1 ELSE 0 END) AS months_delinquent,
        SUM(CASE WHEN bb.STATUS = 'X' THEN 1 ELSE 0 END)                  AS months_unknown,
        MAX(CASE WHEN bb.STATUS IN ('1','2','3','4','5') THEN bb.STATUS ELSE '0' END) AS max_delinquency_status
    FROM dbo.raw_bureau_balance bb
    GROUP BY bb.SK_ID_BUREAU
)
SELECT
    br.SK_ID_CURR,
    SUM(al.months_on_record)                                              AS total_months_on_record,
    SUM(al.months_delinquent)                                             AS total_delinquent_months,
    CAST(SUM(al.months_delinquent) AS FLOAT) 
        / NULLIF(SUM(al.months_on_record), 0)                             AS pct_months_delinquent,
    MAX(al.max_delinquency_status)                                        AS worst_delinquency_status
FROM account_level al
JOIN dbo.raw_bureau br
    ON al.SK_ID_BUREAU = br.SK_ID_BUREAU
GROUP BY br.SK_ID_CURR;
GO

-- SELECT TOP 5 *
-- FROM dbo.fact_bureau_balance_summary