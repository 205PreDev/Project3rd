# AI 이커머스 이미지 생성기

AI를 활용하여 상품 이미지의 배경을 자동으로 교체하고 광고 문구를 생성하는 서비스입니다.

## 시나리오

온라인 판매자를 위한 올인원 AI 마케팅 솔루션입니다.
상품 사진만 업로드하면 AI가 배경을 제거하고, SNS 플랫폼별 맞춤형 배경과 광고 문구를 자동 생성합니다.
디자인 툴이나 마케팅 지식 없이도 3초 만에 전문가급 광고 콘텐츠를 제작할 수 있습니다.

## 주요 기능

- 🖼️ **자동 배경 제거**: Rembg를 사용한 AI 기반 배경 제거
- 🎨 **배경 합성**: Unsplash 무료 이미지를 활용한 배경 교체
- ✍️ **광고 문구 생성**: GPT-4o-mini를 사용한 자동 광고 문구 생성
- 💾 **이미지 관리**: 생성된 이미지 저장 및 관리
- 👤 **사용자 인증**: 회원가입 및 로그인 기능

## 기술 스택

### Backend
- FastAPI 0.109.0
- Python 3.11+
- SQLAlchemy 2.0
- Supabase (PostgreSQL + Storage)
- Rembg (배경 제거)
- OpenAI GPT-4o-mini
- Unsplash API

### Frontend
- React 18
- TypeScript
- Vite
- TailwindCSS
- TanStack Query
- React Hook Form + Zod

### Infrastructure
- Docker & Docker Compose
- Render (호스팅)
- PostgreSQL 15

## 시작하기

### 사전 요구사항

- Docker & Docker Compose
- Node.js 18+
- Python 3.11+

### 환경 변수 설정

1. 루트 디렉토리에 `.env` 파일 생성:
```bash
cp .env.example .env
```

2. 필요한 API 키 설정:
- OpenAI API Key: https://platform.openai.com/api-keys
- Unsplash Access Key: https://unsplash.com/developers
- Supabase URL & Key: https://supabase.com/

### Docker Compose로 실행

```bash
# 모든 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 서비스 중지
docker-compose down
```

서비스 접속:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 로컬 개발 환경

#### Backend

```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일 수정

# 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend

# 의존성 설치
npm install

# 환경 변수 설정
cp .env.example .env
# .env 파일 수정

# 개발 서버 실행
npm run dev
```

## 프로젝트 구조

```
Project3rd/
├── backend/                # FastAPI 백엔드
│   ├── app/
│   │   ├── core/          # 설정, 보안
│   │   ├── api/           # API 라우터
│   │   ├── models/        # 데이터베이스 모델
│   │   ├── schemas/       # Pydantic 스키마
│   │   └── services/      # 비즈니스 로직
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # React 프론트엔드
│   ├── src/
│   │   ├── components/    # React 컴포넌트
│   │   ├── pages/         # 페이지 컴포넌트
│   │   ├── hooks/         # 커스텀 훅
│   │   ├── api/           # API 클라이언트
│   │   └── types/         # TypeScript 타입
│   ├── package.json
│   └── Dockerfile
├── ai/                     # AI 모델 및 스크립트
├── docs/                   # 문서
├── docker-compose.yml
└── README.md
```

## API 문서

서버 실행 후 http://localhost:8000/docs 에서 Swagger UI를 통해 API 문서를 확인할 수 있습니다.

## 개발 로드맵

자세한 개발 계획은 [작업 계획서.md](./작업%20계획서.md)를 참고하세요.

### Week 1-2: 프로젝트 세팅 & 기본 구조 ✅
- 프로젝트 디렉토리 구조 생성
- Backend 보일러플레이트 (FastAPI)
- Frontend 보일러플레이트 (React + Vite)
- Docker Compose 환경 구성
- 환경 변수 파일 생성

### Week 3-4: 사용자 인증 & 데이터베이스
- FastAPI-Users 설정
- 회원가입/로그인 API
- PostgreSQL 연동
- Supabase 설정

### Week 5-7: 이미지 처리 & AI 기능
- Rembg 배경 제거
- Unsplash API 연동
- 이미지 합성 기능
- GPT-4o-mini 광고 문구 생성

### Week 8-9: 프론트엔드 UI
- 이미지 업로드 컴포넌트
- 배경 선택 UI
- 결과 미리보기
- 반응형 디자인

### Week 10-11: 배포 & 최적화
- Render 배포
- 이미지 최적화
- 에러 처리
- 로딩 상태 개선

### Week 12: 테스트 & 문서화
- 통합 테스트
- 사용자 매뉴얼
- 배포 문서

## 비용 예산

MVP 단계: 월 $10-40
- Render (Backend): $7/월 (Hobby) ~ $25/월 (Professional)
- Supabase: 무료 (Free tier)
- OpenAI API: 약 $3-10/월 (GPT-4o-mini 사용)
- Unsplash API: 무료 (50 requests/hour)

## 협업 전략

### 브랜치 전략 (GitHub Flow)
- `main`: 프로덕션 브랜치
- `feature/*`: 기능 개발 브랜치
- 브랜치 명명: `feature/issue번호-기능명`

### 병렬 작업 + 협업 집중
1. **개별 초안 작업 (80% 시간)**
   - 각자 feature 브랜치에서 작업
   - 일일 스탠드업으로 진행 상황 공유

2. **협업 집중 (20% 시간)**
   - 통합 이슈 해결
   - 페어 프로그래밍
   - 코드 리뷰

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 팀

3인 협업 프로젝트 (12주 개발 기간)

## 문의

이슈나 질문이 있으시면 GitHub Issues를 통해 문의해주세요.
