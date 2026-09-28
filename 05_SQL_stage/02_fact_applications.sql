DROP VIEW IF EXISTS dbo.fact_applications;
GO

CREATE VIEW dbo.fact_applications AS
SELECT
    SK_ID_CURR,
    TARGET,
    NAME_CONTRACT_TYPE,
    AMT_INCOME_TOTAL,
    AMT_CREDIT,
    AMT_ANNUITY,
    AMT_GOODS_PRICE,
    EXT_SOURCE_1,
    EXT_SOURCE_2,
    EXT_SOURCE_3,
    EXT_SOURCE_1_MISSING,
    EXT_SOURCE_2_MISSING,
    EXT_SOURCE_3_MISSING,
    WEEKDAY_APPR_PROCESS_START,
    HOUR_APPR_PROCESS_START,
    DAYS_LAST_PHONE_CHANGE,
    OBS_30_CNT_SOCIAL_CIRCLE,
    DEF_30_CNT_SOCIAL_CIRCLE,
    OBS_60_CNT_SOCIAL_CIRCLE,
    DEF_60_CNT_SOCIAL_CIRCLE,
    AMT_REQ_CREDIT_BUREAU_HOUR,
    AMT_REQ_CREDIT_BUREAU_DAY,
    AMT_REQ_CREDIT_BUREAU_WEEK,
    AMT_REQ_CREDIT_BUREAU_MON,
    AMT_REQ_CREDIT_BUREAU_QRT,
    AMT_REQ_CREDIT_BUREAU_YEAR
FROM dbo.raw_application_train;
GO

-- SELECT TOP 5 *
-- FROM dbo.fact_applications

--Note: I left the FLAG_DOCUMENT_2 → FLAG_DOCUMENT_21 columns out for now — 20 flag columns rarely drive a clean dashboard on their own. If you want a "documents submitted count" diagnostic later, we can add a derived column (SELECT SUM of flags) in a later pass rather than bloating this fact view with 20 raw columns. Your call, we can add them back.