SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH,
    IS_NULLABLE,
    ORDINAL_POSITION
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME IN (
    'raw_application_train',
    'raw_bureau',
    'raw_bureau_balance',
    'raw_credit_card_balance',
    'raw_installments_payments',
    'raw_pos_cash_balance',
    'raw_previous_application'
)
ORDER BY TABLE_NAME, ORDINAL_POSITION;