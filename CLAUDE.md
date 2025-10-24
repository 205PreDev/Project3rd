● 📄 문서 상태

  ✅ 완료: 개선사항 원본 파일 반영 완료 (2025-10-24)

  - 온보딩_플로우.md ✅ 개선사항 반영 완료
  - SNS_공유_광고문구_기능.md ✅ 개선사항 반영 완료

  📚 참고 문서:
  - docs/요구사항_명세서.md (기능 요구사항 FR-001~FR-014)
  - docs/설계_명세서.md (시스템 아키텍처, API 설계)
  - docs/프로젝트_계획보고서.md (전체 일정 Week 1-10)

  ---

● 🎯 작업 진행 상황

  ✅ **완료된 작업** (2025-10-24)

  기본 구조 설정
  - ✅ Backend 데이터베이스 모델 7개 (User, Project, Image, CreditTransaction, OnboardingProgress, TrialSession, PromptViolation)
  - ✅ Backend API 라우터 6개 (projects, images, credits, onboarding, trial, prompt)
  - ✅ Backend 설정 파일 (config.py, requirements.txt, .env.example)
  - ✅ Frontend 환경 설정 (package.json, 타입, 스토어, API 서비스, Hooks)
  - ✅ 루트 package.json (한 번에 실행: npm run dev)
  - ✅ 빌드/서버 실행 가이드 문서

  ---

● 📋 다음 할 작업 (우선순위 순)

  ### Phase 1: 핵심 서비스 구현 (Week 5-6)

  **Backend 서비스 레이어** (선행 필수)
  - [ ] TASK-B01: Supabase Storage 서비스 구현 (4-6h, Medium)
    - 파일 업로드/다운로드/삭제
    - URL 생성 및 공개 링크 처리
    - 파일: backend/app/services/storage_service.py

  - [ ] TASK-B02: Credit 서비스 구현 (2-3h, Easy)
    - 크레딧 차감/충전 로직
    - 트랜잭션 기록
    - 파일: backend/app/services/credit_service.py

  - [ ] TASK-B03: Supabase Auth 완전 통합 (3-4h, Medium)
    - JWT 토큰 검증 미들웨어
    - 소셜 로그인 (Google) 플로우
    - 파일: backend/app/core/auth.py

  **AI 서비스 통합** (병렬 가능)
  - [ ] TASK-AI01: Rembg 배경 제거 서비스 (4-6h, Medium)
    - Docker 컨테이너 설정 및 연동
    - API 호출 및 에러 처리
    - 파일: ai/rembg_service/Dockerfile, backend/app/services/rembg_service.py

  - [ ] TASK-AI02: Unsplash 배경 이미지 서비스 (3-4h, Easy)
    - API 연동 및 캐싱 (Redis)
    - 카테고리별 배경 추천 로직
    - 파일: backend/app/services/unsplash_service.py

  - [ ] TASK-AI03: GPT-4 Vision 이미지 분석 (4-5h, Medium)
    - 상품 카테고리/색상/분위기 분석
    - 결과 캐싱 (Redis, TTL 1h)
    - 파일: backend/app/services/openai_service.py

  - [ ] TASK-AI04: GPT-4o-mini 광고 문구 생성 (3-4h, Medium)
    - 플랫폼별 최적화 (Instagram, Facebook, Kakao)
    - 3가지 스타일 옵션 (감성형, 질문형, 간결형)
    - 파일: backend/app/services/caption_service.py

  - [ ] TASK-AI05: OpenAI Moderation API 프롬프트 검증 (2-3h, Easy)
    - 부적절 콘텐츠 차단
    - 금지 키워드 필터링
    - 파일: backend/app/services/moderation_service.py

  ---

  ### Phase 2: Frontend UI 구현 (Week 6-7)

  **온보딩 플로우 (5단계)**
  - [ ] TASK-F01: Stage 1 - 랜딩 페이지 (6-8h, Medium)
    - Before/After 슬라이더
    - 샘플 갤러리
    - CTA 버튼
    - 파일: frontend/src/pages/Landing.tsx

  - [ ] TASK-F02: Stage 2 - 즉시 체험 모드 (5-7h, Medium)
    - 워터마크 미리보기
    - 처리 중 애니메이션
    - Exit Intent 모달
    - 파일: frontend/src/pages/Trial.tsx

  - [ ] TASK-F03: Stage 3 - 회원가입 페이지 (4-5h, Easy)
    - 소셜 로그인 (Google, Kakao)
    - 이메일 가입 폼
    - 파일: frontend/src/pages/Signup.tsx

  - [ ] TASK-F04: Stage 4 - 인터랙티브 튜토리얼 (6-8h, Medium)
    - 3단계 가이드 (프로젝트 생성, 배경 선택, 이미지 업로드)
    - 진행률 표시
    - 파일: frontend/src/components/Tutorial/

  - [ ] TASK-F05: Stage 5 - 체크리스트 & 보상 (3-4h, Easy)
    - 시작 가이드 5개 항목
    - 크레딧 보상 알림
    - 파일: frontend/src/components/Onboarding/Checklist.tsx

  **핵심 기능 UI**
  - [ ] TASK-F06: 이미지 업로드 컴포넌트 (5-6h, Medium)
    - Drag & Drop
    - 파일 검증
    - 미리보기
    - 파일: frontend/src/components/ImageUpload.tsx

  - [ ] TASK-F07: 배경 스타일 선택 UI (4-5h, Easy)
    - 5가지 기본 스타일 그리드
    - 실시간 미리보기
    - 파일: frontend/src/components/StyleSelector.tsx

  - [ ] TASK-F08: 광고 문구 생성 UI (5-6h, Medium)
    - 3가지 스타일 옵션
    - 커스터마이징 폼 (분위기, 길이, 이모지)
    - 클립보드 복사
    - 파일: frontend/src/components/CaptionGenerator.tsx

  - [ ] TASK-F09: SNS 공유 모달 (6-8h, Hard)
    - Instagram 딥링크 + 클립보드
    - Facebook Web Share API
    - Kakao SDK 연동
    - AI 제작 표시 (투명성)
    - 파일: frontend/src/components/ShareModal.tsx

  - [ ] TASK-F10: 대시보드 페이지 (8-10h, Hard)
    - 프로젝트 목록
    - 이미지 갤러리
    - 크레딧 잔액 표시
    - 파일: frontend/src/pages/Dashboard.tsx

  **공통 컴포넌트**
  - [ ] TASK-F11: 라우팅 설정 (2-3h, Easy)
    - React Router 설정
    - Protected Routes
    - 파일: frontend/src/App.tsx

  - [ ] TASK-F12: 레이아웃 컴포넌트 (3-4h, Easy)
    - Header, Footer, Sidebar
    - 반응형 디자인
    - 파일: frontend/src/components/Layout/

  ---

  ### Phase 3: 통합 및 최적화 (Week 8-9)

  **통합 작업**
  - [ ] TASK-I01: Backend-Frontend API 통합 테스트 (4-6h, Medium)
  - [ ] TASK-I02: 이미지 처리 파이프라인 E2E 테스트 (5-7h, Medium)
  - [ ] TASK-I03: Redis 캐싱 전략 구현 (3-4h, Medium)
  - [ ] TASK-I04: Rate Limiting 구현 (2-3h, Easy)

  **추가 기능**
  - [ ] TASK-E01: 일괄 다운로드 (ZIP) (3-4h, Easy)
  - [ ] TASK-E02: 플랫폼별 맞춤 크기 변환 (4-5h, Medium)
  - [ ] TASK-E03: 결제 연동 (Toss Payments) (6-8h, Hard)

  ---

  ### Phase 4: 배포 (Week 10)

  **배포 준비**
  - [ ] TASK-D01: Vercel 배포 설정 (2-3h, Easy)
  - [ ] TASK-D02: 환경 변수 설정 (프로덕션) (1-2h, Easy)
  - [ ] TASK-D03: 성능 최적화 (이미지 압축, 코드 스플리팅) (4-6h, Medium)
  - [ ] TASK-D04: 에러 모니터링 (Sentry) (2-3h, Easy)
  - [ ] TASK-D05: 베타 테스트 및 피드백 수집 (ongoing)

  ---

● 🚀 즉시 착수 권장

  **다음 작업 추천 순서:**
  1. TASK-B01 (Supabase Storage) - 이미지 업로드/다운로드 필수
  2. TASK-B02 (Credit Service) - 크레딧 차감 로직 필요
  3. TASK-AI01 (Rembg) - 핵심 AI 기능
  4. TASK-AI02 (Unsplash) - 배경 이미지 제공
  5. TASK-F01 (랜딩 페이지) - 사용자 진입점

  **병렬 작업 가능:**
  - Backend 서비스 (B01-B03)
  - AI 서비스 (AI01-AI05)
  - Frontend UI (F01-F05)

  ---

● ⚙️ 개발 환경 실행

  ```bash
  # 루트에서 한 번에 실행
  npm run dev

  # Backend: http://localhost:8000
  # Frontend: http://localhost:5173
  # API Docs: http://localhost:8000/docs
  ```