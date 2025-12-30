"""
파밍 가이드 데이터를 JSON 파일에서 로드하여 DB에 저장하는 커맨드
"""
import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from app.models import FarmingMethod


class Command(BaseCommand):
    help = "farming_guides.json에서 파밍 가이드를 로드하여 DB에 저장합니다."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="기존 데이터를 모두 삭제하고 새로 로드합니다.",
        )

    def handle(self, *args, **options):
        clear = options["clear"]

        # JSON 파일 경로
        json_path = Path(__file__).resolve().parent.parent.parent.parent / "data" / "farming_guides.json"

        if not json_path.exists():
            self.stdout.write(self.style.ERROR(f"파일을 찾을 수 없습니다: {json_path}"))
            return

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        league = data.get("league", "Fate of the Vaal")
        methods = data.get("methods", [])

        self.stdout.write(f"리그: {league}")
        self.stdout.write(f"파밍 방법: {len(methods)}개")

        if clear:
            self.stdout.write(self.style.WARNING("기존 데이터 삭제 중..."))
            FarmingMethod.objects.all().delete()

        created_count = 0
        updated_count = 0

        with transaction.atomic():
            for i, method_data in enumerate(methods):
                slug = method_data.get("slug")
                if not slug:
                    self.stdout.write(self.style.WARNING(f"  ⚠️ slug 없음: {method_data.get('name')}"))
                    continue

                defaults = {
                    "name": method_data.get("name", ""),
                    "name_ko": method_data.get("name_ko", ""),
                    "category": method_data.get("category", "mapping"),
                    "difficulty": method_data.get("difficulty", "intermediate"),
                    "rating": method_data.get("rating", 0),
                    "summary": method_data.get("summary", ""),
                    "description": method_data.get("description", ""),
                    "requirements": method_data.get("requirements", []),
                    "recommended_items": method_data.get("recommended_items", []),
                    "steps": method_data.get("steps", []),
                    "tips": method_data.get("tips", []),
                    "estimated_profit_min": method_data.get("estimated_profit_min"),
                    "estimated_profit_max": method_data.get("estimated_profit_max"),
                    "investment_required": method_data.get("investment_required", 0),
                    "league": league,
                    "is_league_specific": method_data.get("is_league_specific", False),
                    "icon": method_data.get("icon", ""),
                    "creator_name": method_data.get("creator_name", ""),
                    "creator_url": method_data.get("creator_url", ""),
                    "video_url": method_data.get("video_url", ""),
                    "source_url": method_data.get("source_url", ""),
                    "sort_order": i,
                    "is_active": True,
                }

                obj, created = FarmingMethod.objects.update_or_create(
                    slug=slug,
                    defaults=defaults,
                )

                if created:
                    created_count += 1
                    self.stdout.write(f"  ✅ 생성: {obj.name_ko}")
                else:
                    updated_count += 1
                    self.stdout.write(f"  🔄 업데이트: {obj.name_ko}")

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(f"완료! 생성: {created_count}개, 업데이트: {updated_count}개")
        )

