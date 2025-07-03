import re
import sys
from pathlib import Path

import pdfplumber
from jinja2 import Environment, FileSystemLoader


def parse_expense_pdf(pdf_path):
    """Parse expense data from a given pdf file.

    Parameters
    ----------
    pdf_path : str or Path
        Path to the expense settlement pdf.

    Returns
    -------
    dict
        Parsed information with keys like 'gwan', 'hang', 'mok',
        'account', 'description', 'amount', and 'vendor'.
    """
    result = {
        "gwan": None,
        "hang": None,
        "mok": None,
        "account": None,
        "description": None,
        "amount": None,
        "vendor": None,
    }

    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

    # Simple regex based extraction. Adjust patterns according to actual pdf.
    patterns = {
        "gwan": r"관[:\s]*([^\n]+)",
        "hang": r"항[:\s]*([^\n]+)",
        "mok": r"목[:\s]*([^\n]+)",
        "account": r"계정과목[\(세목\)]*[:\s]*([^\n]+)",
        "description": r"적요[:\s]*([^\n]+)",
        "amount": r"금액[:\s]*([\d,]+)",
        "vendor": r"거래처[:\s]*([^\n]+)",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            result[key] = match.group(1).strip()

    return result


def render_template(data, output_path):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("proposal_template.html")
    rendered = template.render(**data)
    Path(output_path).write_text(rendered, encoding="utf-8")


def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_proposal.py <input.pdf> <output.html>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = sys.argv[2]

    data = parse_expense_pdf(pdf_path)
    render_template(data, output_path)
    print(f"Proposal saved to {output_path}")


if __name__ == "__main__":
    main()
