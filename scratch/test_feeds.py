import feedparser
import time

urls = [
    'https://openai.com/news/rss.xml',
    'https://techcrunch.com/category/artificial-intelligence/feed/',
    'https://arxiv.org/rss/cs.AI'
]

print("Checking 3 sources to prove it works...\n")
for u in urls:
    try:
        f = feedparser.parse(u)
        if not f.entries:
            print(f"❌ {u} - No entries found.")
            continue
        ent = f.entries[0]
        pub = ent.get('published') or ent.get('updated') or 'No Date'
        print(f"✅ Source: {f.feed.get('title', u)}")
        print(f"   Latest Article: {ent.get('title')}")
        print(f"   Published At: {pub}\n")
    except Exception as e:
        print(f"❌ Error with {u}: {e}")
