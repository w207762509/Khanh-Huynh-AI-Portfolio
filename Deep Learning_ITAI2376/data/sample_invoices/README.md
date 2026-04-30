# Sample invoices

This repository does **not** ship vendor PDFs by default (licensing/size).

For quick testing with Azure’s prebuilt invoice model, Microsoft publishes sample URLs in the official
Document Intelligence samples (for example, invoice images used in the REST/SDK quickstarts).

Recommended workflow:

1. Download a sample invoice PDF or image to this folder (example filename: `sample_invoice.pdf`).
2. Run the agent from the repository root:

```bash
python main.py --invoice data/sample_invoices/sample_invoice.pdf
```

If you cannot obtain a PDF, use any real invoice you are permitted to use and keep it out of Git
(add the filename to `.gitignore` if needed).
