# Basic Guide — Start from Zero

> For people who have **never used AI before**. No tech background needed.
> If you can copy-paste and follow steps, you can do this.

---

# 🇬🇧 English

## 1. Who this is for

- You saw this repo, but words like **agent**, **MCP**, **JSON**, **fork** mean nothing to you.
- You just want your tax return prepared with less pain.
- You do **not** need to know programming.

## 2. Words you will hear (plain English)

| Word | What it means |
|---|---|
| **AI / chatbot** | A computer program you talk to in normal language and it answers. |
| **Agent** | An AI that doesn't just talk — it can *do* things for you, like typing into a website. |
| **opencode** | The free tool that runs the agent on your computer. You type instructions; it acts. |
| **MCP** | A small connector that lets the AI control things (here: a web browser). |
| **Playwright** | The software that moves the browser — clicks, types, takes screenshots. |
| **JSON** | A simple way to store your numbers in a file. Looks like this: `"basic_pay": 50000`. |
| **GitHub** | A website where people keep code. This repo lives there. |
| **Fork** | Press one button on GitHub to copy this whole repo into *your* account. |
| **Terminal / command** | A black window where you type commands and press Enter. |

## 3. What you need

- [ ] A Windows or Mac computer
- [ ] Internet
- [ ] About 1 free hour
- [ ] Your **last year's filed tax return** (PDF or paper) and this year's papers (certificates, bank statements)
- [ ] Patience — first time is the slowest

## 4. Install (do these once, in order)

### Step 1 — Install Node.js

1. Go to https://nodejs.org
2. Download the big green button (LTS version).
3. Run it → Next → Next → Finish.

### Step 2 — Install opencode

Open your terminal (Windows: press `Win+R`, type `powershell`, Enter) and paste:

```
npm install -g opencode-ai
```

Press Enter. Wait until it finishes.

### Step 3 — Fork this repo

1. Open this repo on GitHub.
2. Click the button that says **Fork** (top right).
3. Then on *your* fork page: **Code → Download ZIP**.
4. Unzip it into a folder you will remember, e.g. `C:\tax-agent`.

### Step 4 — Get the config file

Make sure your folder contains `opencode.json` (it's inside the ZIP you downloaded). It must sit in the **same folder** you will start the agent from.

### Step 5 — Install the browser

In the same terminal, paste and Enter:

```
npx @playwright/mcp install-browser chrome-for-testing
```

(Only needed once. It downloads a browser — about 200 MB.)

## 5. Your first run

1. In the terminal, `cd` into your folder:
   ```
   cd C:\tax-agent
   ```
2. Start the agent:
   ```
   opencode
   ```
3. Paste the starter prompt (it's in `NBR-eReturn-Agentic-Entry-Plan.md`, section 8) and press Enter.
4. The agent will ask you to log in to the tax portal — **you type your password yourself**, on the screen. Never tell it to the AI.
5. The agent walks the form, checks your numbers, and **saves a draft**. It stops there.

## 6. Safety — in plain words

The agent **will** click around, type numbers, and save drafts.

The agent will **never**:

- pay money
- submit the return
- see or store your password

Only **you** press *Pay* and *Submit*. Always.

## 7. If something goes wrong

| Problem | Fix |
|---|---|
| `'npm' is not recognized` | Reinstall Node.js from step 1, then close and reopen the terminal. |
| `opencode: command not found` | Close terminal completely, open it again. Still failing? Run `npm install -g opencode-ai` again. |
| Browser not found | Run step 5's command again. |
| Portal screen looks different from the guide | Normal — portals change. Do a fresh "recon" walk (runbook Phase 3) before filling. |
| Agent wants to click Submit/Pay | Stop it. That's your job, not its. |

## 8. Next steps

1. Read [`Tax-Filing-Guide-Bangladesh.md`](Tax-Filing-Guide-Bangladesh.md) — how the tax form works.
2. Read [`NBR-eReturn-Agentic-Entry-Plan.md`](NBR-eReturn-Agentic-Entry-Plan.md) — how the agent runs.
3. Build your two data files from `templates/` — copy the structure, put your own numbers.

---

# 🇧🇩 বাংলা (Bangla)

## ১. কাদের জন্য

- আপনি এই রিপো দেখেছেন, কিন্তু **এজেন্ট**, **MCP**, **JSON**, **ফর্ক** — এই শব্দগুলো বোঝা নেই।
- শুধু চান ট্যাক্স রিটার্নটা সহজে পূরণ হোক।
- প্রোগ্রামিং শেখার **কোনো দরকার নেই**।

## ২. যে শব্দগুলো পাবেন (সহজ বাংলায়)

| শব্দ | মানে |
|---|---|
| **এআই / চ্যাটবট** | কম্পিউটারের এমন একটা প্রোগ্রাম — সাধারণ ভাষায় বললে সে উত্তর দেয়। |
| **এজেন্ট** | এমন এআই যেটা শুধু কথা বলে না — কাজও করে (যেমন ওয়েবসাইটে টাইপ করে)। |
| **opencode** | আপনার কম্পিউটারে এজেন্ট চালানোর ফ্রি টুল। আপনি নির্দেশ দেন, সে কাজ করে। |
| **MCP** | ছোট একটা যোগাযোগকারী — এর মাধ্যমে এআই ব্রাউজার চালায়। |
| **Playwright** | সে সফটওয়্যার যেটা ব্রাউজার চালায় — ক্লিক, টাইপ, স্ক্রিনশট। |
| **JSON** | আপনার হিসাব ফাইলে রাখার সহজ উপায়। এরকম দেখায়: `"basic_pay": 50000`। |
| **GitHub** | লোকজের কোড রাখার ওয়েবসাইট। এই রিপো ওখানেই আছে। |
| **ফর্ক (Fork)** | GitHub-এ এক বাটনে পুরো রিপোটা নিজের অ্যাকাউন্টে কপি করা। |
| **টার্মিনাল / কমান্ড** | কালো একটা উইন্ডো — কমান্ড লিখে Enter চাপেন। |

## ৩. যা লাগবে

- [ ] উইন্ডোজ বা ম্যাক কম্পিউটার
- [ ] ইন্টারনেট
- [ ] প্রায় এক ঘণ্টা ফাঁকা সময়
- [ ] **গত বছরের জমা-দেওয়া রিটার্ন** আর এ বছরের কাগজপত্র (সার্টিফিকেট, ব্যাংক স্টেটমেন্ট)
- [ ] ধৈর্য — প্রথমবারটা সবচেয়ে ধীর হবে

## ৪. ইনস্টল (একবারই করবেন, ধারা ধারা)

### ধাপ ১ — Node.js ইনস্টল

1. যান https://nodejs.org
2. বড় সবুজ বাটনটা ডাউনলোড করুন (LTS)।
3. চালান → Next → Next → শেষ।

### ধাপ ২ — opencode ইনস্টল

টার্মিনাল খুলুন (উইন্ডোজ: `Win+R`, `powershell` লিখে Enter) আর পেস্ট করুন:

```
npm install -g opencode-ai
```

Enter চাপুন। শেষ হওয়া পর্যন্ত অপেক্ষা করুন।

### ধাপ ৩ — এই রিপো ফর্ক করুন

1. GitHub-এ এই রিপো খুলুন।
2. ডান উপরে **Fork** বাটনে চাপুন।
3. তারপর আপনার ফর্ক পেজে: **Code → Download ZIP**।
4. মনে রাখা ফোল্ডারে আনজিপ করুন, যেমন `C:\tax-agent`।

### ধাপ ৪ — কনফিগ ফাইল

ফোল্ডারে `opencode.json` আছে কি না দেখুন (ZIP-এর ভেতরেই আছে)। ঠিক সেই ফোল্ডার থেকেই এজেন্ট চালাবেন।

### ধাপ ৫ — ব্রাউজার ইনস্টল

একই টার্মিনালে পেস্ট করে Enter:

```
npx @playwright/mcp install-browser chrome-for-testing
```

(একবারই লাগে। প্রায় ২০০ MB ডাউনলোড হবে।)

## ৫. প্রথম রান

1. টার্মিনালে আপনার ফোল্ডারে যান:
   ```
   cd C:\tax-agent
   ```
2. এজেন্ট চালু করুন:
   ```
   opencode
   ```
3. স্টার্টার প্রম্পটটা পেস্ট করুন (`NBR-eReturn-Agentic-Entry-Plan.md`-এর §8-এ আছে), Enter।
4. এজেন্ট আপনাকে ট্যাক্স পোর্টালে লগইন করতে বলবে — **পাসওয়ার্ড আপনি নিজে টাইপ করবেন**, এআই-কে কখনো বলবেন না।
5. এজেন্ট ফর্ম ঘুরবে, সংখ্যা মিলিয়ে দেখবে, **ড্রাফট সেভ** করবে। এখানেই থামবে।

## ৬. নিরাপত্তা — সহজ কথায়

এজেন্ট **করবে**: ক্লিক করা, সংখ্যা লেখা, ড্রাফট সেভ।

এজেন্ট **কখনো করবে না**:

- টাকা পরিশোধ
- রিটার্ন জমা দেওয়া
- আপনার পাসওয়ার্ড দেখা বা রাখা

*Pay* আর *Submit* চাপবেন **শুধু আপনি**। সবসময়।

## ৭. কিছু ভুল হলে

| সমস্যা | সমাধান |
|---|---|
| `'npm' is not recognized` | ধাপ ১ থেকে Node.js আবার ইনস্টল করুন, টার্মিনাল বন্ধ করে খুলুন। |
| `opencode: command not found` | টার্মিনাল সম্পূর্ণ বন্ধ করে আবার খুলুন। না হলে `npm install -g opencode-ai` আবার চালান। |
| ব্রাউজার পাওয়া যাচ্ছে না | ধাপ ৫-এর কমান্ড আবার চালান। |
| পোর্টালের স্ক্রিন গাইডের থেকে আলাদা দেখাচ্ছে | স্বাভাবিক — পোর্টাল বদলায়। ভরার আগে নতুন করে একবার ঘুরে দেখুন (runbook Phase 3)। |
| এজেন্ট Submit/Pay-এ চাপ দিতে চাইছে | থামান। ওটা আপনার কাজ, এজেন্টের না। |

## ৮. পরের ধাপ

1. [`Tax-Filing-Guide-Bangladesh.md`](Tax-Filing-Guide-Bangladesh.md) পড়ুন — ট্যাক্স ফর্ম কীভাবে কাজ করে।
2. [`NBR-eReturn-Agentic-Entry-Plan.md`](NBR-eReturn-Agentic-Entry-Plan.md) পড়ুন — এজেন্ট কীভাবে চলে।
3. `templates/` থেকে আপনার দুটো ডেটা ফাইল বানান — গঠন কপি করুন, নিজের সংখ্যা বসান।

---

[⬅ Back to README](README.md)
