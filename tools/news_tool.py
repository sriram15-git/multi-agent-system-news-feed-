import json
import feedparser
from pathlib import Path

DOMAINS_FILE = Path(__file__).parent.parent / "config" / "domain.json"

def fetch_news(topics: list[str], max_per_topic: int = 3) -> dict[str, list[dict]]:
    """
    Fetch news for given topics via RSS feeds.
    Returns { topic: [ {title, summary, link, published}, ... ] }
    """
    with open(DOMAINS_FILE) as f:
        feed_map: dict[str, list[str]] = json.load(f)

    results: dict[str, list[dict]] = {}

    for topic in topics:
        urls   = feed_map.get(topic, [])
        items  = []

        for url in urls:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:max_per_topic]:
                    summary = (
                        entry.get("summary", "")
                        or entry.get("description", "")
                    )
                    # strip HTML tags simply
                    import re
                    summary = re.sub(r"<[^>]+>", "", summary).strip()
                    summary = summary[:300] + "..." if len(summary) > 300 else summary

                    items.append({
                        "title":     entry.get("title", "No title"),
                        "summary":   summary,
                        "link":      entry.get("link", ""),
                        "published": entry.get("published", ""),
                    })
                    if len(items) >= max_per_topic:
                        break
            except Exception as e:
                print(f"[NewsTool] Failed to parse {url}: {e}")

            if len(items) >= max_per_topic:
                break

        results[topic] = items

    return results