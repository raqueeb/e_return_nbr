import re

SERIAL_KEYS = {}
INCOME = ["1_employment", "2_rent", "3_agriculture", "4_business", "5_capitalGain",
          "6_financialAssets", "7_otherSources", "8_firmAop", "9_minorSpouse",
          "10_abroad", "11_totalIncome"]
COMPUTATION = ["12_grossTax", "13_rebate", "14_netTax", "15_minimumTax", "16_taxPayable"]
SURCHARGE = {"17": "17a_netWealthSurcharge", "17a": "17a_netWealthSurcharge",
             "17b": "17b_tobaccoSurcharge", "17c": "17c_environmentalSurcharge"}
REST_COMPUTATION = {"18": "18_delayInterest", "19": "19_totalPayable"}
PAYMENTS = ["20_tds", "21_advanceTax", "22_refundAdjustment", "23_taxPaidWithReturn",
            "24_totalPaid", "25_excessPayment", "26_taxExempt"]

for _i, _k in enumerate(INCOME, start=1):
    SERIAL_KEYS[str(_i)] = _k
for _i, _k in enumerate(COMPUTATION, start=12):
    SERIAL_KEYS[str(_i)] = _k
SERIAL_KEYS.update(SURCHARGE)
SERIAL_KEYS.update(REST_COMPUTATION)
for _i, _k in enumerate(PAYMENTS, start=20):
    SERIAL_KEYS[str(_i)] = _k

LINE_RE = re.compile(r"^\s*(\d{1,2}[a-c]?)\.\s+(.+?)\s+(-?[\d][\d,]*(?:\.\d+)?)\s*(?:\(.*\))?\s*$")
IDENTITY_RE = re.compile(r"Name of the Taxpayer:\s*(.+?)\s+TIN:\s*([\d\s]+)", re.I)
STOP_SIG = re.compile(r"(annexure|note:|signature|declaration)", re.I)


def to_int(raw):
    s = raw.replace(",", "").strip()
    try:
        return int(float(s))
    except ValueError:
        return None


def parse_ereturn(pages):
    out = {"identity": {}, "values": {}, "unparsed": []}
    found = 0
    for pno, text in pages:
        for m in IDENTITY_RE.finditer(text):
            out["identity"]["name"] = m.group(1).strip()
            out["identity"]["tin"] = re.sub(r"\s+", "", m.group(2))
        for raw_line in text.splitlines():
            line = raw_line.replace("\u00a0", " ")
            if STOP_SIG.search(line) and found:
                return out
            m = LINE_RE.match(line)
            if not m:
                continue
            serial, label, amount = m.group(1), m.group(2).strip(), m.group(3)
            key = SERIAL_KEYS.get(serial)
            if key is None or key in out["values"]:
                continue
            if not re.search(r"[A-Za-z]{3}", label):
                continue
            num = to_int(amount)
            if num is None:
                continue
            out["values"][key] = {"value": num, "label": label[:90], "page": pno}
            found += 1
    return out


def is_ereturn(text):
    low = (text or "").lower()
    return "statement of income and tax" in low and IDENTITY_RE.search(text or "")
