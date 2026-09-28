DROP VIEW IF EXISTS dbo.fact_installments_summary;
GO

CREATE VIEW dbo.fact_installments_summary AS
SELECT
    SK_ID_CURR,
    COUNT(*) total_instalments,
    SUM(AMT_INSTALMENT) total_scheduled,
    SUM(AMT_PAYMENT) total_paid,
    SUM(AMT_INSTALMENT - AMT_PAYMENT) total_underpayment,
    AVG(DAYS_LATE) avg_payment_delay,
    MAX(DAYS_LATE) max_payment_delay,
    SUM(CASE WHEN DAYS_LATE > 0 THEN 1 ELSE 0 END) late_payment_count,
    CAST(SUM(CASE WHEN DAYS_LATE > 0 THEN 1 ELSE 0 END) AS FLOAT)
        / NULLIF(COUNT(*), 0) late_payment_rate,
    SUM(CASE WHEN DAYS_LATE < 0 THEN 1 ELSE 0 END) early_payment_count,
    SUM(PAYMENT_MISSED) missed_payment_count,
    AVG(CASE WHEN AMT_INSTALMENT > 0
        THEN AMT_PAYMENT / AMT_INSTALMENT END) avg_payment_ratio
FROM dbo.raw_installments_payments
GROUP BY SK_ID_CURR;
GO

-- SELECT TOP 5 *
-- FROM dbo.fact_installments_summary

-- DAYS_LATE and PAYMENT_MISSED were already derived by your Python cleaning step, so no need to recompute delay from DAYS_ENTRY_PAYMENT - DAYS_INSTALMENT manually — just aggregate the pre-built columns
-- late_payment_rate is the count-based ratio, guarded with NULLIF
-- avg_payment_ratio follows the same per-row-then-average logic as the credit card utilization — computed per instalment, then averaged, so a customer who underpays consistently shows a ratio below 1, not masked by a couple of overpayments elsewhere