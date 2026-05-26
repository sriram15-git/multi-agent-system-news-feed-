import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from pipeline.orchestrator import Orchestrator

def run_once():
    print("=" * 60)
    print("🚀 Triggering the Daily Newsroom pipeline immediately...")
    print("=" * 60)
    try:
        orchestrator = Orchestrator()
        orchestrator.run()
    except Exception as e:
        print(f"\n❌ Error running pipeline: {e}")
        print("Ensure you have created a valid .env file (see .env.example) and your dependencies are installed.")

def run_scheduler():
    from pipeline.scheduler import run_pipeline
    from apscheduler.schedulers.blocking import BlockingScheduler
    from config.config import DAILY_HOUR, DAILY_MINUTE

    scheduler = BlockingScheduler(timezone="Asia/Kolkata")
    scheduler.add_job(
        run_once,
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Daily Newsroom CLI Runner")
    parser.add_argument("--now", action="store_true", help="Run the newsletter pipeline immediately and exit")
    parser.add_argument("--schedule", action="store_true", help="Start the scheduler to run the pipeline daily")
    
    args = parser.parse_args()
    
    # Default behavior if no argument is passed: run once immediately (easier for testing!)
    if not args.now and not args.schedule:
        print("💡 No mode specified. Defaulting to running the pipeline once immediately.")
        print("   (To run on a continuous daily schedule, run with: python main.py --schedule)\n")
        run_once()
    elif args.now:
        run_once()
    elif args.schedule:
        run_scheduler()
