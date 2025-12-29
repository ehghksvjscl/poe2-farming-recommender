from dataclasses import dataclass


@dataclass(frozen=True)
class RecommendationInput:
    level: int
    build_type: str
    preferred_content: str


def build_recommendations(request: RecommendationInput):
    return [
        {
            "zone": "Drowned City",
            "league": "Standard",
            "avg_profit_per_hour": "3.2 Divine",
            "drop_focus": "지도, 유니크",
            "allowed_builds": ["콜드 DOT", "활 빌드"],
            "reason": f"{request.build_type}에 적합하며 안정적인 맵핑 루트입니다.",
        },
        {
            "zone": "Crystal Vault",
            "league": "Season 1",
            "avg_profit_per_hour": "4.1 Divine",
            "drop_focus": "카드, 통화",
            "allowed_builds": ["토템", "미니언"],
            "reason": f"{request.preferred_content} 중심으로 높은 수익을 기대할 수 있습니다.",
        },
    ]
