DROP VIEW IF EXISTS dbo.fact_previous_summary;
GO

CREATE VIEW dbo.fact_previous_summary AS
SELECT
    SK_ID_CURR,
    COUNT(DISTINCT SK_ID_PREV) application_count,
    SUM(CASE WHEN NAME_CONTRACT_STATUS = 'Approved' THEN 1 ELSE 0 END) approved_count,
    SUM(CASE WHEN NAME_CONTRACT_STATUS = 'Refused' THEN 1 ELSE 0 END) refused_count,
    SUM(CASE WHEN NAME_CONTRACT_STATUS = 'Canceled' THEN 1 ELSE 0 END) cancelled_count,
    SUM(CASE WHEN NAME_CONTRACT_STATUS = 'Unused offer' THEN 1 ELSE 0 END) unused_count,
    CAST(SUM(CASE WHEN NAME_CONTRACT_STATUS = 'Approved' THEN 1 ELSE 0 END) AS FLOAT)
        / NULLIF(COUNT(DISTINCT SK_ID_PREV), 0) approval_rate,
    CAST(SUM(CASE WHEN NAME_CONTRACT_STATUS = 'Refused' THEN 1 ELSE 0 END) AS FLOAT)
        / NULLIF(COUNT(DISTINCT SK_ID_PREV), 0) refusal_rate,
    AVG(AMT_CREDIT) avg_previous_credit,
    MAX(AMT_CREDIT) max_previous_credit,
    AVG(AMT_APPLICATION) avg_application_amount,
    AVG(AMT_APPLICATION - AMT_CREDIT) avg_requested_vs_approved_gap,
    AVG(CNT_PAYMENT) avg_repayment_term,
    SUM(LOAN_WAS_ACTIVATED) activated_loan_count
FROM dbo.raw_previous_application
GROUP BY SK_ID_CURR;
GO

-- SELECT TOP 5 *
-- FROM dbo.fact_previous_summary

-- COUNT(DISTINCT SK_ID_PREV) — same reasoning as POS/cash, one row per previous application record so no duplication risk here anyway, but distinct keeps it safe
-- approval_rate / refusal_rate — count-based ratios against total applications, NULLIF guarded
-- avg_requested_vs_approved_gap — AMT_APPLICATION is what the customer asked for, AMT_CREDIT is what was actually approved; a consistently large positive gap means the lender is trimming requests down
-- activated_loan_count sums your pre-built LOAN_WAS_ACTIVATED flag rather than re-deriving it