import os
from datetime import datetime
from config import SCORES_FILE


def load_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    scores = []
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split("|")
                    if len(parts) >= 3:
                        scores.append({
                            "score": int(parts[0]),
                            "accuracy": float(parts[1]),
                            "max_combo": int(parts[2]),
                            "date": parts[3] if len(parts) > 3 else "unknown",
                        })
    except (ValueError, IOError):
        scores = []
    scores.sort(key=lambda s: s["score"], reverse=True)
    return scores[:10]


def save_score(score, accuracy, max_combo):
    scores = load_scores()
    entry = {
        "score": score,
        "accuracy": round(accuracy, 1),
        "max_combo": max_combo,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    scores.append(entry)
    scores.sort(key=lambda s: s["score"], reverse=True)
    scores = scores[:10]
    try:
        with open(SCORES_FILE, "w", encoding="utf-8") as f:
            for s in scores:
                f.write(f"{s['score']}|{s['accuracy']}|{s['max_combo']}|{s['date']}\n")
    except IOError:
        pass
