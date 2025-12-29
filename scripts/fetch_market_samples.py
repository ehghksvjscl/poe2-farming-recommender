#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

OUTPUT_DIR = Path("backend/data/samples")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TRANSLATIONS_DIR = Path("backend/data/translations")
TRANSLATIONS_FILE = TRANSLATIONS_DIR / "ko.json"

USER_AGENT = "Mozilla/5.0 (compatible; poe2-farming-recommender/0.1; +https://github.com/)"
FETCH_TIMEOUT = 20


def load_translations() -> dict[str, dict[str, str]]:
    """Load Korean translations from JSON file."""
    if not TRANSLATIONS_FILE.exists():
        return {}
    try:
        data = json.loads(TRANSLATIONS_FILE.read_text(encoding="utf-8"))
        # Flatten all category translations into a single lookup
        translations = {}
        for category, items in data.items():
            if category.startswith("_"):
                continue
            if isinstance(items, dict):
                translations.update(items)
        return translations
    except (json.JSONDecodeError, IOError):
        return {}


def translate_item(item: dict, translations: dict[str, str]) -> dict:
    """Add Korean name to item if translation exists."""
    if not isinstance(item, dict):
        return item
    
    # Try to find translation for 'text' or 'name' field
    en_name = item.get("text") or item.get("name")
    if en_name and en_name in translations:
        item["name_ko"] = translations[en_name]
    
    # Translate category
    category = item.get("categoryApiId")
    if category and category in translations:
        item["category_ko"] = translations[category]
    
    return item


def translate_data(data: Any, translations: dict[str, str]) -> Any:
    """Recursively translate data."""
    if isinstance(data, list):
        return [translate_item(item, translations) for item in data]
    elif isinstance(data, dict):
        return translate_item(data, translations)
    return data


@dataclass
class FetchResult:
    url: str
    fetched_at: str
    status: int | None
    content_type: str | None
    error: str | None
    data: Any
    fetch_mode: str
    curl_command: str | None


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_curl(url: str) -> str:
    return (
        "curl -L --compressed "
        "-H 'Accept: application/json, text/plain, */*' "
        "-H 'Accept-Language: en-US,en;q=0.9' "
        "-H 'Referer: https://poe.ninja/' "
        f"-H 'User-Agent: {USER_AGENT}' "
        f"'{url}'"
    )


def read_local_source(path: Path, url: str) -> FetchResult:
    raw = path.read_text(encoding="utf-8")
    data: Any
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = raw
    return FetchResult(
        url=url,
        fetched_at=utc_now(),
        status=None,
        content_type="local/file",
        error=None,
        data=data,
        fetch_mode="offline",
        curl_command=None,
    )


def fetch_url(url: str) -> FetchResult:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://poe.ninja/",
        },
    )
    try:
        with urlopen(request, timeout=FETCH_TIMEOUT) as response:
            content_type = response.headers.get("content-type")
            body = response.read()
            status = response.status
            parsed: Any
            if content_type and "application/json" in content_type:
                parsed = json.loads(body.decode("utf-8"))
            else:
                parsed = body.decode("utf-8", errors="replace")
            return FetchResult(
                url=url,
                fetched_at=utc_now(),
                status=status,
                content_type=content_type,
                error=None,
                data=parsed,
                fetch_mode="remote",
                curl_command=None,
            )
    except HTTPError as exc:
        return FetchResult(
            url=url,
            fetched_at=utc_now(),
            status=exc.code,
            content_type=exc.headers.get("content-type") if exc.headers else None,
            error=str(exc),
            data=None,
            fetch_mode="remote",
            curl_command=build_curl(url),
        )
    except URLError as exc:
        return FetchResult(
            url=url,
            fetched_at=utc_now(),
            status=None,
            content_type=None,
            error=str(exc),
            data=None,
            fetch_mode="remote",
            curl_command=build_curl(url),
        )


def write_result(name: str, result: FetchResult) -> None:
    target = OUTPUT_DIR / name
    payload = {
        "source_url": result.url,
        "fetched_at": result.fetched_at,
        "status": result.status,
        "content_type": result.content_type,
        "error": result.error,
        "fetch_mode": result.fetch_mode,
        "curl_command": result.curl_command,
        "data": result.data,
    }

    if isinstance(payload["data"], str):
        payload["data"] = payload["data"][:20000]

    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch PoE economy samples")
    parser.add_argument(
        "--offline-dir",
        type=Path,
        help="Optional directory with pre-downloaded JSON/HTML files to use instead of remote fetch.",
    )
    parser.add_argument(
        "--no-translate",
        action="store_true",
        help="Skip Korean translation of item names.",
    )
    args = parser.parse_args()

    # Load translations
    translations = {} if args.no_translate else load_translations()
    if translations:
        print(f"Loaded {len(translations)} translations")

    # Current league - update this when new league starts
    current_league = "Fate of the Vaal"
    league_encoded = current_league.replace(" ", "%20")

    print(f"Using league: {current_league}")

    targets = {
        "poe2scout_runes.json": f"https://poe2scout.com/api/items?category=runes&league={league_encoded}",
        "poe2scout_currency.json": f"https://poe2scout.com/api/items?category=currency&league={league_encoded}",
    }

    offline_dir = args.offline_dir
    for filename, url in targets.items():
        local_path = offline_dir / filename if offline_dir else None
        if local_path and local_path.exists():
            result = read_local_source(local_path, url)
        else:
            result = fetch_url(url)
        
        # Apply translations to data
        if translations and result.data:
            result = FetchResult(
                url=result.url,
                fetched_at=result.fetched_at,
                status=result.status,
                content_type=result.content_type,
                error=result.error,
                data=translate_data(result.data, translations),
                fetch_mode=result.fetch_mode,
                curl_command=result.curl_command,
            )
        
        write_result(filename, result)
        status = result.status if result.status is not None else result.fetch_mode
        print(f"{filename}: {status}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
