import feedparser
import schedule
import time
import os
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
import hashlib
import json

# ============================================================
# ⚙️  SETTINGS
# ============================================================
CALLMEBOT_PHONE   = "+917505702806"  # 📞 Your WhatsApp number
CALLMEBOT_API_KEY = "your_api_key_here"  # 🔑 Put the API Key you received on WhatsApp here!

CHECK_EVERY_MINUTES = 15

# ============================================================
# 📡  25+ GENUINE AI NEWS SOURCES
# ============================================================
RSS_FEEDS = [
    # Official AI Company Blogs
    "https://huggingface.co/blog/feed.xml",
    "https://openai.com/news/rss.xml",
    "https://www.anthropic.com/news/rss",
    "https://deepmind.google/blog/rss",
    "https://ai.meta.com/blog/rss/",
    "https://stability.ai/news/rss.xml",
    "https://blog.google/technology/ai/rss/",
    "https://blogs.microsoft.com/ai/feed/",

    # AI News & Analysis
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/ai/feed/",
    "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
    "https://arstechnica.com/ai/feed/",
    "https://www.wired.com/tag/artificial-intelligence/feed/rss",
    "https://www.technologyreview.com/feed/",
    "https://spectrum.ieee.org/feeds/topic/artificial-intelligence.rss",

    # Developer & Tools
    "https://simonwillison.net/atom/everything/",
    "https://buttondown.com/ainews/rss",

    # Research Papers
    "https://paperswithcode.com/latest/rss",
    "https://arxiv.org/rss/cs.AI",
    "https://arxiv.org/rss/cs.LG",
]

AI_KEYWORDS = [
    "llm", "gpt", "gemini", "claude", "mistral", "llama", "qwen", "grok",
    "phi-", "deepseek", "model release", "new model", "foundation model",
    "machine learning", "deep learning", "transformer", "diffusion model",
    "multimodal", "reasoning model", "fine-tuning", "rag", "benchmark",
    "ai tool", "ai agent", "copilot", "cursor", "windsurf", "perplexity",
    "midjourney", "stable diffusion", "sora", "imagen", "dalle",
    "hugging face", "open source ai", "openai", "anthropic", "google deepmind",
    "meta ai", "nvidia", "mistral ai", "stability ai",
    "image generation", "video generation", "voice ai", "text to",
    "paper released", "dataset released", "ai announcement",
]

# ============================================================
# 📦  DATA PERSISTENCE
# ============================================================
SEEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seen_articles.json")


def load_seen():
    """Load previously seen article IDs from disk."""
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()


def save_seen(seen):
    """Persist seen article IDs to disk."""
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen), f)


# ============================================================
# 🔧  HELPERS
# ============================================================
def article_id(entry):
    """Generate a unique hash for an article based on link + title."""
    return hashlib.md5(
        (entry.get("link", "") + entry.get("title", "")).encode()
    ).hexdigest()


def is_ai_related(entry):
    """Check whether an entry matches any AI keyword."""
    text = (entry.get("title", "") + " " + entry.get("summary", "")).lower()
    return any(kw in text for kw in AI_KEYWORDS)


def is_recent(entry, minutes=25):
    """Return True if the entry was published within the last *minutes*."""
    try:
        published = entry.get("published_parsed") or entry.get("updated_parsed")
        if not published:
            return True
        pub_dt = datetime(*published[:6])
        return datetime.now(timezone.utc).replace(tzinfo=None) - pub_dt < timedelta(minutes=minutes)
    except Exception:
        return True


# ============================================================
# 📤  WHATSAPP MESSAGING
# ============================================================
def send_whatsapp(message):
    """Send a single WhatsApp message via CallMeBot API."""
    if CALLMEBOT_API_KEY == "your_api_key_here" or CALLMEBOT_PHONE == "+91XXXXXXXXXX":
        print("❌ Error: CallMeBot credentials not set!")
        return

    try:
        encoded_msg = urllib.parse.quote(message)
        url = f"https://api.callmebot.com/whatsapp.php?phone={CALLMEBOT_PHONE}&text={encoded_msg}&apikey={CALLMEBOT_API_KEY}"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            if response.getcode() == 200:
                print(f"[{datetime.now().strftime('%H:%M')}] ✅ Sent!")
            else:
                print(f"❌ Failed to send. HTTP Code: {response.getcode()}")
    except Exception as e:
        print(f"❌ Error: {e}")


# ============================================================
# 🔄  CORE LOOP
# ============================================================
def fetch_and_send():
    """Fetch all RSS feeds, filter for new AI articles, and send them."""
    seen = load_seen()
    new_articles = []
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking news...")

    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                aid = article_id(entry)
                if aid in seen:
                    continue
                if is_ai_related(entry) and is_recent(
                    entry, minutes=CHECK_EVERY_MINUTES + 5
                ):
                    new_articles.append(
                        {
                            "id": aid,
                            "title": entry.get("title", "No Title"),
                            "link": entry.get("link", ""),
                            "source": feed.feed.get("title", "Unknown"),
                        }
                    )
                    seen.add(aid)
        except Exception as e:
            print(f"  Error: {url[:40]} — {e}")

    save_seen(seen)

    if not new_articles:
        print("  No new AI articles.")
        return

    for article in new_articles:
        msg = "🚨 *New AI News!*\n\n"
        msg += f"📌 *{article['title']}*\n\n"
        msg += f"📰 _{article['source']}_\n"
        msg += f"🔗 {article['link']}"
        send_whatsapp(msg)
        time.sleep(2)


def send_welcome():
    """Send a startup welcome / status message."""
    msg = "🤖 *AI News Bot — Active!* ✅\n\n"
    msg += f"⏱ I will check every *{CHECK_EVERY_MINUTES} minutes*\n"
    msg += "📡 Monitoring *20+ genuine sources*:\n\n"
    msg += "• OpenAI, Anthropic, DeepMind, Meta AI\n"
    msg += "• HuggingFace, Stability AI, Microsoft AI\n"
    msg += "• TechCrunch, VentureBeat, The Verge, Wired\n"
    msg += "• ArXiv AI Papers, Papers With Code\n\n"
    msg += "🚨 Any new AI news — will be sent *instantly*! 🔥"
    send_whatsapp(msg)


# ============================================================
# 🚀  ENTRY POINT
# ============================================================
def run():
    print("=" * 45)
    print("🤖 AI News WhatsApp Bot Starting...")
    print(f"📤 To: {CALLMEBOT_PHONE}")
    print(f"⏰ Every: {CHECK_EVERY_MINUTES} min | Sources: {len(RSS_FEEDS)}")
    print("=" * 45)

    send_welcome()
    schedule.every(CHECK_EVERY_MINUTES).minutes.do(fetch_and_send)
    fetch_and_send()

    print(f"\n✅ Running! Ctrl+C to stop.\n")
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    run()
