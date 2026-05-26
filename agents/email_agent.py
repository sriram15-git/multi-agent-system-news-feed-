from tools.gmail_tool import send_email
from config.config    import RECIPIENTS
from datetime         import datetime
import json
from pathlib import Path

HISTORY_FILE = Path(__file__).parent.parent / "memory" / "sent_history.json"


class EmailAgent:
    """
    Sends the HTML digest via Gmail and logs it to sent_history.json.
    """

    def run(self, html_body: str, recipients: list[str] = None) -> bool:
        recipients = recipients or RECIPIENTS
        today      = datetime.now().strftime("%A, %d %B %Y")
        subject    = f"☀️ Your AI Daily Digest — {today}"

        print(f"[EmailAgent] Sending digest to {recipients}...")
        success = send_email(subject, html_body, recipients)

        if success:
            self._log(today, recipients)

        return success

    def _log(self, date: str, recipients: list[str]):
        try:
            history = json.loads(HISTORY_FILE.read_text())
        except Exception:
            history = []

        history.append({"date": date, "recipients": recipients})

        # keep last 30 entries
        history = history[-30:]
        HISTORY_FILE.write_text(json.dumps(history, indent=2))