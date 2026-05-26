import time
from tools.llm_tool import ask_llm
from config.config  import HUMOR_MODE
from pathlib        import Path

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

MODE_FILES = {
    "sarcastic":    "sarcasm_prompt.txt",
    "funny":        "comedy_prompt.txt",
    "roast":        "roast_prompt.txt",
    "gen-z":        "genz_prompt.txt",
    "professional": "professional_prompt.txt",
}


class HumorAgent:
    """
    Rewrites weather summary and news snippets in a chosen personality.
    The personality makes the digest fun to read instead of just informational.
    """

    def __init__(self, mode: str = None):
        self.mode = mode or HUMOR_MODE
        prompt_file = PROMPTS_DIR / MODE_FILES.get(self.mode, "comedy_prompt.txt")
        self._prompt_template = prompt_file.read_text().strip()

    def rewrite_weather(self, weather: dict) -> str:
        prompt = self._prompt_template + f"""

Now rewrite this weather report in your style (2-3 funny lines):

City: {weather['city']}
Temperature: {weather['temp_c']}°C (feels like {weather['feels_like_c']}°C)
Condition: {weather['condition']}
Humidity: {weather['humidity']}%
Rain chance: {weather['rain_chance']}%
Wind: {weather['wind_kmh']} km/h
High / Low: {weather['max_temp']}°C / {weather['min_temp']}°C
"""
        return ask_llm(prompt)

    def rewrite_article(self, title: str, context: str) -> str:
        prompt = self._prompt_template + f"""

Rewrite this news item in your style (3-4 punchy lines):

Title: {title}
Context: {context}
"""
        return ask_llm(prompt)

    def run(self, weather: dict, news: dict[str, list[dict]]) -> dict:
        """
        Returns:
          {
            "weather_funny": str,
            "news": { topic: [ {..., "funny": str}, ... ] }
          }
        """
        print(f"[HumorAgent] Rewriting in '{self.mode}' mode...")

        weather_funny = self.rewrite_weather(weather)

        funny_news: dict[str, list[dict]] = {}
        for topic, articles in news.items():
            funny_news[topic] = []
            for article in articles:
                funny = self.rewrite_article(
                    article["title"],
                    article.get("context", article.get("summary", "")),
                )
                article["funny"] = funny
                funny_news[topic].append(article)
                time.sleep(10)

        print("[HumorAgent] Done.")
        return {
            "weather_funny": weather_funny,
            "news":          funny_news,
        }