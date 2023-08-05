INSERT INTO calaccess_processed_filings_form460scheduleh2itemold (
    filing_id,
    line_item,
    date_repaid_or_forgiven,
    date_of_original_loan,
    recipient_code,
    recipient_committee_id,
    recipient_title,
    recipient_lastname,
    recipient_firstname,
    recipient_name_suffix,
    recipient_city,
    recipient_state,
    recipient_zip,
    recipient_employer,
    recipient_occupation,
    recipient_is_self_employed,
    intermediary_title,
    intermediary_lastname,
    intermediary_firstname,
    intermediary_name_suffix,
    intermediary_city,
    intermediary_state,
    intermediary_zip,
    treasurer_title,
    treasurer_lastname,
    treasurer_firstname,
    treasurer_name_suffix,
    treasurer_city,
    treasurer_state,
    treasurer_zip,
    interest_rate,
    repayment_type,
    amount_repaid_or_forgiven,
    outstanding_principle,
    transaction_id,
    memo_reference_number
)
SELECT
    filing.filing_id,
    item_version.line_item,
    item_version.date_repaid_or_forgiven,
    item_version.date_of_original_loan,
    item_version.recipient_code,
    item_version.recipient_committee_id,
    item_version.recipient_title,
    item_version.recipient_lastname,
    item_version.recipient_firstname,
    item_version.recipient_name_suffix,
    item_version.recipient_city,
    item_version.recipient_state,
    item_version.recipient_zip,
    item_version.recipient_employer,
    item_version.recipient_occupation,
    item_version.recipient_is_self_employed,
    item_version.intermediary_title,
    item_version.intermediary_lastname,
    item_version.intermediary_firstname,
    item_version.intermediary_name_suffix,
    item_version.intermediary_city,
    item_version.intermediary_state,
    item_version.intermediary_zip,
    item_version.treasurer_title,
    item_version.treasurer_lastname,
    item_version.treasurer_firstname,
    item_version.treasurer_name_suffix,
    item_version.treasurer_city,
    item_version.treasurer_state,
    item_version.treasurer_zip,
    item_version.interest_rate,
    item_version.repayment_type,
    item_version.amount_repaid_or_forgiven,
    item_version.outstanding_principle,
    item_version.transaction_id,
    item_version.memo_reference_number
FROM calaccess_processed_filings_form460filing filing
JOIN calaccess_processed_filings_form460filingversion filing_version
ON filing.filing_id = filing_version.filing_id
AND filing.amendment_count = filing_version.amend_id
JOIN calaccess_processed_filings_form460scheduleh2itemversionold item_version
ON filing_version.id = item_version.filing_version_id;
