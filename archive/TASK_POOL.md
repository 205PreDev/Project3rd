# 🎯 Task Pool - 세부 작업 목록

> **작업 방식**: 각 팀원이 자유롭게 태스크를 선택하여 진행
> **업데이트**: GitHub Issues로 관리, 진행 상황은 Projects 칸반 보드에서 추적
> **작성일**: 2025-10-17

---

## 📌 태스크 라벨 시스템

### Priority (우선순위)
- 🔴 **P0 - Critical**: 다른 작업의 블로커, 즉시 처리 필요
- 🟠 **P1 - High**: 이번 주 내 완료 필요
- 🟡 **P2 - Medium**: 다음 주 목표
- 🟢 **P3 - Low**: 여유 있을 때 진행

### Difficulty (난이도)
- 🟢 **Easy**: 1-2시간, 독립 작업 가능
- 🟡 **Medium**: 3-6시간, 기본 지식 필요
- 🔴 **Hard**: 1-2일, 복잡하거나 협업 필요

### Area (영역)
- `backend` `frontend` `ai` `devops` `docs` `testing`

### Status (상태)
- 📝 **Todo**: 시작 전
- 🏃 **In Progress**: 진행 중
- 👀 **Review**: 리뷰 대기
- ✅ **Done**: 완료

---

## 🔥 Week 5 - Critical Tasks (다음 주 필수)

### Backend 환경 설정 및 검증

#### TASK-001: Python 가상환경 설정 및 패키지 설치
- **Priority**: 🔴 P0
- **Difficulty**: 🟢 Easy (1-2h)
- **Area**: `backend` `devops`
- **의존성**: 없음
- **작업 내용**:
  ```bash
  cd backend
  python -m venv venv
  source venv/bin/activate  # Windows: venv\Scripts\activate
  pip install -r requirements.txt
  pip list > installed_packages.txt  # 검증용
  ```
- **완료 조건**:
  - [ ] 가상환경 활성화 성공
  - [ ] 모든 패키지 설치 완료 (에러 없음)
  - [ ] `installed_packages.txt` 커밋

---

#### TASK-002: .env 파일 설정
- **Priority**: 🔴 P0
- **Difficulty**: 🟢 Easy (1h)
- **Area**: `backend` `devops`
- **의존성**: TASK-001
- **작업 내용**:
  - `.env.example` 복사하여 `.env` 생성
  - Supabase 프로젝트 생성 (무료 티어)
  - DATABASE_URL, SUPABASE_URL, SUPABASE_KEY 설정
  - SECRET_KEY 생성 (`openssl rand -hex 32`)
- **완료 조건**:
  - [ ] `.env` 파일 생성 (gitignore 확인)
  - [ ] Supabase 프로젝트 생성 완료
  - [ ] 모든 환경 변수 설정 완료
  - [ ] `.env` 설정 가이드 문서화 (docs/SETUP.md)

---

#### TASK-003: PostgreSQL 데이터베이스 연결 테스트
- **Priority**: 🔴 P0
- **Difficulty**: 🟡 Medium (2h)
- **Area**: `backend`
- **의존성**: TASK-002
- **작업 내용**:
  - Supabase PostgreSQL 연결 확인
  - SQLAlchemy 연결 테스트 스크립트 작성
  - 연결 풀 설정 확인
- **완료 조건**:
  - [ ] 데이터베이스 연결 성공
  - [ ] 테스트 쿼리 실행 성공
  - [ ] 연결 테스트 스크립트 작성 (`scripts/test_db.py`)

---

#### TASK-004: Alembic 마이그레이션 적용
- **Priority**: 🔴 P0
- **Difficulty**: 🟡 Medium (2h)
- **Area**: `backend`
- **의존성**: TASK-003
- **작업 내용**:
  ```bash
  cd backend
  alembic upgrade head
  ```
- **완료 조건**:
  - [ ] 마이그레이션 성공 (에러 없음)
  - [ ] Supabase Dashboard에서 테이블 생성 확인
  - [ ] users, projects, images 테이블 존재 확인

---

#### TASK-005: FastAPI 서버 실행 및 Swagger UI 테스트
- **Priority**: 🔴 P0
- **Difficulty**: 🟢 Easy (1h)
- **Area**: `backend`
- **의존성**: TASK-004
- **작업 내용**:
  ```bash
  uvicorn app.main:app --reload
  ```
  - 브라우저에서 `http://localhost:8000/docs` 접속
  - Swagger UI에서 API 문서 확인
- **완료 조건**:
  - [ ] 서버 실행 성공 (에러 없음)
  - [ ] Swagger UI 정상 로딩
  - [ ] API 엔드포인트 목록 확인

---

#### TASK-006: API 엔드포인트 통합 테스트
- **Priority**: 🟠 P1
- **Difficulty**: 🟡 Medium (3h)
- **Area**: `backend` `testing`
- **의존성**: TASK-005
- **작업 내용**:
  - Swagger UI에서 아래 플로우 테스트:
    1. POST `/api/v1/auth/register` - 회원가입
    2. POST `/api/v1/auth/jwt/login` - 로그인
    3. GET `/api/v1/auth/users/me` - 사용자 정보 조회
    4. POST `/api/v1/projects/` - 프로젝트 생성
    5. GET `/api/v1/credits/balance` - 크레딧 잔액 조회
  - 각 API 응답 검증
- **완료 조건**:
  - [ ] 회원가입/로그인 성공
  - [ ] JWT 토큰 발급 확인
  - [ ] 프로젝트 생성 성공
  - [ ] 크레딧 시스템 동작 확인
  - [ ] 테스트 결과 문서화 (`docs/API_TEST.md`)

---

### Frontend 기본 구조

#### TASK-007: React + TypeScript + Vite 프로젝트 검증
- **Priority**: 🟠 P1
- **Difficulty**: 🟢 Easy (1h)
- **Area**: `frontend`
- **의존성**: 없음
- **작업 내용**:
  ```bash
  cd frontend
  npm install
  npm run dev
  ```
  - 브라우저에서 `http://localhost:5173` 접속
- **완료 조건**:
  - [ ] 프로젝트 빌드 성공
  - [ ] 개발 서버 실행 성공
  - [ ] 기본 페이지 로딩 확인

---

#### TASK-008: TailwindCSS + shadcn/ui 설정
- **Priority**: 🟠 P1
- **Difficulty**: 🟡 Medium (2h)
- **Area**: `frontend`
- **의존성**: TASK-007
- **작업 내용**:
  - TailwindCSS 설정 확인
  - shadcn/ui 초기화 (`npx shadcn-ui@latest init`)
  - Button, Input, Card 컴포넌트 추가
- **완료 조건**:
  - [ ] TailwindCSS 정상 동작
  - [ ] shadcn/ui 설치 완료
  - [ ] 기본 컴포넌트 import 테스트 성공

---

#### TASK-009: React Router v6 라우팅 설정
- **Priority**: 🟠 P1
- **Difficulty**: 🟡 Medium (2-3h)
- **Area**: `frontend`
- **의존성**: TASK-007
- **작업 내용**:
  - React Router 설치 및 설정
  - 기본 라우트 구조 생성:
    - `/` - 메인 페이지
    - `/login` - 로그인
    - `/register` - 회원가입
    - `/dashboard` - 대시보드
    - `/project/:id` - 프로젝트 상세
  - Layout 컴포넌트 생성 (헤더, 사이드바, 푸터)
- **완료 조건**:
  - [ ] 라우팅 설정 완료
  - [ ] 각 페이지 skeleton 생성
  - [ ] 페이지 간 네비게이션 동작 확인

---

#### TASK-010: API 클라이언트 설정 (fetch wrapper)
- **Priority**: 🟠 P1
- **Difficulty**: 🟡 Medium (3h)
- **Area**: `frontend`
- **의존성**: TASK-007
- **작업 내용**:
  - `src/lib/api.ts` 생성
  - fetch wrapper 구현 (JWT 토큰 자동 포함)
  - 에러 핸들링 (401, 403, 500 등)
  - 타입 정의 (`src/types/api.ts`)
- **완료 조건**:
  - [ ] API 클라이언트 구현
  - [ ] TypeScript 타입 정의
  - [ ] 기본 CRUD 함수 작성 (get, post, put, delete)

---

#### TASK-011: TanStack Query (React Query) 설정
- **Priority**: 🟠 P1
- **Difficulty**: 🟡 Medium (2h)
- **Area**: `frontend`
- **의존성**: TASK-010
- **작업 내용**:
  - TanStack Query 설치
  - QueryClient 설정
  - React Query DevTools 추가
  - 기본 커스텀 훅 작성 (`useAuth`, `useProjects`)
- **완료 조건**:
  - [ ] React Query 설정 완료
  - [ ] DevTools 동작 확인
  - [ ] 예시 커스텀 훅 작성

---

#### TASK-012: 로그인 페이지 UI 구현
- **Priority**: 🟠 P1
- **Difficulty**: 🟢 Easy (2-3h)
- **Area**: `frontend`
- **의존성**: TASK-008, TASK-009
- **작업 내용**:
  - `/login` 페이지 UI 구현
  - React Hook Form + Zod 폼 validation
  - shadcn/ui 컴포넌트 사용 (Input, Button, Card)
  - 에러 메시지 표시
- **완료 조건**:
  - [ ] 로그인 페이지 UI 완성
  - [ ] 폼 validation 동작 확인
  - [ ] 반응형 디자인 적용

---

#### TASK-013: 회원가입 페이지 UI 구현
- **Priority**: 🟠 P1
- **Difficulty**: 🟢 Easy (2-3h)
- **Area**: `frontend`
- **의존성**: TASK-008, TASK-009
- **작업 내용**:
  - `/register` 페이지 UI 구현
  - 이메일, 비밀번호, 비밀번호 확인 필드
  - React Hook Form + Zod validation
  - 비밀번호 강도 표시 (선택)
- **완료 조건**:
  - [ ] 회원가입 페이지 UI 완성
  - [ ] 비밀번호 확인 validation
  - [ ] 반응형 디자인 적용

---

#### TASK-014: 인증 Context/Hook 구현
- **Priority**: 🟠 P1
- **Difficulty**: 🟡 Medium (3-4h)
- **Area**: `frontend`
- **의존성**: TASK-010, TASK-011
- **작업 내용**:
  - `src/contexts/AuthContext.tsx` 생성
  - JWT 토큰 localStorage 관리
  - `useAuth` 훅 구현 (login, logout, register)
  - Protected Route 컴포넌트 생성
- **완료 조건**:
  - [ ] AuthContext 구현
  - [ ] 로그인/로그아웃 동작 확인
  - [ ] Protected Route 동작 확인

---

#### TASK-015: 로그인/회원가입 API 연동
- **Priority**: 🟠 P1
- **Difficulty**: 🟡 Medium (3h)
- **Area**: `frontend`
- **의존성**: TASK-006, TASK-012, TASK-013, TASK-014
- **작업 내용**:
  - 로그인 API 호출 연동
  - 회원가입 API 호출 연동
  - 성공 시 JWT 토큰 저장
  - 성공 후 대시보드로 리다이렉트
  - 에러 처리 및 메시지 표시
- **완료 조건**:
  - [ ] 로그인 API 연동 성공
  - [ ] 회원가입 API 연동 성공
  - [ ] 토큰 저장 및 자동 로그인 동작
  - [ ] 에러 핸들링 완료

---

### AI/DevOps 기본 구조

#### TASK-016: Docker Compose 환경 검증
- **Priority**: 🟠 P1
- **Difficulty**: 🟢 Easy (1-2h)
- **Area**: `devops`
- **의존성**: 없음
- **작업 내용**:
  ```bash
  docker-compose up -d
  docker-compose ps
  docker-compose logs
  ```
- **완료 조건**:
  - [ ] Docker Compose 실행 성공
  - [ ] 모든 컨테이너 정상 동작
  - [ ] 로그 확인 (에러 없음)

---

#### TASK-017: Rembg 배경 제거 프로토타입 스크립트
- **Priority**: 🟠 P1
- **Difficulty**: 🟡 Medium (3-4h)
- **Area**: `ai`
- **의존성**: 없음
- **작업 내용**:
  - `ai/scripts/background_removal.py` 생성
  - Rembg 라이브러리 사용
  - 샘플 이미지로 테스트
  - 입력/출력 경로 파라미터화
- **완료 조건**:
  - [ ] 배경 제거 스크립트 작성
  - [ ] 샘플 이미지 테스트 성공
  - [ ] 처리 시간 측정 (10초 이내 목표)
  - [ ] 결과 이미지 품질 확인

---

#### TASK-018: Unsplash API 연동 테스트
- **Priority**: 🟠 P1
- **Difficulty**: 🟢 Easy (2h)
- **Area**: `ai`
- **의존성**: 없음
- **작업 내용**:
  - Unsplash 개발자 계정 생성
  - Access Key 발급
  - `ai/scripts/test_unsplash.py` 생성
  - 키워드로 이미지 검색 테스트 (예: "minimal background")
- **완료 조건**:
  - [ ] Unsplash API 키 발급
  - [ ] 이미지 검색 테스트 성공
  - [ ] 다운로드 테스트 성공
  - [ ] API 제한 확인 (50,000회/월)

---

#### TASK-019: Pillow 이미지 합성 프로토타입
- **Priority**: 🟡 P2
- **Difficulty**: 🟡 Medium (4-5h)
- **Area**: `ai`
- **의존성**: TASK-017, TASK-018
- **작업 내용**:
  - `ai/scripts/image_composition.py` 생성
  - 배경 제거된 상품 이미지 + Unsplash 배경 합성
  - 리사이징 (네이버 쇼핑 규격: 500x500, 1000x1000)
  - 여백 조정, 그림자 효과 (선택)
- **완료 조건**:
  - [ ] 합성 스크립트 작성
  - [ ] 3-5가지 배경 스타일 테스트
  - [ ] 결과 이미지 품질 확인
  - [ ] 처리 시간 측정

---

## 🟡 Week 5-6 - AI Backend 통합

#### TASK-020: ImageProcessingService 클래스 설계
- **Priority**: 🟡 P2
- **Difficulty**: 🔴 Hard (6-8h)
- **Area**: `backend` `ai`
- **의존성**: TASK-006, TASK-017, TASK-019
- **작업 내용**:
  - `backend/app/services/image_processing_service.py` 생성
  - 클래스 메서드:
    - `remove_background(image_path)`
    - `fetch_background(keyword, style)`
    - `compose_image(foreground, background, size)`
    - `save_to_storage(image, project_id)`
  - Supabase Storage 업로드 통합
- **완료 조건**:
  - [ ] 서비스 클래스 구현
  - [ ] 각 메서드 단위 테스트
  - [ ] 전체 워크플로우 테스트

---

#### TASK-021: FastAPI BackgroundTasks 비동기 처리
- **Priority**: 🟡 P2
- **Difficulty**: 🟡 Medium (4h)
- **Area**: `backend`
- **의존성**: TASK-020
- **작업 내용**:
  - 이미지 업로드 API에 BackgroundTasks 추가
  - 처리 상태 추적 (pending → processing → completed/failed)
  - Image 모델에 `status` 필드 추가 (마이그레이션)
- **완료 조건**:
  - [ ] BackgroundTasks 구현
  - [ ] 상태 업데이트 동작 확인
  - [ ] 에러 발생 시 크레딧 환불 로직

---

#### TASK-022: 이미지 처리 API 엔드포인트 구현
- **Priority**: 🟡 P2
- **Difficulty**: 🟡 Medium (4h)
- **Area**: `backend`
- **의존성**: TASK-021
- **작업 내용**:
  - `POST /api/v1/images/process` 엔드포인트
  - 요청 파라미터: `image_id`, `background_style`, `size`
  - BackgroundTask로 이미지 처리 실행
  - 처리 완료 후 결과 URL 반환
- **완료 조건**:
  - [ ] 엔드포인트 구현
  - [ ] Swagger UI 테스트 성공
  - [ ] 크레딧 차감 동작 확인

---

#### TASK-023: 이미지 처리 상태 폴링 API
- **Priority**: 🟡 P2
- **Difficulty**: 🟢 Easy (2h)
- **Area**: `backend`
- **의존성**: TASK-021
- **작업 내용**:
  - `GET /api/v1/images/{id}/status` 엔드포인트
  - 응답: `{status: "processing", progress: 50}`
- **완료 조건**:
  - [ ] 엔드포인트 구현
  - [ ] 상태 반환 테스트

---

## 🟡 Week 7-8 - Frontend 통합 & AI 텍스트

#### TASK-024: OpenAI GPT-4o-mini API 연동
- **Priority**: 🟡 P2
- **Difficulty**: 🟡 Medium (3h)
- **Area**: `backend` `ai`
- **의존성**: 없음
- **작업 내용**:
  - OpenAI API 키 발급 (.env에 추가)
  - `backend/app/services/text_generation_service.py` 생성
  - 프롬프트 템플릿 설계
  - 타겟층별 프롬프트 (20대 여성, 30대 직장인, 40대 주부)
- **완료 조건**:
  - [ ] API 연동 성공
  - [ ] 3가지 타겟층 프롬프트 작성
  - [ ] 테스트 문구 생성 성공

---

#### TASK-025: 광고 문구 생성 API 엔드포인트
- **Priority**: 🟡 P2
- **Difficulty**: 🟡 Medium (3h)
- **Area**: `backend`
- **의존성**: TASK-024
- **작업 내용**:
  - `POST /api/v1/text/generate` 엔드포인트
  - 요청: `{product_name, keywords, target_audience}`
  - 응답: 3가지 버전 (SNS용, 상세용, 스토리텔링용)
  - 크레딧 차감 (0.5 크레딧)
- **완료 조건**:
  - [ ] 엔드포인트 구현
  - [ ] Swagger UI 테스트
  - [ ] 크레딧 차감 확인

---

#### TASK-026: 메인 페이지 UI 구현
- **Priority**: 🟡 P2
- **Difficulty**: 🟡 Medium (4-5h)
- **Area**: `frontend`
- **의존성**: TASK-009
- **작업 내용**:
  - 히어로 섹션 (CTA 버튼)
  - 기능 소개 (3-4가지)
  - 샘플 결과물 갤러리
  - 가격 정보
- **완료 조건**:
  - [ ] 메인 페이지 UI 완성
  - [ ] 반응형 디자인
  - [ ] 애니메이션 효과 (선택)

---

#### TASK-027: 대시보드 페이지 UI 구현
- **Priority**: 🟡 P2
- **Difficulty**: 🟡 Medium (4-5h)
- **Area**: `frontend`
- **의존성**: TASK-009, TASK-015
- **작업 내용**:
  - 크레딧 잔액 카드
  - 프로젝트 목록 (카드 그리드)
  - 최근 생성 이미지 (썸네일)
  - "새 프로젝트" 버튼
- **완료 조건**:
  - [ ] 대시보드 UI 완성
  - [ ] 프로젝트 목록 표시
  - [ ] 크레딧 잔액 표시

---

#### TASK-028: 이미지 업로드 컴포넌트 구현
- **Priority**: 🟡 P2
- **Difficulty**: 🟡 Medium (4h)
- **Area**: `frontend`
- **의존성**: TASK-008
- **작업 내용**:
  - 드래그 앤 드롭 업로드
  - 이미지 미리보기
  - 파일 크기/형식 validation (JPG, PNG, 5MB 이하)
  - 업로드 진행률 표시
- **완료 조건**:
  - [ ] 업로드 컴포넌트 완성
  - [ ] 드래그 앤 드롭 동작
  - [ ] validation 테스트

---

#### TASK-029: 이미지 처리 설정 UI (배경 스타일 선택)
- **Priority**: 🟡 P2
- **Difficulty**: 🟢 Easy (3h)
- **Area**: `frontend`
- **의존성**: TASK-028
- **작업 내용**:
  - 배경 스타일 선택 (3-5가지 프리셋)
  - 이미지 크기 선택 (네이버 쇼핑, 쿠팡)
  - 크레딧 사용량 표시
- **완료 조건**:
  - [ ] 설정 UI 완성
  - [ ] 프리셋 선택 동작

---

#### TASK-030: 이미지 처리 API 연동 (Frontend)
- **Priority**: 🟡 P2
- **Difficulty**: 🟡 Medium (4h)
- **Area**: `frontend`
- **의존성**: TASK-022, TASK-028, TASK-029
- **작업 내용**:
  - 이미지 업로드 API 호출
  - 처리 요청 API 호출
  - 상태 폴링 (2초마다 확인)
  - 처리 완료 후 결과 표시
- **완료 조건**:
  - [ ] 업로드 → 처리 → 결과 E2E 동작
  - [ ] 로딩 상태 표시
  - [ ] 에러 핸들링

---

#### TASK-031: 결과 이미지 미리보기 및 다운로드
- **Priority**: 🟡 P2
- **Difficulty**: 🟢 Easy (2-3h)
- **Area**: `frontend`
- **의존성**: TASK-030
- **작업 내용**:
  - 결과 이미지 미리보기
  - 다운로드 버튼 (다양한 크기)
  - 공유 버튼 (선택)
- **완료 조건**:
  - [ ] 미리보기 표시
  - [ ] 다운로드 동작 확인

---

## 🟢 Week 9-10 - 결제 & 마무리

#### TASK-032: 토스페이먼츠 연동 (Backend)
- **Priority**: 🟡 P2
- **Difficulty**: 🔴 Hard (6-8h)
- **Area**: `backend`
- **의존성**: TASK-006
- **작업 내용**:
  - 토스페이먼츠 계정 생성
  - `POST /api/v1/payments/prepare` - 결제 준비
  - `POST /api/v1/payments/confirm` - 결제 승인
  - 웹훅 엔드포인트 (`POST /api/v1/payments/webhook`)
  - 결제 성공 시 크레딧 추가
- **완료 조건**:
  - [ ] 결제 API 구현
  - [ ] 테스트 결제 성공
  - [ ] 크레딧 자동 충전 확인

---

#### TASK-033: 결제 페이지 UI 구현 (Frontend)
- **Priority**: 🟡 P2
- **Difficulty**: 🟡 Medium (4h)
- **Area**: `frontend`
- **의존성**: TASK-032
- **작업 내용**:
  - 크레딧 패키지 선택 UI
  - 토스페이먼츠 위젯 연동
  - 결제 성공/실패 처리
- **완료 조건**:
  - [ ] 결제 페이지 UI 완성
  - [ ] 테스트 결제 동작 확인

---

#### TASK-034: 생성 히스토리 페이지
- **Priority**: 🟢 P3
- **Difficulty**: 🟡 Medium (3-4h)
- **Area**: `frontend`
- **의존성**: TASK-027
- **작업 내용**:
  - 생성한 이미지 목록 표시
  - 필터링 (날짜, 프로젝트)
  - 페이지네이션
- **완료 조건**:
  - [ ] 히스토리 페이지 완성
  - [ ] 필터링 동작 확인

---

#### TASK-035: 모바일 반응형 최적화
- **Priority**: 🟢 P3
- **Difficulty**: 🟡 Medium (4-5h)
- **Area**: `frontend`
- **의존성**: 모든 Frontend UI
- **작업 내용**:
  - 모든 페이지 모바일 레이아웃 확인
  - TailwindCSS 반응형 클래스 적용
  - 터치 인터랙션 최적화
- **완료 조건**:
  - [ ] 모바일 레이아웃 완성
  - [ ] 크롬 DevTools 모바일 테스트

---

## 📚 Week 11-12 - 테스트 & 배포

#### TASK-036: Backend E2E 테스트 작성
- **Priority**: 🟢 P3
- **Difficulty**: 🔴 Hard (6-8h)
- **Area**: `backend` `testing`
- **의존성**: 모든 Backend API
- **작업 내용**:
  - pytest 테스트 시나리오 작성
  - 회원가입 → 로그인 → 이미지 생성 → 다운로드
  - TestClient 사용
- **완료 조건**:
  - [ ] E2E 테스트 스크립트 작성
  - [ ] 테스트 통과 확인

---

#### TASK-037: Render에 Backend 배포
- **Priority**: 🟠 P1
- **Difficulty**: 🟡 Medium (3-4h)
- **Area**: `devops`
- **의존성**: TASK-006
- **작업 내용**:
  - Render 계정 생성
  - Web Service 생성 (Python)
  - 환경 변수 설정
  - Supabase PostgreSQL 연결
- **완료 조건**:
  - [ ] 배포 성공
  - [ ] API 접속 확인
  - [ ] Swagger UI 접속 확인

---

#### TASK-038: Vercel/Render에 Frontend 배포
- **Priority**: 🟠 P1
- **Difficulty**: 🟢 Easy (2h)
- **Area**: `devops`
- **의존성**: 모든 Frontend UI
- **작업 내용**:
  - Vercel 또는 Render Static Site 생성
  - 빌드 설정 (`npm run build`)
  - 환경 변수 설정 (API URL)
- **완료 조건**:
  - [ ] 배포 성공
  - [ ] 프로덕션 URL 접속 확인

---

#### TASK-039: Sentry 에러 모니터링 설정
- **Priority**: 🟢 P3
- **Difficulty**: 🟢 Easy (1-2h)
- **Area**: `devops`
- **의존성**: TASK-037, TASK-038
- **작업 내용**:
  - Sentry 계정 생성 (무료 티어)
  - Backend/Frontend Sentry SDK 설치
  - 에러 발생 테스트
- **완료 조건**:
  - [ ] Sentry 설정 완료
  - [ ] 테스트 에러 수집 확인

---

#### TASK-040: API 문서 작성 (docs/API.md)
- **Priority**: 🟢 P3
- **Difficulty**: 🟢 Easy (2-3h)
- **Area**: `docs`
- **의존성**: 모든 Backend API
- **작업 내용**:
  - 주요 엔드포인트 설명
  - 요청/응답 예시
  - 에러 코드 설명
- **완료 조건**:
  - [ ] API 문서 작성 완료
  - [ ] Markdown 포맷 확인

---

#### TASK-041: 사용자 가이드 작성 (docs/USER_GUIDE.md)
- **Priority**: 🟢 P3
- **Difficulty**: 🟢 Easy (2-3h)
- **Area**: `docs`
- **의존성**: 모든 Frontend UI
- **작업 내용**:
  - 회원가입부터 이미지 생성까지 단계별 가이드
  - 스크린샷 추가
  - FAQ (자주 묻는 질문)
- **완료 조건**:
  - [ ] 사용자 가이드 작성
  - [ ] 스크린샷 추가

---

#### TASK-042: README.md 업데이트
- **Priority**: 🟢 P3
- **Difficulty**: 🟢 Easy (1h)
- **Area**: `docs`
- **의존성**: 없음
- **작업 내용**:
  - 프로젝트 소개
  - 기능 목록
  - 설치 가이드
  - 기술 스택
  - 팀원 소개
- **완료 조건**:
  - [ ] README 업데이트
  - [ ] 배지 추가 (선택)

---

#### TASK-043: 소프트 런칭 준비
- **Priority**: 🟠 P1
- **Difficulty**: 🟢 Easy (2h)
- **Area**: `devops`
- **의존성**: TASK-037, TASK-038
- **작업 내용**:
  - 테스트 계정 3개 생성
  - 샘플 이미지 5개 준비
  - 지인 초대 (5-10명)
  - 피드백 수집 양식 준비 (Google Forms)
- **완료 조건**:
  - [ ] 런칭 준비 완료
  - [ ] 초대 이메일 발송
  - [ ] 피드백 수집 시작

---

## 📊 태스크 통계

### 난이도별 분포
- 🟢 Easy: 15개 (35%)
- 🟡 Medium: 23개 (53%)
- 🔴 Hard: 5개 (12%)

### 영역별 분포
- Backend: 12개
- Frontend: 16개
- AI: 5개
- DevOps: 6개
- Testing: 2개
- Docs: 4개

### 예상 총 작업 시간
- Easy: 15개 × 2h = 30h
- Medium: 23개 × 4h = 92h
- Hard: 5개 × 7h = 35h
- **총 157시간 ≈ 8주 (3인 병렬 작업 시)**

---

## 🎯 작업 진행 방법

### 1. GitHub Issues 등록
```bash
# 각 태스크를 이슈로 등록
gh issue create --title "TASK-001: Python 가상환경 설정" --label "backend,devops,P0,easy"
```

### 2. 칸반 보드 활용 (GitHub Projects)
- **Columns**: Todo → In Progress → Review → Done
- 각자 "In Progress"에 작업 중인 태스크 이동

### 3. 브랜치 생성
```bash
git checkout develop
git pull
git checkout -b feature/task-001-python-env
```

### 4. 작업 완료 후 PR
- 최소 1명 리뷰 필요
- CI/CD 테스트 통과 필수

### 5. 일일 업데이트 (선택)
```
📅 2025-10-17
👤 [이름]
✅ 완료: TASK-001 Python 환경 설정
🏃 진행중: TASK-002 .env 파일 설정 (80%)
🚧 블로커: Supabase 연결 이슈
```

---

## 📝 다음 단계

1. **즉시 착수 가능 (병렬 작업)**:
   - TASK-001: Python 환경 설정
   - TASK-007: React 프로젝트 검증
   - TASK-016: Docker Compose 검증
   - TASK-017: Rembg 프로토타입
   - TASK-018: Unsplash API 테스트

2. **Week 5 목표**:
   - Backend 서버 실행 및 API 테스트 (TASK-001~006)
   - Frontend 기본 구조 및 인증 (TASK-007~015)
   - AI 스크립트 프로토타입 (TASK-017~019)

3. **협업 필요 태스크** (진행도 낮을 시 페어 프로그래밍):
   - TASK-020: ImageProcessingService (AI + Backend)
   - TASK-030: 이미지 처리 API 연동 (Frontend + Backend)
   - TASK-032: 결제 시스템 (Backend + Frontend)

---

**작성일**: 2025-10-17
**버전**: 1.0
**다음 업데이트**: 태스크 진행에 따라 실시간 수정
