"""
list-sessions.py - List all Claude Code CLI sessions for this project
Usage: python list-sessions.py
       python list-sessions.py --resume   (to pick one and resume)
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime

PROJECT_DIR = Path(os.environ["USERPROFILE"]) / ".claude" / "projects" / "d--Python-Openclaw"

def get_session_info(jsonl_path):
    slug = None
    first_user_text = None
    last_timestamp = None
    message_count = 0

    try:
        with open(jsonl_path, encoding="utf-8", errors="replace") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                except Exception:
                    continue

                ts = obj.get("timestamp")
                if ts:
                    last_timestamp = ts

                if slug is None:
                    slug = obj.get("slug")

                if obj.get("type") == "user" and obj.get("userType") == "external":
                    message_count += 1
                    if first_user_text is None:
                        content = obj.get("message", {}).get("content", "")
                        if isinstance(content, list):
                            for block in content:
                                if isinstance(block, dict) and block.get("type") == "text":
                                    text = block["text"].strip()
                                    # skip injected system content
                                    if text and not text.startswith("<system-reminder>"):
                                        first_user_text = text[:120]
                                        break
                        elif isinstance(content, str) and content.strip():
                            text = content.strip()
                            if not text.startswith("<system-reminder>"):
                                first_user_text = text[:120]
    except Exception as e:
        return None

    size_kb = jsonl_path.stat().st_size // 1024
    mtime = datetime.fromtimestamp(jsonl_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")

    return {
        "uuid": jsonl_path.stem,
        "slug": slug or "(unnamed)",
        "first_message": first_user_text or "(image/no text)",
        "last_modified": mtime,
        "size_kb": size_kb,
        "user_messages": message_count,
    }


def main():
    if not PROJECT_DIR.exists():
        print(f"No sessions found at {PROJECT_DIR}")
        return

    sessions = []
    for f in sorted(PROJECT_DIR.glob("*.jsonl"), key=lambda x: x.stat().st_mtime, reverse=True):
        info = get_session_info(f)
        if info:
            sessions.append(info)

    if not sessions:
        print("No sessions found.")
        return

    print(f"\nFound {len(sessions)} session(s):\n")
    for i, s in enumerate(sessions, 1):
        print(f"[{i}] {s['slug']}")
        print(f"    Date:     {s['last_modified']}  |  Size: {s['size_kb']}KB  |  Messages: {s['user_messages']}")
        print(f"    First:    {s['first_message']}")
        print(f"    UUID:     {s['uuid']}")
        print()

    if "--resume" in sys.argv:
        try:
            choice = int(input("Enter number to resume (0 to cancel): "))
            if 1 <= choice <= len(sessions):
                uuid = sessions[choice - 1]["uuid"]
                print(f"\nRun this command:\n\n  claude --resume {uuid}\n")
        except (ValueError, KeyboardInterrupt):
            pass


if __name__ == "__main__":
    main()
