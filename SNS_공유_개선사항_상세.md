# SNS 공유 기능 개선사항 상세

## 📋 개선사항 요약

사용자 피드백을 반영한 4가지 핵심 개선사항:

1. **"바로" 문구 제거** - 사용자 통제 강화
2. **문구 생성 조건 세분화** - 커스터마이징 강화
3. **3가지 옵션 제공** - 선택의 폭 확대
4. **AI 제작 표시** - 투명성과 신뢰도 향상

---

## 1. 버튼 문구 변경

### 변경 전 (문제)
```
[🚀 SNS에 바로 공유하기]
```

**문제점:**
- "바로"라는 단어가 사용자 통제 없이 자동 게시될 것 같은 오해 유발
- 사용자가 검토할 시간 없이 즉시 진행될 것 같은 불안감

### 변경 후 (개선)
```
[📤 SNS에 공유하기]
```

**개선 효과:**
- 중립적인 표현으로 사용자에게 충분한 통제권 부여
- 공유 전 준비 단계가 있음을 암시
- 사용자 불안감 해소

---

## 2. 문구 생성 조건 세분화

### 기존 (단순)
```
분위기 선택만 제공:
  😊 밝고 친근한
  🔥 열정적인
  💎 고급스러운
  🎯 직접 작성
```

### 개선 (상세 설정)

```yaml
┌─────────────────────────────────────────────┐
│  📝 광고 문구 생성 설정                      │
├─────────────────────────────────────────────┤
│                                             │
│  1️⃣ 분위기 선택 (또는 직접 작성)            │
│     😊 밝고 친근한                           │
│     🔥 열정적인                              │
│     💎 고급스러운                            │
│     ✏️ 직접 작성                             │
│                                             │
│  2️⃣ 문구 스타일 (다중 선택 가능)            │
│     길이:                                   │
│       ☐ 짧게 (2-3문장)                      │
│       ☑ 보통 (4-5문장) ⭐ 권장              │
│       ☐ 길게 (6문장 이상)                   │
│                                             │
│     표현:                                   │
│       ☑ 이모지 사용                         │
│       ☐ 미사여구 자제 (간결하게)            │
│       ☐ 과한 표현 자제 (과장 금지)          │
│       ☑ 해시태그 포함 (10-15개)             │
│                                             │
│  3️⃣ 추가 입력 (선택)                        │
│     프롬프트 입력:                           │
│     ┌─────────────────────────────────────┐ │
│     │ 예: "할인 정보 강조"                │ │
│     │     "환경 보호 강조"                │ │
│     │     "브랜드 스토리 포함"            │ │
│     └─────────────────────────────────────┘ │
│                                             │
│  [✨ AI 문구 생성하기 (-0.5 크레딧)]        │
│                                             │
└─────────────────────────────────────────────┘
```

### 설정 옵션 상세

#### 2️⃣-1. 길이 옵션

```javascript
const lengthOptions = {
  short: {
    label: "짧게 (2-3문장)",
    target_length: "100-150자",
    suitable_for: ["카카오톡", "트위터"],
    example: `스타일과 편안함을 모두 잡은 러닝화 👟
지금 만나보세요!
링크는 프로필 ↑

#운동화 #스니커즈 #데일리 #패션`
  },

  medium: {
    label: "보통 길이 (4-5문장)",
    target_length: "200-300자",
    suitable_for: ["인스타그램", "페이스북"],
    recommended: true,
    example: `🌟 새로운 나를 만나는 시간!

프리미엄 운동화로 매일을 특별하게 만들어보세요 ✨

가벼운 착화감과 트렌디한 디자인으로
당신의 스타일을 완성해드려요 👟

지금 바로 만나보세요!
링크는 프로필에서 확인하세요 ❤️

#운동화 #스니커즈 #데일리룩 #OOTD
#신발추천 #패션 #스타일`
  },

  long: {
    label: "길게 (6문장 이상)",
    target_length: "400-600자",
    suitable_for: ["네이버 블로그", "페이스북"],
    example: `[신상품 출시] 당신의 발걸음을 가볍게! 🌟

안녕하세요! 오늘은 특별한 신상품을 소개해드려요.

✨ 이런 분들께 추천해요:
• 하루 종일 서서 일하시는 분
• 가벼운 운동화를 찾으시는 분
• 트렌디한 디자인을 좋아하시는 분

💎 핵심 특징:
1. 초경량 소재 (250g)
2. 통기성 좋은 메쉬 원단
3. 충격 흡수 쿠션
4. 어떤 옷에도 어울리는 디자인

🎁 오늘만 특별 할인!
정가 89,000원 → 62,300원 (30% OFF)

자세한 정보는 프로필 링크에서 확인하세요!

#운동화 #스니커즈 #신상품 #특가 #데일리
#패션 #스타일 #러닝화 #신발추천`
  }
};
```

#### 2️⃣-2. 표현 스타일 옵션

```javascript
const styleOptions = {
  // 이모지 사용 여부
  use_emoji: {
    label: "이모지 사용",
    default: true,
    effect: {
      enabled: "감성적이고 눈에 띄는 문구",
      disabled: "깔끔하고 전문적인 문구"
    },
    example_enabled: "🌟 새로운 나를 만나는 시간! ✨",
    example_disabled: "새로운 나를 만나는 시간!"
  },

  // 미사여구 자제
  avoid_flowery: {
    label: "미사여구 자제 (간결하게)",
    default: false,
    effect: {
      enabled: "간결하고 직설적인 표현",
      disabled: "감성적이고 풍부한 표현"
    },
    example_enabled: "가벼운 운동화. 편안한 착화감. 지금 구매하세요.",
    example_disabled: "당신의 발걸음을 더욱 가볍고 특별하게 만들어줄 프리미엄 운동화를 만나보세요."
  },

  // 과한 표현 자제
  avoid_exaggeration: {
    label: "과한 표현 자제 (과장 금지)",
    default: false,
    prohibited_phrases: [
      "최고의", "세계 최초", "혁명적인", "기적의",
      "완벽한", "절대", "무조건", "100%"
    ],
    effect: {
      enabled: "사실 중심의 정직한 표현",
      disabled: "강조와 과장을 포함한 표현"
    },
    example_enabled: "가벼운 소재로 만든 편안한 운동화입니다.",
    example_disabled: "세계 최고 수준의 혁명적인 초경량 운동화! 완벽한 착화감을 경험하세요!"
  },

  // 해시태그 포함
  include_hashtags: {
    label: "해시태그 포함",
    default: true,
    options: {
      count: {
        instagram: "10-15개 (최대 30개)",
        facebook: "3-5개 권장",
        kakao: "0개 (사용 안 함)"
      }
    },
    example: "#운동화 #스니커즈 #데일리룩 #OOTD #신발추천"
  }
};
```

#### 3️⃣ 프롬프트 추가 입력

```javascript
const promptExamples = [
  {
    category: "할인/프로모션",
    prompts: [
      "30% 할인 정보를 강조해주세요",
      "오늘만 특가라는 걸 부각해주세요",
      "무료 배송 혜택을 언급해주세요",
      "첫 구매 고객 할인을 포함해주세요"
    ]
  },
  {
    category: "브랜드/가치",
    prompts: [
      "환경 보호 가치를 강조해주세요",
      "수제 제작 과정을 언급해주세요",
      "브랜드 스토리를 포함해주세요",
      "장인 정신을 강조해주세요"
    ]
  },
  {
    category: "기능/특징",
    prompts: [
      "통기성이 좋다는 점을 강조해주세요",
      "가벼운 무게를 부각해주세요",
      "내구성이 뛰어나다는 걸 언급해주세요",
      "쿠션이 좋다는 점을 포함해주세요"
    ]
  },
  {
    category: "감성/스토리",
    prompts: [
      "일상의 소중함을 담아주세요",
      "꿈을 향한 도전을 연상시켜주세요",
      "자신감을 주는 느낌으로 작성해주세요",
      "따뜻한 감성을 담아주세요"
    ]
  }
];

// UI에서 예시 표시
<PromptInput>
  <label>프롬프트 입력 (상세 요청사항):</label>
  <textarea
    placeholder="예: 할인 정보 강조, 환경 보호 강조"
    maxLength={200}
  />

  <details>
    <summary>💡 예시 보기</summary>
    <div className="prompt-examples">
      {promptExamples.map(category => (
        <div key={category.category}>
          <h4>{category.category}</h4>
          <ul>
            {category.prompts.map((prompt, i) => (
              <li key={i} onClick={() => setPrompt(prompt)}>
                {prompt}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  </details>
</PromptInput>
```

---

## 3. 3가지 옵션 제공

### 기존 (단일 결과)
```
생성된 문구 1개만 제공
  → 마음에 안 들면 재생성 (추가 크레딧 소비)
  → 선택의 폭 없음
```

### 개선 (3가지 옵션)

```yaml
생성된 문구 3가지 중 선택:

┌─────────────────────────────────────────┐
│  ⭕ 옵션 1 (추천) - 감성형               │
│  ───────────────────────────────────    │
│  🌟 새로운 나를 만나는 시간!            │
│                                         │
│  프리미엄 운동화로 매일을 특별하게      │
│  만들어보세요 ✨                        │
│                                         │
│  지금 바로 만나보세요 👟                │
│                                         │
│  #운동화 #스니커즈 #데일리룩            │
│                                         │
│  📊 245자 | 🏷️ 8개 해시태그             │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  ⚪ 옵션 2 - 질문형                      │
│  ───────────────────────────────────    │
│  매일 신는 운동화,                      │
│  특별해져야 하지 않을까요?              │
│                                         │
│  가벼운 착화감과 트렌디한 디자인으로    │
│  당신의 일상을 업그레이드하세요 ⚡      │
│                                         │
│  #운동화 #스니커즈 #패션                │
│                                         │
│  📊 168자 | 🏷️ 6개 해시태그             │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  ⚪ 옵션 3 (간결) - 직접형               │
│  ───────────────────────────────────    │
│  스타일과 편안함, 둘 다 잡은 러닝화 👟  │
│                                         │
│  지금 만나보세요!                       │
│  링크는 프로필 ↑                        │
│                                         │
│  #운동화 #스니커즈                      │
│                                         │
│  📊 95자 | 🏷️ 4개 해시태그              │
└─────────────────────────────────────────┘
```

### 옵션 생성 전략

```python
async def generate_three_variations(
    image_analysis: dict,
    user_settings: dict,
    tone: str
) -> list[dict]:
    """
    3가지 스타일의 문구 생성

    Returns:
        [
            {
                "type": "recommended",  # 감성형 (추천)
                "caption": "...",
                "length": 245,
                "hashtag_count": 8
            },
            {
                "type": "question",  # 질문형
                "caption": "...",
                "length": 168,
                "hashtag_count": 6
            },
            {
                "type": "concise",  # 간결형
                "caption": "...",
                "length": 95,
                "hashtag_count": 4
            }
        ]
    """

    # GPT 프롬프트 구성
    prompt = f"""
다음 이미지와 설정을 바탕으로 **3가지 스타일**의 광고 문구를 생성해주세요.

===== 이미지 분석 =====
{json.dumps(image_analysis, ensure_ascii=False, indent=2)}

===== 사용자 설정 =====
분위기: {tone}
길이: {user_settings['length']}
이모지 사용: {user_settings['use_emoji']}
미사여구 자제: {user_settings['avoid_flowery']}
과한 표현 자제: {user_settings['avoid_exaggeration']}
추가 요청: {user_settings.get('custom_prompt', '')}

===== 요구사항 =====
3가지 스타일로 각각 생성:

1. 감성형 (추천):
   - 감성적이고 따뜻한 느낌
   - 이야기가 있는 문구
   - 중간 길이 (200-250자)
   - 해시태그 8-10개

2. 질문형:
   - 질문으로 시작하여 공감 유도
   - 문제 → 해결 구조
   - 조금 짧게 (150-200자)
   - 해시태그 5-7개

3. 간결형:
   - 핵심만 간결하게
   - 강렬한 한 줄
   - 짧게 (80-120자)
   - 해시태그 3-5개

===== 출력 형식 (JSON) =====
{{
  "variations": [
    {{
      "type": "recommended",
      "caption": "감성형 문구...",
      "length": 245,
      "hashtags": ["#운동화", ...],
      "hashtag_count": 8
    }},
    {{
      "type": "question",
      "caption": "질문형 문구...",
      "length": 168,
      "hashtags": [...],
      "hashtag_count": 6
    }},
    {{
      "type": "concise",
      "caption": "간결형 문구...",
      "length": 95,
      "hashtags": [...],
      "hashtag_count": 4
    }}
  ]
}}

**중요:**
- 사용자가 "미사여구 자제" 선택 시 화려한 표현 금지
- "과한 표현 자제" 선택 시 "최고", "완벽", "혁명적" 등 금지
- 각 스타일은 명확히 구분되어야 함
"""

    response = await openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 e커머스 마케팅 카피라이터입니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=1500
    )

    result = json.loads(response.choices[0].message.content)
    return result["variations"]
```

### 사용자 선택 UI

```tsx
function CaptionVariationSelector({ variations, onSelect }) {
  const [selected, setSelected] = useState<number>(0);

  return (
    <div className="caption-variations">
      <h3>생성된 문구 3가지 중 선택하세요</h3>

      {variations.map((variant, index) => (
        <div
          key={index}
          className={`variation-card ${selected === index ? 'selected' : ''}`}
          onClick={() => setSelected(index)}
        >
          {/* 라디오 버튼 */}
          <div className="radio">
            {selected === index ? '⭕' : '⚪'}
          </div>

          {/* 타입 표시 */}
          <div className="type-badge">
            {variant.type === 'recommended' && '추천'}
            {variant.type === 'question' && '질문형'}
            {variant.type === 'concise' && '간결'}
          </div>

          {/* 문구 */}
          <div className="caption-text">
            {variant.caption}
          </div>

          {/* 메타 정보 */}
          <div className="meta">
            <span>📊 {variant.length}자</span>
            <span>🏷️ {variant.hashtag_count}개 해시태그</span>
          </div>
        </div>
      ))}

      {/* 액션 버튼 */}
      <div className="actions">
        <button onClick={() => regenerate()}>
          🔄 다시 생성 (-0.3 크레딧)
        </button>
        <button onClick={() => onSelect(variations[selected])}>
          ✅ 이 문구 사용하기
        </button>
      </div>
    </div>
  );
}
```

---

## 4. AI 제작 표시 (투명성)

### 이유

```yaml
긍정적 효과:
  1. 투명성 향상:
    - 사용자에게 AI 사용 사실을 명확히 고지
    - 윤리적이고 정직한 브랜드 이미지

  2. 바이럴 마케팅:
    - AI 도구에 관심 있는 사람들의 유입
    - "어떤 툴 쓰셨어요?" → 자연스러운 홍보

  3. 차별화:
    - 경쟁사는 AI 사용 사실을 숨김
    - 우리는 당당하게 공개 → 신뢰도 상승

부정적 우려 완화:
  - "AI로 만들어서 성의 없다"는 인식
    → 해결: 고품질 결과물로 증명
    → "AI로 이 정도 퀄리티가?"라는 긍정 반응 유도
```

### 표시 위치 및 형식

```yaml
┌─────────────────────────────────────────────┐
│  [완성된 광고 이미지]                        │
│  [선택한 광고 문구]                          │
│                                             │
│  [📱 인스타그램 앱으로 공유하기]             │
│                                             │
│  ────────────────────────────────────       │
│  ℹ️ 이 광고는 [서비스명] AI로 제작되었습니다. │
│     GPT-4o-mini 사용 • 제작 시간: 5초        │
│  ────────────────────────────────────       │
│                                             │
│  💡 더 알아보기: [링크]                      │
└─────────────────────────────────────────────┘
```

### 상세 표시 옵션

```javascript
const aiAttributionOptions = {
  // MVP: 간단한 표시
  simple: {
    text: "이 광고는 [서비스명] AI로 제작되었습니다.",
    position: "화면 하단",
    style: "작고 눈에 띄지 않게",
    color: "gray"
  },

  // 상세 표시
  detailed: {
    text: `ℹ️ 제작 정보:
- 이미지: Rembg (배경 제거) + Unsplash (배경)
- 광고 문구: GPT-4o-mini
- 제작 시간: 5초
- 도구: [서비스명]`,
    position: "모달 또는 접을 수 있는 섹션",
    cta: "💡 더 알아보기"
  },

  // 워터마크 (이미지에 직접)
  watermark: {
    text: "Made with [서비스명]",
    position: "이미지 우측 하단",
    opacity: 0.3,
    removable: true, // Pro 플랜에서 제거 가능
    size: "small"
  },

  // 광고 문구 내 포함
  in_caption: {
    text: "\n\n───\n📸 이미지: [서비스명] AI\n✍️ 문구: GPT-4o-mini",
    position: "광고 문구 맨 아래",
    optional: true, // 사용자가 제거 가능
    benefit: "바이럴 효과"
  }
};
```

### 구현 예시

```tsx
// AI 제작 정보 컴포넌트
function AIAttributionBadge({ mode = "simple", removable = false }) {
  const [collapsed, setCollapsed] = useState(true);

  if (mode === "simple") {
    return (
      <div className="ai-attribution simple">
        <span className="icon">ℹ️</span>
        <span className="text">
          이 광고는 <strong>[서비스명]</strong> AI로 제작되었습니다.
        </span>
        {removable && (
          <button className="remove" onClick={() => {}}>
            제거 (Pro)
          </button>
        )}
      </div>
    );
  }

  if (mode === "detailed") {
    return (
      <details className="ai-attribution detailed" open={!collapsed}>
        <summary onClick={() => setCollapsed(!collapsed)}>
          <span className="icon">🤖</span>
          <span>AI 제작 정보 보기</span>
        </summary>

        <div className="content">
          <h4>제작 과정</h4>
          <ul>
            <li>
              <strong>이미지 배경 제거:</strong> Rembg (AI 모델)
            </li>
            <li>
              <strong>배경 합성:</strong> Unsplash 고품질 이미지
            </li>
            <li>
              <strong>광고 문구:</strong> GPT-4o-mini (OpenAI)
            </li>
            <li>
              <strong>제작 시간:</strong> 약 5초
            </li>
          </ul>

          <div className="cta">
            <a href="/about-ai" target="_blank">
              💡 AI 기술 더 알아보기
            </a>
          </div>
        </div>
      </details>
    );
  }

  return null;
}

// 사용 예시
<ShareModal>
  {/* 이미지 미리보기 */}
  <ImagePreview src={imageUrl} />

  {/* 광고 문구 */}
  <CaptionEditor caption={selectedCaption} />

  {/* AI 제작 정보 */}
  <AIAttributionBadge
    mode="simple"
    removable={user.plan === "pro"}
  />

  {/* 공유 버튼 */}
  <ShareButton platform="instagram" />
</ShareModal>
```

### 워터마크 옵션 (이미지에 직접)

```python
from PIL import Image, ImageDraw, ImageFont

def add_ai_watermark(
    image_path: str,
    service_name: str,
    position: str = "bottom-right",
    opacity: float = 0.3
) -> str:
    """
    이미지에 AI 제작 워터마크 추가

    Args:
        image_path: 원본 이미지 경로
        service_name: 서비스 이름
        position: 워터마크 위치
        opacity: 투명도 (0.0 ~ 1.0)

    Returns:
        watermarked_image_path: 워터마크 추가된 이미지 경로
    """
    img = Image.open(image_path).convert("RGBA")

    # 워터마크 레이어 생성
    txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)

    # 폰트 설정
    font = ImageFont.truetype("arial.ttf", 20)

    # 텍스트
    watermark_text = f"Made with {service_name}"

    # 위치 계산
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    if position == "bottom-right":
        x = img.width - text_width - 20
        y = img.height - text_height - 20
    elif position == "bottom-left":
        x = 20
        y = img.height - text_height - 20
    elif position == "center":
        x = (img.width - text_width) // 2
        y = (img.height - text_height) // 2

    # 워터마크 그리기
    alpha = int(255 * opacity)
    draw.text(
        (x, y),
        watermark_text,
        font=font,
        fill=(255, 255, 255, alpha)
    )

    # 합성
    watermarked = Image.alpha_composite(img, txt)

    # 저장
    output_path = image_path.replace(".png", "_watermarked.png")
    watermarked.convert("RGB").save(output_path, quality=95)

    return output_path
```

---

## 5. 사용자 제어 강화 요약

### Before (기존)
```
1. SNS 공유 버튼 클릭
   ↓
2. 플랫폼 선택
   ↓
3. 자동 생성된 문구 1개 표시
   ↓
4. 마음에 안 들면 재생성 (추가 크레딧)
   ↓
5. 공유
```

### After (개선)
```
1. SNS 공유 버튼 클릭
   ↓
2. 플랫폼 선택
   ↓
3. 상세 설정 (분위기, 길이, 스타일, 프롬프트)
   ↓
4. 3가지 옵션 중 선택
   ↓
5. 선택한 문구 편집 가능
   ↓
6. AI 제작 정보 확인 (투명성)
   ↓
7. 공유
```

### 개선 효과

```yaml
사용자 만족도:
  - 통제권 강화: 70% → 95%
  - 문구 만족도: 3.5/5 → 4.5/5
  - 재생성 비율: 40% → 15% (3개 중 선택하므로)

비즈니스 지표:
  - 크레딧 절약: 재생성 감소로 사용자 비용 절감
  - 완료율 증가: 40% → 70% (선택지 제공으로)
  - 바이럴 효과: AI 제작 표시로 유입 +20%

기술 지표:
  - API 호출 절감: 재생성 감소로 비용 절감
  - 사용자 체류 시간: +30% (설정 시간 포함)
```

---

## 6. MVP 구현 우선순위

### P0 (필수 - Week 9-10)
```yaml
✅ 버튼 문구 변경:
  - "SNS에 바로 공유하기" → "SNS에 공유하기"

✅ 기본 설정 옵션:
  - 분위기 선택 (4가지)
  - 길이 선택 (3가지)
  - 이모지 사용 여부

✅ 3가지 옵션 제공:
  - 감성형 (추천)
  - 질문형
  - 간결형

✅ AI 제작 표시 (simple):
  - 화면 하단에 작게 표시
  - "이 광고는 [서비스명] AI로 제작되었습니다."
```

### P1 (중요 - Week 11-12)
```yaml
⬜ 고급 설정 옵션:
  - 미사여구 자제
  - 과한 표현 자제
  - 해시태그 개수 조절

⬜ 프롬프트 추가 입력:
  - 자유 입력 (200자)
  - 예시 제공

⬜ AI 제작 정보 상세:
  - 접을 수 있는 섹션
  - 제작 과정 설명
  - "더 알아보기" 링크
```

### P2 (선택 - Post-MVP)
```yaml
⬜ 워터마크 옵션:
  - 이미지에 직접 표시
  - Pro 플랜에서 제거 가능

⬜ 광고 문구 내 AI 표시:
  - 문구 맨 아래 포함
  - 사용자가 제거 가능

⬜ 커스텀 톤 저장:
  - 자주 쓰는 설정 저장
  - "내 스타일" 프리셋
```

---

**작성일:** 2025-10-23
**버전:** 1.0
**작성자:** AI 이커머스 팀
**다음 검토:** MVP 구현 완료 후
