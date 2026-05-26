import time
from tools.llm_tool import ask_llm
from pathlib        import Path

PROMPT_FILE = Path(__file__).parent.parent / "prompts" / "research_prompt.txt"


class ResearchAgent:
    """
    Enriches each raw headline with context, background, and implications.
    Turns "Vijay movie announced" → "Why this matters + context + implications".
    """

    def __init__(self):
        self._prompt_template = PROMPT_FILE.read_text().strip()

    def run(self, news: dict[str, list[dict]]) -> dict[str, list[dict]]:
        """
        For each article, ask the LLM to enrich it.
        Returns same structure with an added 'context' field.
        """
        print("[ResearchAgent] Enriching articles with context...")

        enriched: dict[str, list[dict]] = {}

        for topic, articles in news.items():
            enriched[topic] = []
            for article in articles:
                prompt = self._prompt_template.format(
                    title=article["title"],
                    summary=article.get("summary", ""),
                )
                context = ask_llm(prompt)
                article["context"] = context
                enriched[topic].append(article)
                print(f"  [ResearchAgent] Enriched: {article['title'][:60]}...")
                time.sleep(10)

        print("[ResearchAgent] Done.")
        return enriched