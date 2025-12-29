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
