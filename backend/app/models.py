from django.db import models


class ContentPreference(models.Model):
    key = models.CharField(max_length=32, unique=True)
    label = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    icon_url = models.URLField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "label"]

    def __str__(self) -> str:
        return f"{self.label} ({self.key})"


class MarketItem(models.Model):
    """poe2scout.com에서 가져온 시장 아이템 정보"""

    CATEGORY_CHOICES = [
        ("currency", "Currency"),
        ("runes", "Runes"),
        ("essences", "Essences"),
        ("fragments", "Fragments"),
        ("waystones", "Waystones"),
        ("omens", "Omens"),
        ("breachstones", "Breachstones"),
        ("deliriuminstill", "Delirium Instill"),
        ("uniques", "Uniques"),
        ("accessory", "Accessory"),
        ("armour", "Armour"),
        ("weapon", "Weapon"),
        ("jewel", "Jewel"),
        ("other", "Other"),
    ]

    item_id = models.IntegerField(unique=True, help_text="poe2scout itemId")
    name = models.CharField(max_length=128)
    name_ko = models.CharField(max_length=128, blank=True, help_text="한국어 이름")
    type = models.CharField(max_length=64, blank=True)
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES)
    category_api_id = models.CharField(max_length=32, blank=True, help_text="poe2scout categoryApiId")
    icon_url = models.URLField(blank=True, default="")
    current_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    league = models.CharField(max_length=64, default="Fate of the Vaal")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-current_price"]
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["league"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.category}) - {self.current_price} exalted"


class PriceHistory(models.Model):
    """아이템 가격 히스토리 (시계열 데이터)"""

    item = models.ForeignKey(MarketItem, on_delete=models.CASCADE, related_name="price_logs")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.IntegerField(default=0, help_text="시장에 올라온 수량")
    recorded_at = models.DateTimeField()

    class Meta:
        ordering = ["-recorded_at"]
        unique_together = ["item", "recorded_at"]
        indexes = [
            models.Index(fields=["item", "recorded_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.item.name} @ {self.recorded_at}: {self.price}"


class FarmingMethod(models.Model):
    """파밍 방법 가이드"""

    DIFFICULTY_CHOICES = [
        ("beginner", "초보자"),
        ("intermediate", "중급"),
        ("advanced", "고급"),
        ("expert", "전문가"),
    ]

    CATEGORY_CHOICES = [
        ("mapping", "맵핑"),
        ("boss", "보스"),
        ("league", "리그 컨텐츠"),
        ("crafting", "제작"),
        ("trading", "거래"),
        ("mechanic", "메카닉"),
    ]

    name = models.CharField(max_length=128, help_text="파밍 방법 이름")
    name_ko = models.CharField(max_length=128, help_text="한국어 이름")
    slug = models.SlugField(unique=True, help_text="URL용 슬러그")
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=16, choices=DIFFICULTY_CHOICES, default="intermediate")
    rating = models.PositiveSmallIntegerField(default=0, help_text="추천 별점 (0-5)")
    
    # 설명
    summary = models.TextField(help_text="요약 설명")
    description = models.TextField(help_text="상세 설명 (마크다운 지원)")
    
    # 파밍 정보
    requirements = models.JSONField(default=list, help_text="필요 조건 리스트")
    recommended_items = models.JSONField(default=list, help_text="추천 아이템/서판 리스트")
    steps = models.JSONField(default=list, help_text="파밍 단계별 가이드")
    tips = models.JSONField(default=list, help_text="팁 리스트")
    
    # 수익 정보
    estimated_profit_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, 
                                                help_text="시간당 최소 예상 수익 (Divine)")
    estimated_profit_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                                help_text="시간당 최대 예상 수익 (Divine)")
    investment_required = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                               help_text="초기 투자 비용 (Divine)")
    
    # 관련 아이템
    related_items = models.ManyToManyField(MarketItem, blank=True, related_name="farming_methods",
                                            help_text="관련 시장 아이템")
    
    # 리그 정보
    league = models.CharField(max_length=64, default="Fate of the Vaal")
    is_league_specific = models.BooleanField(default=False, help_text="리그 한정 컨텐츠 여부")
    
    # 크리에이터 정보
    creator_name = models.CharField(max_length=64, blank=True, help_text="파밍 방법을 알린 크리에이터")
    creator_url = models.URLField(blank=True, help_text="크리에이터 채널 URL")
    
    # 메타
    icon = models.CharField(max_length=64, blank=True, help_text="아이콘 이모지 또는 클래스")
    video_url = models.URLField(blank=True, help_text="유튜브 가이드 영상 URL")
    source_url = models.URLField(blank=True, help_text="출처 URL")
    
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "-estimated_profit_max"]
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["difficulty"]),
            models.Index(fields=["league"]),
        ]

    def __str__(self) -> str:
        return f"{self.name_ko} ({self.category})"
