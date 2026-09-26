# Tax Optimization Guideline — AY 2026-27 (Experimental)

# কর-সাশ্রয় নির্দেশিকা — নির্ণয় বছর ২০২৬-২৭ (পরীক্ষামূলক)

> ⚠ **EXPERIMENTAL / পরীক্ষামূলক.** Researched against Bangladesh tax law (Finance Act 2026) on 26-Sep-2026 and cross-checked against a filed AY 2026-27 computation. Tax rules change **every year**. This is a how-to for the arithmetic — **not tax advice, not investment advice**. The e-Return portal and a qualified practitioner are the final word. **Your mileage will vary.**

> ⚠ এই নথি **পরীক্ষামূলক**। ২৬ সেপ্টেম্বর ২০২৬ তারিখে বাংলাদেশের কর আইন (আর্থিক আইন ২০২৬) অনুযায়ী গবেষণা করে একটি দাখিলকৃত রিটার্নের সাথে মিলিয়ে যাচাই করা হয়েছে। করের নিয়ম **প্রতি বছর** বদলায়। এটি শুধু হিসাবের ধরন বোঝানোর গাইড — **কর-পরামর্শ নয়, বিনিয়োগ-পরামর্শ নয়।** ই-রিটার্ন পোর্টাল ও যোগ্য কর-ব্যক্তিই চূড়ান্ত। **আপনার ফল ভিন্ন হতে পারে।**

**Related files / সম্পর্কিত ফাইল:** [guide §6](Tax-Filing-Guide-Bangladesh.md) · [runbook Phase 2a](NBR-eReturn-Agentic-Entry-Plan.md) · [`tools/optimize.py`](tools/optimize.py) · [`tools/tax-rules.example.json`](tools/tax-rules.example.json)

---

## 🇬🇧 English

### 1. The one rule that matters — Section 78 rebate

```
Rebate = LEAST of:
  (a) 3%  × total taxable income (A)      ← the cap that binds most large taxpayers
  (b) 10% × eligible investment (B)       ← Schedule-5 total, within instrument caps
  (c) Tk 7,50,000                        ← absolute ceiling
```

- **A** excludes tax-exempt income, income taxed at reduced/final rates, and partnership shares — it is close to "total income" on your return.
- **B** is what you legitimately put in Schedule 5 (serials 1–10), each instrument inside its own cap (§4).
- **Finance Act 2026 changed this.** Section 78 of the Income Tax Act 2023 used to say **15% / Tk 10,00,000**; from AY 2026-27 it is **10% / Tk 7,50,000**. Employer certificates, older blogs and older NBR publications still quote the old numbers — the portal computes the new ones.
- The rebate is a **credit against tax payable**, not cash — it cannot push your tax below zero (minimum tax still applies).

### 2. Slab table — AY 2026-27 (general taxpayer)

| Total income (Tk) | Rate |
|---|---|
| 0 – 4,00,000 | 0% |
| 4,00,001 – 7,00,000 | 10% |
| 7,00,001 – 11,00,000 | 15% |
| 11,00,001 – 16,00,000 | 20% |
| 16,00,001 – 36,00,000 | 25% |
| above 36,00,000 | 30% |

Higher nil-band by category (secondary sources — confirm your category on the portal): women & senior citizens (65+) **4,25,000** · persons with disability / third gender **5,00,000** · freedom fighters **5,25,000**.

**Why trust this table:** the 4,00,000 nil-band version reproduces a filed AY 2026-27 gross-tax line **exactly**; the 3,75,000 draft-stage (Finance Bill) version does not. Finance Act 2026 raised the threshold from the bill's 3,75,000 to 4,00,000.

### 3. How much do I still need to invest? (breakeven)

Extra investment increases the rebate **only while term (b) is still the least**:

```
breakeven B* = min(3% × A, 7,50,000) ÷ 10%     (≈ 30% of income for income ≤ 2.5 crore)
```

- Below `B*`: every extra Tk of *eligible* investment adds **10 paisa** of rebate.
- At/above `B*`: line 13 sticks at the cap — extra investment saves **Tk 0**.
- Investments count only if made **inside the income year (by 30 June)**, in the right serial, with documents.

**Synthetic example (not personal):** taxable income 25,00,000 · eligible investment 6,00,000 →
(a) 10% × 6,00,000 = 60,000 · (b) 3% × 25,00,000 = 75,000 · (c) 7,50,000 → rebate **60,000** (R-limited).
Investing 1,50,000 more reaches B* = 7,50,000 → rebate 75,000. Beyond that: Tk 0 saved.

Run `tools/optimize.py` on your own data to get this verdict pre-filled (Phase 2a of the runbook).

### 4. Instrument caps — Schedule 5 (Sixth Schedule Part 3)

| Sch-5 # | Instrument | Cap (AY 2026-27) | Notes |
|---|---|---|---|
| 1 | Life insurance premium | 10% of actual sum assured | own/spouse/minor child; premium payable in Bangladesh |
| 2 | DPS / MSS with a scheduled bank | **Tk 1,20,000 / year** | per year, not balance |
| 3 | Govt securities / sanchayapatra | **Tk 5,00,000** | unit/MF/ETF: the old 5-lakh cap was **removed for new investments** by Finance Act 2026 — but must be held to maturity/prescribed period; early encashment → rebate repaid |
| 4 | Listed shares / stocks | no fixed cap | new investments per Part 3 |
| 5 | PF under PF Act 1925 | no cap | PF must be *recognized* (Finance Act 2026 tightened this) |
| 6 | RPF — self **+ employer** | no cap | claim **both halves** in this one serial |
| 7 | Superannuation fund | no cap | |
| 8 | Benevolent fund / group insurance | no cap | |
| 9 | Zakat | no cap | |
| 10 | Donations / other eligible spend | per Part 3 | approved institutions only — keep the certificate |

Caps are rules, not targets: sitting **at** a cap is fine, claiming **over** it invites scrutiny.

### 5. Other levers (outside Schedule 5)

- **Minimum tax: flat Tk 5,000** anywhere in Bangladesh from AY 2026-27 (first-time filers Tk 1,000). Old 3,000/4,000/5,000 city tiers are gone — `payable = max(slab tax − rebate, 5,000)`.
- **Exempt income lines** (pension, 6th Schedule) must be claimed on line 26 — they shrink the rebate base A and feed your wealth statement.
- **Quarterly advance tax** spreads the March crunch (and the paid-before-30-June instruction matters for deductions too).
- **Surcharge** bites from Tk 4 crore net wealth (rising tiers) — a different chapter; check it if you are in that range.
- Wrong serial = lost rebate. Line 11 must equal the sum of lines 1–10; line 13 must equal the main page.

### 6. Run the engine

```
python tools/optimize.py --baseline payload/ereturn-2025-26.json --deltas payload/deltas-2026-27.json
```

Writes `payload/optimization-report.md` (English + বাংলা): slab recompute vs line 12, rebate verdict with breakeven, per-serial headroom, beyond-Sch-5 checks. Rules live in `tools/tax-rules.example.json` — **edit them every July** after reading that year's Finance Act. The runbook gates the fill on the human acknowledging this report.

### 7. Honesty rails

- Never claim an investment you do not have; every Schedule-5 row needs a document before filing.
- The portal is the source of truth — if line 13 disagrees with your arithmetic, **the portal wins**; investigate, don't override.
- Business income, capital gains, foreign income, prior-year amendments → use a professional (guide §14).
- This file was researched once (Sep 2026). Re-check the sources below every year.

---

## 🇧🇩 বাংলা

### ১. মূল নিয়ম — ধারা ৭৮ রিবেট

```
রিবেট = নিম্নের সবচেয়ে কম:
  (ক) মোট করযোগ্য আয়ের ৩%        ← বেশিরভাগ বড় করদাতার ক্ষেত্রে এটিই সীমা
  (খ) যোগ্য বিনিয়োগের ১০%       ← অনুসূচী-৫-এর মোট, প্রতিটি মাধ্যমের ক্যাপের মধ্যে
  (গ) ৭,৫০,০০০ টাকা              ← সর্বোচ্চ ছাদ
```

- **(ক)**-এ করমুক্ত আয়, অনুকর-হারের/চূড়ান্ত করের আয় ও অংশীদারিত্বের অংশ বাদ — রিটার্নের "মোট আয়"-এর কাছাকাছি।
- **(খ)** হলো অনুসূচী-৫-এ সঠিক সিরিয়ালে দাখিলকৃত বিনিয়োগ (৪ নম্বর অনুচ্ছেদের ক্যাপের মধ্যে)।
- **আর্থিক আইন ২০২৬ এটি বদলেছে।** আয়কর আইন ২০২৩-এর ধারা ৭৮-এ আগে ছিল **১৫% / ১০ লাখ**; ২০২৬-২৭ নির্ণয় বছর থেকে **১০% / ৭,৫০,০০০ টাকা**। পুরনো নিয়মওয়ালা সার্টিফিকেট/ব্লগ/NBR প্রকাশনা এখনো ১৫%/১০ লাখ বলে — পোর্টাল নতুন হিসাব করে।
- রিবেট নগদ টাকা নয় — **করের বিপরীতে ছাড়**; ন্যূনতম কর (৫,০০০ টাকা) তাও প্রযোজ্য থাকে।

### ২. স্ল্যাব সারণি — নির্ণয় বছর ২০২৬-২৭ (সাধারণ করদাতা)

| মোট আয় (টাকা) | হার |
|---|---|
| ০ – ৪,০০,০০০ | ০% |
| ৪,০০,০০১ – ৭,০০,০০০ | ১০% |
| ৭,০০,০০১ – ১১,০০,০০০ | ১৫% |
| ১১,০০,০০১ – ১৬,০০,০০০ | ২০% |
| ১৬,০০,০০১ – ৩৬,০০,০০০ | ২৫% |
| ৩৬,০০,০০০-এর বেশি | ৩০% |

ক্যাটাগরি অনুযায়ী কর-মুক্ত সীমা বেশি (গৌণ সূত্র — পোর্টালে নিজের ক্যাটাগরি যাচাই করুন): নারী ও ৬৫+ বয়স্ক **৪,২৫,০০০** · প্রতিবন্ধী/তৃতীয় লিঙ্গ **৫,০০,০০০** · মুক্তিযোদ্ধা **৫,২৫,০০০**।

**এই সারণি কেন বিশ্বাসযোগ্য:** ৪,০০,০০০ সীমার হিসাব একটি দাখিলকৃত ২০২৬-২৭ রিটার্নের মোট-কর লাইনকে **একদম ঠিকঠাক** পুনরাউৎসার্হ করে; বিল পর্যায়ের ৩,৭৫,০০০ সীমা করে না। আর্থিক আইন ২০২৬-এ সীমাটি বিলের ৩,৭৫,০০০ থেকে ৪,০০,০০০ করা হয়েছে।

### ৩. আরও কত টাকা বিনিয়োগ লাগবে? (ব্রেকইভেন)

বিনিয়োগ বাড়ালে রিবেট তখনই বাড়ে যখন **(খ) এর মান সবচেয়ে কম** থাকে:

```
ব্রেকইভেন B* = min(৩% × আয়, ৭,৫০,০০০) ÷ ১০%     (আয় ২.৫ কোটির নিচে হলে ≈ আয়ের ৩০%)
```

- `B*`-এর নিচে: যোগ্য বিনিয়োগের প্রতি ১ টাকায় **১০ পয়সা** রিবেট।
- `B*`-এ বা তার বেশি: line 13 আটকে থাকে — অতিরিক্ত বিনিয়োগে **০ টাকা** সাশ্রয়।
- বিনিয়োগ গণ্য হবে শুধু **আয়-বছরের মধ্যে (৩০ জুনের আগে)**, সঠিক সিরিয়ালে, কাগজপত্রসহ।

**কাল্পনিক উদাহরণ (ব্যক্তিগত নয়):** করযোগ্য আয় ২৫,০০,০০০ · বিনিয়োগ ৬,০০,০০০ →
(ক) ৬০,০০০ · (খ) ৭৫,০০০ · (গ) ৭,৫০,০০০ → রিবেট **৬০,০০০** (R সীমাবদ্ধ)।
আর ১,৫০,০০০ টাকা বিনিয়োগ করলে B* = ৭,৫০,০০০ পূরণ → রিবেট ৭৫,০০০। তার বেশি কিছু নয়।

নিজের সংখ্যায় এই সিদ্ধান্ত আগেই পেতে চালান `tools/optimize.py` (রানবুক Phase 2a)।

### ৪. ক্যাপ সারণি — অনুসূচী-৫ (ষষ্ঠ অনুসূচীর অংশ ৩)

| Sch-5 # | মাধ্যম | ক্যাপ (২০২৬-২৭) | নোট |
|---|---|---|---|
| ১ | লাইফ ইন্স্যুরেন্স প্রিমিয়াম | আসল সাম অ্যাসিওর্ডের ১০% | নিজ/স্বামী-স্ত্রী/কিশোর সন্তান; প্রিমিয়াম বাংলাদেশে পরিশোধিত হতে হবে |
| ২ | ডিপিএস / এমএসএস (তালিকাভুক্ত ব্যাংক) | **১,২০,০০০ টাকা / বছর** | ব্যালান্স নয় — বছরের জমা |
| ৩ | সরকারি সিকিউরিটি / সঞ্চয়পত্র | **৫,০০,০০০ টাকা** | ইউনিট/MF/ETF: পুরনো ৫-লাখ ক্যাপ **নতুন বিনিয়োগে আর্থিক আইন ২০২৬-এ তুলে নেওয়া হয়েছে** — তবে মেয়াদ/নির্ধারিত সময় পর্যন্ত রাখতে হবে; আগে তুললে রিবেট ফেরত |
| ৪ | তালিকাভুক্ত শেয়ার / স্টক | নির্দিষ্ট ক্যাপ নেই | অংশ ৩ অনুযায়ী নতুন বিনিয়োগ |
| ৫ | পিএফ আইন ১৯২৫-এর পিএফ | ক্যাপ নেই | পিএফ অবশ্যই *স্বীকৃত* হতে হবে (আর্থিক আইন ২০২৬) |
| ৬ | আরপিএফ — নিজ **+ নিয়োগকর্তা** | ক্যাপ নেই | **দুই অংশই** এক সিরিয়ালে দাবি করুন |
| ৭ | সুপারঅ্যানুয়েশন | ক্যাপ নেই | |
| ৮ | বেনিভোলেন্ট ফান্ড / গ্রুপ ইন্স্যুরেন্স | ক্যাপ নেই | |
| ৯ | জাকাত | ক্যাপ নেই | |
| ১০ | দান / অন্যান্য যোগ্য ব্যয় | অংশ ৩ অনুযায়ী | শুধু অনুমোদিত প্রতিষ্ঠান — সার্টিফিকেট রাখুন |

ক্যাপ লক্ষ্য নয় — নিয়ম। ক্যাপে **পৌঁছানো** স্বাভাবিক, ক্যাপ **ছাড়ালে** প্রশ্ন হতে পারে।

### ৫. অনুসূচী-৫-এর বাইরের বিষয়

- **ন্যূনতম কর: ২০২৬-২৭ থেকে সারা দেশে সমতল ৫,০০০ টাকা** (নতুন ফাইলার ১,০০০ টাকা)। আগের ৩/৪/৫ হাজার শহর-ভিত্তিক স্তর বিলুপ্ত — `পরিশোধযোগ্য = max(স্ল্যাব কর − রিবেট, ৫,০০০)`।
- **করমুক্ত আয়ের লাইন** (পেনশন / ষষ্ঠ অনুসূচী) line 26-এ দাবি করুন — এতে রিবেটের ভিত্তি (ক) কমে ও সম্পদ-বিবরণী জোড়া হয়।
- **প্রান্তিক অগ্রিম কর** মার্চের চাপ কমায়; ৩০ জুনের আগে পরিশোধ নিয়মও মনে রাখুন।
- **সারচার্জ** ৪ কোটি টাকা সম্পদ থেকে প্রযোজ্য (ধাপে ধাপে বাড়ে) — সেই পর্যায়ে থাকলে আলাদাভাবে দেখুন।
- ভুল সিরিয়াল = রিবেট নষ্ট। line 11 = ১–১০ নম্বরের যোগফল; line 13 = মূল পৃষ্ঠার রিবেট।

### ৬. ইঞ্জিন চালান

```
python tools/optimize.py --baseline payload/ereturn-2025-26.json --deltas payload/deltas-2026-27.json
```

ফলাফল `payload/optimization-report.md`-এ (ইংরেজি + বাংলা): স্ল্যাব পুনর্হিসাব vs line 12, ব্রেকইভেনসহ রিবেট সিদ্ধান্ত, সিরিয়ালভিত্তিক হেডরুম, Sch-5-এর বাইরের পরীক্ষা। নিয়ম থাকে `tools/tax-rules.example.json`-এ — **প্রতি জুলাই** নতুন আর্থিক আইন পড়ে হালনাগাদ করুন। রানবুক অনুযায়ী ইঞ্জিনের রিপোর্ট মানুষ দেখে জানার আগে ফর্ম পূরণ শুরু হয় না।

### ৭. সততার নিয়ম

- যে বিনিয়োগ নেই তা কখনো দাবি করবেন না; দাখিলের আগে প্রতিটি সিরিয়ালের কাগজ থাকতে হবে।
- পোর্টালই চূড়ান্ত সত্য — line 13 আপনার হিসাবের সাথে মিললেও মিললে না; বোঝো, কিন্তু বদলাবেন না।
- ব্যবসায়িক আয়, মূলধনী লাভ, বিদেশি আয়, আগের বছরের সংশোধন → পেশাদারের সাহায্য নিন (গাইড §১৪)।
- এই ফাইল একবার গবেষণা করা (সেপ্টেম্বর ২০২৬)। প্রতি বছর নিচের সূত্রগুলো দিয়ে যাচাই করুন।

---

## Sources / সূত্র (researched 26-Sep-2026)

1. **PwC Bangladesh — "Finance Act 2026: Key Amendments"** (30-Jun-2026): rebate cut to 10% of investment / Tk 0.75m — <https://www.pwc.com/bd/en/assets/pdfs/budget/finance-act-2026-key-amendments.pdf>
2. **KPMG — "Salient features of Finance Bill 2026"** (14-Jun-2026): rebate = lowest of 3% / 10% / Tk 0.75m — <https://assets.kpmg.com/content/dam/kpmg/bd/pdf/Salient_features_of_Finance_Bill_2026(Tax-and_VAT).pdf>
3. **TNP Legal — "The Finance Act 2026: A Practitioner's Guide"** (Jul-2026): §78 change (down from 15% / Tk 10 lakh), minimum-tax & compliance changes — <https://tnp.legal/wp-content/uploads/2026/07/TNP_Finance_Act_2026_Briefing.pdf>
4. **Income Tax Act 2023 — Sixth Schedule Part 3 (full text)**: instrument caps — insurance 10% of sum assured, DPS 1,20,000, govt securities 5,00,000 — <https://www.taxvatpoint.com/income-tax-act-2023-6th-schedule-part-3/>
5. **Corporate Practice BD — "General tax rebate … Section 78"** (08-Jul-2026): original §78 text (15% / Tk 10 lakh) + Part-3 cap table — <https://www.corporatepracticebd.com/2026/07/general-tax-rebate-in-respect-of.html>
6. **The Daily Star — "Tax season tips: how to claim tax rebates"**: eligible-instrument list & caps as applied — <https://www.thedailystar.net/business/news/tax-season-tips-here-how-you-can-claim-tax-rebates-4019406>
7. **The Daily Star — "Budget 2026-27: why tax rebate policy needs structural overhaul"** (08-Apr-2026): status of caps (Tk 5L govt securities, Tk 1.2L DPS, 10% insurance) before the Finance Act — <https://www.thedailystar.net/business/news/budget-2026-27-why-tax-rebate-policy-needs-structural-overhaul-4146916>
8. **Salient Features of Finance Act 2026** (studylib): flat minimum tax Tk 5,000 / Tk 1,000 new filers; Part-3 amendments (unit/MF/ETF new-investment rule, hold-to-maturity) — <https://studylib.net/doc/28794719/1787225909190>
9. **Awahab & Co — "Finance Act 2026 Client Alert"** (Jul-2026): thresholds rising AY 2026-27→2030-31, rebate cap Tk 7.5 lakh, future 35% top rate — <https://www.awahabco.com/post/finance-act-2026-client-alert-july-2026>
10. **taxpertbd — "How to legally save tax … Section 78"**: worked rebate example under the new formula — <https://taxpertbd.com/how-you-can-save-tax/>
11. **Independent check:** the §2 slab table reproduces a filed AY 2026-27 gross-tax line exactly; the Finance-Bill-era 3,75,000 nil band does not. Bill-stage summaries (e.g., KPMG's 3,75,000 threshold) predate the enacted 4,00,000.

**Yearly routine:** after every budget, re-read that year's Finance Act (bdlaws.minlaw.gov.bd → Finance Act), update `tools/tax-rules.example.json` + this file, and re-run the engine. Slabs, R%, absolute cap and instrument caps can **all** move.
