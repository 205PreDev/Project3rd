"""
GPT-4o-mini 광고 문구 생성 서비스
"""
from typing import Optional, List, Dict, Any
import openai
from fastapi import HTTPException
from app.core.config import settings


class CaptionGenerationService:
    """GPT-4o-mini를 통한 광고 문구 생성 서비스"""

    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set")

        openai.api_key = settings.OPENAI_API_KEY
        if settings.OPENAI_ORG_ID:
            openai.organization = settings.OPENAI_ORG_ID

        self.model = "gpt-4o-mini"  # 빠르고 저렴한 모델
        self.max_tokens = 500
        self.temperature = 0.8  # 창의성 높임

    async def generate_caption(
        self,
        product_description: str,
        platform: str = "instagram",
        style: str = "engaging",
        mood: Optional[str] = None,
        max_length: int = 100,
        include_emoji: bool = True,
        include_hashtags: bool = True
    ) -> Dict[str, Any]:
        """
        광고 문구 생성

        Args:
            product_description: 상품 설명
            platform: 플랫폼 ("instagram", "facebook", "kakao")
            style: 스타일 ("engaging", "question", "concise")
            mood: 분위기 (선택)
            max_length: 최대 글자 수
            include_emoji: 이모지 포함 여부
            include_hashtags: 해시태그 포함 여부

        Returns:
            {
                "success": bool,
                "captions": list[str],  # 3가지 옵션
                "hashtags": list[str],
                "platform": str
            }
        """
        try:
            # 플랫폼별 특성 정의
            platform_specs = {
                "instagram": {
                    "max_length": 2200,
                    "tone": "visual and trendy",
                    "hashtag_count": "5-10"
                },
                "facebook": {
                    "max_length": 500,
                    "tone": "friendly and conversational",
                    "hashtag_count": "3-5"
                },
                "kakao": {
                    "max_length": 1000,
                    "tone": "casual and personal",
                    "hashtag_count": "3-7"
                }
            }

            spec = platform_specs.get(platform.lower(), platform_specs["instagram"])

            # 스타일별 지침
            style_prompts = {
                "engaging": "Create engaging, emotional captions that connect with the audience",
                "question": "Use questions to spark curiosity and engagement",
                "concise": "Keep it short, punchy, and memorable"
            }

            style_guide = style_prompts.get(style.lower(), style_prompts["engaging"])

            # 프롬프트 구성
            prompt = f"""
Generate 3 different {platform} ad captions for this product:

Product: {product_description}
{f"Mood/Vibe: {mood}" if mood else ""}

Requirements:
- Platform: {platform} ({spec['tone']})
- Style: {style_guide}
- Max length: {max_length} characters
- {"Include relevant emojis" if include_emoji else "No emojis"}
- {"Suggest {spec['hashtag_count']} relevant hashtags" if include_hashtags else "No hashtags"}

Return in JSON format:
{{
    "captions": ["caption1", "caption2", "caption3"],
    "hashtags": ["tag1", "tag2", "tag3", ...]
}}

Make each caption unique and compelling. Focus on benefits and emotional appeal.
"""

            # OpenAI API 호출
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a creative social media copywriter specialized in product marketing."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )

            result = response.choices[0].message.content

            # JSON 파싱
            import json
            try:
                parsed = json.loads(result)
                return {
                    "success": True,
                    "captions": parsed.get("captions", []),
                    "hashtags": parsed.get("hashtags", []),
                    "platform": platform
                }
            except json.JSONDecodeError:
                # 파싱 실패 시 기본 응답
                return {
                    "success": False,
                    "captions": [result],
                    "hashtags": [],
                    "platform": platform,
                    "error": "Failed to parse JSON response"
                }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate caption: {str(e)}"
            )

    async def generate_multi_platform_captions(
        self,
        product_description: str,
        mood: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        모든 플랫폼용 광고 문구 생성

        Args:
            product_description: 상품 설명
            mood: 분위기 (선택)

        Returns:
            플랫폼별 광고 문구
        """
        try:
            results = {}

            for platform in ["instagram", "facebook", "kakao"]:
                result = await self.generate_caption(
                    product_description=product_description,
                    platform=platform,
                    style="engaging",
                    mood=mood
                )
                results[platform] = result

            return {
                "success": True,
                "platforms": results
            }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate multi-platform captions: {str(e)}"
            )

    async def generate_caption_with_product_analysis(
        self,
        product_analysis: Dict[str, Any],
        platform: str = "instagram",
        style: str = "engaging"
    ) -> Dict[str, Any]:
        """
        상품 분석 결과를 기반으로 광고 문구 생성

        Args:
            product_analysis: GPT-4 Vision 분석 결과
            platform: 플랫폼
            style: 스타일

        Returns:
            광고 문구
        """
        # 분석 결과에서 정보 추출
        category = product_analysis.get("category", "product")
        colors = ", ".join(product_analysis.get("colors", []))
        mood = product_analysis.get("mood", "modern")
        description = product_analysis.get("description", "")

        # 상세한 상품 설명 구성
        product_description = f"""
Category: {category}
Colors: {colors}
Style: {mood}
Description: {description}
"""

        return await self.generate_caption(
            product_description=product_description,
            platform=platform,
            style=style,
            mood=mood
        )

    async def optimize_caption_for_seo(
        self,
        caption: str,
        keywords: List[str]
    ) -> Dict[str, Any]:
        """
        SEO 키워드를 활용한 캡션 최적화

        Args:
            caption: 원본 캡션
            keywords: SEO 키워드 리스트

        Returns:
            최적화된 캡션
        """
        prompt = f"""
Optimize this social media caption by naturally incorporating these SEO keywords:

Original caption: {caption}

Keywords to include: {", ".join(keywords)}

Requirements:
- Keep the original tone and style
- Naturally integrate keywords without forcing them
- Maintain readability and engagement
- Return the optimized caption only

Optimized caption:
"""

        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=300,
                temperature=0.7
            )

            optimized = response.choices[0].message.content

            return {
                "success": True,
                "original": caption,
                "optimized": optimized,
                "keywords_used": keywords
            }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to optimize caption: {str(e)}"
            )


# 싱글톤 인스턴스
_caption_service: Optional[CaptionGenerationService] = None


def get_caption_service() -> CaptionGenerationService:
    """CaptionGenerationService 싱글톤 인스턴스 반환"""
    global _caption_service
    if _caption_service is None:
        _caption_service = CaptionGenerationService()
    return _caption_service
