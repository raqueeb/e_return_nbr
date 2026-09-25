# Field Map — NBR e-Return (Phase 3 recon example)

### [Rakibul Hassan](https://aiwithr.github.io/about/) with the help of OpenCode

**Example output** of the recon phase: real portal routes (verified live Sep 2026), **no personal figures**. Copy into your workspace as `payload/field-map.md` and fill the Value/JSON-key columns during your own read-only walk.

**Portal:** https://etaxnbr.gov.bd · hash-route SPA · AY via header combobox  
**Mode:** Regular e-Return wizard · refs (`eNNN`) are session-stale — re-snapshot every run.

---

## 0. Entry flow (pre-auth)

| Step | Route / action | Notes |
|------|----------------|-------|
| 1 | `#/landing-page` | Tiles: eTIN (ext) · **eReturn** · ReturnVerify/PSR · eReturnLedger · eTaxPayment(eTDS) · eTaxService (ext) |
| 2 | eReturn tile → dialog | “Are you registered in eReturn System?” → **I am already registered** |
| 3 | `#/auth/sign-in` | TIN + Password → Sign in (disabled until filled). No captcha on form. Links: Forgot password · Change mobile number · Register |

## 1. Shell (all post-login pages)

- Header: logo → `#/user-panel/home` · **Assessment Year combobox** · user menu
- Left nav: Home · Submission → Regular e-Return `#/user-panel/assessment/regular-return` · Tax Record → TIN Certificate / Express Certificate / Certificate Status / Acknowledgement / Return / Challan / History

## 2. Wizard routes (fill order)

| # | Route | Section | Your value → JSON key |
|---|-------|---------|----------------------|
| 1 | `#/user-panel/assessment/regular-return` | Assessment info (scheme, AY/IY, resident, heads checkboxes) | e.g. heads → `personal` / flags |
| 2 | `#/user-panel/additional-information` | Rebate trigger, IT-10B triggers, house area | flags |
| 3 | `#/user-panel/employment` | Income ▸ Employment (Sch-1): employer tabs, basic/RPF/other rows | `schedule1_employment.*` |
| 4 | `#/user-panel/financial-assets` | Income ▸ Financial Assets: Sanchayapatra table + Bank/FI table; `Import From NSD` | `attachments.sanchayList`, `bankTds`, `incomeLines.6_*` |
| 5 | `#/user-panel/rent` | Income ▸ Rent (Sch-2): property tab, deductions table (disabled totals auto) | `schedule2_rent.*` |
| 6 | `#/user-panel/tax-exempted-income` | Income ▸ Tax Exempted (pension etc.) | `attachments.sourcesOfFund` exempt |
| 7 | `#/user-panel/rebate` | Sch-5: category checkboxes + rows; `Import from Income`; totals auto | `schedule5_investment.*` |
| 8 | `#/user-panel/expenditure` | IT-10BB: lifestyle rows + “Tax … paid” row + total | `it10bb_lifestyle.*` |
| 9 | `#/user-panel/assets-and-liabilities` | IT-10B: properties/advances/sanchay/car/jewel/furniture/banks/cash + sources-of-fund; `Import and Autofill` | `it10b_wealth.*`, `attachments.*` |
| 10 | `#/user-panel/tax-and-payment` | Summary, computation (Reset/Save), payments 20–23, Final payable, `Update Tax Payment Status` | `taxComputation.*`, `taxPayments.*` |
| 11 | `#/user-panel/post-sub-return-view` | **Return View**: full form preview, English/Bangla; `Back` · **`Submit Return`** 🚫 | verify only |

Nav model: steps 1–2 **Continue**; from step 3 a **tab bar** (Assessment · Income · Rebate · Expenditure · Assets & Liabilities · Tax & Payment · Return View) + income **sub-nav** (Employment / Financial Assets / Rent / Tax Exempted). Every section: **Back · Save Draft · Save & Continue**.

## 3. eReturn Ledger (`ledger.etaxnbr.gov.bd`)

Reached from step 10 → **Update Tax Payment Status** (auto-SSO).

| Page | Route | Purpose |
|---|---|---|
| Salary (Others) | `#/pages/source-tax/private-salary` | claim employer salary TDS → line 20 |
| Bank/FI, Sanchayapatra, … | `#/pages/source-tax/…` | claim bank/sanchay TDS |
| AIT on Car | `#/pages/ait/car` | search **Unique Key (txn no)** → claim car AIT → line 21 |
| Tax Paid with Return (173) | `#/pages/challan-entry/regular-tax` | Challan No → Save → line 23 |
| Dashboard | `#/pages/dashboard` | totals mirror lines 20+21(+23) |

⚠️ Verify only — never delete/re-add an existing claim (UI warns “Claim already exists …”).

## 4. Safety buttons

🚫 `Pay Now` · `Submit Return` · `Proceed to online return` · `Reset Calculation` · ledger claim delete  
✅ `Continue` / `Back` / tabs / `Save Draft` (when intended)

## 5. Mapped fields (fill during your recon)

| Section | Label | Ref | Type | Value on screen | JSON key | Notes |
|---------|-------|-----|------|-----------------|----------|-------|
| | | | | | | |

## 6. Auto-computed (verify only — do not type)

Line 11 = Σ1–10 · Line 14 = 12−13 · Line 16 = max(14,15) · Line 19 = 16+17+18 · Line 24 = 20+21+22+23 · Line 25 = 24−19 · Sch-5 line 11 = Σ serials · Sch-5 line 12 = rebate formula · IT-10B chain (3,5,7,10) · Rent disabled totals · Return View renders everything read-only

## 7. Unmapped / blocked

| JSON key | Why blocked | Resolution |
|----------|-------------|------------|
| | | |
