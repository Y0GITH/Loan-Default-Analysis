-- since raw_bureau is one row per previous credit account, but we want one row per customer (SK_ID_CURR) so it joins cleanly to dim_customer.

DROP VIEW IF EXISTS dbo.fact_bureau_summary;
GO

CREATE VIEW dbo.fact_bureau_summary AS
SELECT
    SK_ID_CURR,
    COUNT(SK_ID_BUREAU)                                                AS previous_credit_count,
    SUM(CASE WHEN CREDIT_ACTIVE = 'Active' THEN 1 ELSE 0 END)          AS active_credit_count,
    SUM(CASE WHEN CREDIT_ACTIVE = 'Closed' THEN 1 ELSE 0 END)          AS closed_credit_count,
    SUM(CASE WHEN AMT_CREDIT_SUM_OVERDUE > 0 THEN 1 ELSE 0 END)        AS overdue_account_count,
    SUM(CNT_CREDIT_PROLONG)                                            AS prolonged_count,
    SUM(AMT_CREDIT_SUM)                                                AS total_credit,
    SUM(AMT_CREDIT_SUM_DEBT)                                           AS total_debt,
    SUM(AMT_CREDIT_SUM_OVERDUE)                                        AS total_overdue,
    MAX(AMT_CREDIT_MAX_OVERDUE)                                        AS max_overdue,
    AVG(AMT_CREDIT_SUM)                                                AS avg_credit_amount,
    -- ratios, guarded against divide-by-zero
    CAST(SUM(AMT_CREDIT_SUM_DEBT) AS FLOAT) 
        / NULLIF(SUM(AMT_CREDIT_SUM), 0)                               AS debt_to_credit_ratio,
    CAST(SUM(CASE WHEN CREDIT_ACTIVE = 'Active' THEN 1 ELSE 0 END) AS FLOAT) 
        / NULLIF(COUNT(SK_ID_BUREAU), 0)                               AS active_credit_ratio,
    CAST(SUM(CASE WHEN CREDIT_ACTIVE = 'Closed' THEN 1 ELSE 0 END) AS FLOAT) 
        / NULLIF(COUNT(SK_ID_BUREAU), 0)                               AS closed_credit_ratio
FROM dbo.raw_bureau
GROUP BY SK_ID_CURR;
GO

-- SELECT TOP 5 *
-- FROM dbo.fact_bureau_summary

-- This is now a proper customer-grain fact : previous_credit_count, total_debt, debt_to_credit_ratio etc all sit at one row per SK_ID_CURR, ready to join straight to dim_customer and fact_applications.