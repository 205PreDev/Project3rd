# SNS 공유 & 광고 문구 추천 기능 설계서

> ✅ **최신 버전**: 이 문서는 개선사항이 반영된 최신 버전입니다.
>
> 주요 개선사항 (2025-10-24 반영):
> - **버튼 문구 변경**: "SNS에 바로 공유하기" → "SNS에 공유하기" (사용자 통제 강화)
> - **상세 문구 설정**: 길이, 이모지, 미사여구/과한표현 자제, 커스텀 프롬프트
> - **3가지 문구 옵션**: 감성형(추천), 질문형, 간결형 중 선택
> - **AI 제작 표시**: 투명성 및 바이럴 마케팅 (워터마크, 푸터)
>
> 상세 구현 스펙은 **`SNS_공유_개선사항_상세.md`** 참조

## 📋 목차
1. [기능 개요](#1-기능-개요)
2. [SNS 직접 공유 기능](#2-sns-직접-공유-기능)
3. [이미지 분석 기반 문구 추천](#3-이미지-분석-기반-문구-추천)
4. [맥락별 문구 생성](#4-맥락별-문구-생성)
5. [기술 구현](#5-기술-구현)
6. [UI/UX 플로우](#6-uiux-플로우)
7. [수익화 전략](#7-수익화-전략)

---

## 1. 기능 개요

### 핵심 가치 제안

```yaml
문제:
  - 이커머스 판매자들은 이미지 만든 후 SNS 게시물 작성에 또 시간 소비
  - 광고 문구 작성에 막막함 (어떻게 써야 클릭률이 높을까?)
  - 플랫폼별로 다른 문구를 만들어야 함 (인스타 vs 페이스북 vs 블로그)

해결책:
  1. 완성 이미지를 SNS에 바로 공유 (원클릭)
  2. AI가 이미지를 분석하고 맥락에 맞는 문구 자동 생성
  3. 플랫폼별 최적화된 문구 제공
  4. 해시태그 자동 추천

차별화 포인트:
  - 이미지 생성 + 문구 생성 + SNS 공유 "All-in-One"
  - 경쟁사는 이미지만 제공 (Canva, Remove.bg)
```

### 타겟 플랫폼

```javascript
const targetPlatforms = {
  // ===== Phase 1 (MVP) =====
  instagram: {
    name: "인스타그램",
    icon: "📷",
    maxLength: 2200, // 캡션 최대 길이
    hashtagLimit: 30,
    imageFormats: ["JPG", "PNG"],
    optimalSize: "1080x1080",
    priority: "high"
  },

  facebook: {
    name: "페이스북",
    icon: "👍",
    maxLength: 63206,
    hashtagLimit: 10, // 권장
    imageFormats: ["JPG", "PNG"],
    optimalSize: "1200x630",
    priority: "high"
  },

  kakao: {
    name: "카카오톡",
    icon: "💬",
    shareType: "image_link", // 이미지 + 링크
    maxLength: 1000,
    priority: "high" // 한국 사용자
  },

  // ===== Phase 2 =====
  naver_blog: {
    name: "네이버 블로그",
    icon: "✍️",
    maxLength: 10000,
    imageFormats: ["JPG", "PNG", "GIF"],
    priority: "medium"
  },

  twitter: {
    name: "트위터",
    icon: "🐦",
    maxLength: 280,
    imageFormats: ["JPG", "PNG", "GIF"],
    priority: "medium"
  },

  pinterest: {
    name: "핀터레스트",
    icon: "📌",
    maxLength: 500,
    optimalSize: "1000x1500", // 세로형
    priority: "medium"
  }
};
```

---

## 2. SNS 직접 공유 기능

### Flow 2-1: 공유 버튼 (완성 화면)

```
┌────────────────────────────────────────────────────────────────┐
│              🎉 첫 이미지 생성 완료! 🎉                         │
│                                                                │
│         [━━━━━━━━━━━━━━━━━━━━━━━━] 100% 완료                 │
│                                                                │
│   ┌──────────────────────────────────────────────────┐        │
│   │   Before              After                     │        │
│   │  [원본 이미지]       [완성된 이미지]             │        │
│   └──────────────────────────────────────────────────┘        │
│                                                                │
│   📝 AI가 만든 광고 문구                                       │
│   ┌──────────────────────────────────────────────────┐        │
│   │  "당신의 스타일을 완성하세요.                     │        │
│   │   프리미엄 운동화로 매일을 특별하게."             │        │
│   └──────────────────────────────────────────────────┘        │
│                                                                │
│   🎁 보상: +2 크레딧 (첫 이미지 생성 완료!)                    │
│   💰 남은 크레딧: 12개                                         │
│                                                                │
│   ┌────────────────────────────────────────────────┐          │
│   │  [📥 다운로드]  [📤 SNS에 공유하기]            │          │
│   └────────────────────────────────────────────────┘          │
│                                                                │
│   ────────────── 다음은? ──────────────                       │
│   [다른 배경]  [문구 재생성]  [AI 편집]                       │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Flow 2-2: SNS 공유 모달

```
┌────────────────────────────────────────────────────────────────┐
│  🚀 SNS에 바로 공유하기                              [X 닫기]  │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│   어디에 공유할까요?                                           │
│                                                                │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│   │ 📷 인스타그램 │  │ 👍 페이스북   │  │ 💬 카카오톡   │       │
│   │              │  │              │  │              │       │
│   │ 가장 인기!    │  │ 도달률 높음   │  │ 빠른 공유    │       │
│   │              │  │              │  │              │       │
│   │  [선택하기]   │  │  [선택하기]   │  │  [선택하기]   │       │
│   └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                                │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│   │ ✍️ 네이버블로그│  │ 🐦 트위터    │  │ 📌 핀터레스트 │       │
│   │ (출시 예정)   │  │ (출시 예정)   │  │ (출시 예정)   │       │
│   │  [대기 중]    │  │  [대기 중]    │  │  [대기 중]    │       │
│   └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                                │
│   💡 팁: 플랫폼마다 최적화된 문구와 해시태그를 제공해드려요!    │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Flow 2-3: 인스타그램 공유 준비 (개선)

```
┌────────────────────────────────────────────────────────────────┐
│  📷 인스타그램에 공유하기                         [< 뒤로]  [X]│
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  미리보기                                                       │
│  ┌──────────────────────────────────────────────────┐         │
│  │                                                  │         │
│  │          [완성된 이미지 미리보기]                 │         │
│  │           1080x1080 최적화                       │         │
│  │                                                  │         │
│  └──────────────────────────────────────────────────┘         │
│                                                                │
│  📝 광고 문구 생성 설정                                         │
│                                                                │
│  1️⃣ 분위기 선택 (또는 직접 작성)                               │
│  ┌──────────────────────────────────────────────────┐         │
│  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐               │         │
│  │  │😊 밝고│ │🔥 열정│ │💎 고급│ │✏️ 직접│               │         │
│  │  │친근한 │ │적인  │ │스러운│ │작성  │               │         │
│  │  │[선택]│ │     │ │     │ │     │               │         │
│  │  └─────┘ └─────┘ └─────┘ └─────┘               │         │
│  └──────────────────────────────────────────────────┘         │
│                                                                │
│  2️⃣ 문구 스타일 (선택)                                         │
│  ┌──────────────────────────────────────────────────┐         │
│  │  ☐ 짧게 작성 (2-3문장)                            │         │
│  │  ☑ 보통 길이 (4-5문장) ⭐ 권장                    │         │
│  │  ☐ 길게 작성 (6문장 이상)                         │         │
│  │                                                  │         │
│  │  ☑ 이모지 사용                                    │         │
│  │  ☐ 미사여구 자제 (간결하게)                       │         │
│  │  ☐ 과한 표현 자제 (과장 금지)                     │         │
│  │  ☑ 해시태그 포함 (10-15개)                        │         │
│  └──────────────────────────────────────────────────┘         │
│                                                                │
│  3️⃣ 추가 입력 (선택)                                           │
│  ┌──────────────────────────────────────────────────┐         │
│  │  프롬프트 입력 (상세 요청사항):                   │         │
│  │  ┌────────────────────────────────────────────┐  │         │
│  │  │ 예: "할인 정보 강조", "환경 보호 강조"      │  │         │
│  │  │                                            │  │         │
│  │  └────────────────────────────────────────────┘  │         │
│  └──────────────────────────────────────────────────┘         │
│                                                                │
│  ┌────────────────────────────────────────────────┐           │
│  │  [✨ AI 문구 생성하기 (-0.5 크레딧)]           │           │
│  └────────────────────────────────────────────────┘           │
│                                                                │
└────────────────────────────────────────────────────────────────┘
       ↓ (생성 후)
┌────────────────────────────────────────────────────────────────┐
│  생성된 문구 3가지 중 선택하세요                                │
│                                                                │
│  ┌──────────────────────────────────────────────────┐         │
│  │  ⭕ 옵션 1 (추천)                                 │         │
│  │  ┌────────────────────────────────────────────┐  │         │
│  │  │ 🌟 새로운 나를 만나는 시간!                │  │         │
│  │  │                                            │  │         │
│  │  │ 프리미엄 운동화로 매일을 특별하게          │  │         │
│  │  │ 만들어보세요 ✨                            │  │         │
│  │  │                                            │  │         │
│  │  │ 지금 바로 만나보세요 👟                    │  │         │
│  │  │                                            │  │         │
│  │  │ #운동화 #스니커즈 #데일리룩 #OOTD          │  │         │
│  │  │ #신발추천 #패션 #스타일                    │  │         │
│  │  │                                (245자, 8개)│  │         │
│  │  └────────────────────────────────────────────┘  │         │
│  └──────────────────────────────────────────────────┘         │
│                                                                │
│  ┌──────────────────────────────────────────────────┐         │
│  │  ⚪ 옵션 2                                        │         │
│  │  ┌────────────────────────────────────────────┐  │         │
│  │  │ 매일 신는 운동화, 특별해져야 하지 않을까요? │  │         │
│  │  │                                            │  │         │
│  │  │ 가벼운 착화감과 트렌디한 디자인으로        │  │         │
│  │  │ 당신의 일상을 업그레이드하세요 ⚡          │  │         │
│  │  │                                (168자, 6개)│  │         │
│  │  └────────────────────────────────────────────┘  │         │
│  └──────────────────────────────────────────────────┘         │
│                                                                │
│  ┌──────────────────────────────────────────────────┐         │
│  │  ⚪ 옵션 3 (간결)                                 │         │
│  │  ┌────────────────────────────────────────────┐  │         │
│  │  │ 스타일과 편안함, 둘 다 잡은 러닝화 👟       │  │         │
│  │  │                                            │  │         │
│  │  │ 지금 만나보세요!                           │  │         │
│  │  │ 링크는 프로필 ↑                            │  │         │
│  │  │                                (95자, 4개) │  │         │
│  │  └────────────────────────────────────────────┘  │         │
│  └──────────────────────────────────────────────────┘         │
│                                                                │
│  ┌────────────────────────────────────────────────┐           │
│  │  [🔄 다시 생성 (-0.3 크레딧)]  [✏️ 직접 수정]  │           │
│  └────────────────────────────────────────────────┘           │
│                                                                │
│  🔗 쇼핑몰 링크 추가 (선택)                                    │
│  ┌──────────────────────────────────────────────────┐         │
│  │  https://smartstore.naver.com/...                │         │
│  │  [링크 추가하기]                                  │         │
│  └──────────────────────────────────────────────────┘         │
│                                                                │
│  ┌────────────────────────────────────────────────┐           │
│  │  [📱 인스타그램 앱으로 공유하기]               │           │
│  │  (이미지와 선택한 문구가 클립보드에 복사됩니다) │           │
│  └────────────────────────────────────────────────┘           │
│                                                                │
│  💡 팁: 인스타그램 앱에서 붙여넣기하면 바로 게시할 수 있어요!   │
│                                                                │
│  ────────────────────────────────────────────────────         │
│  ℹ️ 이 광고는 [서비스명] AI로 제작되었습니다.                  │
│     GPT-4o-mini 사용 • 제작 시간: 5초                         │
│  ────────────────────────────────────────────────────         │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### 기술적 제약 및 해결책

```yaml
제약사항:
  인스타그램 API:
    - 공식 API는 비즈니스 계정만 자동 게시 가능
    - 개인 계정은 불가능

  페이스북 API:
    - Graph API로 자동 게시 가능
    - 앱 승인 필요

해결책:
  MVP (Phase 1):
    방법: "딥링크 + 클립보드 복사"

    인스타그램:
      1. 이미지 다운로드
      2. 문구 클립보드 복사
      3. 인스타그램 앱 실행 (딥링크)
      4. 사용자가 붙여넣기 + 게시

    페이스북:
      1. Web Share API 사용
      2. 또는 페이스북 Share Dialog

    카카오톡:
      1. Kakao SDK 사용
      2. 이미지 + 텍스트 공유

  Phase 2 (자동화):
    - 비즈니스 계정 연동
    - Instagram Graph API
    - 예약 게시 기능
```

### MVP 구현 (딥링크 방식)

```typescript
// SNS 공유 서비스
class SocialShareService {
  /**
   * 인스타그램 공유 (딥링크 + 클립보드)
   */
  async shareToInstagram(imageUrl: string, caption: string) {
    // 1. 이미지 다운로드
    const blob = await fetch(imageUrl).then(r => r.blob());

    // 2. 클립보드에 이미지 복사 (최신 브라우저)
    try {
      await navigator.clipboard.write([
        new ClipboardItem({
          'image/png': blob
        })
      ]);
    } catch (e) {
      // 폴백: 다운로드
      this.downloadImage(blob, 'instagram-post.png');
    }

    // 3. 문구 클립보드 복사
    await navigator.clipboard.writeText(caption);

    // 4. 안내 메시지
    this.showToast({
      title: '준비 완료! ✅',
      message: '인스타그램 앱에서 이미지를 붙여넣고\n문구도 붙여넣으세요!',
      actions: [
        {
          text: '인스타그램 열기',
          onClick: () => {
            // 딥링크로 앱 실행
            window.location.href = 'instagram://camera';

            // 앱이 없으면 웹으로 이동
            setTimeout(() => {
              window.open('https://www.instagram.com/', '_blank');
            }, 1000);
          }
        }
      ]
    });
  }

  /**
   * 페이스북 공유 (Web Share API)
   */
  async shareToFacebook(imageUrl: string, caption: string) {
    // 방법 1: Web Share API (모바일)
    if (navigator.share) {
      try {
        await navigator.share({
          title: '새 상품 이미지',
          text: caption,
          url: imageUrl
        });
      } catch (e) {
        // 사용자가 취소
      }
    } else {
      // 방법 2: Facebook Share Dialog (데스크톱)
      const shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(imageUrl)}&quote=${encodeURIComponent(caption)}`;
      window.open(shareUrl, '_blank', 'width=600,height=400');
    }
  }

  /**
   * 카카오톡 공유 (Kakao SDK)
   */
  async shareToKakao(imageUrl: string, caption: string, linkUrl?: string) {
    if (!window.Kakao) {
      throw new Error('카카오 SDK가 로드되지 않았습니다');
    }

    Kakao.Link.sendDefault({
      objectType: 'feed',
      content: {
        title: '새 상품 이미지',
        description: caption,
        imageUrl: imageUrl,
        link: {
          mobileWebUrl: linkUrl,
          webUrl: linkUrl
        }
      },
      buttons: [
        {
          title: '자세히 보기',
          link: {
            mobileWebUrl: linkUrl,
            webUrl: linkUrl
          }
        }
      ]
    });
  }

  /**
   * 이미지 다운로드 (폴백)
   */
  private downloadImage(blob: Blob, filename: string) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }
}
```

---

## 3. 이미지 분석 기반 문구 추천

### 이미지 분석 흐름

```
[완성된 이미지]
       ↓
┌─────────────────────────────────────┐
│  1. Vision API로 이미지 분석         │
│     - 상품 카테고리 인식              │
│     - 색상 분석                      │
│     - 분위기 감지                    │
│     - 배경 스타일 파악                │
└─────────────────────────────────────┘
       ↓
┌─────────────────────────────────────┐
│  2. 메타데이터 수집                  │
│     - 사용자가 선택한 배경 스타일     │
│     - 타겟 고객층 (20대 여성 등)     │
│     - 상품 카테고리 (사용자 입력)    │
└─────────────────────────────────────┘
       ↓
┌─────────────────────────────────────┐
│  3. GPT-4o-mini로 문구 생성          │
│     - 분위기별 3가지 버전             │
│     - 플랫폼별 최적화                │
│     - 해시태그 자동 추천              │
└─────────────────────────────────────┘
       ↓
[맞춤형 광고 문구 완성]
```

### Backend API 구현

```python
from openai import OpenAI
import json

class ImageCaptionGenerator:
    """이미지 분석 기반 광고 문구 생성"""

    def __init__(self):
        self.openai = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def analyze_image(self, image_url: str) -> dict:
        """
        GPT-4 Vision으로 이미지 분석

        Returns:
            {
                "category": "운동화",
                "colors": ["white", "black"],
                "style": "minimalist",
                "mood": "energetic"
            }
        """
        response = self.openai.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """이 상품 이미지를 분석해주세요.

                            다음 정보를 JSON으로 반환:
                            - category: 상품 카테고리 (예: 운동화, 가방, 시계)
                            - colors: 주요 색상 3가지
                            - style: 배경 스타일 (minimalist, luxury, natural 등)
                            - mood: 전체적인 분위기 (energetic, calm, sophisticated 등)
                            - target_audience: 추정 타겟 고객 (20대 여성, 30대 남성 등)
                            """
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url}
                        }
                    ]
                }
            ],
            max_tokens=300
        )

        # JSON 파싱
        analysis = json.loads(response.choices[0].message.content)
        return analysis

    async def generate_captions(
        self,
        image_analysis: dict,
        user_context: dict,
        tone: str = "friendly",  # friendly, passionate, luxury, direct
        platform: str = "instagram"
    ) -> dict:
        """
        맥락에 맞는 광고 문구 생성

        Args:
            image_analysis: 이미지 분석 결과
            user_context: 사용자 입력 (상품명, 특징 등)
            tone: 문구 톤앤매너
            platform: 플랫폼 (instagram, facebook 등)

        Returns:
            {
                "main_caption": "메인 광고 문구",
                "variations": ["버전1", "버전2", "버전3"],
                "hashtags": ["#운동화", "#스니커즈", ...],
                "call_to_action": "지금 바로 만나보세요!"
            }
        """
        # 플랫폼별 설정
        platform_config = {
            "instagram": {
                "max_length": 2200,
                "hashtag_count": "10-15개",
                "style": "감성적, 이모지 활용"
            },
            "facebook": {
                "max_length": 500,
                "hashtag_count": "3-5개",
                "style": "정보 전달 중심"
            },
            "kakao": {
                "max_length": 200,
                "hashtag_count": "없음",
                "style": "짧고 임팩트 있게"
            }
        }

        config = platform_config.get(platform, platform_config["instagram"])

        # 톤앤매너 정의
        tone_guides = {
            "friendly": "밝고 친근한 느낌, 친구에게 말하듯이",
            "passionate": "열정적이고 에너지 넘치는 느낌",
            "luxury": "고급스럽고 세련된 느낌",
            "direct": "간결하고 직접적인 느낌"
        }

        # GPT 프롬프트 구성
        prompt = f"""
당신은 e커머스 마케팅 전문가입니다.
다음 정보를 바탕으로 {platform} 광고 문구를 작성해주세요.

===== 이미지 분석 =====
- 상품 카테고리: {image_analysis['category']}
- 주요 색상: {', '.join(image_analysis['colors'])}
- 배경 스타일: {image_analysis['style']}
- 분위기: {image_analysis['mood']}
- 타겟 고객: {image_analysis.get('target_audience', '20-30대')}

===== 사용자 입력 =====
- 상품명: {user_context.get('product_name', '')}
- 핵심 특징: {user_context.get('key_features', '')}
- 판매 링크: {user_context.get('link', '')}

===== 요구사항 =====
- 플랫폼: {platform}
- 최대 길이: {config['max_length']}자
- 톤앤매너: {tone_guides[tone]}
- 해시태그: {config['hashtag_count']}
- 스타일: {config['style']}

===== 출력 형식 (JSON) =====
{{
  "main_caption": "메인 광고 문구 (2-3문장)",
  "variations": [
    "버전1 (같은 내용, 다른 표현)",
    "버전2",
    "버전3"
  ],
  "hashtags": ["해시태그1", "해시태그2", ...],
  "call_to_action": "행동 유도 문구 (예: 지금 바로 구매하세요!)",
  "emoji_suggestions": ["💎", "✨", ...]
}}

**중요:**
1. 타겟 고객에게 공감되는 언어 사용
2. 이미지의 분위기와 일치하는 표현
3. 플랫폼 특성에 맞는 길이와 형식
4. 해시태그는 인기 있고 관련성 높은 것으로
"""

        response = self.openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 e커머스 마케팅 카피라이터입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,  # 창의성
            max_tokens=1000
        )

        # JSON 파싱
        result = json.loads(response.choices[0].message.content)

        return result


# API 엔드포인트
@router.post("/images/{image_id}/generate-caption")
async def generate_image_caption(
    image_id: int,
    request: CaptionGenerationRequest,
    current_user: User = Depends(get_current_user)
):
    """
    이미지 기반 광고 문구 생성

    Request Body:
        {
            "tone": "friendly",  // friendly, passionate, luxury, direct
            "platform": "instagram",
            "product_name": "프리미엄 러닝화",
            "key_features": "가볍고 통기성 좋음",
            "link": "https://..."
        }
    """
    # 1. 이미지 조회
    image = await get_image(image_id)
    if not image:
        raise HTTPException(404, "이미지를 찾을 수 없어요")

    # 2. 크레딧 확인 (0.5 크레딧 차감)
    if current_user.credits < 0.5:
        raise HTTPException(402, "크레딧이 부족해요")

    generator = ImageCaptionGenerator()

    # 3. 이미지 분석 (캐싱 적용)
    cache_key = f"image_analysis:{image_id}"
    analysis = await redis.get(cache_key)

    if not analysis:
        analysis = await generator.analyze_image(image.url)
        await redis.setex(cache_key, 3600, json.dumps(analysis))
    else:
        analysis = json.loads(analysis)

    # 4. 광고 문구 생성
    captions = await generator.generate_captions(
        image_analysis=analysis,
        user_context={
            "product_name": request.product_name,
            "key_features": request.key_features,
            "link": request.link
        },
        tone=request.tone,
        platform=request.platform
    )

    # 5. 크레딧 차감
    await deduct_credit(current_user.id, 0.5, reason="caption_generation")

    # 6. 저장 (히스토리)
    await save_caption_history(
        user_id=current_user.id,
        image_id=image_id,
        captions=captions,
        tone=request.tone,
        platform=request.platform
    )

    return {
        "image_analysis": analysis,
        "captions": captions,
        "credits_remaining": current_user.credits - 0.5
    }
```

---

## 4. 맥락별 문구 생성

### 톤앤매너 (Tone) 옵션

```typescript
const toneOptions = [
  {
    id: "friendly",
    name: "밝고 친근한",
    icon: "😊",
    description: "친구에게 추천하듯 자연스럽고 밝은 느낌",
    example: "🌟 새로운 나를 만나는 시간! 프리미엄 운동화로 매일을 특별하게 만들어보세요 ✨",
    적합플랫폼: ["instagram", "kakao"],
    인기도: "high"
  },

  {
    id: "passionate",
    name: "열정적인",
    icon: "🔥",
    description: "에너지 넘치고 역동적인 느낌",
    example: "🔥 지금이 바로 그 순간! 당신의 스타일을 완성할 완벽한 운동화를 만나보세요!",
    적합플랫폼: ["instagram", "facebook"],
    인기도: "medium"
  },

  {
    id: "luxury",
    name: "고급스러운",
    icon: "💎",
    description: "세련되고 프리미엄한 느낌",
    example: "💎 디테일이 만드는 차이. 프리미엄 소재와 장인 정신이 담긴 러닝화를 경험하세요.",
    적합플랫폼: ["instagram", "naver_blog"],
    인기도: "medium"
  },

  {
    id: "direct",
    name: "직접적인",
    icon: "🎯",
    description: "간결하고 핵심만 전달",
    example: "🎯 가볍고 통기성 좋은 러닝화. 오늘만 30% 할인! 지금 바로 구매하세요.",
    적합플랫폼: ["facebook", "kakao"],
    인기도: "high"
  }
];
```

### 플랫폼별 최적화 예시

```javascript
// 같은 이미지, 다른 플랫폼
const platformOptimizedCaptions = {
  // 인스타그램: 감성적, 해시태그 많음
  instagram: {
    caption: `🌟 새로운 나를 만나는 시간!

프리미엄 운동화로 매일을 특별하게 만들어보세요 ✨

가볍고 통기성 좋은 소재로 하루 종일 편안함을 선사합니다.
당신의 스타일을 완성할 완벽한 선택 👟

지금 바로 만나보세요!
링크는 프로필에서 확인하세요 ❤️

#운동화 #스니커즈 #데일리룩 #OOTD #신발추천
#패션 #스타일 #러닝화 #운동화추천 #신발
#스니커즈추천 #패션스타그램 #daily #fashion`,

    length: 245,
    hashtags: 14,
    emojis: 6
  },

  // 페이스북: 정보 전달, 해시태그 적음
  facebook: {
    caption: `[신상품 출시] 프리미엄 러닝화 💎

✅ 가벼운 무게 (250g)
✅ 뛰어난 통기성
✅ 충격 흡수 쿠션
✅ 세련된 디자인

오늘만 특별가 30% 할인!
자세한 정보: [링크]

#운동화 #신상품 #특가`,

    length: 156,
    hashtags: 3,
    emojis: 3,
    style: "정보 중심"
  },

  // 카카오톡: 짧고 임팩트
  kakao: {
    caption: `🔥 오늘만 30% 할인!

프리미엄 러닝화
정가 89,000원 → 62,300원

가볍고 편안한 착용감
지금 바로 구매하세요 👟`,

    length: 89,
    hashtags: 0,
    emojis: 2,
    style: "할인 강조"
  },

  // 네이버 블로그: 길고 상세함
  naver_blog: {
    caption: `[상품 리뷰] 가벼움의 끝판왕! 프리미엄 러닝화 후기

안녕하세요! 오늘은 요즘 제가 푹 빠진 러닝화를 소개해드리려고 해요 ✨

# 첫인상
박스를 열자마자 느껴지는 프리미엄함!
깔끔한 디자인과 고급스러운 소재가 눈에 띄었어요.

# 착용감
놀라울 정도로 가볍습니다! (실측 250g)
발에 딱 맞는 핏감에 하루 종일 신어도 발이 안 아파요.

# 장점
1. 통기성이 정말 좋아요
2. 쿠션이 탄탄해서 충격 흡수 excellent
3. 어떤 옷에도 잘 어울리는 디자인

# 단점
1. 가격이 조금 있는 편 (하지만 가치는 충분!)

# 총평
만족도 ⭐⭐⭐⭐⭐ (5/5)

구매 링크: [링크]
오늘까지 30% 할인 중이니 서두르세요!

#운동화추천 #러닝화 #신발리뷰 #데일리슈즈`,

    length: 450,
    hashtags: 4,
    style: "리뷰 형식"
  }
};
```

---

## 5. 기술 구현

### 5.1 Frontend 컴포넌트

```tsx
// SNS 공유 컴포넌트
function SocialShareButton({ imageId, imageUrl }) {
  const [showModal, setShowModal] = useState(false);
  const [selectedPlatform, setSelectedPlatform] = useState<Platform | null>(null);
  const [tone, setTone] = useState<Tone>("friendly");
  const [caption, setCaption] = useState<CaptionResult | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  // 광고 문구 생성
  const generateCaption = async () => {
    setIsGenerating(true);

    try {
      const response = await fetch(`/api/v1/images/${imageId}/generate-caption`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tone,
          platform: selectedPlatform,
          product_name: "프리미엄 러닝화", // 사용자 입력
          key_features: "가볍고 통기성 좋음",
          link: "https://smartstore.naver.com/..."
        })
      });

      const data = await response.json();
      setCaption(data.captions);
    } catch (error) {
      showToast("문구 생성 실패", "error");
    } finally {
      setIsGenerating(false);
    }
  };

  // 플랫폼 선택 시 자동 생성
  useEffect(() => {
    if (selectedPlatform) {
      generateCaption();
    }
  }, [selectedPlatform, tone]);

  return (
    <>
      <button
        onClick={() => setShowModal(true)}
        className="btn-primary"
      >
        🚀 SNS에 바로 공유하기
      </button>

      {/* 플랫폼 선택 모달 */}
      <Modal show={showModal} onClose={() => setShowModal(false)}>
        <h2>어디에 공유할까요?</h2>

        <div className="platform-grid">
          {platforms.map(platform => (
            <PlatformCard
              key={platform.id}
              platform={platform}
              onClick={() => setSelectedPlatform(platform.id)}
            />
          ))}
        </div>
      </Modal>

      {/* 문구 생성 및 공유 모달 */}
      <Modal
        show={selectedPlatform !== null}
        onClose={() => setSelectedPlatform(null)}
        size="large"
      >
        <h2>📷 {platforms.find(p => p.id === selectedPlatform)?.name}에 공유하기</h2>

        {/* 이미지 미리보기 */}
        <div className="image-preview">
          <img src={imageUrl} alt="공유할 이미지" />
        </div>

        {/* 톤앤매너 선택 */}
        <div className="tone-selector">
          <h3>📝 광고 문구 분위기 선택</h3>
          <div className="tone-options">
            {toneOptions.map(option => (
              <button
                key={option.id}
                className={tone === option.id ? 'active' : ''}
                onClick={() => setTone(option.id)}
              >
                {option.icon} {option.name}
              </button>
            ))}
          </div>
        </div>

        {/* 생성된 문구 */}
        {isGenerating ? (
          <div className="loading">
            <Spinner />
            <p>AI가 맞춤 문구를 생성하고 있어요...</p>
          </div>
        ) : caption ? (
          <div className="caption-result">
            <h3>생성된 문구</h3>

            {/* 메인 문구 */}
            <div className="caption-box">
              <textarea
                value={caption.main_caption}
                onChange={e => setCaption({
                  ...caption,
                  main_caption: e.target.value
                })}
                rows={8}
              />

              <div className="caption-meta">
                <span>{caption.main_caption.length}자</span>
                <span>{caption.hashtags.length}개 해시태그</span>
              </div>
            </div>

            {/* 해시태그 */}
            <div className="hashtags">
              {caption.hashtags.map((tag, i) => (
                <span key={i} className="hashtag">{tag}</span>
              ))}
            </div>

            {/* 액션 버튼 */}
            <div className="actions">
              <button onClick={generateCaption}>
                🔄 다시 생성
              </button>
              <button onClick={() => navigator.clipboard.writeText(caption.main_caption)}>
                📋 복사
              </button>
              <button
                onClick={() => {
                  if (selectedPlatform === 'instagram') {
                    shareToInstagram(imageUrl, caption.main_caption);
                  } else if (selectedPlatform === 'facebook') {
                    shareToFacebook(imageUrl, caption.main_caption);
                  }
                }}
                className="btn-primary"
              >
                {selectedPlatform === 'instagram' ? '📱 인스타그램 앱으로 공유' : '공유하기'}
              </button>
            </div>
          </div>
        ) : null}
      </Modal>
    </>
  );
}
```

---

## 6. UI/UX 플로우

### 전체 플로우 다이어그램

```
[이미지 생성 완료]
       ↓
[🚀 SNS 공유 버튼 클릭]
       ↓
┌─────────────────────────┐
│  플랫폼 선택             │
│  📷 인스타그램           │
│  👍 페이스북             │
│  💬 카카오톡             │
└─────────────────────────┘
       ↓
[인스타그램 선택]
       ↓
┌─────────────────────────┐
│  톤앤매너 선택           │
│  😊 밝고 친근한          │
│  🔥 열정적인             │
│  💎 고급스러운           │
│  🎯 직접적인             │
└─────────────────────────┘
       ↓
[AI 문구 생성 중... 5초]
       ↓
┌─────────────────────────┐
│  생성된 문구             │
│  ┌───────────────────┐  │
│  │ 🌟 새로운 나를...  │  │
│  │ (편집 가능)        │  │
│  └───────────────────┘  │
│                         │
│  해시태그 (10개)         │
│  #운동화 #스니커즈 ...   │
│                         │
│  [📋 복사] [🔄 재생성]  │
└─────────────────────────┘
       ↓
[📱 인스타그램 앱으로 공유]
       ↓
┌─────────────────────────┐
│  안내 메시지             │
│  ✅ 이미지 클립보드 복사  │
│  ✅ 문구 클립보드 복사    │
│                         │
│  인스타그램 앱에서       │
│  붙여넣기하세요!         │
│                         │
│  [인스타그램 열기]       │
└─────────────────────────┘
       ↓
[완료!]
```

---

## 7. 수익화 전략

### 크레딧 차감 정책

```yaml
광고 문구 생성:
  기본 문구 (1회):
    - 크레딧: 0.5 차감
    - 포함: 메인 문구 + 해시태그 + 3가지 변형

  재생성 (톤 변경):
    - 크레딧: 0.3 차감 (할인)

  프리미엄 문구 (GPT-4 사용):
    - 크레딧: 1 차감
    - 더 창의적이고 정교한 문구
    - Pro 플랜 사용자만

SNS 공유 (무료):
  - 생성된 문구를 SNS에 공유하는 것은 무료
  - 바이럴 효과 기대

무료 혜택:
  - 첫 3회 문구 생성 무료
  - 친구 초대 시 +3회 무료
```

### 프리미엄 기능 (Pro 플랜)

```javascript
const proFeatures = {
  // Level 1: 기본 사용자
  free: {
    caption_generation: {
      model: "gpt-4o-mini",
      daily_limit: 10,
      variations: 3,
      platforms: ["instagram", "facebook"]
    }
  },

  // Level 2: Pro 플랜
  pro: {
    caption_generation: {
      model: "gpt-4", // 더 정교함
      daily_limit: 100, // 무제한에 가까움
      variations: 5,
      platforms: ["instagram", "facebook", "kakao", "naver_blog", "twitter"],

      // 추가 기능
      ab_testing: true, // A/B 테스트용 2가지 버전
      scheduled_posts: true, // 예약 게시
      analytics: true, // 문구별 성과 분석
      custom_tone: true // 커스텀 톤 저장
    },

    pricing: "39,900원/월"
  }
};
```

### 예상 수익 영향

```yaml
기대 효과:
  1. 유료 전환율 증가:
    - 현재: 15% → 개선: 20%
    - 이유: SNS 공유는 필수 기능이므로

  2. 크레딧 소비 증가:
    - 현재: 주당 5 크레딧 → 개선: 주당 8 크레딧
    - 이미지 생성(1) + 문구 생성(0.5) 패키지 판매

  3. 바이럴 효과:
    - SNS 공유 시 워터마크에 서비스 로고 추가
    - "이 이미지는 [서비스명]으로 제작되었습니다"
    - 유입 증가 예상: 20-30%

수익 시나리오:
  월 사용자 1,000명 가정:
  - 유료 전환: 200명 (20%)
  - 평균 크레딧 구매: 50 크레딧 (9,900원)
  - 문구 생성 사용: 150명 (추가 크레딧 소비)

  월 매출:
    - 기본: 200명 × 9,900원 = 1,980,000원
    - 추가 크레딧: 150명 × 5,000원 = 750,000원
    - 합계: 2,730,000원

  증가율:
    - 기존 대비 +38% (광고 문구 기능 없을 때)
```

---

## 8. 구현 우선순위

### MVP (Week 9-10)

```yaml
P0 (필수):
  ✅ SNS 공유 버튼 (인스타그램, 페이스북)
  ✅ 딥링크 + 클립보드 방식
  ✅ 기본 광고 문구 생성 (GPT-4o-mini)
  ✅ 톤앤매너 4가지 (friendly, passionate, luxury, direct)
  ✅ 플랫폼별 최적화 (인스타그램, 페이스북)

P1 (중요):
  ⬜ 이미지 분석 (GPT-4 Vision)
  ⬜ 해시태그 자동 추천
  ⬜ 카카오톡 공유

P2 (선택):
  ⬜ 문구 재생성 (0.3 크레딧)
  ⬜ 문구 히스토리 저장
```

### Post-MVP (Week 11-12)

```yaml
개선:
  ⬜ 네이버 블로그 연동
  ⬜ 예약 게시 기능 (Pro)
  ⬜ A/B 테스트용 문구 2종 생성
  ⬜ 문구 성과 분석 (클릭률, 전환율)
  ⬜ 커스텀 톤 저장 기능
```

---

## 9. 성공 지표 (KPI)

```yaml
사용률:
  - SNS 공유 버튼 클릭률: 40% 목표
  - 문구 생성 사용률: 60% 목표 (공유 클릭자 중)
  - 실제 SNS 게시율: 30% 목표

만족도:
  - 생성된 문구 만족도: 4.0/5.0 이상
  - 재생성 비율: 20% 이하 (첫 생성이 만족스러움)

비즈니스:
  - 크레딧 소비 증가: +50%
  - 유료 전환율 증가: +5%p (15% → 20%)
  - 바이럴 유입 증가: +20%
```

---

**작성일:** 2025-10-23
**버전:** 1.0
**작성자:** AI 이커머스 팀
**다음 검토:** MVP 구현 완료 후
