# Expense Proposal Generator

This repository now includes a small script to generate a Korean "품의서" (proposal) based on information contained in a "지출결의서" PDF.

## Requirements

- Python 3.8+
- `pdfplumber`
- `jinja2`

Install dependencies with:

```bash
pip install pdfplumber jinja2
```

## Usage

```
python scripts/generate_proposal.py expense.pdf output.html
```

The script extracts key fields from `expense.pdf` and writes an HTML proposal to `output.html` using `templates/proposal_template.html`.

Customize the regular expressions in `scripts/generate_proposal.py` if your PDF format differs.
