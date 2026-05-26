from tools.news_tool import fetch_news
from config.config   import TOPICS


class NewsAgent:
    """
    Fetches latest headlines for all configured topics via RSS.
    Returns { topic: [article, ...] }
    """

    def run(self, topics: list[str] = None) -> dict[str, list[dict]]:
        topics = topics or TOPICS
        print(f"[NewsAgent] Fetching news for {len(topics)} topics...")

        news = fetch_news(topics, max_per_topic=1)

        total = sum(len(v) for v in news.values())
        print(f"[NewsAgent] Collected {total} articles.")
        return news