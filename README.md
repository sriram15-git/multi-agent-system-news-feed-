# 🤖 Multi-Agent AI Daily Newsroom

A fully autonomous pipeline that fetches real-time weather and news, enriches headlines with AI context, rewrites the content with a custom comedic/sarcastic personality, and emails a styled HTML digest every morning. Deployed 100% free using GitHub Actions.

---

## 🌟 Key Features

* **Multi-Agent Pipeline:** Coordinated sequence of single-responsibility agents:
  $$\text{Weather} \longrightarrow \text{News} \longrightarrow \text{Research} \longrightarrow \text{Humor} \longrightarrow \text{Digest} \longrightarrow \text{Email}$$
* **Sarcastic Commentator Personality:** Tailored to Tamil Nadu culture (with references to TASMAC, Chennai auto fares, EB bills, traffic, and more).
* **Dual-Backend Support:** Automatically leverages the cloud-based Google Gemini 2.5 Flash API or falls back to a locally hosted Ollama model.
* **Styled HTML Email:** Automatically sent to recipients via Gmail SMTP.
* **100% Free Production Deployment:** Automated scheduler runs daily at 9:00 AM IST via GitHub Actions free-tier runner.
* **Robust & Resilient:** Handles rate-limiting with exponential backoff and features safe fallbacks for empty configuration parameters.

---

## 📁 Repository Structure

```text
multi-agent-system-news-feed/
│
├── main.py                        # CLI entry point (--now / --schedule)
│
├── pipeline/
│   ├── orchestrator.py            # Co-ordinates all agents in order
│   └── scheduler.py               # Local APScheduler runner
│
├── agents/                        # Specialized agents (Single Responsibility)
│   ├── weather_agent.py           # Handles weather agent logic
│   ├── news_agent.py              # Fetches RSS news feeds
│   ├── research_agent.py          # Enriches headlines with background context
│   ├── humor_agent.py             # Applies chosen comedic persona
│   ├── digest_agent.py            # Compiles styled HTML & Markdown digests
│   └── email_agent.py             # Interfaces with SMTP mail services
│
├── tools/                         # Low-level API/IO adapters
│   ├── weather_tool.py            # Fetches weather from Open-Meteo
│   ├── news_tool.py               # Parses RSS xml feeds using feedparser
│   ├── llm_tool.py                # Wrapper for Gemini API & Ollama
│   └── gmail_tool.py              # Sends emails using Python's smtplib
│
├── prompts/                       # Humor agent prompt files (.txt)
├── config/                        # Holds settings and RSS feed configurations
├── memory/                        # User preferences and sent history log
├── output/                        # Saved copy of latest generated digest
└── .github/workflows/
    └── daily_digest.yml           # GitHub Actions workflow configurations
```

---

## 🚀 Local Setup & Run

### 1. Prerequisites
Make sure you have Python 3.11+ installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables
Create a file named `.env` in the root directory and copy the contents from `.env.example`:
```env
GEMINI_API_KEY=your_gemini_api_key
GMAIL_ADDRESS=your_gmail@gmail.com
GMAIL_APP_PASSWORD=your_16_character_app_password
RECIPIENTS=recipient1@example.com,recipient2@example.com
WEATHER_CITY=Vellore
WEATHER_LATITUDE=12.9165
WEATHER_LONGITUDE=79.1325
HUMOR_MODE=sarcastic
```
> *Note: For GMAIL_APP_PASSWORD, generate a 16-character App Password from Google Account → Security → 2-Step Verification → App Passwords.*

### 4. Run Immediately
```bash
python main.py --now
```

### 5. Run Continuous Local Scheduler
```bash
python main.py --schedule
```

---

## ⚙️ Production Deployment (GitHub Actions)

This project runs 100% serverless on GitHub Actions. To deploy:

1. Push this code to your GitHub repository.
2. In GitHub, go to **Settings → Secrets and variables → Actions → Secrets** and add the following repository secrets:
   * `GEMINI_API_KEY`
   * `GMAIL_ADDRESS`
   * `GMAIL_APP_PASSWORD`
   * `RECIPIENTS`
3. Optional configuration variables can be added as secrets or variables:
   * `WEATHER_CITY`, `WEATHER_LATITUDE`, `WEATHER_LONGITUDE`, `HUMOR_MODE`
4. The workflow in `.github/workflows/daily_digest.yml` will automatically trigger every day at **9:00 AM IST** (3:30 AM UTC). You can also run it manually from the **Actions** tab in GitHub at any time!
