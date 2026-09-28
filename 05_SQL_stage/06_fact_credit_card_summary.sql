DROP VIEW IF EXISTS dbo.fact_credit_card_summary;
GO

CREATE VIEW dbo.fact_credit_card_summary AS
SELECT
    SK_ID_CURR,
    COUNT(DISTINCT SK_ID_PREV) card_contract_count,
    AVG(AMT_BALANCE) avg_balance,
    MAX(AMT_BALANCE) max_balance,
    AVG(AMT_CREDIT_LIMIT_ACTUAL) avg_credit_limit,
    AVG(CASE WHEN AMT_CREDIT_LIMIT_ACTUAL > 0 
        THEN AMT_BALANCE / AMT_CREDIT_LIMIT_ACTUAL END) avg_utilization,
    MAX(CASE WHEN AMT_CREDIT_LIMIT_ACTUAL > 0 
        THEN AMT_BALANCE / AMT_CREDIT_LIMIT_ACTUAL END) max_utilization,
    SUM(AMT_DRAWINGS_ATM_CURRENT) total_atm_drawings,
    SUM(AMT_DRAWINGS_POS_CURRENT) total_pos_drawings,
    SUM(CNT_DRAWINGS_ATM_CURRENT) atm_transaction_count,
    SUM(CNT_DRAWINGS_POS_CURRENT) pos_transaction_count,
    AVG(CASE WHEN AMT_BALANCE > 0 
        THEN AMT_PAYMENT_TOTAL_CURRENT / AMT_BALANCE END) avg_payment_to_balance_ratio,
    AVG(CAST(SK_DPD AS FLOAT)) avg_dpd,
    MAX(SK_DPD) max_dpd,
    SUM(CASE WHEN SK_DPD > 0 THEN 1 ELSE 0 END) delinquent_month_count
FROM dbo.raw_credit_card_balance
GROUP BY SK_ID_CURR;
GO

-- SELECT TOP 5 *
-- FROM dbo.fact_credit_card_summary

-- avg_utilization / max_utilization are computed per-row first (AMT_BALANCE / AMT_CREDIT_LIMIT_ACTUAL, guarded against divide-by-zero with the CASE WHEN > 0), then averaged/maxed across months — that's the "ratio of averages vs average of ratios" issue, and per-row-then-aggregate is the more correct approach for a utilization metric
-- avg_payment_to_balance_ratio same logic — only computed for months where there was an actual balance to measure against