"""
MarketItem의 한글 이름을 번역하는 management command

1. ko.json 파일에서 번역 적용
2. poe2db.tw/kr/ 에서 없는 번역 가져오기

사용법:
    python manage.py translate_items
    python manage.py translate_items --fetch-poe2db  # poe2db.tw에서 추가 번역 가져오기
    python manage.py translate_items --update-json   # 새 번역을 ko.json에 저장
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.core.management.base import BaseCommand

from app.models import MarketItem


TRANSLATIONS_FILE = Path("data/translations/ko.json")
POE2DB_BASE = "https://poe2db.tw"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
FETCH_TIMEOUT = 15


class Command(BaseCommand):
    help = "MarketItem의 한글 이름을 번역합니다."

    def add_arguments(self, parser):
        parser.add_argument(
            "--fetch-poe2db",
            action="store_true",
            help="poe2db.tw에서 없는 번역을 가져옵니다.",
        )
        parser.add_argument(
            "--update-json",
            action="store_true",
            help="새로운 번역을 ko.json 파일에 저장합니다.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="실제로 저장하지 않고 결과만 출력합니다.",
        )

    def handle(self, *args, **options):
        fetch_poe2db = options["fetch_poe2db"]
        update_json = options["update_json"]
        dry_run = options["dry_run"]

        # 1. ko.json에서 번역 로드
        translations = self._load_translations()
        self.stdout.write(f"ko.json에서 {len(translations)}개 번역 로드")

        # 2. 번역이 없는 아이템 목록
        items_without_ko = MarketItem.objects.filter(name_ko="").exclude(name="")
        total_items = items_without_ko.count()
        self.stdout.write(f"번역 필요한 아이템: {total_items}개")

        # 3. ko.json 번역 적용
        applied_count = 0
        still_missing = []

        for item in items_without_ko:
            ko_name = translations.get(item.name)
            if ko_name:
                if not dry_run:
                    item.name_ko = ko_name
                    item.save(update_fields=["name_ko"])
                applied_count += 1
            else:
                still_missing.append(item)

        self.stdout.write(self.style.SUCCESS(f"ko.json에서 {applied_count}개 번역 적용"))
        self.stdout.write(f"아직 번역 없음: {len(still_missing)}개")

        # 4. poe2db.tw에서 추가 번역 가져오기
        if fetch_poe2db and still_missing:
            self.stdout.write("\npoe2db.tw에서 번역 가져오는 중...")
            new_translations = self._fetch_from_poe2db(still_missing[:100], dry_run)  # 처음 100개만
            
            if update_json and new_translations and not dry_run:
                self._update_translations_file(translations, new_translations)
                self.stdout.write(self.style.SUCCESS(f"ko.json에 {len(new_translations)}개 번역 추가"))

        # 5. 최종 통계
        translated_count = MarketItem.objects.exclude(name_ko="").count()
        total_count = MarketItem.objects.count()
        self.stdout.write(f"\n번역 완료: {translated_count}/{total_count} ({translated_count*100//total_count}%)")

    def _load_translations(self) -> dict[str, str]:
        """ko.json에서 모든 번역을 플랫하게 로드"""
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

    def _fetch_from_poe2db(self, items: list[MarketItem], dry_run: bool) -> dict[str, str]:
        """poe2db.tw/kr/ 검색으로 한글 이름 가져오기"""
        new_translations = {}
        
        for i, item in enumerate(items):
            if not item.name:
                continue
                
            self.stdout.write(f"  [{i+1}/{len(items)}] {item.name}...", ending="")
            
            try:
                ko_name = self._search_poe2db(item.name)
                if ko_name:
                    new_translations[item.name] = ko_name
                    if not dry_run:
                        item.name_ko = ko_name
                        item.save(update_fields=["name_ko"])
                    self.stdout.write(f" → {ko_name}")
                else:
                    self.stdout.write(" (번역 없음)")
            except Exception as e:
                self.stdout.write(f" (에러: {e})")
            
            # Rate limiting
            time.sleep(0.5)
        
        return new_translations

    def _search_poe2db(self, en_name: str) -> str | None:
        """poe2db.tw에서 아이템 검색하여 한글 이름 반환"""
        # poe2db.tw 검색 API 또는 페이지 크롤링
        # 아이템 페이지 URL 패턴: https://poe2db.tw/kr/Exalted_Orb
        
        # 영문 이름을 URL 형식으로 변환
        url_name = en_name.replace(" ", "_").replace("'", "")
        url = f"{POE2DB_BASE}/kr/{url_name}"
        
        request = Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
            },
        )
        
        try:
            with urlopen(request, timeout=FETCH_TIMEOUT) as response:
                html = response.read().decode("utf-8")
                
                # 페이지 제목에서 한글 이름 추출
                # <title>고급 오브 - PoE2DB, Path of Exile 2 Wiki</title>
                title_match = re.search(r"<title>([^<]+?)\s*[-–]", html)
                if title_match:
                    ko_name = title_match.group(1).strip()
                    # 영문 이름이 아니면 반환
                    if ko_name and ko_name != en_name and not ko_name.isascii():
                        return ko_name
                
                # og:title에서도 시도
                og_match = re.search(r'property="og:title"\s+content="([^"]+)"', html)
                if og_match:
                    ko_name = og_match.group(1).strip()
                    if ko_name and ko_name != en_name and not ko_name.isascii():
                        return ko_name
                        
        except HTTPError as e:
            if e.code != 404:
                raise
        except URLError:
            pass
        
        return None

    def _update_translations_file(self, existing: dict[str, str], new: dict[str, str]) -> None:
        """ko.json 파일에 새 번역 추가"""
        try:
            data = json.loads(TRANSLATIONS_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError):
            data = {"_meta": {"language": "ko", "source": "https://poe2db.tw/kr/"}}
        
        # 새 번역을 적절한 카테고리에 추가
        if "fetched" not in data:
            data["fetched"] = {}
        
        data["fetched"].update(new)
        data["_meta"]["updated_at"] = __import__("datetime").date.today().isoformat()
        
        TRANSLATIONS_FILE.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8"
        )

