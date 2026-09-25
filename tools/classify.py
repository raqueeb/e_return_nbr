import re
from pathlib import Path

IDENTITY_SIG = re.compile(r"TIN\s*:\s*[\d\s]{8,}", re.I)
ERETURN_SIG = "statement of income and tax"
BANK_SIG = re.compile(
    r"(trust\s+agra|agra\s+bank|brac\s+bank|dbbl|dutch-bangla|islami\s+bank|"
    r"city\s+bank|ebbl|mutual\s+trust|premiere\s+bank|bangladesh\s+bank|"
    r"bank\s+statement|account\s+statement|e-?statement|statement\s+period|"
    r"a/c\s+name|withdrawal\s+deposit|available\s+balance|closing\s+balance)",
    re.I,
)
SANCHAY_SIG = re.compile(r"(sanchayapatra|sanchay\s+patra|সঞ্চয়পত্র)", re.I)
CHALLAN_SIG = re.compile(r"(challan|e-?tax\s+payment|treasury|government\s+order|ait\s+on\s+car)", re.I)
PENSION_SIG = re.compile(r"pension", re.I)
RENT_SIG = re.compile(r"(house\s+rent|rental\s+agreement|বাসাভাড়া)", re.I)
SALARY_SIG = re.compile(r"(tax\s+deduction\s+certificate|salary\s+certificate|link3|employer)", re.I)

NAME_HINTS = [
    ("ereturn", ("e-return", "ereturn", "return 20")),
    ("sanchayapatra", ("sanchay", "sanchayapatra")),
    ("bank-statement", ("bank", "statement")),
    ("salary-tax-report", ("link3", "salary", "tax report")),
    ("challan", ("challan", "ait")),
    ("pension", ("pension",)),
    ("rent", ("rent",)),
]


def classify_text(text, name=""):
    low = (text or "").lower()
    fname = Path(name).stem.lower() if name else ""
    if ERETURN_SIG in low and IDENTITY_SIG.search(text or ""):
        return "ereturn", "high"
    for ctype, hints in NAME_HINTS:
        if any(h in fname for h in hints):
            return ctype, "medium"
    if SANCHAY_SIG.search(low):
        return "sanchayapatra", "medium"
    if SALARY_SIG.search(low):
        return "salary-tax-report", "medium"
    if BANK_SIG.search(low):
        return "bank-statement", "medium"
    if CHALLAN_SIG.search(low):
        return "challan", "medium"
    if PENSION_SIG.search(low):
        return "pension", "low"
    if RENT_SIG.search(low):
        return "rent", "low"
    if len(low.strip()) > 200:
        return "pdf-text", "low"
    return "unknown", "none"


def classify_file(path, text=""):
    ext = Path(path).suffix.lower()
    if ext in {".xlsx", ".xls", ".csv"}:
        return "excel", "high"
    if ext in {".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".webp"}:
        return "image", "none"
    if ext == ".pdf":
        return classify_text(text, Path(path).name)
    return "unknown", "none"
