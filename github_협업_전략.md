# GitHub 협업 전략

> **목적**: 3인 팀이 GitHub를 활용하여 효율적으로 협업하는 방법
> **작성일**: 2025-10-17
> **프로젝트**: AI 기반 e-커머스 상품 이미지 생성 서비스

---

## 📌 핵심 원칙

1. **투명성**: 모든 작업은 GitHub에서 추적 가능해야 함
2. **자율성**: 각자 원하는 태스크를 자유롭게 선택
3. **책임성**: 선택한 작업은 끝까지 완료하거나 도움 요청
4. **소통**: 블로커 발생 시 즉시 이슈/PR에 코멘트

---

## 🎯 GitHub Issues - 작업 관리의 중심

### 왜 Issues를 사용하는가?

#### 1. 실시간 협업 & 가시성 📊
```
문제 상황 (Markdown 파일):
- 팀원 A: "TASK-015 누가 하는 중이에요?"
- 팀원 B: "어... 제가 어제부터 하고 있는데 말 안 했네요"
- 팀원 C: "아 저도 그거 오늘 시작했는데..."
→ 중복 작업 발생!

해결 (GitHub Issues):
- Issue #15가 "In Progress"이고 Assignee가 팀원 B
- 팀원 C는 한눈에 보고 다른 작업 선택
→ 중복 작업 방지
```

#### 2. 효율적인 작업 선택 🎯
```
Labels 필터링:
- 🔴 P0 + backend + easy → "급한데 쉬운 백엔드 작업"
- 🟡 P2 + frontend + medium → "여유 있을 때 할 프론트엔드 작업"
- unassigned + hard → "도전해볼 어려운 작업"

각자 실력/시간에 맞춰 선택 가능!
```

#### 3. 체계적인 커뮤니케이션 💬
```markdown
Issue #20: ImageProcessingService 클래스 설계

팀원 A (댓글):
"Rembg 라이브러리 설치 시 CUDA 에러 나는데 해결 방법 아시는 분?"

팀원 C (댓글):
"CPU 버전으로 설치하면 됩니다: pip install rembg[cpu]"

→ 문제 해결 과정이 이슈에 기록됨
→ 나중에 같은 문제 발생 시 검색으로 찾을 수 있음
```

#### 4. PR과 자동 연동 🔗
```bash
# 커밋 메시지에 Issue 번호 포함
git commit -m "feat: Python 환경 설정 완료 #1"

# PR 설명에 작성
Closes #1

→ PR 머지 시 Issue #1 자동으로 닫힘
→ 작업 추적이 자동화됨
```

#### 5. GitHub Projects 칸반 보드 📋
```
Visual 관리:
┌─────────┬──────────────┬─────────┬──────┐
│  Todo   │ In Progress  │ Review  │ Done │
├─────────┼──────────────┼─────────┼──────┤
│ #1 #2   │ #5 (팀원 A)  │ #10     │ #15  │
│ #3 #4   │ #7 (팀원 B)  │ #12     │ #18  │
│ #6 #8   │ #9 (팀원 C)  │         │ #22  │
└─────────┴──────────────┴─────────┴──────┘

진행률: 25/43 (58%) 자동 계산
```

#### 6. 알림 & 업데이트 🔔
```
GitHub 알림:
- 내가 Assignee인 이슈에 댓글 → 알림
- 내가 작성한 PR에 리뷰 요청 → 알림
- 멘션 (@username) → 알림

→ Discord/Slack 없이도 실시간 소통 가능
```

#### 7. 검색 & 필터링 🔍
```
강력한 검색:
is:issue is:open label:P0
→ 긴급 작업만 보기

is:issue assignee:@me is:open
→ 내가 맡은 작업만

is:issue label:backend no:assignee
→ 아직 아무도 안 잡은 백엔드 작업

is:issue author:@teamA closed:>2025-10-01
→ 팀원 A가 이번 달 완료한 작업
```

#### 8. 프로젝트 메트릭 📈
```
자동으로 확인 가능:
- Burndown Chart: 남은 작업 추세 그래프
- Velocity: 주당 평균 완료 이슈 개수
- Contributor Activity: 각 팀원의 기여도
- Cycle Time: 이슈 열림 → 닫힘까지 평균 시간

→ 데이터 기반 프로젝트 관리
```

---

## 🏗️ GitHub Issues 구조

### Issue 템플릿

```markdown
## 📝 작업 내용
- 구체적인 작업 설명

## 🎯 완료 조건
- [ ] 조건 1
- [ ] 조건 2
- [ ] 조건 3

## 📚 참고 자료
- 관련 문서 링크
- 의존하는 다른 이슈

## ⏱️ 예상 시간
3-4 시간

## 🔗 관련 이슈
- Depends on: #이슈번호
- Blocks: #이슈번호

## 💬 메모
- 특별히 주의할 점
```

### Label 시스템

#### Priority (우선순위)
- 🔴 **P0-Critical**: 다른 작업의 블로커, 즉시 처리
- 🟠 **P1-High**: 이번 주 내 완료 필요
- 🟡 **P2-Medium**: 다음 주 목표
- 🟢 **P3-Low**: 여유 있을 때

#### Difficulty (난이도)
- 🟢 **easy**: 1-2시간, 독립 작업 가능
- 🟡 **medium**: 3-6시간, 기본 지식 필요
- 🔴 **hard**: 1-2일, 복잡하거나 협업 필요

#### Area (영역)
- `backend` `frontend` `ai` `devops` `docs` `testing`

#### Type (타입)
- `feature` `bug` `refactor` `docs` `chore`

#### Status (상태) - Projects에서 자동 관리
- 📝 **todo**: 시작 전
- 🏃 **in-progress**: 진행 중
- 👀 **review**: 리뷰 대기
- ✅ **done**: 완료

---

## 📊 GitHub Projects - 칸반 보드

### 프로젝트 생성

1. Repository → Projects → New project
2. Board 템플릿 선택
3. Columns 설정:
   - 📝 **Backlog** (우선순위 낮은 작업)
   - 📋 **Todo** (이번/다음 주 목표)
   - 🏃 **In Progress** (현재 진행 중)
   - 👀 **Review** (PR 리뷰 대기)
   - ✅ **Done** (완료)

### Automation 설정

```yaml
자동화 규칙:
- Issue 생성 시 → Backlog 컬럼으로 이동
- Assignee 지정 시 → In Progress 컬럼으로 이동
- PR 생성 시 → Review 컬럼으로 이동
- PR 머지 시 → Done 컬럼으로 이동
- Issue 닫힘 시 → Done 컬럼으로 이동
```

### 필터링 & 뷰

```
기본 뷰:
- All Issues: 모든 작업
- My Tasks: 내가 Assignee인 작업만
- High Priority: P0, P1만
- Backend: backend 라벨만
- Available: Assignee 없는 작업 (작업 선택용)
```

---

## 🔄 작업 워크플로우

### 1. 작업 선택

```bash
# 1. GitHub Projects에서 "Available" 뷰 확인
# 2. 관심 있는 이슈 클릭
# 3. 난이도, 예상 시간, 의존성 확인
# 4. 자신을 Assignee로 지정
# 5. 이슈를 "In Progress" 컬럼으로 이동
```

**팁**:
- 첫 작업은 "easy" 선택 (환경 익히기)
- 의존성(`Depends on`) 확인 필수
- 예상 시간의 1.5배 여유 두기

### 2. 브랜치 생성 & 작업

```bash
# develop 브랜치에서 시작
git checkout develop
git pull origin develop

# feature 브랜치 생성 (이슈 번호 포함)
git checkout -b feature/task-001-python-env

# 작업 진행...
```

**브랜치 명명 규칙**:
```
feature/task-번호-간단한설명
bugfix/issue-번호-간단한설명
hotfix/긴급수정-설명

예시:
feature/task-001-python-env
feature/task-012-login-page
bugfix/issue-45-credit-deduction
```

### 3. 커밋

```bash
# 작업 단위로 자주 커밋
git add .
git commit -m "feat: Python 가상환경 설정 완료 #1"

# 커밋 메시지 규칙 (Conventional Commits)
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 포맷팅 (기능 변경 없음)
refactor: 코드 리팩토링
test: 테스트 코드
chore: 빌드, 설정 파일

# 이슈 번호는 항상 끝에 #번호
```

### 4. Push & PR 생성

```bash
# 원격에 Push
git push origin feature/task-001-python-env

# GitHub에서 PR 생성
# 또는 CLI 사용 (gh 설치 시)
gh pr create --base develop --head feature/task-001-python-env \
  --title "feat: Python 가상환경 설정 완료" \
  --body "Closes #1"
```

**PR 템플릿**:
```markdown
## 🎯 작업 내용
- Python 가상환경 설정
- requirements.txt 패키지 설치
- 설치 검증 완료

## 🔗 관련 이슈
Closes #1

## ✅ 체크리스트
- [x] 로컬 테스트 완료
- [x] 코드 린트 통과
- [x] 문서 업데이트 완료 (해당 시)

## 📸 스크린샷 (UI 변경 시)
(이미지 첨부)

## 💬 리뷰어에게
- pip install 시 에러 없음을 확인해주세요
- installed_packages.txt 확인 부탁드립니다
```

### 5. 코드 리뷰

**리뷰어 역할**:
```markdown
체크리스트:
- [ ] 코드가 요구사항을 충족하는가?
- [ ] 네이밍이 명확한가?
- [ ] 중복 코드는 없는가?
- [ ] 에러 핸들링이 적절한가?
- [ ] 테스트 코드가 있는가? (필요 시)
- [ ] 문서 업데이트 완료되었는가?
```

**피드백 작성 규칙**:
```markdown
좋은 예:
✅ LGTM! 깔끔한 구현입니다.
💡 제안: 이 부분은 useCallback으로 최적화할 수 있을 것 같습니다.
❓ 질문: 이 API 호출이 실패하면 어떻게 처리되나요?
🐛 버그: 여기서 null 체크가 필요할 것 같습니다.

나쁜 예:
❌ "이거 왜 이렇게 했어요?" (부정적)
❌ "다시 짜세요" (구체적이지 않음)
❌ "별로네요" (비건설적)
```

**리뷰 속도**:
- P0 이슈: 24시간 이내
- P1 이슈: 48시간 이내
- P2-P3: 주말 전까지

### 6. 수정 & 재요청

```bash
# 리뷰 피드백 반영
git add .
git commit -m "fix: 리뷰 피드백 반영 - null 체크 추가 #1"
git push

# PR에 자동 업데이트됨
# 리뷰어에게 재요청 (GitHub UI)
```

### 7. 머지 & 마무리

```bash
# 리뷰 승인 후 Squash Merge
# (GitHub UI에서 Squash and merge 버튼)

# 로컬 브랜치 정리
git checkout develop
git pull origin develop
git branch -d feature/task-001-python-env

# 이슈 자동으로 닫힘 (PR에 "Closes #1" 있으면)
# Projects 보드에서도 자동으로 Done으로 이동
```

---

## 🚨 블로커 처리

### 블로커 발생 시

```markdown
Issue #20에 댓글:

@team
🚨 블로커 발생

현재 상황:
- Rembg 라이브러리 설치 시 CUDA 에러 발생
- 에러 메시지: "RuntimeError: CUDA out of memory"

시도한 해결 방법:
- GPU 메모리 확인 → 2GB (부족)
- 배치 사이즈 감소 → 여전히 에러

도움 요청:
- CPU 버전으로 전환 가능한가요?
- 또는 다른 배경 제거 라이브러리 추천 부탁드립니다

Label 추가: "blocked" "help-wanted"
```

### 협업으로 전환

```markdown
블로커 심각 시:
1. 이슈에 "blocked" 라벨 추가
2. 팀원 멘션 (@username)
3. Pair Programming 제안
   - Discord 화면 공유
   - 1-2시간 집중 해결

해결 후:
- 해결 과정 이슈에 코멘트로 기록
- "blocked" 라벨 제거
- 다른 팀원이 참고할 수 있도록
```

---

## 📅 주간 루틴

### 월요일: 주간 계획

```markdown
Weekly Planning Meeting (선택 사항, 30분):
1. 지난주 완료 작업 리뷰 (Projects Done 컬럼)
2. 이번 주 목표 설정
   - P0, P1 이슈 우선순위 확인
   - 각자 2-3개 이슈 선택
3. 블로커 공유
4. 협업 필요한 작업 식별
```

### 수요일: 중간 점검

```markdown
Mid-week Check (비공식, Discord/Slack):
- 진행 상황 간단 공유
- 예상보다 오래 걸리는 작업 있는지
- 도움 필요한 부분 있는지
```

### 금요일: 주간 리뷰

```markdown
Weekly Review (30분):
1. 완료된 작업 축하 🎉
2. 미완료 작업 다음 주로 이월
3. 진행률 확인 (Burndown Chart)
4. 프로세스 개선 사항 논의
   - 무엇이 잘 됐는가?
   - 무엇을 개선할 수 있는가?
```

---

## 🔍 Issue 검색 치트시트

```bash
# 내가 할 수 있는 작업 찾기
is:issue is:open no:assignee label:easy

# 긴급 작업
is:issue is:open label:P0

# 내가 맡은 작업
is:issue is:open assignee:@me

# 특정 영역 작업
is:issue is:open label:backend

# 블로커된 작업
is:issue is:open label:blocked

# 리뷰 필요한 PR
is:pr is:open review:required

# 특정 팀원이 완료한 작업
is:issue is:closed author:@username closed:>2025-10-01

# 오래된 이슈
is:issue is:open created:<2025-10-01

# 댓글 많은 이슈 (논의 활발)
is:issue is:open comments:>5
```

---

## 📈 프로젝트 메트릭 추적

### GitHub Insights 활용

```
Repository → Insights 메뉴:

1. Pulse (7일간 활동 요약)
   - 생성/닫힌 이슈 수
   - 머지된 PR 수
   - 활동한 팀원

2. Contributors
   - 각 팀원의 커밋 수
   - 코드 추가/삭제 라인 수
   - 기여도 그래프

3. Network
   - 브랜치 히스토리 시각화
   - 머지 흐름 확인

4. Forks (Public 레포 시)
   - 포크된 횟수
```

### Projects 메트릭

```
Projects → Insights:

1. Burndown Chart
   - 남은 이슈 수 추세
   - 예상 완료 시점

2. Velocity
   - 주당 평균 완료 이슈 수
   - 속도 개선 추세

3. Cycle Time
   - 이슈 생성 → 완료 평균 시간
   - 병목 구간 식별

4. Work in Progress (WIP)
   - 동시 진행 중인 작업 수
   - 이상적: 팀원당 1-2개
```

---

## 🎓 Best Practices

### DO ✅

1. **이슈 생성 전 중복 확인**
   - 검색으로 비슷한 이슈 있는지 확인
   - 있으면 댓글로 추가, 없으면 새로 생성

2. **자주 커밋, 자주 Push**
   - 작은 단위로 자주 커밋
   - 매일 퇴근 전 Push (백업 효과)

3. **명확한 커밋 메시지**
   - 무엇을(What) + 왜(Why)
   - 나중에 히스토리 볼 때 이해 가능하도록

4. **PR은 작게**
   - 한 PR에 한 가지 기능
   - 리뷰하기 쉽도록 (300줄 이내 권장)

5. **리뷰는 빠르게**
   - 리뷰 요청 받으면 24-48시간 내 응답
   - 블로커되지 않도록

6. **이슈에 진행 상황 업데이트**
   - 50% 완료 시 댓글로 진행 상황 공유
   - 예상보다 오래 걸리면 멘션으로 도움 요청

### DON'T ❌

1. **main 브랜치에 직접 커밋 금지**
   - 항상 feature 브랜치 생성 후 PR

2. **리뷰 없이 머지 금지**
   - 최소 1명 승인 필요
   - 긴급해도 리뷰 받기

3. **Force Push 금지 (공유 브랜치)**
   - 히스토리 꼬임 방지
   - 필요하면 팀원에게 먼저 알리기

4. **큰 파일 커밋 금지**
   - .gitignore 확인
   - 이미지는 Supabase Storage 사용

5. **애매한 커밋 메시지 금지**
   - ❌ "수정", "fix", "asdf"
   - ✅ "feat: 로그인 페이지 UI 구현 #12"

6. **오래된 브랜치 방치 금지**
   - PR 머지 후 브랜치 삭제
   - 주기적으로 stale 브랜치 정리

---

## 🛠️ 도구 & 설정

### 로컬 Git 설정

```bash
# 사용자 정보 설정
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 기본 브랜치 이름
git config --global init.defaultBranch main

# 에디터 설정 (VSCode)
git config --global core.editor "code --wait"

# 자동 CRLF 변환 (Windows)
git config --global core.autocrlf true

# Pull 전략 (rebase)
git config --global pull.rebase true

# 색상 활성화
git config --global color.ui true
```

### Git Alias (단축 명령어)

```bash
# ~/.gitconfig에 추가

[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    pl = pull
    ps = push

    # 예쁜 로그
    lg = log --graph --oneline --decorate --all

    # 마지막 커밋 수정
    amend = commit --amend --no-edit

    # 브랜치 정리
    cleanup = "!git branch --merged | grep -v '\\*\\|main\\|develop' | xargs -n 1 git branch -d"
```

### VSCode 확장 프로그램

```
추천 확장:
1. GitHub Pull Requests and Issues
   - VSCode 내에서 이슈/PR 관리

2. GitLens
   - 코드 히스토리 시각화
   - Blame, 커밋 작성자 확인

3. Git Graph
   - 브랜치 그래프 시각화

4. GitHub Copilot (선택)
   - AI 코드 자동완성
```

### GitHub CLI 설치 (선택)

```bash
# Windows (winget)
winget install --id GitHub.cli

# 인증
gh auth login

# 유용한 명령어
gh issue list                    # 이슈 목록
gh issue create                  # 이슈 생성
gh issue view 번호               # 이슈 상세
gh pr create                     # PR 생성
gh pr list                       # PR 목록
gh pr checkout 번호              # PR 체크아웃 (리뷰용)
gh pr review --approve           # PR 승인
```

---

## 🎯 마일스톤 관리

### 마일스톤 생성

```
Repository → Issues → Milestones → New milestone

예시:
- Week 5: Backend & Frontend 기본 구조
  - Due date: 2025-10-24
  - Description: 서버 실행, 인증, AI 프로토타입

- Week 8: AI-Backend 통합
  - Due date: 2025-11-14
  - Description: 이미지 처리 E2E 완료

- Week 12: MVP 런칭
  - Due date: 2025-12-12
  - Description: 배포 완료, 소프트 런칭
```

### 이슈에 마일스톤 할당

```
Issue 생성 시 또는 수정 시:
Milestone 선택 → Week 5

자동으로 진행률 계산:
Week 5: 8/15 issues completed (53%)
```

---

## 📞 커뮤니케이션 채널별 역할

| 채널 | 용도 | 응답 속도 |
|------|------|----------|
| **GitHub Issues** | 작업 관련 모든 논의, 기록 | 24-48시간 |
| **GitHub PR** | 코드 리뷰, 피드백 | 24-48시간 |
| **Discord/Slack** | 긴급 질문, 비공식 소통 | 즉시-1시간 |
| **주간 회의** | 계획, 리뷰, 전략 논의 | 주 1회 |

**원칙**:
- 코드/작업 관련은 반드시 GitHub에 기록
- 채팅은 빠른 소통용, 중요한 결정은 이슈에 남기기

---

## 🆘 문제 해결 가이드

### "누가 이 작업 하는 중이에요?"
→ Issue 보고 Assignee 확인

### "이 작업 누가 할 거예요?"
→ Available 뷰에서 자유롭게 선택

### "내가 할 작업이 없어요"
→ Backlog에서 이슈 가져오거나, 새 이슈 제안

### "작업이 예상보다 오래 걸려요"
→ 이슈에 진행 상황 코멘트 + help-wanted 라벨

### "리뷰가 너무 늦어요"
→ PR에 리뷰어 멘션 + Discord 알림

### "머지 충돌 났어요"
```bash
git checkout develop
git pull
git checkout feature/my-branch
git merge develop
# 충돌 해결 후
git commit
git push
```

### "실수로 main에 커밋했어요"
```bash
# 아직 Push 전이면
git reset HEAD~1
git checkout -b feature/correct-branch
git add .
git commit -m "올바른 커밋"

# 이미 Push했으면 팀원에게 알리고 revert
```

---

## 📚 참고 자료

### GitHub 공식 문서
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [About Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues)
- [About Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects)

### 커밋 컨벤션
- [Conventional Commits](https://www.conventionalcommits.org/)

### Git 학습
- [Pro Git Book](https://git-scm.com/book/ko/v2)
- [Learn Git Branching](https://learngitbranching.js.org/?locale=ko)

---

## 🔄 이 문서 업데이트

```markdown
협업 과정에서 개선 사항 발견 시:
1. Issue 생성: "docs: GitHub 협업 전략 업데이트 제안"
2. 개선 사항 제안
3. 팀원 동의 후 PR
4. 머지 후 전체 공유
```

**Last Updated**: 2025-10-17
**Version**: 1.0
**Authors**: 전체 팀원

---

## ✅ 체크리스트: 협업 준비 완료?

- [ ] GitHub 계정 생성 및 레포지토리 접근 권한
- [ ] Git 로컬 설정 완료 (user.name, user.email)
- [ ] GitHub Projects 보드 확인
- [ ] Label 시스템 이해
- [ ] 이슈 템플릿 숙지
- [ ] PR 템플릿 숙지
- [ ] 브랜치 전략 이해 (main, develop, feature)
- [ ] 커밋 메시지 컨벤션 숙지
- [ ] 코드 리뷰 가이드 숙지
- [ ] 첫 이슈 선택 완료!

**모두 체크했다면 → 협업 시작! 🚀**
