"""
OpenAI GPT-4 Vision 이미지 분석 서비스
"""
import base64
from typing import Optional, Dict, Any
import openai
from fastapi import HTTPException, UploadFile
from app.core.config import settings


class OpenAIVisionService:
    """GPT-4 Vision을 통한 이미지 분석 서비스"""

    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set")

        openai.api_key = settings.OPENAI_API_KEY
        if settings.OPENAI_ORG_ID:
            openai.organization = settings.OPENAI_ORG_ID

        self.model = "gpt-4-vision-preview"
        self.max_tokens = 500

    def _encode_image(self, image_bytes: bytes) -> str:
        """
        이미지를 Base64로 인코딩

        Args:
            image_bytes: 이미지 바이트 데이터

        Returns:
            Base64 인코딩된 문자열
        """
        return base64.b64encode(image_bytes).decode('utf-8')

    async def analyze_image(
        self,
        image_file: UploadFile,
        prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        이미지 분석 (범용)

        Args:
            image_file: 업로드된 이미지 파일
            prompt: 커스텀 프롬프트 (선택)

        Returns:
            분석 결과 딕셔너리
        """
        try:
            # 이미지 읽기 및 인코딩
            image_bytes = await image_file.read()
            base64_image = self._encode_image(image_bytes)

            # 기본 프롬프트
            if not prompt:
                prompt = "Describe this image in detail."

            # GPT-4 Vision API 호출
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=self.max_tokens
            )

            result = response.choices[0].message.content

            return {
                "success": True,
                "analysis": result,
                "model": self.model
            }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to analyze image: {str(e)}"
            )

    async def analyze_product(
        self,
        image_file: UploadFile
    ) -> Dict[str, Any]:
        """
        상품 이미지 분석 (카테고리, 색상, 분위기)

        Args:
            image_file: 업로드된 상품 이미지

        Returns:
            {
                "success": bool,
                "category": str,
                "colors": list[str],
                "mood": str,
                "description": str,
                "background_suggestions": list[str]
            }
        """
        prompt = """
Analyze this product image and provide the following information in JSON format:
{
    "category": "main product category (e.g., fashion, food, tech, beauty, sports, home)",
    "subcategory": "specific subcategory if applicable",
    "colors": ["list of dominant colors"],
    "mood": "overall mood/vibe (e.g., elegant, playful, modern, rustic)",
    "description": "brief product description",
    "background_suggestions": ["3 suggested background styles that would complement this product"]
}

Please respond ONLY with valid JSON, no additional text.
"""

        try:
            result = await self.analyze_image(image_file, prompt)
            analysis = result["analysis"]

            # JSON 파싱 시도
            import json
            try:
                parsed = json.loads(analysis)
                return {
                    "success": True,
                    **parsed
                }
            except json.JSONDecodeError:
                # JSON 파싱 실패 시 기본값 반환
                return {
                    "success": False,
                    "category": "general",
                    "colors": ["neutral"],
                    "mood": "modern",
                    "description": analysis,
                    "background_suggestions": ["minimalist", "gradient", "texture"]
                }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to analyze product: {str(e)}"
            )

    async def analyze_product_from_bytes(
        self,
        image_bytes: bytes
    ) -> Dict[str, Any]:
        """
        바이트 데이터에서 상품 분석

        Args:
            image_bytes: 이미지 바이트 데이터

        Returns:
            분석 결과
        """
        prompt = """
Analyze this product image and provide:
1. Main category (fashion/food/tech/beauty/sports/home/other)
2. Top 3 dominant colors
3. Overall mood/aesthetic
4. Brief description
5. 3 background style recommendations

Format: JSON
"""

        try:
            base64_image = self._encode_image(image_bytes)

            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=self.max_tokens
            )

            analysis = response.choices[0].message.content

            # JSON 파싱
            import json
            try:
                parsed = json.loads(analysis)
                return {"success": True, **parsed}
            except:
                return {
                    "success": False,
                    "category": "general",
                    "colors": ["neutral"],
                    "mood": "modern",
                    "description": analysis,
                    "background_suggestions": ["minimalist", "gradient", "texture"]
                }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to analyze product from bytes: {str(e)}"
            )

    async def get_seo_keywords(
        self,
        image_file: UploadFile
    ) -> Dict[str, Any]:
        """
        SEO 키워드 추출

        Args:
            image_file: 업로드된 이미지

        Returns:
            SEO 키워드 리스트
        """
        prompt = """
Analyze this image and suggest 10 SEO-friendly keywords that would help this product rank better in search engines.
Consider:
- Product type and category
- Visual characteristics
- Target audience
- Use cases

Return only the keywords as a JSON array: ["keyword1", "keyword2", ...]
"""

        try:
            result = await self.analyze_image(image_file, prompt)
            analysis = result["analysis"]

            import json
            try:
                keywords = json.loads(analysis)
                return {
                    "success": True,
                    "keywords": keywords
                }
            except:
                # 파싱 실패 시 기본 키워드 반환
                return {
                    "success": False,
                    "keywords": ["product", "quality", "trendy", "modern", "stylish"]
                }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get SEO keywords: {str(e)}"
            )


# 싱글톤 인스턴스
_openai_vision_service: Optional[OpenAIVisionService] = None


def get_openai_vision_service() -> OpenAIVisionService:
    """OpenAIVisionService 싱글톤 인스턴스 반환"""
    global _openai_vision_service
    if _openai_vision_service is None:
        _openai_vision_service = OpenAIVisionService()
    return _openai_vision_service
