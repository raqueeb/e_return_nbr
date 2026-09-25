import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from classify import classify_file
from parsers.ereturn import parse_ereturn

EXCEL_EXTS = {".xlsx", ".xls", ".csv"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".webp"}
MAX_CELLS_PER_SHEET = 4000
THIN_TEXT_CHARS = 100


def ocr_available():
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        return True
    except Exception:
        return False


def ocr_image(path):
    from PIL import Image
    import pytesseract
    return pytesseract.image_to_string(Image.open(path), lang="eng+ben")


def extract_excel(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    sheets = {}
    for ws in wb.worksheets:
        cells = {}
        for row in ws.iter_rows():
            for cell in row:
                v = cell.value
                if v is None or v == "":
                    continue
                if isinstance(v, datetime):
                    v = v.isoformat()
                elif isinstance(v, date):
                    v = v.isoformat()
                cells[f"{ws.title}!{cell.coordinate}"] = v
                if len(cells) >= MAX_CELLS_PER_SHEET:
                    break
            if len(cells) >= MAX_CELLS_PER_SHEET:
                break
        if cells:
            sheets[ws.title] = cells
    wb.close()
    return sheets


def extract_pdf(path, allow_ocr):
    import pdfplumber
    pages, tables, method = [], [], "pdf-text"
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            pages.append((i, text))
            for t in page.extract_tables() or []:
                tables.append({"page": i, "rows": t})
        total = sum(len(t.strip()) for _, t in pages)
    if allow_ocr and total < THIN_TEXT_CHARS * max(len(pages), 1):
        try:
            import fitz
            doc = fitz.open(path)
            pages = [(i + 1, doc[i].get_text()) for i in range(len(doc))]
            total = sum(len(t.strip()) for _, t in pages)
            doc.close()
        except Exception:
            pass
        if total < THIN_TEXT_CHARS * max(len(pages), 1):
            try:
                import fitz, pytesseract
                from PIL import Image
                import io
                doc = fitz.open(path)
                ocr_pages = []
                for i in range(len(doc)):
                    pix = doc[i].get_pixmap(dpi=200)
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    ocr_pages.append((i + 1, pytesseract.image_to_string(img, lang="eng+ben")))
                if sum(len(t.strip()) for _, t in ocr_pages) > total:
                    pages = ocr_pages
                    method = "ocr"
                doc.close()
            except Exception:
                method = "pdf-text+needs-ocr"
    return pages, tables, method


def full_text(pages):
    return "\n".join(t for _, t in pages)


def apply_mapping_excel(data, rules):
    import fnmatch
    mapped = {}
    for rule in rules:
        sheet, _, cell = rule.get("cell", "").rpartition("!")
        pat = rule.get("file", "*")
        for _fname, sheets in data.items():
            if not fnmatch.fnmatch(Path(_fname).name, pat):
                continue
            for sname, cells in sheets.items():
                if sname == sheet and cell in cells:
                    mapped[rule["key"]] = {"value": cells[cell], "source": f"{_fname}#{rule['cell']}"}
    return mapped


def apply_mapping_text(text, rules, source):
    import fnmatch
    mapped = {}
    for rule in rules:
        if not fnmatch.fnmatch(Path(source).name, rule.get("file", "*")):
            continue
        m = re.search(rule["regex"], text, re.I | re.M)
        if m:
            raw = m.group(1)
            val = raw.replace(",", "")
            try:
                val = int(float(val))
            except ValueError:
                pass
            mapped[rule["key"]] = {"value": val, "source": source}
    return mapped


def load_rules(path):
    if not path:
        return []
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    return cfg.get("rules", [])


def main():
    ap = argparse.ArgumentParser(description="Extract tax documents (PDF/Excel/images) into staging JSON.")
    ap.add_argument("--docs", required=True, help="Folder with your documents")
    ap.add_argument("--out", required=True, help="Staging output folder (e.g. payload/staging)")
    ap.add_argument("--map", default="", help="Optional mapping.json rules file")
    ap.add_argument("--no-ocr", action="store_true", help="Skip OCR attempts")
    ap.add_argument("--exclude", action="append", default=[], help="Folder names to skip (repeatable)")
    args = ap.parse_args()

    docs = Path(args.docs).resolve()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    allow_ocr = not args.no_ocr and ocr_available()
    rules = load_rules(args.map)
    excel_rules = [r for r in rules if "cell" in r]
    text_rules = [r for r in rules if "regex" in r]

    skips = set(args.exclude) | {"payload", "screenshots", "node_modules", "images"}
    files = []
    for p in sorted(docs.rglob("*")):
        if not p.is_file() or p.name.startswith("~$"):
            continue
        if any(part.startswith(".") or part in skips for part in p.relative_to(docs).parts):
            continue
        if p.suffix.lower() in EXCEL_EXTS | IMAGE_EXTS | {".pdf"}:
            files.append(p)

    inventory, agent_items = [], []
    for path in files:
        rel = str(path.relative_to(docs))
        ext = path.suffix.lower()
        entry = {"file": rel, "type": "?", "method": "-", "items": 0, "confidence": "none", "notes": ""}
        result = {"file": rel, "size": path.stat().st_size}
        try:
            if ext in EXCEL_EXTS:
                data = {rel: extract_excel(path)}
                result.update(type="excel", method="excel-cells", data=data,
                              mapped=apply_mapping_excel(data, excel_rules))
                entry.update(type="excel", method="excel-cells",
                             items=sum(len(v) for v in data[rel].values()), confidence="high")
            elif ext in IMAGE_EXTS:
                if allow_ocr:
                    text = ocr_image(path)
                    result.update(type="image", method="ocr", text=text,
                                  mapped=apply_mapping_text(text, text_rules, rel))
                    entry.update(type="image", method="ocr", items=len(text.split()), confidence="low")
                else:
                    result.update(type="image", method="none", needs_ai="OCR unavailable or disabled")
                    entry.update(type="image", method="none", notes="needs AI vision")
                    agent_items.append((rel, "image file - read with vision"))
            else:
                pages, tables, method = extract_pdf(path, allow_ocr)
                text = full_text(pages)
                ctype, confidence = classify_file(path, text)
                result.update(type=ctype, method=method, pages=len(pages),
                              page_text={str(n): t for n, t in pages}, tables=tables)
                entry.update(type=ctype, method=method, items=len(text.split()), confidence=confidence)
                if ctype == "ereturn":
                    parsed = parse_ereturn(pages)
                    result["ereturn"] = parsed
                    entry["items"] = len(parsed["values"])
                    entry["confidence"] = "high"
                result["mapped"] = apply_mapping_text(text, text_rules, rel)
                if method.endswith("needs-ocr") or (not text.strip() and not tables):
                    result["needs_ai"] = "no extractable text"
                    entry.notes = "needs AI vision"
                    agent_items.append((rel, "no extractable text - read with vision"))
                elif confidence in {"none", "low"} and ctype == "unknown":
                    agent_items.append((rel, "unrecognized format - identify and map manually"))
        except Exception as exc:
            result["error"] = f"{type(exc).__name__}: {exc}"
            entry.notes = f"error: {type(exc).__name__}"
            agent_items.append((rel, f"failed to parse ({type(exc).__name__}) - handle with AI"))

        safe = re.sub(r"[^A-Za-z0-9._-]+", "_", path.stem)[:60]
        (out / f"{safe}.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        inventory.append(entry)

    inv_lines = ["# Document inventory", "",
                 "| File | Type | Method | Items | Confidence | Notes |",
                 "|---|---|---|---|---|---|"]
    for e in inventory:
        inv_lines.append(f"| {e['file']} | {e['type']} | {e['method']} | {e['items']} | {e['confidence']} | {e['notes']} |")
    totals = {"total": len(inventory), "needs_ai": len(agent_items)}
    inv_lines += ["", f"Total files: {totals['total']} · Need AI: {totals['needs_ai']}", ""]
    (out / "inventory.md").write_text("\n".join(inv_lines), encoding="utf-8")

    af = ["# Files for the AI agent", "",
          "Deterministic extraction could not fully handle these. Let the agent read them with vision during the run.", ""]
    for rel, why in agent_items:
        af.append(f"- `{rel}` — {why}")
    af += ["", "Everything else is already in `*.json` in this folder. Review `inventory.md`, then map values with `tools/mapping.example.json` as a guide.", ""]
    (out / "for-agent.md").write_text("\n".join(af), encoding="utf-8")

    print(f"Extracted {len(inventory)} file(s) -> {out}")
    print(f"  inventory.md  for-agent.md  ({len(agent_items)} file(s) need AI)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
