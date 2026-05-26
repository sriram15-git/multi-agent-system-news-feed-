import sys
import json
from pathlib import Path

# Make sure project root is on the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.weather_agent  import WeatherAgent
from agents.news_agent     import NewsAgent
from agents.research_agent import ResearchAgent
from agents.humor_agent    import HumorAgent
from agents.digest_agent   import DigestAgent
from agents.email_agent    import EmailAgent
from config.config         import HUMOR_MODE

PREFS_FILE = Path(__file__).parent.parent / "memory" / "preferences.json"


class Orchestrator:
    """
    Runs the full pipeline:
      Weather → News → Research → Humor → Digest → Email
    """

    def __init__(self):
        prefs               = json.loads(PREFS_FILE.read_text())
        self.recipient_name = prefs.get("name", "Friend")
        self.topics         = prefs.get("topics", [])
        self.humor_mode     = prefs.get("humor_mode", HUMOR_MODE)

    def run(self):
        print("=" * 50)
        print("🤖 Daily Newsroom — Starting pipeline")
        print("=" * 50)

        # Step 1: Weather
        weather = WeatherAgent().run()

        # Step 2: News
        news = NewsAgent().run(self.topics)

        # Step 3: Research (enriches with context)
        enriched_news = ResearchAgent().run(news)

        # Step 4: Humor rewrite
        humor_output = HumorAgent(mode=self.humor_mode).run(weather, enriched_news)

        # Step 5: Build digest HTML
        html = DigestAgent().run(weather, humor_output, self.recipient_name)

        # Step 6: Send email
        EmailAgent().run(html)

        print("=" * 50)
        print("✅ Pipeline complete!")
        print("=" * 50)