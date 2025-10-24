"""
Google Gemini API Service
이미지 분석 및 광고 문구 생성
"""
import os
import json
from typing import Dict, Optional, List
from fastapi import HTTPException
try:
    import google.generativeai as genai
except ImportError:
    genai = None
from app.core.config import get_settings

settings = get_settings()


class GeminiService:
    """Google Gemini API를 사용한 이미지 분석 및 텍스트 생성 서비스"""

    def __init__(self):
        """Initialize Gemini service"""
        if genai is None:
            raise ImportError("google-generativeai package is not installed. Run: pip install google-generativeai")

        self.api_key = settings.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY must be set in environment variables")

        # Configure Gemini API
        genai.configure(api_key=self.api_key)

        # Use Gemini 2.5 Flash (무료 티어, 이미지 분석 지원)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        print("✅ Using model: gemini-2.5-flash")

    def analyze_image(self, image_data: bytes) -> Dict[str, any]:
        """
        이미지를 분석하여 카테고리, 색상, 분위기 등을 추출

        Args:
            image_data: 이미지 바이트 데이터

        Returns:
            Dict containing:
            - category: 상품 카테고리
            - colors: 주요 색상 리스트
            - mood: 분위기/스타일
            - description: 상품 설명
        """
        try:
            # PIL Image로 변환
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_data))

            # Gemini API 요청 prompt
            prompt = """
이 이미지를 분석하여 다음 정보를 JSON 형식으로 제공해주세요:

1. category: 상품의 카테고리 (예: 전자기기, 패션, 가구, 식품 등)
2. colors: 이미지에서 주요 색상 3개 (영문, 예: ["black", "white", "red"])
3. mood: 이미지의 전반적인 분위기 (예: modern, vintage, elegant, casual, professional)
4. description: 상품에 대한 간단한 설명 (1-2문장, 한글)

응답은 반드시 다음 형식의 JSON만 출력하세요:
{
  "category": "카테고리",
  "colors": ["색상1", "색상2", "색상3"],
  "mood": "분위기",
  "description": "설명"
}
"""

            # Gemini로 이미지 분석
            response = self.model.generate_content([prompt, image])

            # 응답 텍스트 추출
            text = response.text.strip()

            # JSON 파싱 (마크다운 코드 블록 제거)
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

            analysis = json.loads(text)
            return analysis

        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse Gemini response: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to analyze image with Gemini: {str(e)}"
            )

    def generate_caption(
        self,
        product_description: str,
        platform: str = "instagram",
        style: str = "감성형",
        length: str = "medium"
    ) -> List[str]:
        """
        상품 설명을 기반으로 SNS 광고 문구 생성

        Args:
            product_description: 상품 설명
            platform: SNS 플랫폼 (instagram, facebook, kakao)
            style: 문구 스타일 (감성형, 질문형, 간결형)
            length: 문구 길이 (short, medium, long)

        Returns:
            광고 문구 3개의 리스트
        """
        try:
            # 플랫폼별 가이드라인
            platform_guide = {
                "instagram": "해시태그와 이모지를 활용하고, 시각적이고 감성적인 표현",
                "facebook": "친근하고 대화형 톤, 행동 유도 문구 포함",
                "kakao": "간결하고 직관적인 메시지, 이모지 적절히 활용"
            }

            # 스타일별 가이드
            style_guide = {
                "감성형": "감성적이고 스토리텔링이 있는 표현",
                "질문형": "고객에게 질문을 던지는 형식으로 호기심 유발",
                "간결형": "핵심 메시지만 간결하게 전달"
            }

            # 길이별 가이드
            length_guide = {
                "short": "1-2문장 (50자 이내)",
                "medium": "2-3문장 (50-100자)",
                "long": "3-4문장 (100-150자)"
            }

            prompt = f"""
다음 상품에 대한 {platform} SNS 광고 문구를 3가지 만들어주세요.

상품 설명: {product_description}

요구사항:
- 플랫폼: {platform} ({platform_guide.get(platform, '')})
- 스타일: {style} ({style_guide.get(style, '')})
- 길이: {length} ({length_guide.get(length, '')})
- 각 문구는 서로 다른 접근 방식 사용
- 자연스러운 한국어 표현
- AI가 생성했다는 언급 없이 작성

응답은 반드시 다음 형식의 JSON만 출력하세요:
{{
  "captions": [
    "광고 문구 1",
    "광고 문구 2",
    "광고 문구 3"
  ]
}}
"""

            # Gemini로 텍스트 생성
            response = self.model.generate_content(prompt)

            # 응답 텍스트 추출
            text = response.text.strip()

            # JSON 파싱 (마크다운 코드 블록 제거)
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

            captions_data = json.loads(text)
            return captions_data.get("captions", [])

        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse Gemini response: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate caption with Gemini: {str(e)}"
            )


# Singleton instance
_gemini_service = None


def get_gemini_service() -> GeminiService:
    """Get or create GeminiService singleton"""
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service
