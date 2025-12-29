from django.db import migrations, models


def seed_content_preferences(apps, schema_editor):
    ContentPreference = apps.get_model("app", "ContentPreference")
    content = [
        {
            "key": "mapping",
            "label": "맵핑",
            "description": "경로석 파밍",
            "icon_url": "https://web.poecdn.com/gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvUXVlc3RJdGVtcy9QaW5uYWNsZUtleTEiLCJ3IjoxLCJoIjoxLCJzY2FsZSI6MSwicmVhbG0iOiJwb2UyIn1d/0d3dddab3b/PinnacleKey1.png",
            "sort_order": 1,
        },
        {
            "key": "bossing",
            "label": "보스",
            "description": "보스 킬링",
            "icon_url": "https://web.poecdn.com/gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQXJtb3Vycy9IZWxtZXRzL1VuaXF1ZXMvQ3Jvd25PZlRoZVZpY3RvciIsInciOjIsImgiOjIsInNjYWxlIjoxLCJyZWFsbSI6InBvZTIifV0/8397c94ec0/CrownOfTheVictor.png",
            "sort_order": 2,
        },
        {
            "key": "expedition",
            "label": "탐험",
            "description": "탐험 콘텐츠",
            "icon_url": "https://web.poecdn.com/gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvRXhwZWRpdGlvbi9CYXJ0ZXJSZWZyZXNoQ3VycmVuY3kiLCJ3IjoxLCJoIjoxLCJzY2FsZSI6MSwicmVhbG0iOiJwb2UyIn1d/b0f42eaf8d/BarterRefreshCurrency.png",
            "sort_order": 3,
        },
        {
            "key": "ritual",
            "label": "의식",
            "description": "의식 제단",
            "icon_url": "https://web.poecdn.com/gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvT21lbnMvVm9vZG9vT21lbnMxUmVkIiwidyI6MSwiaCI6MSwic2NhbGUiOjEsInJlYWxtIjoicG9lMiJ9XQ/1c90d2eb1f/VoodooOmens1Red.png",
            "sort_order": 4,
        },
        {
            "key": "breach",
            "label": "균열",
            "description": "균열 파밍",
            "icon_url": "https://web.poecdn.com/gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvQnJlYWNoL0JyZWFjaENhdGFseXN0RmlyZSIsInciOjEsImgiOjEsInNjYWxlIjoxLCJyZWFsbSI6InBvZTIifV0/156de12dd6/BreachCatalystFire.png",
            "sort_order": 5,
        },
        {
            "key": "delirium",
            "label": "환영",
            "description": "환영 콘텐츠",
            "icon_url": "https://web.poecdn.com/gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvRGlzdGlsbGVkRW1vdGlvbnMvRGlzdGlsbGVkRGVzcGFpciIsInciOjEsImgiOjEsInNjYWxlIjoxLCJyZWFsbSI6InBvZTIifV0/794fb40302/DistilledDespair.png",
            "sort_order": 6,
        },
        {
            "key": "heist",
            "label": "강탈",
            "description": "강탈 계약서",
            "icon_url": "https://web.poecdn.com/gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvSW5jdXJzaW9uQ3JhZnRpbmdPcmJzL0luY3Vyc2lvbkdyZWF0ZXJWYWFsT3JiIiwic2NhbGUiOjEsInJlYWxtIjoicG9lMiJ9XQ/7ba6f79f63/IncursionGreaterVaalOrb.png",
            "sort_order": 7,
        },
        {
            "key": "abyss",
            "label": "심연",
            "description": "심연 콘텐츠",
            "icon_url": "https://web.poecdn.com//gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvQWJ5c3MvUHJlc2VydmVkSmF3Ym9uZSIsInNjYWxlIjoxLCJyZWFsbSI6InBvZTIifV0/2bb7939b21/PreservedJawbone.png",
            "sort_order": 8,
        },
    ]
    ContentPreference.objects.bulk_create(
        [ContentPreference(**item) for item in content],
        ignore_conflicts=True,
    )


def remove_content_preferences(apps, schema_editor):
    ContentPreference = apps.get_model("app", "ContentPreference")
    ContentPreference.objects.filter(
        key__in=[
            "mapping",
            "bossing",
            "expedition",
            "ritual",
            "breach",
            "delirium",
            "heist",
            "abyss",
        ]
    ).delete()


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ContentPreference",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.CharField(max_length=32, unique=True)),
                ("label", models.CharField(max_length=64)),
                ("description", models.CharField(max_length=255)),
                ("icon_url", models.URLField()),
                ("sort_order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["sort_order", "label"]},
        ),
        migrations.RunPython(seed_content_preferences, remove_content_preferences),
    ]
