# 추천 로직 서버 확정 및 API 스펙 초안

## 1) 추천 로직 실행 위치: **서버**

추천 로직은 **서버에서 실행**하는 것으로 확정한다. 주요 이유는 아래와 같다.

### 데이터 크기
- 추천은 아이템 메타, 드랍 테이블, 지도/콘텐츠 보정값, 시세(가격) 등 **대형 데이터**를 참조한다.
- 이를 클라이언트로 전송/캐싱하면 **전송량 증가**와 **초기 로딩 지연**이 커진다.
- 서버 실행 시 필요한 데이터만 조회/가공해 **응답 페이로드를 최소화**할 수 있다.

### 업데이트
- 시세/보상 테이블은 **잦은 업데이트**가 발생한다.
- 서버 실행은 **중앙 집중 업데이트**가 가능하여, 배포/버전 관리 비용을 줄인다.
- 클라이언트 캐시 갱신 문제(낡은 추천 로직/데이터)도 최소화된다.

### 일관성
- 클라이언트마다 환경(브라우저, 메모리, 캐시 상태)이 달라 **결과가 달라질 수 있음**.
- 서버에서 동일 데이터/알고리즘을 사용하면 **결과 일관성**을 확보할 수 있다.
- 재현 가능한 추천 결과는 A/B 테스트, 로그 분석에도 유리하다.

## 2) API 스펙 초안

> 베이스 URL 예시: `/api`

### 2.1 `POST /recommend`
추천 결과를 요청한다.

**Request Body (예시)**
```json
{
  "league": "Standard",
  "budget": "medium",
  "playstyle": ["fast-clear", "bossing"],
  "build_tags": ["totem", "minion"],
  "filters": {
    "reward_types": ["currency", "unique"],
    "content_types": ["maps", "delve"],
    "min_profit_per_hour": 5.0
  },
  "pagination": {
    "limit": 20,
    "offset": 0
  }
}
```

**Response (예시)**
```json
{
  "meta": {
    "league": "Standard",
    "total": 125,
    "limit": 20,
    "offset": 0,
    "updated_at": "2024-01-01T00:00:00Z"
  },
  "recommendations": [
    {
      "id": "map-juiced-alch-and-go",
      "title": "주스 맵핑 - 알치앤고",
      "summary": "낮은 진입비용으로 빠른 회전",
      "reward": {
        "avg_profit_per_hour": 6.2,
        "drop_focus": ["currency", "scarab"]
      },
      "requirements": {
        "budget": "low",
        "content_types": ["maps"],
        "build_tags": ["fast-clear"]
      },
      "tags": ["mapping", "budget-friendly"]
    }
  ]
}
```

### 2.2 `GET /items`
추천에 사용되는 아이템/자원 목록(필터 옵션 포함)을 조회한다.

**Query Params (예시)**
- `league`: 리그
- `type`: `currency` | `unique` | `scarab` | `fragment`
- `search`: 검색어
- `limit`, `offset`

**Response (예시)**
```json
{
  "meta": { "total": 320, "limit": 50, "offset": 0 },
  "items": [
    { "id": "divine-orb", "name": "Divine Orb", "type": "currency" }
  ]
}
```

### 2.3 `GET /filters`
추천 필터 UI에 필요한 **가능한 값의 리스트**를 제공한다. `league`는 단일 선택이다.

**Response (예시)**
```json
{
  "league": "Standard",
  "reward_types": ["currency", "unique", "divination", "scarab"],
  "content_types": ["maps", "delve", "heist", "expedition"],
  "build_tags": ["fast-clear", "bossing", "totem", "minion"]
}
```

## 3) 클라이언트 역할 범위

클라이언트는 아래 역할로 **범위를 제한**한다.

- 사용자 입력 수집 및 검증(필터/검색)
- API 호출(`/recommend`, `/items`, `/filters`)
- 응답 데이터 렌더링(리스트/상세/정렬/페이징)
- 상태 관리(로딩/에러/빈 결과)

추천 로직, 데이터 통합/정규화, 모델링/랭킹은 **서버 전담**으로 유지한다.
