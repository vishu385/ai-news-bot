# 🤖 AI News WhatsApp Bot

Checks 20+ genuine AI news sources every **15 minutes** and instantly sends new articles to WhatsApp via **Twilio**.

---

## 📁 Project Files

| File | Description |
|---|---|
| `ai_news_bot.py` | Main bot script |
| `requirements.txt` | Python dependencies |
| `run_bot.bat` | One-click Windows launcher |
| `.env.example` | Example environment variables |
| `seen_articles.json` | Auto-generated — tracks sent articles |

---

## 🚀 Setup Guide

### 1. Install Python
- Download: <https://www.python.org/downloads/>
- Make sure to check **"Add Python to PATH"** during installation ✅

### 2. Twilio Setup
1. Create an account on [Twilio](https://www.twilio.com/) (free trial available)
2. Copy the **Account SID** and **Auth Token** — you will put these in `ai_news_bot.py`
3. Activate the WhatsApp Sandbox:
   - Twilio Console → Messaging → Try it out → **Send a WhatsApp message**
   - Send the join message from your phone to the sandbox number (e.g. `join <your-code>`)

### 3. Configure the Bot
Update these values in `ai_news_bot.py`:
```python
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN  = "your_auth_token"
FROM_WHATSAPP      = "whatsapp:+14155238886"   # Twilio sandbox number
TO_WHATSAPP        = "whatsapp:+91XXXXXXXXXX"  # Your number
```

### 4. Run It!

**Option A — Double-click:**
```
run_bot.bat
```

**Option B — Using Terminal:**
```bash
pip install -r requirements.txt
python ai_news_bot.py
```

---

## ⚠️ Important Notes

1. **Twilio Free Trial** can only send messages to verified numbers.
2. **WhatsApp Sandbox** expires after 72 hours — you will need to send the join message again.
3. **Auth Token** should never be shared publicly — see `.env.example` for a safer approach.
4. Press `Ctrl+C` in the terminal to stop the bot.

---

## 📡 Sources Monitored

| Category | Sources |
|---|---|
| **AI Company Blogs** | OpenAI, Anthropic, DeepMind, Meta AI, HuggingFace, Stability AI, Google AI, Microsoft AI |
| **Tech News** | TechCrunch, VentureBeat, The Verge, Ars Technica, Wired, MIT Tech Review, IEEE Spectrum |
| **Research** | ArXiv (cs.AI, cs.LG), Papers With Code |
| **Dev Tools** | Simon Willison's Blog, AI News (Buttondown) |

---

## 🔧 Customization

- **Change interval**: Update `CHECK_EVERY_MINUTES = 15`
- **Add new RSS feeds**: Add URLs to the `RSS_FEEDS` list
- **Change keywords**: Modify the `AI_KEYWORDS` list

---

*Built with ❤️ for staying updated on AI news!*
