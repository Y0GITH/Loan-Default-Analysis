-- pos_cash_balance — same pattern as before, monthly records at SK_ID_PREV grain, rolled up to customer level.

DROP VIEW IF EXISTS dbo.fact_pos_cash_summary;
GO

CREATE VIEW dbo.fact_pos_cash_summary AS
SELECT
    SK_ID_CURR,
    COUNT(DISTINCT SK_ID_PREV)                                          AS pos_contract_count,
    SUM(CASE 
            WHEN NAME_CONTRACT_STATUS = 'Active' THEN 1 ELSE 0 END) AS active_months,
    SUM(CASE 
            WHEN NAME_CONTRACT_STATUS = 'Completed' THEN 1 
            ELSE 0 END) AS completed_months,
    AVG(CAST(SK_DPD AS FLOAT)) AS avg_dpd,
    MAX(SK_DPD) AS max_dpd,
    AVG(CAST(SK_DPD_DEF AS FLOAT)) AS avg_dpd_def,
    MAX(SK_DPD_DEF) AS max_dpd_def,
    SUM(CASE 
        WHEN SK_DPD > 0 THEN 1 
        ELSE 0 END) AS delinquent_month_count,
    AVG(CNT_INSTALMENT_FUTURE) avg_remaining_instalments
FROM dbo.raw_pos_cash_balance
GROUP BY SK_ID_CURR;
GO

-- SELECT TOP 5 *
-- FROM dbo.fact_pos_cash_summary

-- COUNT(DISTINCT SK_ID_PREV) counts unique loan contracts, not rows — since each contract has many monthly rows
-- SK_DPD = days past due at that snapshot month, SK_DPD_DEF = days past due excluding a tolerance window (a stricter version) — averaging and maxing both gives you typical vs worst-case lateness
-- delinquent_month_count counts how many monthly snapshots had any lateness at all — frequency, separate from severity