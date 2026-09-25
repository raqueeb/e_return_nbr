# e-Return NBR — Agentic Filling Strategy (Bangladesh)

An **agentic playbook** for pre-filling the Bangladesh NBR e-Return (etaxnbr.gov.bd) using [opencode](https://opencode.ai) + Playwright MCP: an AI agent walks the return wizard, patches your draft against your own data files, and **stops at Save draft** — you review, pay, and submit yourself.

> **Not tax advice.** The guide teaches form mechanics; your figures, your responsibility. Nothing in this repo ever pays or submits — safety rails are built into the runbook.

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

## Credits

Built by [Rakibul Hassan](https://aiwithr.github.io/) with the help of opencode + Playwright MCP. Portal structure verified live against etaxnbr.gov.bd (Sep 2026) — re-verify, portals change.

[MIT](LICENSE)
