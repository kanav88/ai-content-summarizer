from datetime import datetime
from pathlib import Path
import re

SUMMARY_DIR = Path("summaries")


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:50] or "summary"


def save_summary(title: str, content: str) -> str:
    SUMMARY_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}_{slugify(title)}.md"
    file_path = SUMMARY_DIR / filename

    markdown_content = f"""# {title}

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

{content}
"""

    file_path.write_text(markdown_content, encoding="utf-8")
    return str(file_path)


def list_summaries():
    SUMMARY_DIR.mkdir(exist_ok=True)
    files = sorted(SUMMARY_DIR.glob("*.md"), reverse=True)

    summaries = []

    for file in files:
        content = file.read_text(encoding="utf-8")
        first_line = content.splitlines()[0] if content else "# Untitled"
        title = first_line.replace("#", "").strip()

        summaries.append({
            "title": title,
            "filename": file.name,
            "path": str(file),
            "content": content
        })

    return summaries
