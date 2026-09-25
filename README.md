![NBR e-Return](images/nbr.png)

# e-Return NBR — Agentic Filling Strategy (Bangladesh)

An **agentic playbook** for pre-filling the Bangladesh NBR e-Return (etaxnbr.gov.bd) using [opencode](https://opencode.ai) (but anything will work) + Playwright MCP: an AI agent walks the return wizard, patches your draft against your own data files, and **stops at Save draft** — you review, pay, and submit yourself. This started as a fun Facebook [post](https://www.facebook.com/share/p/1JNZ6wwUno/), but became a reality now.

> **Not tax advice.** The guide teaches form mechanics; your figures, your responsibility. Nothing in this repo ever pays or submits — safety rails are built into the runbook.

## Why I built this

Even as a high-tech professional, I realized I had low financial literacy when it came to managing my own taxes. **I wanted to change that.** I wanted to build true financial literacy, so I decided to tackle filing my own tax return on the portal myself.

As I started working through the form, I struggled to wrap my head around the underlying logic—why certain figures needed to go in specific fields, or how the portal’s internal rules were structured. On top of that, navigating the input process itself proved quite challenging.

That is when I realized **I could use an AI agent to help guide me through the mechanics of the process.**

It took me **nearly 1 month of part-time work—nights and weekends, between my job and family**—to figure out how to bridge these gaps. Having spent years in the AI industry and authoring [**11 books on AI in Bangla**](https://aiwithr.github.io/resources/) to help everyday people use AI in daily life, this project naturally grew out of that same mission.

> **It is my gift to the community.** You shouldn't have to spend a month trying to decipher the process — take what I built and save your time.

## What this really is

Not a tax product — a **working pattern for building agents that operate government/service web portals**: how to recon a form wizard safely, keep state in JSON, verify against a read-only view, and hard-stop before irreversible actions.

Concretely, it's a **tax-lawyer-agent starter** — and a blueprint for adapting the same approach to any other portal with a form wizard.

## Fork it & make it yours

This repo is a **template, not a finished tool**. The intended flow: fork it, swap the portal-specific parts for yours, keep the hard-won safety model.

**Keep** (the transferable part):

- The safety allowlist model — agent may navigate/fill/save, never pay/submit/reset
- The phased workflow: recon → fill → verify → human handoff
- The **baseline + deltas** JSON pattern (last-year data + this-year patches)
- `opencode.json` + Playwright MCP setup
- Run-report discipline: every unverified item must be listed, never silently skipped

**Replace** (the portal-specific part):

- `templates/baseline.example.json` / `templates/deltas.example.json` → your form's fields, your keys
- `templates/field-map.md` → your portal's routes and sections (fill it during your own recon)
- The domain allowlist (`etaxnbr.gov.bd`, `ledger.etaxnbr.gov.bd`) → your portal's domains
- The starter prompt (§8 of the runbook) → your task description

**Five steps:** fork → read the guide + runbook → build your two JSON files from *your* documents → recon your portal read-only → fill, verify, and hand off to a human for the irreversible parts.

Other portals, same pattern: another taxpayer's tax-lawyer agent, other NBR services, passports, land records, utilities — anything that's a form wizard behind a login.

## What's inside

| File | What it is |
|---|---|
| [`Tax-Filing-Guide-Bangladesh.md`](Tax-Filing-Guide-Bangladesh.md) | Concepts guide: slabs, income heads, schedules, rebate, IT-10B/10BB, verification checklist |
| [`NBR-eReturn-Agentic-Entry-Plan.md`](NBR-eReturn-Agentic-Entry-Plan.md) | The runbook: phases, live portal routes, fill order, verification gate, safety rails, starter prompt |
| [`opencode.json`](opencode.json) | opencode config registering Playwright MCP |
| [`templates/field-map.md`](templates/field-map.md) | Redacted example of the Phase-3 recon map (real routes, no personal figures) |
| [`templates/baseline.example.json`](templates/baseline.example.json) | Schema for the last-year baseline data file |
| [`templates/deltas.example.json`](templates/deltas.example.json) | Schema for current-year corrections/patches |

## Quickstart

After you fork:

1. **Read** the [guide](Tax-Filing-Guide-Bangladesh.md) (concepts) then the [runbook](NBR-eReturn-Agentic-Entry-Plan.md) (execution).
2. **Build your two data files** from *your* last-year filed PDF and *your* current-year documents — start from the JSON templates. Same keys, real values.
3. **Configure**: copy `opencode.json` into your workspace, then
   ```
   npx @playwright/mcp install-browser chrome-for-testing
   ```
   Restart opencode — browser tools should now be exposed.
4. **Recon** (Phase 3): walk the wizard read-only, fill your `payload/field-map.md`.
5. **Fill** (Phase 4): patch the draft vs your merged JSON, Save Draft per section.
6. **Verify** (Phase 5) against Return View; hand off for payment + **Submit** (human only).

Paste-ready starter prompt: see §8 of the runbook.

## Safety model (summary)

- Agent may click: navigate, fill, **Save Draft**.
- Agent may **never** click: `Pay Now`, `Submit Return`, `Proceed to online return`, `Reset Calculation`, or delete/replace existing ledger claims.
- Password / OTP / PIN are always typed by the human, never stored.
- Domains allowlisted: `etaxnbr.gov.bd`, `ledger.etaxnbr.gov.bd` (the ledger opens automatically from the return for tax-payment claims).

## Private files (never commit)

Your real numbers live **outside** this repo pattern:

```
payload/ereturn-2025-26.json   # your last-year baseline
payload/deltas-2026-27.json    # your current-year patches
payload/field-map.md           # your filled recon map
screenshots/, run-report.md    # session outputs
```

`.gitignore` excludes them by default.

## Credits & community

Built by [Rakibul Hassan](https://aiwithr.github.io/about/) in spare time — roughly **one month of part-time work** on top of a day job, informed by years in the AI industry and [11 Bangla books](https://aiwithr.github.io/resources/) on using AI in everyday life. Portal structure verified live against etaxnbr.gov.bd (Sep 2026) — re-verify, portals change.

If this saves you a weekend: **star it, fork it, make it yours — and PR your improvements back.** That's the gift regifting.

[MIT](LICENSE)
