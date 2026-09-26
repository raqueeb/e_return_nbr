"""Tax Optimization Engine (EXPERIMENTAL / পরীক্ষামূলক).

Rules research-validated for AY 2026-27 against Bangladesh Finance Act 2026 and a
filed computation — but tax law changes every year. This is arithmetic on your own
numbers, NOT tax or investment advice. The e-Return portal is the source of truth:
verify every figure before filing. Your mileage may vary.

Key law (verify yearly, sources in tax-rules.example.json "sources"):
  - Slabs: Finance Act 2026 general-taxpayer bands for AY 2026-27
    (nil up to 4,00,000; then 3L@10%, 4L@15%, 5L@20%, 20L@25%, rest 30%).
  - Rebate: Section 78, Income Tax Act 2023, as amended by Finance Act 2026
    = least of (3% of total income, 10% of eligible investment, Tk 7,50,000).
    Before Finance Act 2026 it was 15% / Tk 10,00,000 — documents quoting those
    predate the amendment.
Background and full how-to: tax_optimize.md (repo root).
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path


def deep_merge(base, patch):
    out = dict(base)
    for k, v in patch.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def get_path(d, path, default=0):
    cur = d
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur if cur is not None else default


def slab_tax(total, slabs):
    # Progressive bands from rules["slabs"] — Finance Act 2026 AY 2026-27 bands
    # reproduce a filed line-12 exactly (the 3,75,000 nil-band variant does not).
    tax, prev = 0.0, 0
    for band in slabs:
        cap, rate = band["up_to"], band["rate"]
        if cap is None:
            if total > prev:
                tax += (total - prev) * rate
            break
        if total > prev:
            tax += (min(total, cap) - prev) * rate
        prev = cap
        if total <= cap:
            break
    return int(round(tax))


def marginal_rate(total, slabs):
    prev = 0
    for band in slabs:
        cap = band["up_to"]
        if cap is None or total <= cap:
            return band["rate"], band["label"]
        prev = cap
    return slabs[-1]["rate"], slabs[-1]["label"]


def fmt(n):
    if n is None:
        return "-"
    try:
        s = str(int(round(float(n))))
    except (TypeError, ValueError):
        return str(n)
    neg = s.startswith("-")
    s = s.lstrip("-")
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ",".join(parts) + "," + tail
    return ("-" if neg else "") + s


def analyze(data, rules):
    income = get_path(data, "incomeLines.11_totalIncome")
    investment = get_path(data, "schedule5_investment.11_totalInvestment")
    if not investment:
        serial_keys = [e["key"] for e in rules["schedule5"]]
        investment = sum(get_path(data, f"schedule5_investment.{k}") for k in serial_keys)
    # Section 78 rebate (ITA 2023, amended by Finance Act 2026 for AY 2026-27):
    # least of 3% of total income, R% of eligible investment, absolute cap Tk 7,50,000.
    # Values live in tax-rules.example.json — confirm on the portal each year.
    rebate_rules = rules["rebate"]
    R, cap_pct, abs_cap = rebate_rules["R"], rebate_rules["incomeCapPct"], rebate_rules["absoluteCap"]
    cap_income = int(round(cap_pct * income))
    term_R, term_income, term_abs = int(round(R * investment)), cap_income, abs_cap
    computed_rebate = min(term_R, term_income, term_abs)
    claimed_rebate = get_path(data, "taxComputation.13_rebate")
    # Breakeven = point where R% x investment catches the better of the two caps.
    breakeven = int(round(min(cap_income, abs_cap) / R)) if R else None
    binding = min([("R% x investment", term_R), ("3% x total income", term_income),
                   (f"Tk {fmt(abs_cap)} absolute cap", term_abs)], key=lambda t: t[1])[0]
    cap_bound = term_income <= term_R and term_income <= term_abs
    headroom = max(0, breakeven - investment) if breakeven else 0
    extra_rebate = max(0, min(term_income, term_abs) - computed_rebate)
    gross_tax_line = get_path(data, "taxComputation.12_grossTax")
    slab = slab_tax(income, rules["slabs"])
    rate, band_label = marginal_rate(income, rules["slabs"])
    payable = get_path(data, "taxComputation.16_taxPayable")
    min_tax = rules.get("minimumTax", 5000)

    sch5 = []
    for entry in rules["schedule5"]:
        sch5.append({
            "sl": entry["sl"], "instrument": entry["instrument"],
            "claimed": get_path(data, f"schedule5_investment.{entry['key']}"),
            "cap": entry["cap"], "capNote": entry.get("capNote"),
        })
    emp_rpf = get_path(data, "schedule1_employment.11_employerRPF")
    rpf_claimed = get_path(data, "schedule5_investment.6_selfEmployerRPF")

    checks = []
    exempt_claimed = get_path(data, "taxPayments.26_taxExempt")
    sch1_exempt = get_path(data, "schedule1_employment.14_exempt6thSchedule")
    gratuity = get_path(data, "schedule1_employment.4_gratuityPension")
    if exempt_claimed == 0 and (sch1_exempt > 0 or gratuity > 0):
        checks.append("exempt")
    rent_value = get_path(data, "schedule2_rent.6_totalRentalValue")
    repair = get_path(data, "schedule2_rent.7a_repairCollection")
    if rent_value > 0 and repair < rules["misc"]["repairDeductionPct"] * rent_value:
        checks.append("rent")
    if 0 < payable < min_tax:
        checks.append("minimum")
    tds = get_path(data, "taxPayments.20_tds")
    advance = get_path(data, "taxPayments.21_advanceTax")
    if tds + advance < payable and payable > 0:
        checks.append("advance")

    return {
        "assessmentYear": rules.get("assessmentYear", "?"),
        "income": income, "investment": investment, "R": R,
        "term_R": term_R, "term_income": term_income, "term_abs": term_abs,
        "computed_rebate": computed_rebate, "claimed_rebate": claimed_rebate,
        "breakeven": breakeven, "binding": binding, "cap_bound": cap_bound,
        "headroom": headroom, "extra_rebate": extra_rebate,
        "slab_tax": slab, "gross_tax_line": gross_tax_line,
        "rate": rate, "band_label": band_label,
        "payable": payable, "min_tax": min_tax,
        "sch5": sch5, "emp_rpf": emp_rpf, "rpf_claimed": rpf_claimed,
        "checks": checks, "rules": rules,
    }


def verdict_lines(a):
    if a["cap_bound"]:
        return [
            f"BINDING CAP: the 3% rule limits your rebate to {fmt(a['term_income'])} Tk.",
            f"Extra Schedule-5 investment saves Tk 0 until total investment drops below {fmt(a['breakeven'])} Tk (it is currently {fmt(a['investment'])}).",
            f"Breakeven = (3% x income) / R% = {fmt(a['breakeven'])} Tk at R={int(a['R']*100)}%.",
        ]
    return [
        f"HEADROOM: your rebate is limited by R% x investment ({fmt(a['term_R'])} Tk).",
        f"Invest up to {fmt(a['headroom'])} Tk more in Schedule-5 to reach the max rebate of {fmt(min(a['term_income'], a['term_abs']))} Tk.",
        f"Breakeven = (3% x income) / R% = {fmt(a['breakeven'])} Tk at R={int(a['R']*100)}%.",
    ]


def render_en(a):
    L = [f"# Tax Optimization Report — AY {a['assessmentYear']}",
         "",
         f"Generated by `tools/optimize.py` on {date.today().isoformat()} · merged locally from baseline + deltas · **math-based headroom only — not investment advice**.",
         "",
         "> ⚠ **EXPERIMENTAL / পরীক্ষামূলক** — rules researched against Bangladesh Finance Act 2026 "
         "(Section 78: 3% / 10% / Tk 7,50,000) for AY 2026-27. Law changes yearly — verify every "
         "figure on the e-Return portal. Background: `tax_optimize.md`. Not tax advice.",
         "",
         "## 🇬🇧 English", "",
         "### 1. Slab position", "",
         f"- Total income: **{fmt(a['income'])} Tk**",
         f"- Marginal rate: **{int(a['rate']*100)}%** (band: {a['band_label']})",
         f"- Slab tax recomputed: {fmt(a['slab_tax'])} Tk · line 12 on your data: {fmt(a['gross_tax_line'])} Tk"
         + (" → **MATCH**" if a['slab_tax'] == a['gross_tax_line'] else " → **MISMATCH — verify line 12**"),
         "",
         "### 2. Rebate verdict", "",
         f"- Qualifying investment (Sch-5 line 11): {fmt(a['investment'])} Tk",
         f"- (a) R% x investment = {int(a['R']*100)}% x {fmt(a['investment'])} = **{fmt(a['term_R'])}**",
          f"- (b) 3% x total income = **{fmt(a['term_income'])}**",
          f"- (c) absolute cap Tk {fmt(a['term_abs'])} = **{fmt(a['term_abs'])}**",
         f"- Computed rebate = min(a,b,c) = **{fmt(a['computed_rebate'])}** Tk · claimed line 13 = {fmt(a['claimed_rebate'])} Tk"
         + (" → MATCH" if a['computed_rebate'] == a['claimed_rebate'] else " → MISMATCH — verify line 13"),
         "", "**Verdict:**", ""]
    L += [f"  - {s}" for s in verdict_lines(a)]
    L += ["", "### 3. Schedule-5 category headroom", "",
          "| Sl | Instrument | Claimed (Tk) | Cap | Status |", "|---|---|---|---|---|"]
    for e in a["sch5"]:
        cap = fmt(e["cap"]) if e["cap"] is not None else (e.get("capNote") or "verify/yearly")
        if e["cap"] is not None:
            status = "unused room" if e["cap"] > e["claimed"] else "at/over cap — verify"
        elif e.get("capNote"):
            status = "per rule note — verify yearly"
        else:
            status = "not checked — fill cap in tax-rules"
        L.append(f"| {e['sl']} | {e['instrument']} | {fmt(e['claimed'])} | {cap} | {status} |")
    L += ["", "- Each extra Tk in Schedule-5 saves **{}%** in tax — but only until the breakeven in §2 (currently {}).".format(
        int(a["R"] * 100), "reached — extra investment saves nothing" if a["cap_bound"] else "not reached")]
    if a["emp_rpf"] > 0 and a["rpf_claimed"] == 0:
        L.append(f"- ⚠ Employer RPF ({fmt(a['emp_rpf'])} Tk) is in salary but **not claimed** in Sch-5 line 6.")
    elif a["emp_rpf"] > 0 and a["rpf_claimed"] == a["emp_rpf"]:
        L.append(f"- ⚠ Sch-5 line 6 ({fmt(a['rpf_claimed'])} Tk) equals the employer contribution alone — confirm **your own** RPF contribution is included too.")
    L += ["", "### 4. Beyond Schedule 5", ""]
    ck = a["checks"]
    if "exempt" in ck:
        L.append("- ⚠ Exempt income (pension / 6th Schedule) shows 0 on line 26 while salary data suggests otherwise — claim it; it also feeds sources-of-fund.")
    if "rent" in ck:
        L.append("- ⚠ Schedule-2 repair deduction looks below the 25% guide value — verify admissible deductions with receipts.")
    if "minimum" in ck:
        L.append(f"- ℹ Computed payable is below the Tk {fmt(a['min_tax'])} minimum tax — the floor applies (payable = max(slab - rebate, minimum)).")
    if "advance" in ck:
        L.append("- ℹ TDS + advance tax < payable — consider quarterly advance tax to avoid March lump-sum pressure and the Q1 incentive.")
    if not ck:
        L.append("- No issues detected in the four beyond-Schedule-5 checks.")
    L += ["", "### 5. Honesty rails", "",
          "- ⚠ **Experimental tool** — rules researched against Finance Act 2026, but law changes yearly; the portal is the source of truth.",
          "- This report is arithmetic on your own numbers — **not investment advice**.",
          "- Never claim an investment you do not have; every row needs a document before filing.",
          "- Caps, slabs and R% change yearly — verify against the Finance Act / NBR portal.",
          "- Investments count only if made before 30 June (income-year end).",
          ""]
    return "\n".join(L)


def render_bn(a, en):
    L = ["", "---", "", "## 🇧🇩 বাংলা", "",
         f"### ১. স্ল্যাব অবস্থা", "",
         f"- মোট আয়: **{fmt(a['income'])} টাকা**",
         f"- মার্জিনাল রেট: **{int(a['rate']*100)}%**",
         f"- স্ল্যাব কর হিসাব (নতুন): {fmt(a['slab_tax'])} টাকা · আপনার ডেটার line 12: {fmt(a['gross_tax_line'])} টাকা"
         + (" → **মিলে যাচ্ছে**" if a['slab_tax'] == a['gross_tax_line'] else " → **মিলছে না — line 12 যাচাই করুন**"),
         "",
         "### ২. রিবেট সিদ্ধান্ত", "",
         f"- যোগ্য বিনিয়োগ (Sch-5 line 11): {fmt(a['investment'])} টাকা",
          f"- (a) R% × বিনিয়োগ = {fmt(a['term_R'])} · (b) আয়ের 3% = {fmt(a['term_income'])} · (c) সর্বোচ্চ ক্যাপ {fmt(a['term_abs'])} = {fmt(a['term_abs'])}",
         f"- গণনাকৃত রিবেট = {fmt(a['computed_rebate'])} টাকা · line 13 = {fmt(a['claimed_rebate'])} টাকা"
         + (" → মিলে যাচ্ছে" if a['computed_rebate'] == a['claimed_rebate'] else " → মিলছে না — যাচাই করুন"),
         "", "**সিদ্ধান্ত:**", ""]
    if a["cap_bound"]:
        L += ["  - **৩% ক্যাপ কার্যকর** — রিবেট সর্বোচ্চ " + fmt(a["term_income"]) + " টাকা।",
              f"  - ৩% ক্যাপের কারণে আর বেশি Sch-5 বিনিয়োগ করলে **০ টাকা** সাশ্রয় হবে।",
              f"  - ব্রেকইভেন = {fmt(a['breakeven'])} টাকা (বর্তমান বিনিয়োগ {fmt(a['investment'])} টাকা)।"]
    else:
        L += ["  - **শূন্যপূরণের সুযোগ আছে** — রিবেট এখন R% × বিনিয়োগ দিয়ে সীমাবদ্ধ।",
              f"  - সর্বোচ্চ রিবেট {fmt(min(a['term_income'], a['term_abs']))} টাকায় পৌঁছাতে আর {fmt(a['headroom'])} টাকা বিনিয়োগ করা যেতে পারে।",
              f"  - ব্রেকইভেন = {fmt(a['breakeven'])} টাকা।"]
    L += ["", "### ৩. Sch-5 ক্যাটাগরি হেডরুম", "",
          "| ক্রম | মাধ্যম | দাবি (টাকা) | ক্যাপ | অবস্থা |", "|---|---|---|---|---|"]
    inst_bn = {"Life insurance premium": "লাইফ ইন্স্যুরেন্স প্রিমিয়াম", "Deposit Pension Scheme (DPS)": "ডিপিএস",
               "Govt securities / sanchayapatra / MF / ETF": "সরকারি সিকিউরিটি / সঞ্চয়পত্র",
               "Listed shares / mutual funds": "তালিকাভুক্ত শেয়ার / মিউচুয়াল ফান্ড",
               "PF under PF Act 1925": "পিএফ অ্যাক্ট ১৯২৫", "Self + employer contribution to RPF": "নিজ + নিয়োগকর্তা RPF",
               "Superannuation": "সুপারঅ্যানুয়েশন", "Benevolent fund": "বেনিভোলেন্ট ফান্ড",
               "Zakat": "জাকাত", "Other qualifying investments": "অন্যান্য যোগ্য বিনিয়োগ"}
    for e in a["sch5"]:
        cap = fmt(e["cap"]) if e["cap"] is not None else (e.get("capNote") or "যাচাই প্রয়োজন")
        if e["cap"] is not None:
            status = "জায়গা আছে" if e["cap"] > e["claimed"] else "সীমায় — যাচাই"
        elif e.get("capNote"):
            status = "নোট অনুযায়ী — বছরে যাচাই"
        else:
            status = "ক্যাপ নেই — rules ফাইলে যোগ করুন"
        L.append(f"| {e['sl']} | {inst_bn.get(e['instrument'], e['instrument'])} | {fmt(e['claimed'])} | {cap} | {status} |")
    L += ["", f"- Sch-5-এ প্রতি ১০০ টাকা বিনিয়োগে সাশ্রয় **{int(a['R']*100)}%** — তবে ব্রেকইভেনের আগে পর্যন্ত" + (" (এখনই পৌঁছে গেছে — সুবিধা শূন্য)" if a["cap_bound"] else "।")]
    if a["emp_rpf"] > 0 and a["rpf_claimed"] == 0:
        L.append(f"- ⚠ নিয়োগকর্তার RPF ({fmt(a['emp_rpf'])} টাকা) বেতনে আছে কিন্তু Sch-5 line 6-এ দাবি করা **নেই**।")
    elif a["emp_rpf"] > 0 and a["rpf_claimed"] == a["emp_rpf"]:
        L.append(f"- ⚠ Sch-5 line 6 ({fmt(a['rpf_claimed'])} টাকা) শুধু নিয়োগকর্তার অংশের সমান — **আপনার নিজের** অংশও আছে কি না দেখুন।")
    L += ["", "### ৪. Sch-5-এর বাইরের পরীক্ষা", ""]
    ck = a["checks"]
    if "exempt" in ck:
        L.append("- ⚠ করমুক্ত আয় (পেনশন / ৬ষ্ঠ অনুসূচী) line 26-এ শূন্য দেখাচ্ছে কিন্তু বেতনের তথ্য অন্যরকম বলছে — দাবি করুন।")
    if "rent" in ck:
        L.append("- ⚠ Sch-2 মেরামত ছাড় ২৫% গাইডের নিচে মনে হচ্ছে — রসিদসহ যাচাই করুন।")
    if "minimum" in ck:
        L.append(f"- ℹ পরিশোধযোগ্য টাকা {fmt(a['min_tax'])} ন্যূনতম করের নিচে — ন্যূনতম কর প্রযোজ্য হবে।")
    if "advance" in ck:
        L.append("- ℹ TDS + অগ্রিম কর < পরিশোধযোগ্য — মার্চের চাপ এড়াতে প্রতি প্রান্তিক অগ্রিম কর বিবেচনা করুন।")
    if not ck:
        L.append("- চারটি পরীক্ষায় কোনো সমস্যা পাওয়া যায়নি।")
    L += ["", "### ৫. সততার নিয়ম", "",
          "- ⚠ **পরীক্ষামূলক টুল** — Finance Act 2026 অনুযায়ী যাচাই করা হলেও আইন বছরে বদলায়; পোর্টালই চূড়ান্ত সত্য।",
          "- এই রিপোর্ট শুধু আপনার নিজের সংখ্যার গাণিতিক হিসাব — **বিনিয়োগ পরামর্শ নয়**।",
          "- না থাকা বিনিয়োগ কখনো দাবি করবেন না; জমা দেওয়ার আগে প্রতিটি দাবির কাগজ থাকতে হবে।",
          "- ক্যাপ, স্ল্যাব আর R% প্রতি বছর বদলায় — আর্থিক আইন / NBR থেকে যাচাই করুন।",
          "- বিনিয়োগ গণ্য হবে যদি ৩০ জুনের আগে করা হয়।",
          ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="EXPERIMENTAL tax optimization report from baseline + deltas (offline, no API).")
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--deltas", required=True)
    ap.add_argument("--rules", default=str(Path(__file__).with_name("tax-rules.example.json")))
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    baseline = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
    deltas = json.loads(Path(args.deltas).read_text(encoding="utf-8"))
    rules = json.loads(Path(args.rules).read_text(encoding="utf-8"))
    data = deep_merge(baseline, deltas)

    a = analyze(data, rules)
    report = render_en(a) + render_bn(a, None)
    out = Path(args.out) if args.out else Path(args.baseline).parent / "optimization-report.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")

    print(f"Total income: {fmt(a['income'])} | marginal {int(a['rate']*100)}% | slab tax {fmt(a['slab_tax'])} vs line12 {fmt(a['gross_tax_line'])}")
    print(f"Rebate: computed {fmt(a['computed_rebate'])} vs claimed {fmt(a['claimed_rebate'])} | binding: {a['binding']}")
    print("VERDICT:", "3% cap BINDING - extra Sch-5 saves Tk 0" if a["cap_bound"] else f"HEADROOM - up to {fmt(a['headroom'])} Tk more investable")
    print(f"Report: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
