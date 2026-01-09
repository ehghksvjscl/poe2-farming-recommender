# My Project

Django + React 풀스택 프로젝트 템플릿

## 프로젝트 구조

```
.
├── backend/          # Django REST Framework 백엔드
│   ├── app/          # 메인 앱
│   ├── config/       # Django 설정
│   └── data/         # 데이터 파일
├── frontend/         # React (Vite) 프론트엔드
│   └── src/
│       ├── components/
│       ├── hooks/
│       └── utils/
├── docs/             # 문서
├── prompts/          # AI 프롬프트
└── scripts/          # 자동화 스크립트
```

## 실행 방법

### 한 번에 실행하기
```bash
./start-dev.sh
```

### 개별 실행하기

#### 1. 백엔드 (Django)
```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 마이그레이션
python manage.py migrate

# 서버 실행 (http://localhost:8000)
python manage.py runserver
```

#### 2. 프론트엔드 (React)
```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행 (http://localhost:5173)
npm run dev
```

## API 엔드포인트

- `GET /api/health/` - 헬스체크

## 환경 변수

### Backend (`backend/.env`)
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Frontend (`frontend/.env`)
```
VITE_API_URL=http://localhost:8000/api
```
