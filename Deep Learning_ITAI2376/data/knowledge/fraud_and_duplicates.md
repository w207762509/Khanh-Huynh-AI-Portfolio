# Duplicate and anomaly checks (synthetic policy)

Finance teams commonly watch for duplicate payments using:

- Same `VendorName` + same `InvoiceId` + same `InvoiceTotal` within a 30-day window
- Same `InvoiceTotal` with materially different `InvoiceId` but identical line items (possible rescan)

Anomalies worth highlighting:

- `InvoiceDate` in the future
- `DueDate` before `InvoiceTotal` is plausible but `DueDate` far before `InvoiceDate` is suspicious
- Extremely large single-line amounts relative to historical vendor spend (requires context; flag as "review")

This knowledge base is intentionally generic and should be combined with your organization's real controls.
