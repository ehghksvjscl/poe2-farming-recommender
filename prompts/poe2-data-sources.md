# PoE2 데이터 분석 참고 사이트

PoE2(Path of Exile 2) 데이터 분석 시 참고할 사이트들입니다.

## 1. poe2db.tw

- **URL**: https://poe2db.tw/
- **한국어**: https://poe2db.tw/kr/
- **용도**: 게임 데이터베이스
  - 아이템 정보 (화폐, 룬, 에센스, 유니크 등)
  - 젬 (스킬 젬, 보조 젬, 혈통 보조)
  - 패시브 스킬 트리
  - 퀘스트 정보
  - 속성 부여 (Modifiers)
  - 제작 정보
- **특징**: 다국어 지원 (TW, CN, US, KR, JP, RU, PT, TH, FR, DE, ES)

## 2. poe2scout.com

- **URL**: https://poe2scout.com/
- **용도**: 시장 가격 API
- **API 엔드포인트**:

### 리그 목록
```
GET https://poe2scout.com/api/leagues
```

응답 예시:
```json
[
  {"value": "Fate of the Vaal", "divinePrice": 465.9, ...},
  {"value": "Standard", "divinePrice": 1694.1, ...}
]
```

### 아이템 가격
```
GET https://poe2scout.com/api/items?category={category}&league={league}
```

**카테고리 목록**:
- `currency` - 화폐
- `runes` - 룬
- `essences` - 에센스
- `fragments` - 조각
- `waystones` - 경로석
- `omens` - 전조
- `catalysts` - 촉매
- `vaultkeys` - 금고 열쇠
- `uncutgems` - 미가공 젬
- `lineagesupportgems` - 혈통 보조 젬
- `ultimatum` - 얼티메이텀
- `ritual` - 의식
- `delirium` - 환영
- `breach` - 균열

## 사용 예시

```bash
# 현재 리그 확인
curl -s "https://poe2scout.com/api/leagues"

# Fate of the Vaal 리그의 화폐 가격 조회
curl -s "https://poe2scout.com/api/items?category=currency&league=Fate%20of%20the%20Vaal"
```

## 주의사항

- 리그는 주기적으로 변경되므로 `/api/leagues`로 최신 리그 확인 권장
- Standard, Hardcore는 영구 리그
- HC(하드코어) 리그는 이름 앞에 "HC " 접두어가 붙음

