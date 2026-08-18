import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

SOURCE_URL = "https://pvp-data.warmycat.com/usage.json"
OUTPUT = Path("data/current.json")


def fetch_json(url):
    request = Request(
        url,
        headers={
            "User-Agent": "LINE-Rangers-Usage-Tracker/1.0"
        }
    )

    with urlopen(request, timeout=30) as response:
        return json.load(response)


def main():
    source = fetch_json(SOURCE_URL)

    metadata = source.get("metadata", {})
    rangers = source.get("rangers", [])

    characters = []

    for ranger in rangers:
        ranger_id = ranger.get("rangerId")

        if not ranger_id:
            continue

        usage_rate = ranger.get("usageRate")

        if usage_rate is None:
            continue

        characters.append({
            "id": ranger_id,
            "name": ranger.get("name", ranger_id),
            "usageRate": float(usage_rate)
        })

    characters.sort(
        key=lambda x: x["usageRate"],
        reverse=True
    )

    output = {
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "sourceGeneratedAtUtc": metadata.get("generatedAtUtc"),
        "league": metadata.get("league"),
        "sampleCount": metadata.get("sampleCount"),
        "characterCount": len(characters),
        "characters": characters
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT.write_text(
        json.dumps(
            output,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print(f"Updated {len(characters)} characters")


if __name__ == "__main__":
    main()
