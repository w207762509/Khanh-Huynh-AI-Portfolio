# Invoice validation tolerances (synthetic policy)

Accounts payable should treat small rounding differences as normal when comparing OCR-extracted
numbers to printed totals.

- Currency rounding tolerance: **USD 0.02** (two cents) between computed subtotals and stated totals.
- If `TotalTax` is missing, do not assume tax is zero; flag the field as missing and request a human review.
- If line item `Amount` is missing but `Quantity` and `Unit` price exist, compute `Amount` as `Quantity * UnitPrice`
  only when both values are present and credible.

When OCR confidence is low for `InvoiceTotal`, prioritize human verification even if arithmetic checks pass.
