import json
import os
from datetime import datetime
from config import LOG_FILE


def log_interaction(question: str, tier: str, response: str) -> None:
    """
    Append a structured record of this interaction to the audit log.
    """
    # Make sure the logs directory exists before writing the file.
    log_dir = os.path.dirname(LOG_FILE)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "tier": tier,
        "question": question[:300],
        "response_preview": response[:200],
        "question_length": len(question),
        "response_length": len(response),
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    print(f'[LOGGED] tier={tier} | "{question[:60]}" → {len(response)} chars')