DROP VIEW IF EXISTS dbo.report_final;
GO

CREATE VIEW dbo.report_final AS
SELECT
    dc.SK_ID_CURR,
    dc.CODE_GENDER,
    dc.FLAG_OWN_CAR,
    dc.FLAG_OWN_REALTY,
    dc.OWN_CAR_AGE,
    dc.CNT_CHILDREN,
    dc.CNT_FAM_MEMBERS,
    dc.NAME_TYPE_SUITE,
    dc.NAME_INCOME_TYPE,
    dc.NAME_EDUCATION_TYPE,
    dc.NAME_FAMILY_STATUS,
    dc.NAME_HOUSING_TYPE,
    dc.OCCUPATION_TYPE,
    dc.ORGANIZATION_TYPE,
    dc.REGION_RATING_CLIENT,
    dc.REGION_RATING_CLIENT_W_CITY,
    dc.AGE_YEARS,
    dc.YEARS_EMPLOYED,

    fa.TARGET,
    fa.NAME_CONTRACT_TYPE,
    fa.AMT_INCOME_TOTAL,
    fa.AMT_CREDIT,
    fa.AMT_ANNUITY,
    fa.AMT_GOODS_PRICE,
    fa.EXT_SOURCE_1,
    fa.EXT_SOURCE_2,
    fa.EXT_SOURCE_3,

    fb.previous_credit_count,
    fb.active_credit_count,
    fb.closed_credit_count,
    fb.overdue_account_count,
    fb.total_credit,
    fb.total_debt,
    fb.total_overdue,
    fb.max_overdue,
    fb.debt_to_credit_ratio,
    fb.active_credit_ratio,

    fbb.total_delinquent_months,
    fbb.pct_months_delinquent,
    fbb.worst_delinquency_status,

    fpc.pos_contract_count,
    fpc.avg_dpd pos_avg_dpd,
    fpc.max_dpd pos_max_dpd,
    fpc.delinquent_month_count pos_delinquent_months,

    fcc.card_contract_count,
    fcc.avg_balance cc_avg_balance,
    fcc.avg_utilization cc_avg_utilization,
    fcc.max_utilization cc_max_utilization,
    fcc.avg_dpd cc_avg_dpd,
    fcc.delinquent_month_count cc_delinquent_months,

    fi.total_instalments,
    fi.late_payment_count,
    fi.late_payment_rate,
    fi.avg_payment_delay,
    fi.max_payment_delay,
    fi.total_underpayment,
    fi.avg_payment_ratio,

    fp.application_count previous_application_count,
    fp.approved_count previous_approved_count,
    fp.refused_count previous_refused_count,
    fp.approval_rate previous_approval_rate,
    fp.refusal_rate previous_refusal_rate,
    fp.avg_previous_credit

FROM dbo.dim_customer dc
LEFT JOIN dbo.fact_applications fa
    ON dc.SK_ID_CURR = fa.SK_ID_CURR
LEFT JOIN dbo.fact_bureau_summary fb
    ON dc.SK_ID_CURR = fb.SK_ID_CURR
LEFT JOIN dbo.fact_bureau_balance_summary fbb
    ON dc.SK_ID_CURR = fbb.SK_ID_CURR
LEFT JOIN dbo.fact_pos_cash_summary fpc
    ON dc.SK_ID_CURR = fpc.SK_ID_CURR
LEFT JOIN dbo.fact_credit_card_summary fcc
    ON dc.SK_ID_CURR = fcc.SK_ID_CURR
LEFT JOIN dbo.fact_installments_summary fi
    ON dc.SK_ID_CURR = fi.SK_ID_CURR
LEFT JOIN dbo.fact_previous_summary fp
    ON dc.SK_ID_CURR = fp.SK_ID_CURR;
GO

SELECT TOP 5 *
FROM dbo.report_final

-- LEFT JOIN used everywhere off dim_customer — every applicant exists in dim_customer,
-- but not every applicant has bureau history, previous applications, or a credit card,
-- so INNER JOIN would silently drop customers with no history. LEFT JOIN keeps all
-- customers and just leaves NULLs where that history doesn't exist.
-- aliased duplicate column names (avg_dpd, avg_balance etc appear in multiple summary
-- tables) get prefixed (pos_avg_dpd, cc_avg_dpd) so Power BI doesn't choke on duplicates.