from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class RecommendationInput:
    preferred_content: List[str] = field(default_factory=list)
    profit_goal: str = "medium"
    investment: str = "low"
    league: str = "Fate of the Vaal"


# 샘플 파밍 가이드 데이터 (추후 DB/JSON으로 분리)
FARMING_GUIDES = [
    {
        "id": "mapping-alch-go",
        "zone": "T16 경로석 알키앤고",
        "content_types": ["mapping"],
        "investment": "zero",
        "profit_range": {"low": True, "medium": True},
        "avg_profit_per_hour": "2-4 Divine",
        "drop_focus": "화폐, 경로석",
        "reason": "초보자도 쉽게 시작할 수 있는 기본 맵핑 파밍입니다. 투자 없이 바로 시작 가능합니다.",
        "strategy": "T16 경로석에 연금술 오브를 사용하고 바로 클리어합니다. 맵 보스를 빠르게 처치하고 다음 맵으로 이동하세요.",
        "requirements": "T16 경로석, 연금술 오브",
        "tips": "맵 클리어 속도가 수익과 직결됩니다. 불필요한 몬스터는 스킵하세요.",
    },
    {
        "id": "expedition-logbook",
        "zone": "탐험 항해일지",
        "content_types": ["expedition"],
        "investment": "medium",
        "profit_range": {"medium": True, "high": True},
        "avg_profit_per_hour": "5-10 Divine",
        "drop_focus": "룬 파편, 유물, 화폐",
        "reason": "안정적인 고수익 콘텐츠입니다. 항해일지 가격 대비 좋은 수익률을 보장합니다.",
        "strategy": "항해일지에서 화폐 보상과 유물 상인을 우선적으로 선택합니다. 폭발물 배치 시 최대한 많은 몬스터를 포함시키세요.",
        "requirements": "항해일지, 폭발물 충분히",
        "tips": "다누이 유물과 투젠 도박이 핵심 수익원입니다.",
    },
    {
        "id": "ritual-farming",
        "zone": "의식 파밍",
        "content_types": ["ritual", "mapping"],
        "investment": "low",
        "profit_range": {"low": True, "medium": True},
        "avg_profit_per_hour": "3-6 Divine",
        "drop_focus": "전조, 청원 파편, 화폐",
        "reason": "맵핑과 함께 추가 수익을 얻을 수 있습니다. 전조 아이템이 고가에 거래됩니다.",
        "strategy": "의식 제단에서 고가 전조 아이템을 우선 선택합니다. 연기(Defer) 기능을 활용해 좋은 아이템을 모으세요.",
        "requirements": "의식 스카랍 또는 아틀라스 패시브",
        "tips": "고가 전조(삭제의 전조, 고귀화의 전조)를 노리세요.",
    },
    {
        "id": "breach-farming",
        "zone": "균열 파밍",
        "content_types": ["breach"],
        "investment": "low",
        "profit_range": {"low": True, "medium": True},
        "avg_profit_per_hour": "3-5 Divine",
        "drop_focus": "균열 파편, 촉매, 균열석",
        "reason": "균열 파편과 촉매가 꾸준한 수익을 제공합니다. 균열 보스 도전도 가능합니다.",
        "strategy": "균열 스카랍을 사용하여 맵에서 균열을 다수 생성합니다. 균열 내 몬스터를 최대한 빠르게 처치하세요.",
        "requirements": "균열 스카랍",
        "tips": "촉매 수집에 집중하면 안정적인 수익을 얻을 수 있습니다.",
    },
    {
        "id": "boss-farming",
        "zone": "보스 파밍 (불타는 거석)",
        "content_types": ["bossing"],
        "investment": "high",
        "profit_range": {"high": True, "extreme": True},
        "avg_profit_per_hour": "10-20+ Divine",
        "drop_focus": "유니크 장비, 보스 전용 드랍",
        "reason": "고투자 고수익 콘텐츠입니다. 보스 전용 유니크와 조각이 높은 가격에 거래됩니다.",
        "strategy": "정점 열쇠 조각을 모아 보스에 도전합니다. 보스 메카닉을 숙지하고 빠른 킬을 목표로 하세요.",
        "requirements": "정점 열쇠 조각, 보스 메카닉 이해",
        "tips": "보스별 드랍 테이블을 확인하고 수익성 높은 보스를 선택하세요.",
    },
    {
        "id": "delirium-farming",
        "zone": "환영 파밍",
        "content_types": ["delirium", "mapping"],
        "investment": "medium",
        "profit_range": {"medium": True, "high": True},
        "avg_profit_per_hour": "6-12 Divine",
        "drop_focus": "시뮬라크럼 파편, 환영 오브, 클러스터 주얼",
        "reason": "환영 안개가 추가 보상을 대폭 증가시킵니다. 고밀도 몬스터로 빠른 파밍이 가능합니다.",
        "strategy": "환영 오브를 사용하여 맵 전체에 환영을 적용합니다. 안개가 사라지기 전 최대한 많은 몬스터를 처치하세요.",
        "requirements": "환영 오브, 빠른 클리어 속도",
        "tips": "시뮬라크럼 파편을 모아 시뮬라크럼에 도전하면 추가 수익을 얻을 수 있습니다.",
    },
]


def build_recommendations(request: RecommendationInput):
    results = []
    
    for guide in FARMING_GUIDES:
        # 콘텐츠 타입 필터링
        if request.preferred_content:
            if not any(ct in guide["content_types"] for ct in request.preferred_content):
                continue
        
        # 투자 수준 필터링
        if request.investment != guide["investment"]:
            # 무자본은 소자본도 포함, 소자본은 중자본도 일부 포함
            investment_order = ["zero", "low", "medium", "high"]
            req_idx = investment_order.index(request.investment)
            guide_idx = investment_order.index(guide["investment"])
            if guide_idx > req_idx + 1:  # 1단계 초과 차이나면 제외
                continue
        
        # 수익 목표 필터링
        if request.profit_goal not in guide["profit_range"]:
            continue
        
        results.append({
            "zone": guide["zone"],
            "league": request.league,
            "avg_profit_per_hour": guide["avg_profit_per_hour"],
            "drop_focus": guide["drop_focus"],
            "reason": guide["reason"],
            "investment": guide["investment"],
            "strategy": guide.get("strategy"),
            "requirements": guide.get("requirements"),
            "tips": guide.get("tips"),
        })
    
    return results
