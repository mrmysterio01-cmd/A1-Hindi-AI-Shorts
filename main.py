
import os
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API_KEY = os.environ.get("GEMINI_API_KEY")

def generate_story():
    if not API_KEY:
        raise RuntimeError("GEMINI_API_KEY secret is missing")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-2.5-flash:generateContent"
        f"?key={API_KEY}"
    )

    prompt = """
    Write one original Hindi horror/suspense story for a YouTube Short.

    Requirements:
    - Hindi language, natural spoken style.
    - 30 to 45 seconds of narration.
    - A powerful opening hook in the first 3 seconds.
    - Suspenseful middle and surprising ending.
    - Suitable for a general audience.
    - No copyrighted characters or copied stories.

    Return only valid JSON in this format:
    {
      "title": "Short title in Hindi",
      "story": "Complete Hindi narration",
      "scenes": [
        "Visual description for scene 1",
        "Visual description for scene 2",
        "Visual description for scene 3"
      ]
    }
    """

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=90) as response:
        result = json.loads(response.read().decode("utf-8"))

    text = result["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(text)


def main():
    story = generate_story()

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    filename = datetime.now(timezone.utc).strftime(
        "story_%Y%m%d_%H%M%S.json"
    )

    output_file = output_dir / filename
    output_file.write_text(
        json.dumps(story, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Story generated: {output_file}")
    print(story["title"])


if __name__ == "__main__":
    main()
