"""
poe2scout.com에서 시장 데이터를 가져와 DB에 저장하는 management command

사용법:
    python manage.py fetch_market_data
    python manage.py fetch_market_data --categories currency runes
    python manage.py fetch_market_data --league "Fate of the Vaal"
    python manage.py fetch_market_data --clear  # 기존 데이터 삭제 후 새로 가져오기
"""

from __future__ import annotations

import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from app.models import MarketItem, PriceHistory


# poe2scout API 설정
POE2SCOUT_API_BASE = "https://poe2scout.com/api"
USER_AGENT = "Mozilla/5.0 (compatible; poe2-farming-recommender/0.1)"
FETCH_TIMEOUT = 30

# 번역 파일 경로
TRANSLATIONS_FILE = Path("data/translations/ko.json")

# 지원하는 카테고리 목록
CATEGORIES = [
    "currency",
    "runes",
    "essences",
    "fragments",
    "waystones",
    "omens",
    "breachstones",
    "deliriuminstill",
    "uniques",
]


class Command(BaseCommand):
    help = "poe2scout.com에서 시장 데이터를 가져와 DB에 저장합니다."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.translations: dict[str, str] = {}

    def add_arguments(self, parser):
        parser.add_argument(
            "--league",
            type=str,
            default="Fate of the Vaal",
            help="리그 이름 (기본값: Fate of the Vaal)",
        )
        parser.add_argument(
            "--categories",
            nargs="+",
            default=CATEGORIES,
            help=f"가져올 카테고리 목록 (기본값: {', '.join(CATEGORIES)})",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="기존 데이터를 모두 삭제하고 새로 가져옵니다.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="실제로 저장하지 않고 가져올 데이터만 출력합니다.",
        )
        parser.add_argument(
            "--no-translate",
            action="store_true",
            help="한글 번역을 적용하지 않습니다.",
        )

    def handle(self, *args, **options):
        league = options["league"]
        categories = options["categories"]
        clear = options["clear"]
        dry_run = options["dry_run"]
        no_translate = options["no_translate"]

        # 번역 로드
        if not no_translate:
            self.translations = self._load_translations()
            self.stdout.write(f"번역: {len(self.translations)}개 로드")

        self.stdout.write(f"리그: {league}")
        self.stdout.write(f"카테고리: {', '.join(categories)}")

        if clear and not dry_run:
            self.stdout.write(self.style.WARNING("기존 데이터 삭제 중..."))
            PriceHistory.objects.all().delete()
            MarketItem.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("기존 데이터 삭제 완료"))

        total_items = 0
        total_price_logs = 0

        for category in categories:
            self.stdout.write(f"\n📦 {category} 카테고리 처리 중...")

            try:
                data = self._fetch_category(category, league)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ❌ 가져오기 실패: {e}"))
                continue

            if not data:
                self.stdout.write(self.style.WARNING(f"  ⚠️ 데이터 없음"))
                continue

            items_count, logs_count = self._save_items(data, category, league, dry_run)
            total_items += items_count
            total_price_logs += logs_count

            self.stdout.write(
                self.style.SUCCESS(f"  ✅ 아이템 {items_count}개, 가격로그 {logs_count}개")
            )

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"총 {total_items}개 아이템, {total_price_logs}개 가격로그 처리 완료"))

    def _fetch_category(self, category: str, league: str) -> list[dict[str, Any]]:
        """poe2scout API에서 카테고리 데이터 가져오기"""
        league_encoded = league.replace(" ", "%20")
        url = f"{POE2SCOUT_API_BASE}/items?category={category}&league={league_encoded}"

        request = Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json",
            },
        )

        try:
            with urlopen(request, timeout=FETCH_TIMEOUT) as response:
                body = response.read()
                return json.loads(body.decode("utf-8"))
        except HTTPError as e:
            raise CommandError(f"HTTP 에러 {e.code}: {e.reason}")
        except URLError as e:
            raise CommandError(f"URL 에러: {e.reason}")
        except json.JSONDecodeError as e:
            raise CommandError(f"JSON 파싱 에러: {e}")

    def _save_items(
        self, items: list[dict], category: str, league: str, dry_run: bool
    ) -> tuple[int, int]:
        """아이템 데이터를 DB에 저장"""
        items_count = 0
        logs_count = 0

        for item_data in items:
            item_id = item_data.get("itemId")
            if not item_id:
                continue

            name = item_data.get("name") or ""
            item_type = item_data.get("type") or ""
            category_api_id = item_data.get("categoryApiId") or category
            icon_url = item_data.get("iconUrl") or ""
            current_price = item_data.get("currentPrice")
            price_logs = item_data.get("priceLogs", [])

            if dry_run:
                self.stdout.write(f"    {name}: {current_price} exalted")
                items_count += 1
                logs_count += len([p for p in price_logs if p])
                continue

            with transaction.atomic():
                # 한글 이름 찾기
                name_ko = self._get_korean_name(name) if name else ""

                # MarketItem 생성 또는 업데이트
                market_item, created = MarketItem.objects.update_or_create(
                    item_id=item_id,
                    defaults={
                        "name": name,
                        "name_ko": name_ko,
                        "type": item_type,
                        "category": self._normalize_category(category_api_id),
                        "category_api_id": category_api_id,
                        "icon_url": icon_url,
                        "current_price": Decimal(str(current_price)) if current_price else None,
                        "league": league,
                    },
                )
                items_count += 1

                # PriceHistory 저장
                for log in price_logs:
                    if not log:
                        continue

                    price = log.get("price")
                    quantity = log.get("quantity", 0)
                    time_str = log.get("time")

                    if not price or not time_str:
                        continue

                    recorded_at = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
                    if timezone.is_naive(recorded_at):
                        recorded_at = timezone.make_aware(recorded_at)

                    PriceHistory.objects.update_or_create(
                        item=market_item,
                        recorded_at=recorded_at,
                        defaults={
                            "price": Decimal(str(price)),
                            "quantity": quantity,
                        },
                    )
                    logs_count += 1

        return items_count, logs_count

    def _normalize_category(self, category_api_id: str) -> str:
        """poe2scout categoryApiId를 우리 모델의 category로 변환"""
        mapping = {
            "accessory": "accessory",
            "armour": "armour",
            "weapon": "weapon",
            "jewel": "jewel",
            "currency": "currency",
            "rune": "runes",
            "runes": "runes",
            "essence": "essences",
            "essences": "essences",
            "fragment": "fragments",
            "fragments": "fragments",
            "waystone": "waystones",
            "waystones": "waystones",
            "omen": "omens",
            "omens": "omens",
            "breachstone": "breachstones",
            "breachstones": "breachstones",
            "deliriuminstill": "deliriuminstill",
            "unique": "uniques",
            "uniques": "uniques",
        }
        return mapping.get(category_api_id.lower(), "other")

    def _load_translations(self) -> dict[str, str]:
        """ko.json에서 번역 로드"""
        if not TRANSLATIONS_FILE.exists():
            return {}

        try:
            data = json.loads(TRANSLATIONS_FILE.read_text(encoding="utf-8"))
            translations = {}
            for category, items in data.items():
                if category.startswith("_"):
                    continue
                if isinstance(items, dict):
                    translations.update(items)
            return translations
        except (json.JSONDecodeError, IOError):
            return {}

    def _get_korean_name(self, en_name: str) -> str:
        """영문 이름으로 한글 이름 찾기"""
        return self.translations.get(en_name, "")

