![NBR e-Return](images/nbr.png)

🇧🇩 **[বাংলা সংস্করণের জন্য এখানে ক্লিক করুন (Read in Bangla)](README_bn.md)**

# e-Return NBR — Your AI Tax Filing Assistant (Bangladesh)

This is an **AI-powered guide** to help you fill out your Bangladesh NBR e-Return (etaxnbr.gov.bd). Think of it as having a smart, digital assistant that reads your tax documents, carefully types the numbers into the government website for you, and **stops right before saving**. You are always in control—you review everything, pay, and click the final submit button yourself. 

What started as a fun Facebook [post](https://www.facebook.com/share/p/1JNZ6wwUno/) has now become a real, working tool to save you time and headache.

> **Disclaimer: This is not professional tax advice.** This guide helps you navigate the website's mechanics. The numbers you enter are your responsibility. Our built-in safety rules ensure the AI can never pay or submit the form for you.

> **Use any AI you like.** While I used [opencode](https://opencode.ai), this method works perfectly with any modern AI agent (like Claude Code, Gemini CLI, Cursor, etc.). It uses a standard bridge called "MCP" that simply allows the AI to control a web browser.

---

## Why I Built This

Even as a high-tech professional, I realized I had very little financial literacy when it came to managing my own taxes. **I wanted to change that.** I wanted to build true financial confidence, so I decided to tackle filing my own tax return on the online portal myself.

As I started working through the form, I struggled to wrap my head around the underlying logic—why certain figures needed to go in specific boxes, and how the portal’s internal rules were actually set up. On top of that, navigating the website and typing everything in was confusing and frustrating.

That is when the lightbulb went off: **I could use an AI agent to guide me through the mechanics of this whole process.**

It took me **nearly a whole month of part-time work**—late nights and weekends, juggling my day job and family time—to figure out how to make this work safely. Having spent years in the AI industry and writing [**11 books on AI in Bangla**](https://aiwithr.github.io/resources/) to help everyday people use AI in their daily lives, building this tool felt like a natural next step.

> **This is my gift to the community.** You shouldn't have to spend a month trying to decipher this system. Take what I have built, skip the headache, and save your valuable time.

---

## Making Sense of the Tech (What this really is)

This isn't a magical software you buy; it is a **blueprint** for using AI to safely interact with government websites. Here is the simple breakdown of how it works:

1. **The Brain (AI Agent):** You give it instructions.
2. **The Hands (Playwright MCP):** A tool that lets the AI "click" and "type" on a web browser.
3. **The Memory (JSON Files):** Simple text files where you keep your numbers (like last year's data and this year's income) so the AI knows exactly what to type.

It is basically a starter kit for building your own personal "digital tax lawyer." And once you learn how it works here, you can use the same trick for passport portals, utility bills, or any online form.

---

## How to Make It Yours (Forking)

This repository (repo) is a template. The idea is to copy it (which is called "forking"), customize it with your own numbers, and use the safety rules I have already set up.

**What you keep from me:**
- The strict safety rules (the AI can navigate and fill, but never submit).
- The step-by-step workflow.
- The setup files that connect the AI to your browser.

**What you change for yourself:**
- The simple data files where you put your actual income numbers.
- Your personal login details (which you type yourself).

---

## What's Inside the Box?

| File | What it means for you |
|---|---|
| [`Tax-Filing-Guide-Bangladesh.md`](Tax-Filing-Guide-Bangladesh.md) | The human guide: explains how Bangladesh tax math actually works. |
| [`NBR-eReturn-Agentic-Entry-Plan.md`](NBR-eReturn-Agentic-Entry-Plan.md) | The robot guide: step-by-step instructions the AI follows to fill the form. |
| [`tax_optimize.md`](tax_optimize.md) | Tips on how to legally save on taxes (rebates, investment caps). |
| [`opencode.json`](opencode.json) | The settings file that connects the AI to your web browser. |
| [`tools/extract.py`](tools/extract.py) | A magic script that reads your PDF documents and turns them into text files so you don't have to type numbers by hand. |
| [`templates/baseline.example.json`](templates/baseline.example.json) | A blank template to put last year's tax numbers. |
| [`templates/deltas.example.json`](templates/deltas.example.json) | A blank template to put this year's new tax numbers. |

---

## Quickstart (Let's Get Started!)

**Are you completely new to AI?** Stop here and read the **[Basic Guide (Start from Zero)](basic_guide.md)** first. It is written for absolute beginners.

If you are ready, here is the flow after you copy (fork) this project:

1. **Read up:** Skim the tax guide and the agent runbook so you know the plan.
2. **Prepare your data:** Don't type numbers by hand! Put your tax PDFs in a folder and run our helper tool:
   ```bash
   python tools/extract.py --docs /path/to/your-documents --out payload/staging
   ```
   This reads your files and helps you fill out your `baseline` and `deltas` JSON templates.
3. **Optimize:** Run our optimization tool to see if you can save money on your taxes this year.
4. **Connect the browser:** Run the setup command (`npx @playwright/mcp install-browser chrome-for-testing`) so the AI has a browser to work with.
5. **Recon & Fill:** Ask the AI to log in. You type your password. Then, sit back and watch as the AI navigates the portal, fills in the boxes based on your files, and safely clicks **Save Draft**.
6. **You take the wheel:** Review the draft, pay any taxes owed, and hit **Submit** yourself.

---

## Our Promise on Safety

- **The AI is allowed to:** click around, navigate pages, type your numbers, and click **Save Draft**.
- **The AI will NEVER:** click `Pay Now`, click `Submit Return`, or reset your calculations. 
- Your passwords and OTP pins are **always typed by you**. The AI never sees them or stores them.

## A Note on Privacy

Your real tax numbers are completely private. We have set up the system (using `.gitignore`) so your personal files, passwords, and screenshots are never accidentally uploaded to the internet. 

---

## Credits

Built by [Rakibul Hassan](https://aiwithr.github.io/about/) in my spare time. I have written [11 books on AI in Bangla](https://aiwithr.github.io/resources/) and I believe technology should make our lives easier, not harder. 

If this saves you a stressful weekend, please star the project, share it with friends, and enjoy your free time! 

[MIT License](LICENSE)