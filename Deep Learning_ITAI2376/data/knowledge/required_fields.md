# Minimum invoice fields for processing (synthetic policy)

For an invoice to be considered "processable" without escalation, the extraction should include:

- Vendor identity: `VendorName` or `VendorAddressRecipient`
- Document reference: `InvoiceId` or `InvoiceNumber` (either is acceptable)
- Dates: `InvoiceDate` and ideally `DueDate`
- Totals: `InvoiceTotal` and either `SubTotal` or itemized `Items`

If `Items` exist, AP expects at least description and amount for each material line.

If PII such as full bank account numbers appear, redact in downstream systems; this agent should not
copy sensitive banking details into external tickets.
