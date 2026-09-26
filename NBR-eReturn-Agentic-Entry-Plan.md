# NBR e-Return Agentic Entry Plan (template)

### [Rakibul Hassan](https://aiwithr.github.io/about/) with the help of OpenCode

**Portal:** https://etaxnbr.gov.bd (+ `ledger.etaxnbr.gov.bd` via SSO)  
**Tool:** Playwright MCP (in opencode)  
**Strategy:** The portal keeps a **running draft**. Open it → compare each screen against **merged JSON** (LY baseline + AY deltas) → patch differences → **Save draft only**  
**Human does:** login/OTP · balance payment + s.173 challan · final review · **Submit**

> **Shareable:** this runbook has no personal data.  
> **Private:** `payload/*.json`, any correction worksheet, screenshots, and `run-report.md` hold real figures — do not share those.

Concepts, slabs, and form help: see `Tax-Filing-Guide-Bangladesh.md`.

---

## 0. Safety rails (non-negotiable)

1. **Never** click `Pay Now`, `Submit Return`, `Proceed to online return`, `Reset Calculation`, or any bank/payment redirect.
2. **Never** delete or re-add an existing ledger claim (the UI itself warns: *“Claim already exists … delete first”* — do neither).
3. **Never** write password, OTP, or card/mobile-banking PIN into files, chat, or screenshots.
4. **Domain allowlist:** only `etaxnbr.gov.bd` + `ledger.etaxnbr.gov.bd` (and their asset CDNs). The ledger opens automatically from the return via session handoff — that navigation is expected. If a payment gateway page opens, stop and hand back.
5. **Save as draft** after every section (and before any long pause).
6. **One section per pass** — snapshot → fill → verify → screenshot → save.
7. If on-screen total ≠ expected (§6), **stop**, screenshot, report — do not force-through.
8. Open items in `payload/deltas-2026-27.json` → `openItems[]` must be listed in `run-report.md` before you finish (user may still submit manually after fixing).

---

## 1. One-time setup

### 1a. Playwright MCP

`opencode.json` in this folder already contains:

```json
"mcp": {
  "playwright": {
    "type": "local",
    "command": ["npx", "-y", "@playwright/mcp@latest",
                "--browser", "chromium",
                "--caps", "vision,storage,testing",
                "--user-data-dir", ".playwright-profile"],
    "enabled": true,
    "timeout": 30000
  }
}
```

- **Quit and restart opencode** after first save of `opencode.json`.
- Confirm tools exist: prompt should expose `browser_navigate`, `browser_snapshot`, `browser_fill_form`, `browser_type`, `browser_click`, `browser_select_option`, `browser_take_screenshot`, `browser_wait_for`, `browser_storage_state`.
- **First-run browser install** (otherwise navigate fails with “chrome-for-testing is not installed”):
  ```
  npx @playwright/mcp install-browser chrome-for-testing
  ```
  ~200 MB one-time download; no restart needed after it completes.

### 1b. First-run browser

1. Agent: `browser_navigate` → `https://etaxnbr.gov.bd` → landing page (hash `#/landing-page`).
2. Click the **eReturn** tile → dialog “Are you registered in eReturn System?” → **I am already registered** → `#/auth/sign-in`.
3. **Pause — human:** type TIN + password in the browser window (no captcha on the form; complete OTP if prompted) → “logged in”.
4. The wizard opens at `#/user-panel/assessment/regular-return` (or **auto-resumes the last-visited section** of an existing draft).
5. Optional: `browser_storage_state` → save `.playwright-profile/login.json` (cookies only) for faster resume.

### 1c. Data files

| File | Role |
|------|------|
| `payload/ereturn-2025-26.json` | Baseline — full last-year (LY) filed return |
| `payload/deltas-2026-27.json` | Current AY corrections / patches |
| `payload/field-map.md` | Filled during recon |
| Optional private worksheet | Human-readable source of truth (not required by agent) |

*Your filenames may differ — keep the same roles: baseline + deltas + field map.*

**Merge rule:** `value = delta[key] ?? baseline[key]`  
Exception: assessment year, income year end, and period labels always come from the **current** AY in deltas (`incomeYearEnd` / `assessmentYear`).

Build both JSONs from **your** last-year submitted PDF and **your** current-year documents/worksheet before Phase 1 — start with the document extractor (§1d) instead of typing values by hand. The agent never invents amounts.

### 1d. Documents → JSON (`tools/extract.py`)

Put everything you downloaded — last year's e-Return, bank statements, sanchayapatra PDFs, pension/rent papers, employer tax report, challans, car AIT, your calculation Excel — into one folder, then:

```
pip install -r tools/requirements.txt
python tools/extract.py --docs /path/to/your-documents --out payload/staging --map tools/mapping.json
```

- Writes `payload/staging/*.json` (one per file), `inventory.md` (type + confidence per file), `for-agent.md` (files that need AI vision).
- e-Return PDFs are parsed line-by-line into baseline keys (lines 1–26); Excel becomes a cell inventory (`Sheet!C7` → value); other PDFs keep per-page text + tables for mapping.
- Copy `tools/mapping.example.json` → `tools/mapping.json` and edit the rules for *your* files (Excel `sheet!cell` → key, PDF regex → key).
- Uncertain values are flagged, never guessed. The extractor only **reads** local files — it never uploads anything.

Review the staging output, then assemble `payload/` baseline + deltas from §1c.

---

## 2. Phases

| Phase | Name | Gate to next |
|-------|------|----------------|
| 0 | Preflight + login | MCP tools work; human logged in |
| 1 | Baseline JSON sanity | Spot-check LY totals vs PDF |
| 2 | Delta JSON sanity | Diff table printed |
| 2a | Tax optimization | Human has seen `optimization-report.md` |
| 3 | Recon map | `field-map.md` covers all keys (or unmapped listed) |
| 4 | Prefill + patch + save | Section checklist 100% |
| 5 | Verify totals | §6 invariants all pass or explicit mismatch report |
| 6 | Stop + handoff | `run-report.md` written; draft saved |

**Do not start Phase 4 until Phase 3 map exists. Do not fill before the Phase 2a report has been shown to the human.**

---

## 2a. Phase 2a — Tax Optimization Engine (before fill)

An offline rules engine analyzes the merged data against current slabs and surfaces overlooked opportunities **before any portal editing starts**:

```
python tools/optimize.py --baseline payload/ereturn-2025-26.json --deltas payload/deltas-2026-27.json
```

Output: `payload/optimization-report.md` (bilingual EN + বাংলা). The agent must **show the report to the human and wait** — suggestions may change the deltas.

Formulas, caps and research sources: [`tax_optimize.md`](tax_optimize.md) (**experimental** — researched for AY 2026-27; re-verify each year).

What it computes (rules live in `tools/tax-rules.example.json`, edit yearly):

1. **Slab position** — marginal rate + recomputed slab tax vs line 12 (sanity check)
2. **Rebate verdict** — breakeven `(3% × income) / R%`; if the 3% cap binds, extra Schedule-5 investment saves **Tk 0** and the report says so
3. **Schedule-5 headroom** — per-serial claimed vs cap (caps ship as `null` → "verify yearly", never invented) + RPF both-halves check
4. **Beyond Sch-5 checks** — unclaimed exempt/pension line 26, Sch-2 repair deduction, minimum-tax floor, advance-tax incentive
5. **Honesty rails** — math only, not investment advice; document every claim; investments count before 30 June

**Gate:** human acknowledges the report → may patch deltas with accepted suggestions → Phase 3.

---

## 3. Phase 3 — Recon (no edits)

**Live-verified wizard structure** (walked read-only 25-Sep-2026 — your session should re-confirm):

| # | Route | Section |
|---|-------|---------|
| 1 | `#/user-panel/assessment/regular-return` | Assessment info (scheme, AY/IY, resident, heads-of-income checkboxes) |
| 2 | `#/user-panel/additional-information` | Rebate trigger, IT-10B triggers, house-property area |
| 3 | `#/user-panel/employment` | Income ▸ Employment (Sch-1) |
| 4 | `#/user-panel/financial-assets` | Income ▸ Financial Assets (sanchay + bank tabs) |
| 5 | `#/user-panel/rent` | Income ▸ Rent (Sch-2) |
| 6 | `#/user-panel/tax-exempted-income` | Income ▸ Tax Exempted |
| 7 | `#/user-panel/rebate` | Sch-5 investment rebate |
| 8 | `#/user-panel/expenditure` | IT-10BB lifestyle |
| 9 | `#/user-panel/assets-and-liabilities` | IT-10B wealth (has `Import and Autofill`) |
| 10 | `#/user-panel/tax-and-payment` | Tax computation + payments + `Update Tax Payment Status` |
| 11 | `#/user-panel/post-sub-return-view` | **Return View** (final form preview; `Submit Return` here) |

Navigation model: steps 1–2 use **Continue**; from step 3 a **tab bar** (Assessment · Income · Rebate · Expenditure · Assets & Liabilities · Tax & Payment · Return View) plus an **income sub-nav** (Employment / Financial Assets / Rent / Tax Exempted). Every section has **Back · Save Draft · Save & Continue**.

Recon protocol:

1. Walk every route with **view-only** clicks (Continue / tabs / links — never Save).
2. Append a row to `payload/field-map.md` for each control (Section, Label, Ref, Type, JSON key, Notes).
3. Mark readonly/auto fields under “Auto-computed” — never type those.
4. Record the **draft’s current value** vs your merged-JSON target — that diff is the fill list.
5. Open **Update Tax Payment Status** once to map the ledger (§4a).

**Recon stop condition:** every key you intend to set is either mapped or listed under “Unmapped / blocked”.

---

## 4. Phase 4 — Fill order

For each step: **snapshot → fill merged values → assert §6 row → screenshot `screenshots/NN-section.png` → Save draft.**

| Step | Section (route from §3) | JSON (delta wins) | Screenshot prefix |
|------|-------------------------|-------------------|-------------------|
| 1 | 1 Assessment info | `personal` + AY labels; heads-of-income checkboxes | `01-assessment` |
| 2 | 2 Additional information | rebate/IT-10B triggers; area field | `02-additional` |
| 3 | 3 Employment | `schedule1_employment` | `03-employment` |
| 4 | 4 Financial assets | `attachments` sanchay + bank rows; `incomeLines.6_*` | `04-fin-assets` |
| 5 | 5 Rent | `schedule2_rent` | `05-rent` |
| 6 | 6 Tax exempted | `attachments.sourcesOfFund` exempt rows | `06-exempt` |
| 7 | 7 Rebate (Sch-5) | `schedule5_investment` — use `Import from Income` helper | `07-sch5` |
| 8 | 8 Expenditure (IT-10BB) | `it10bb_lifestyle` incl. line-8 tax row | `08-it10bb` |
| 9 | 9 Assets & Liabilities (IT-10B) | `it10b_wealth` + `attachments` (properties/banks/car) — `Import and Autofill` helper | `09-it10b` |
| 10 | 10 Tax & Payment | `taxComputation` (auto) + `taxPayments` 20–26 | `10-payments` |
| 11 | 11 Return View | §6 only — **no `Submit Return`** | `11-return-view` |

Annexure-type rows (salary/bank/sanchay TDS, car AIT) live **inside** steps 4/10 and the ledger — not separate top-level pages. Salary TDS row expansion: Source Tax row caret on step 10.

### Fill techniques (Playwright MCP)

- Prefer `browser_fill_form` for many textboxes on one page.
- Numbers: plain digits, no commas (portal usually formats).
- Dropdowns: `browser_select_option` with visible option text.
- If refs stale after navigation: always **new `browser_snapshot`** before next action.
- If a11y names missing: `browser_take_screenshot` + temporary vision/targeted `browser_type` by label text; record in field-map.

### Line 23 (tax paid with return) — confirmed mechanism

- Leave **0** during the draft-only run.
- After the human pays the balance: Tax & Payment → **Update Tax Payment Status** → ledger → **Tax Paid with Return (173)** → enter Challan No → **Save** → value flows into line 23 (ledger dashboard shows the total first).
- Expected balance (for human later): `line19 − line20 − line21` from merged tax figures.

### Car AIT annexure — confirmed mechanism

- Ledger **Claim AIT → AIT on Car** searches by *Unique Key (Transaction No.)*; an existing claim responds with *“Claim already exists …”* — that **confirms** the claim; never delete it.
- On the return, line 21 (Advance Income Tax) and the annexure row should already reflect it; if line 21 = 0, set it from `taxPayments.21_advanceTax` and re-check.

### 4a. Update Tax Payment Status → eReturn Ledger

`ledger.etaxnbr.gov.bd` opens via automatic session handoff (SSO). Verify claims — **do not re-create them**:

| Ledger page | Route | What to verify |
|---|---|---|
| Salary (Others) | `#/pages/source-tax/private-salary` | Σ claimed = payload salary TDS; count = challans |
| Bank/FI | `#/pages/source-tax/bank-tds` | one row per bank, TDS sums |
| Sanchayapatra | `#/pages/source-tax/sanchayapatra` | rows **Verified**, TDS sums |
| AIT on Car | `#/pages/ait/car` | search txn key → “already exists” = claimed |
| Tax Paid with Return (173) | `#/pages/challan-entry/regular-tax` | line-23 challan appears here after payment |
| Dashboard | `#/pages/dashboard` | total = line 20 + line 21 (+23 later) |

Left nav also has Dividend/Service/Import/Commercial-vehicle/Others claim pages (usually empty for salary taxpayers) and refund/carry-forward adjustment pages — leave untouched.

---

## 5. Persistence pattern

```
for section in checklist:
    snapshot()
    fill(section, merge(baseline, deltas))
    assert_on_screen(section)
    screenshot(f"screenshots/{nn}-{section}.png")
    click_save_draft()
    tick(section)
```

If session dies: restart opencode/MCP → `browser_navigate` to portal → human re-login if needed → resume at first unticked section.

---

## 6. Verification gate (Phase 5)

Do **not** hardcode personal totals in this document. Build the expected table from the **merged** JSON, then compare to the **Return View** (`#/user-panel/post-sub-return-view`) and/or Tax & Payment summary.

**Return View notes:** renders the complete IT-11GA form read-only (English/Bangla toggle) with every annexure; if it bounces with HTTP 400 on `check-return-view`, that click was mid-load — retry once. The only **`Submit Return`** button in the whole portal is at the bottom of this page.

### 6a. Print expected (agent)

For each key below, compute `delta ?? baseline` and print `key = value`:

- `incomeLines.*` (especially `11_totalIncome`)
- `taxComputation.*` (especially `12_grossTax`, `13_rebate`, `19_totalPayable`)
- `taxPayments.*` (especially `20_tds`, `21_advanceTax`, `24_totalPaid`, `26_taxExempt`)
- `schedule2_rent.7_allowableDeduction`, `8_totalAdmissible`, `9_netIncome`, `12_totalRentalIncome`
- `schedule5_investment.3_*`, `5_*`, `6_*`, `11_totalInvestment`, `12_rebateAmount`
- `it10bb_lifestyle.total`, `8_tdsAndLastYearTax`
- `it10b_wealth.2_previousNetWealth`, `5_netWealthEnd`, `7_grossWealth`, `8k_i_bankBalance`, `8k_ii_cashInHand`, `10_totalAssets`
- `attachments.sourcesOfFund.*`

### 6b. Invariants (must all hold on screen)

| # | Check |
|---|--------|
| 1 | Main line **24 = line 19** (once line 23 filled); else 24 = 20+21+22+23 matches formula |
| 2 | Line **25 excess = 0** (or explain refund case) |
| 3 | Line **11 = sum of income lines 1–10** |
| 4 | Line **14 = 12 − 13**; line **16 = max(14, 15)**; line **19 = 16+17+18** |
| 5 | Sch-2: **line 7 = line 8**; **line 9 = line 6 − line 8**; main line 2 = Sch-2 line 12 |
| 6 | Sch-5: **line 11 = sum of serials 1–10**; line 13 on main page ties to Sch-5 line 12 (± portal incentive only) |
| 7 | Opening IT-10B line 2 **= last year’s closing line 5** (from baseline) |
| 8 | IT-10B: **line 5 = line 7 = line 10** (when assets fully filled) |
| 9 | IT-10B total assets ≥ each non-zero asset line; bank total = sum of bank rows |
| 10 | IT-10BB total = sum of lines 1–9; IT-10B line 4(a) = IT-10BB total |
| 11 | Exempt line 26 = sources-of-fund exempt parts in payload |
| 12 | Every JSON key that should be filled is either on screen or listed blocked in field-map |

**Any mismatch:** do not continue. Save draft, write mismatch table into `run-report.md`, stop.

---

## 7. Phase 6 — Handoff

1. Ensure **Save as draft** succeeded (status text visible).
2. Final screenshot of draft/review page.
3. Write `run-report.md`:

```markdown
# Run report — current AY draft prefill
- Date/time:
- Assessment year:
- Sections filled: [x]
- Screenshots: screenshots/
- Verification: PASS | FAIL (invariant table + key totals from merged JSON)
- Line 23 status: typed | left 0
- Car AIT annexure: complete | incomplete
- Open items (from deltas.openItems): ...
- Next human steps: review screen → pay balance (line 19 − 20 − 21) → paste challan → Submit
```

4. Tell user: **review all screenshots + portal draft; only they may Submit.**

---

## 8. Prompt to start (paste into opencode)

```
Read NBR-eReturn-Agentic-Entry-Plan.md and execute from Phase 0.
Use Playwright MCP tools only on etaxnbr.gov.bd and ledger.etaxbr.gov.bd.
Baseline: payload/ereturn-2025-26.json
Deltas:   payload/deltas-2026-27.json
Walk the wizard (§3 routes), patch the draft vs merged JSON, Save draft per section.
Run tools/optimize.py (Phase 2a), show me optimization-report.md, and wait for my OK before filling.
Verify ledger claims (§4a) — verify only, never delete/re-add.
Stop at Save as draft + run-report.md. Never submit, pay, or reset calculations.
Pause for me at login and if any verification check fails.
Use only values from the merged JSON — do not invent amounts.
```

---

## 9. File map

```
<workspace>/
  README.md                              # quickstart (shareable)
  LICENSE                                # MIT (shareable)
  opencode.json                          # Playwright MCP (shareable)
  basic_guide.md                         # zero-to-start guide, EN+BN (shareable)
  tax_optimize.md                        # tax optimization guideline, EN+BN, experimental (shareable)
  NBR-eReturn-Agentic-Entry-Plan.md      # this runbook (shareable)
  Tax-Filing-Guide-Bangladesh.md         # concepts (shareable)
  tools/
    extract.py                           # documents → staging JSON (shareable)
    optimize.py                          # Phase 2a tax optimization report (shareable)
    tax-rules.example.json               # slabs + rebate rules, edit yearly (shareable)
    classify.py                          # file-type fingerprints (shareable)
    parsers/ereturn.py                   # e-Return PDF → baseline keys (shareable)
    mapping.example.json                 # example source→key rules (shareable)
    requirements.txt                     # python deps (shareable)
  templates/
    field-map.md                         # redacted example with real routes (shareable)
    baseline.example.json                # schema, fake values (shareable)
    deltas.example.json                  # schema, fake values (shareable)
  payload/
    ereturn-2025-26.json                 # LY baseline (private — gitignored)
    deltas-2026-27.json                  # AY patches (private — gitignored)
    field-map.md                         # Phase 3 output (private — gitignored)
    staging/                             # extract.py output (private — gitignored)
  screenshots/                           # Phase 4 output (private — gitignored)
  run-report.md                          # Phase 6 output (private — gitignored)
  .playwright-profile/                   # browser user-data (do not commit/share)
```

Optional private human checklist (your workspace only): a correction worksheet or similar — **not** required by this template.

---

## 10. Known portal facts (live-verified 25-Sep-2026)

- **Landing** `#/landing-page`: tiles eTIN (ext) · eReturn · ReturnVerify/PSR · eReturnLedger · eTaxPayment(eTDS) · eTaxService (ext)
- **eReturn** tile → registered? dialog → `#/auth/sign-in` (TIN + password, no captcha on form)
- **Post-login:** header AY selector · left nav Home / Submission→Regular e-Return / Tax Record (TIN cert, Express cert, Acknowledgement, Return, Challan, History)
- **Wizard:** 11 routes — see §3; per-section `Save Draft` / `Save & Continue`; `Reset Calculation` + `Save` inside Tax computation (avoid Reset)
- **Update Tax Payment Status** (step 10) → ledger SSO → claim pages + s.173 — see §4a
- **Return View:** final form preview; **`Submit Return`** is human-only
- Support: hotline 09643 717171 · ticket.etaxnbr.gov.bd

---

*Template: Playwright MCP · last-year baseline first · current-year deltas · draft-only (human submits). No taxpayer identifiers or amounts in this file.*
