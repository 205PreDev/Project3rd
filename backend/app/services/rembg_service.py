"""
Rembg 배경 제거 서비스
"""
import httpx
from io import BytesIO
from typing import Optional
from fastapi import HTTPException, UploadFile
from PIL import Image

from app.core.config import settings


class RembgService:
    """Rembg API를 통한 배경 제거 서비스"""

    def __init__(self):
        self.api_url = settings.REMBG_API_URL
        self.timeout = 60.0  # 60초 타임아웃

    async def remove_background(
        self,
        image_file: UploadFile
    ) -> bytes:
        """
        이미지 배경 제거

        Args:
            image_file: 업로드된 이미지 파일

        Returns:
            배경이 제거된 PNG 이미지 (bytes)

        Raises:
            HTTPException: API 호출 실패 시
        """
        try:
            # 이미지 파일 읽기
            image_bytes = await image_file.read()

            # Rembg API 호출
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.api_url}/remove",
                    files={"file": (image_file.filename, image_bytes, image_file.content_type)}
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Rembg API error: {response.text}"
                    )

                # PNG 형식으로 반환
                return response.content

        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail="Background removal timed out"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to remove background: {str(e)}"
            )

    async def remove_background_from_bytes(
        self,
        image_bytes: bytes,
        filename: str = "image.png"
    ) -> bytes:
        """
        이미지 bytes에서 배경 제거

        Args:
            image_bytes: 이미지 데이터
            filename: 파일명 (기본: image.png)

        Returns:
            배경이 제거된 PNG 이미지 (bytes)
        """
        try:
            # Rembg API 호출
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.api_url}/remove",
                    files={"file": (filename, image_bytes, "image/png")}
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Rembg API error: {response.text}"
                    )

                return response.content

        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail="Background removal timed out"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to remove background: {str(e)}"
            )

    async def remove_background_with_alpha(
        self,
        image_file: UploadFile,
        alpha_matting: bool = True,
        alpha_matting_foreground_threshold: int = 240,
        alpha_matting_background_threshold: int = 10
    ) -> bytes:
        """
        고급 배경 제거 (Alpha Matting)

        Args:
            image_file: 업로드된 이미지 파일
            alpha_matting: Alpha matting 활성화 여부
            alpha_matting_foreground_threshold: 전경 임계값
            alpha_matting_background_threshold: 배경 임계값

        Returns:
            배경이 제거된 PNG 이미지 (bytes)
        """
        try:
            image_bytes = await image_file.read()

            # Rembg API 호출 (파라미터 포함)
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.api_url}/remove",
                    files={"file": (image_file.filename, image_bytes, image_file.content_type)},
                    data={
                        "alpha_matting": str(alpha_matting).lower(),
                        "alpha_matting_foreground_threshold": alpha_matting_foreground_threshold,
                        "alpha_matting_background_threshold": alpha_matting_background_threshold
                    }
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Rembg API error: {response.text}"
                    )

                return response.content

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to remove background with alpha: {str(e)}"
            )

    def validate_image(self, image_bytes: bytes) -> bool:
        """
        이미지 유효성 검증

        Args:
            image_bytes: 이미지 데이터

        Returns:
            유효한 이미지 여부
        """
        try:
            image = Image.open(BytesIO(image_bytes))
            # 최대 크기 검증 (10MB)
            if len(image_bytes) > settings.MAX_UPLOAD_SIZE:
                return False
            # 이미지 형식 검증
            if image.format not in ["PNG", "JPEG", "JPG"]:
                return False
            return True
        except Exception:
            return False


# 싱글톤 인스턴스
_rembg_service: Optional[RembgService] = None


def get_rembg_service() -> RembgService:
    """RembgService 싱글톤 인스턴스 반환"""
    global _rembg_service
    if _rembg_service is None:
        _rembg_service = RembgService()
    return _rembg_service
