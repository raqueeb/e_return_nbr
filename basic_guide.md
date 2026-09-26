# **Basic Guide — Start from Zero**

### [Rakibul Hassan](https://aiwithr.github.io/about/) **with the help of OpenCode**

For people who have **never used AI before**. No tech background needed.  
If you can copy-paste and follow steps, you can do this.

# **🇬🇧 English**

## **1\. Who this is for**

* You saw this repo, but words like **agent**, **MCP**, **JSON**, **fork** mean nothing to you.  
* You just want your tax return prepared with less pain.  
* You do **not** need to know programming.

## **2\. Words you will hear (plain English)**

| Word | What it means |
| :---- | :---- |
| **AI / chatbot** | A computer program you talk to in normal language and it answers. |
| **Agent** | An AI that doesn't just talk — it can *do* things for you, like typing into a website. |
| **opencode** | The free tool that runs the agent on your computer. You type instructions; it acts. |
| **MCP** | A small connector that lets the AI control things (here: a web browser). |
| **Playwright** | The software that moves the browser — clicks, types, takes screenshots. |
| **JSON** | A simple way to store your numbers in a file. Looks like this: "basic\_pay": 50000\. |
| **GitHub** | A website where people keep code. This repo lives there. |
| **Fork** | Press one button on GitHub to copy this whole repo into *your* account. |
| **Terminal / command** | A black window where you type commands and press Enter. |

## **3\. What you need**

* \[ \] A Windows or Mac computer  
* \[ \] Internet  
* \[ \] About 1 free hour  
* \[ \] Your **last year's filed tax return** (PDF or paper) and this year's papers (certificates, bank statements)  
* \[ \] Patience — first time is the slowest

## **4\. Install (do these once, in order)**

### **Step 1 — Install Node.js**

> 1. Go to [https://nodejs.org](https://nodejs.org?utm_source=gemini)  
> 2. Download the big green button (LTS version).  
> 3. Run it → Next → Next → Finish.

### **Step 2 — Install opencode**

Open your terminal (Windows: press Win+R, type powershell, Enter) and paste:

npm install \-g opencode-ai

Press Enter. Wait until it finishes.

### **Step 3 — Fork this repo**

> 1. Open this repo on GitHub.  
> 2. Click the button that says **Fork** (top right).  
> 3. Then on *your* fork page: **Code → Download ZIP**.  
> 4. Unzip it into a folder you will remember, e.g. C:\\tax-agent.

### **Step 4 — Get the config file**

Make sure your folder contains opencode.json (it's inside the ZIP you downloaded). It must sit in the **same folder** you will start the agent from.

> **Not using opencode?** Any MCP-capable agent works exactly the same — Claude Code, OpenAI Codex CLI, Command Code, Gemini CLI, Cursor, and more. MCP is an open standard, so the browser tools are identical everywhere; only the config file's format changes (a cosmetic difference — see runbook §1a).

### **Step 5 — Install the browser**

In the same terminal, paste and Enter:

npx @playwright/mcp install-browser chrome-for-testing

(Only needed once. It downloads a browser — about 200 MB.)

## **5\. Turn your documents into JSON (one command — no typing\!)**

Don't copy numbers from PDFs by hand. Make a folder with everything you downloaded (last year's e-Return, bank statements, sanchayapatra, pension, rent, challans, your Excel), install the helpers once, and run:

pip install \-r tools/requirements.txt  
python tools/extract.py \--docs C:\\your-documents \--out payload/staging

Then open payload/staging/inventory.md — it tells you what was found in each file and how sure it is. The agent (or you) turns that into the two data files using templates/ as the shape.

## **6\. Your first run**

> 1. In the terminal, cd into your folder:  
>    cd C:\\tax-agent

> 2. Start the agent:  
>    opencode

> 3. Paste the starter prompt (it's in NBR-eReturn-Agentic-Entry-Plan.md, section 8\) and press Enter.  
> 4. The agent will ask you to log in to the tax portal — **you type your password yourself**, on the screen. Never tell it to the AI.  
> 5. The agent walks the form, checks your numbers, and **saves a draft**. It stops there.

## **7\. Safety — in plain words**

The agent **will** click around, type numbers, and save drafts.  
The agent will **never**:

* pay money  
* submit the return  
* see or store your password

Only **you** press *Pay* and *Submit*. Always.

## **8\. If something goes wrong**

| Problem | Fix |
| :---- | :---- |
| 'npm' is not recognized | Reinstall Node.js from step 1, then close and reopen the terminal. |
| opencode: command not found | Close terminal completely, open it again. Still failing? Run npm install \-g opencode-ai again. |
| Browser not found | Run step 5's command again. |
| Portal screen looks different from the guide | Normal — portals change. Do a fresh "recon" walk (runbook Phase 3\) before filling. |
| Agent wants to click Submit/Pay | Stop it. That me job, not its. |
| extract.py says module not found | Run pip install \-r tools/requirements.txt once, then try again. |

## **9\. Next steps**

> 1. Read [Tax-Filing-Guide-Bangladesh.md](Tax-Filing-Guide-Bangladesh.md) — how the tax form works.  
> 2. Read [NBR-eReturn-Agentic-Entry-Plan.md](NBR-eReturn-Agentic-Entry-Plan.md) — how the agent runs.  
> 3. Run the document extractor (step 5), review payload/staging/inventory.md, then shape your two data files after templates/.

# **🇧🇩 বাংলা (Bangla)**

## **১. কাদের জন্য এই গাইড**

* এই রিপোটা চোখে পড়েছে, কিন্তু **এজেন্ট**, **MCP**, **JSON**, **ফর্ক**—এই ভারী ইংরেজি টেকনিক্যাল শব্দগুলো দেখে কিছুই মাথায় ঢুকছে না? একদম ভয় পাবেন না।  
* আপনি হয়তো শুধু চান কোনো ঝামেলা ছাড়া সহজে আপনার ট্যাক্স রিটার্নটা প্রসেস হয়ে যাক।  
* আর সবচেয়ে বড় কথা—এর জন্য আপনার কোডিং বা প্রোগ্রামিং শেখার কোনো দরকারই নেই।

## **২. যেসব শব্দ বারবার শুনবেন (সহজ বাংলায় দেখে নিন)**

| শব্দ | সহজ ভাষায় এটার মানে কী |
| :---- | :---- |
| **এআই / চ্যাটবট** | কম্পিউটারের একটা স্পেশাল প্রোগ্রাম—যাকে আপনি সাধারণ ভাষায় কোনো নির্দেশ দিলে সে উত্তর দেয় বা কাজ করে। |
| **এজেন্ট** | এমন এক এআই, যে শুধু আপনার সাথে চ্যাটই করবে না—বরং আপনার হয়ে ওয়েবসাইটে গিয়ে টাইপ বা ফিলআপ করার মতো কাজও করে দিতে পারে। |
| **opencode** | একটা একদম ফ্রি টুল, যেটা দিয়ে আপনি আপনার কম্পিউটারে এআই এজেন্ট চালাবেন। আপনি ইনস্ট্রাকশন দেবেন, সে অ্যাকশন নেবে। |
| **MCP** | সহজ ভাষায় একটা ছোট্ট কানেক্টর—যেটার সাহায্যে এআই আপনার ব্রাউজারকে কন্ট্রোল বা অপারেট করতে পারে। |
| **Playwright** | আসল টুল যেটা ব্যাকগ্রাউন্ডে ব্রাউজার ড্রাইভ করে—ক্লিক করা, টাইপ করা বা স্ক্রিনশট নেওয়ার কাজগুলো এ-ই সামলায়। |
| **JSON** | ফাইলে আপনার টাকার হিসাব বা ডেটা গুছিয়ে রাখার একটা পাওয়ারফুল আর সিম্পল ফরম্যাট। দেখতে এমন হয়: "basic\_pay": 50000। |
| **GitHub** | যেখানে সারাবিশ্বের কোডার আর ডেভেলপাররা নিজেদের কোড ও ফাইল জমা রাখেন। আমাদের এই প্রজেক্টও ওখানেই লাইভ আছে। |
| **ফর্ক (Fork)** | GitHub-এর একটা বাটন। ওটাতে একটা সিঙ্গেল ক্লিক করলেই পুরো প্রজেক্টটা কপি হয়ে আপনার নিজস্ব অ্যাকাউন্টে চলে আসবে। |
| **টার্মিনাল / কমান্ড** | কম্পিউটারের সেই কালো স্ক্রিন উইন্ডোটা, যেখানে আপনি নির্দেশ লিখে এন্টার চাপলেই কাজ শুরু হয়ে যায়। |

## **৩. যা যা আপনার সঙ্গে রাখতে হবে**

* \[ \] একটা সচল উইন্ডোজ (Windows) বা ম্যাক (Mac) কম্পিউটার  
* \[ \] একটা রানিং ইন্টারনেট কানেকশন  
* \[ \] হাতে গুনে মাত্র ১ ঘণ্টার মতো ফ্রি টাইম  
* \[ \] **গত বছরের জমা দেওয়া ট্যাক্স রিটার্নের কপি** (পিডিএফ বা কাগজ) আর এই বছরের সব প্রয়োজনীয় ডকুমেন্টস (ব্যাংক স্টেটমেন্ট, সার্টিফিকেট ইত্যাদি)  
* \[ \] সামান্য একটু ধৈর্য—কারণ ফার্স্ট টাইমে সবকিছু সেটআপ করতে একটু সময় তো লাগবেই\!

## **৪. ইনস্টল করার একদম সিম্পল ধাপগুলো (একবারই করবেন, পর পর)**

### **ধাপ ১ — Node.js ইনস্টল করে নিন**

১. প্রথমে চলে যান [https://nodejs.org](https://nodejs.org) লিংকে।  
২. সেখানে থাকা বড় সবুজ রঙের বাটনটা (LTS ভার্সন) ক্লিক করে ডাউনলোড করুন।  
৩. ফাইলটা চালু করুন → Next → Next ক্লিক করতে করতে Finish দিয়ে ইনস্টলেশন কমপ্লিট করুন।

### **ধাপ ২ — opencode ইনস্টল করুন**

আপনার কম্পিউটারের টার্মিনালটা ওপেন করুন (উইন্ডোজ ইউজার হলে: কিবোর্ডে Win+R চাপুন, powershell লিখে Enter চাপুন)। তারপর নিচের কোডটা কপি করে পেস্ট করুন:

npm install \-g opencode-ai

এবার Enter চাপুন। ইনস্টলেশন শেষ হওয়া পর্যন্ত কয়েক মুহূর্ত ওয়েট করুন।

### **ধাপ ৩ — এই রিপোটা ফর্ক করে নিন**

১. GitHub-এ গিয়ে আমাদের এই প্রজেক্টের পেজটা ওপেন করুন।  
২. ডানপাশের ওপরের দিকে **Fork** নামে একটা বাটন পাবেন, ওটাতে একটা ক্লিক করুন।  
৩. এবার আপনার নিজের ফর্ক পেজে গিয়ে দেখুন: **Code → Download ZIP** অপশনে ক্লিক করে ফাইলটা নামিয়ে নিন।  
৪. আপনার চেনা কোনো ফোল্ডারে ফাইলটা আনজিপ (Unzip) করে রেখে দিন, যেমন: C:\\tax-agent ফোল্ডারে।

### **ধাপ ৪ — কনফিগ ফাইলটা একটু চেক করে নিন**

নিশ্চিত হয়ে নিন আপনার ফোল্ডারে opencode.json ফাইলটা আছে কি না (আপনার ডাউনলোড করা ZIP ফাইলের ভেতরেই এটা দেওয়া ছিল)। মনে রাখবেন, ঠিক এই ফোল্ডার থেকেই আমরা পরে এজেন্ট চালু করব।

> **opencode ছাড়া অন্য কোনো টুল ব্যবহার করবেন?** Claude Code, OpenAI Codex CLI, Command Code, Gemini CLI, Cursor — সবকটিই ঠিক একরকমই কাজ করে। MCP একটা ওপেন স্ট্যান্ডার্ড, তাই ব্রাউজার কন্ট্রোলের টুলগুলো সব টুলে হুবহু একই। শুধু কনফিগ ফাইলটার ফরম্যাটটা একটু আলাদা — এর বেশি কিছু নয় (রানবুক §1a দেখুন)।

### **ধাপ ৫ — ব্রাউজার ইনস্টল দিন**

একই টার্মিনাল উইন্ডোতে নিচের লেখাটা পেস্ট করুন আর Enter চাপুন:

npx @playwright/mcp install-browser chrome-for-testing

(চিন্তার কিছু নেই, এটা জীবনে মাত্র একবারই করা লাগবে। এটা একটা ব্রাউজার ডাউনলোড করবে—সাইজ মাত্র ২০০ এমবি-র মতো।)

## **৫. নিজের ডকুমেন্টগুলো JSON-এ রূপান্তর (এক কমান্ডে — কিছুই টাইপ করতে হবে না\!)**

গত বছরের e-Return, ব্যাংক স্টেটমেন্ট, সঞ্চয়পত্র, পেনশন, ভাড়া, চালান, আপনার নিজের Excel — সব একটা ফোল্ডারে রাখুন। একবার হেল্পার ইনস্টল করে কমান্ড দিন:

pip install \-r tools/requirements.txt  
python tools/extract.py \--docs C:\\your-documents \--out payload/staging

এরপর payload/staging/inventory.md ফাইলটা খুলুন — কোন ফাইলে কী পাওয়া গেছে আর কতটা নিশ্চিত সেটা এখানে লেখা থাকবে। এরপর এজেন্ট (বা আপনি নিজে) templates/ ফাইলগুলোর আকার ধরে দুটো ডাটা ফাইল তৈরি করবেন।

## **৬. আপনার প্রথম রান বা এআই এজেন্ট চালানো**

১. টার্মিনালে কমান্ড দিয়ে আপনার নির্দিষ্ট ফোল্ডারে ঢুকে যান:

cd C:\\tax-agent

২. এবার এজেন্ট স্টার্ট করতে টাইপ করুন:

opencode

৩. আমাদের স্টার্টার প্রম্পটটা কপি করে পেস্ট করে দিন (এটা NBR-eReturn-Agentic-Entry-Plan.md ফাইলের ৮ নম্বর সেকশনে পাবেন) এবং Enter চাপুন।  
৪. এজেন্ট তখন আপনাকে এনবিআর ট্যাক্স পোর্টালে লগইন করতে বলবে—**মনে রাখবেন, পাসওয়ার্ডটা আপনার নিজের হাতেই স্ক্রিনে টাইপ করবেন**, ভুলেও কোনোদিন পাসওয়ার্ড এআই-কে দেবেন না বা টাইপ করতে বলবেন না।  
৫. এবার এজেন্ট নিজে থেকেই ফর্মের ভেতরে ঢুকবে, আপনার দেওয়া হিসাবের সংখ্যাগুলো মেলাবে এবং কাজ শেষে পুরো ফাইলটা **ড্রাফট সেভ (Save Draft)** করে রেখে দেবে। ব্যস, এজেন্টের কাজ এখানেই শেষ\!

## **৭. আপনার সিকিউরিটি ও সেফটি—সোজা কথায়**

আমাদের তৈরি এই এজেন্ট আপনার হয়ে পোর্টালে **যা যা করবে**: সাইটে ক্লিক করে ঘুরে বেড়াবে, ডাটা ইনপুট দিয়ে সংখ্যা বসাবে এবং ড্রাফট সেভ করে রাখবে।  
তবে এজেন্ট **ভুলও যা কখনো করবে না**:

* টাকা পেমেন্ট বা ফি পরিশোধ করা  
* ট্যাক্স রিটার্ন ফাইনাল সাবমিট করা  
* আপনার গোপনীয় পাসওয়ার্ড দেখা বা কোথাও সেভ করে রাখা

পেমেন্ট করার জন্য *Pay* আর জমা দেওয়ার জন্য *Submit* বাটনগুলো **শুধু আপনি নিজে চাপবেন**। সবসময় এই সিকিউরিটি রুল বজায় থাকবে।

## **৮. মাঝপথে কোনো প্রবলেম হলে বা আটকে গেলে**

| সমস্যা | ঝটপট সমাধান |
| :---- | :---- |
| 'npm' is not recognized দেখালে | ধাপ ১-এ গিয়ে Node.js আবার ঠিকমতো ইনস্টল দিন। তারপর টার্মিনাল বন্ধ করে আবার নতুন করে চালু করুন। |
| opencode: command not found দেখালে | টার্মিনালটা পুরোপুরি ক্লোজ করে আবার নতুন করে ওপেন করুন। তাও না হলে npm install \-g opencode-ai কমান্ডটা আবার চালান। |
| ব্রাউজার খুঁজে পাওয়া যাচ্ছে না বললে | ধাপ ৫-এর ব্রাউজার ইনস্টলের কমান্ডটা আরেকবার রান করুন। |
| পোর্টালে গিয়ে সাইটের স্ক্রিন গাইডের সাথে না মিললে | এতে নার্ভাস হওয়ার কিছু নেই, ট্যাক্স পোর্টাল মাঝে মাঝেই আপডেট হয়। ফর্ম ফিলআপ করার আগে ম্যানুয়ালি একবার ঘুরে দেখে নিন (runbook Phase 3 খেয়াল করুন)। |
| এজেন্ট যদি হুট করে Submit বা Pay বাটনে ক্লিক করতে চায় | সাথে সাথে ওকে থামান\! টাকা দেওয়া বা সাবমিট করা আপনার নিজস্ব কাজ, এজেন্টের নয়। |
| extract.py চালালে module not found দেখালে | একবার pip install \-r tools/requirements.txt চালান, তারপর আবার চেষ্টা করুন। |

## **৯. এরপর যা করবেন**

১. [Tax-Filing-Guide-Bangladesh.md](Tax-Filing-Guide-Bangladesh.md) গাইডটা পড়ে নিন—ট্যাক্স ফর্মের কোন অংশে কী থাকে আর কীভাবে কাজ করে তা বোঝার জন্য।  
২. [NBR-eReturn-Agentic-Entry-Plan.md](NBR-eReturn-Agentic-Entry-Plan.md) ফাইলটা দেখুন—এজেন্ট মূলত কীভাবে ভেতরে ভেতরে কাজ প্রসেস করে তা জানতে।  
৩. ধাপ ৫-এর এক্সট্র্যাক্টর কমান্ডটা চালান, payload/staging/inventory.md দেখে নিন, তারপর templates/ দেখে আপনার দুটো ডাটা ফাইল তৈরি করুন।  
[⬅ Back to README](README.md)  
আপনার যদি অন্য ফাইলটিও (যেমন "Why I built this" অংশটি) টেক্সট আকারে দরকার হয়, আমাকে জানাবেন\!