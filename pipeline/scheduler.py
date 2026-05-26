import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from apscheduler.schedulers.blocking import BlockingScheduler
from pipeline.orchestrator           import Orchestrator
from config.config                   import DAILY_HOUR, DAILY_MINUTE


def run_pipeline():
    Orchestrator().run()


if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone="Asia/Kolkata")

    scheduler.add_job(
        run_pipeline,
        trigger="cron",
        hour=DAILY_HOUR,
        minute=DAILY_MINUTE,
        id="daily_digest",
    )

    print(f"⏰ Scheduler started. Will run daily at {DAILY_HOUR:02d}:{DAILY_MINUTE:02d} IST")
    print("   Press Ctrl+C to stop.\n")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\n🛑 Scheduler stopped.")