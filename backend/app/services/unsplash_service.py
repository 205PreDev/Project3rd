"""
Unsplash 배경 이미지 서비스
"""
import httpx
from typing import Optional, List
from fastapi import HTTPException
from app.core.config import settings


class UnsplashService:
    """Unsplash API를 통한 배경 이미지 검색 서비스"""

    def __init__(self):
        if not settings.UNSPLASH_ACCESS_KEY:
            raise ValueError("UNSPLASH_ACCESS_KEY is not set")

        self.access_key = settings.UNSPLASH_ACCESS_KEY
        self.base_url = "https://api.unsplash.com"
        self.timeout = 10.0

    async def search_photos(
        self,
        query: str,
        per_page: int = 20,
        page: int = 1,
        orientation: Optional[str] = None
    ) -> dict:
        """
        키워드로 사진 검색

        Args:
            query: 검색 키워드
            per_page: 페이지당 결과 수 (1-30)
            page: 페이지 번호
            orientation: 이미지 방향 ("landscape", "portrait", "squarish")

        Returns:
            {
                "total": int,
                "total_pages": int,
                "results": [
                    {
                        "id": str,
                        "urls": {"raw", "full", "regular", "small", "thumb"},
                        "user": {"name", "username"},
                        "description": str,
                        "alt_description": str
                    }
                ]
            }
        """
        try:
            params = {
                "query": query,
                "per_page": min(per_page, 30),
                "page": page,
                "client_id": self.access_key
            }

            if orientation:
                params["orientation"] = orientation

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/search/photos",
                    params=params
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Unsplash API error: {response.text}"
                    )

                return response.json()

        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail="Unsplash API request timed out"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to search photos: {str(e)}"
            )

    async def get_random_photos(
        self,
        count: int = 10,
        query: Optional[str] = None,
        orientation: Optional[str] = None
    ) -> List[dict]:
        """
        랜덤 사진 가져오기

        Args:
            count: 가져올 사진 수 (1-30)
            query: 검색 키워드 (선택)
            orientation: 이미지 방향 (선택)

        Returns:
            사진 객체 리스트
        """
        try:
            params = {
                "count": min(count, 30),
                "client_id": self.access_key
            }

            if query:
                params["query"] = query
            if orientation:
                params["orientation"] = orientation

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/photos/random",
                    params=params
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Unsplash API error: {response.text}"
                    )

                data = response.json()
                # 단일 사진일 경우 리스트로 변환
                if isinstance(data, dict):
                    return [data]
                return data

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get random photos: {str(e)}"
            )

    async def get_photo_by_id(self, photo_id: str) -> dict:
        """
        사진 ID로 상세 정보 조회

        Args:
            photo_id: Unsplash 사진 ID

        Returns:
            사진 객체
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/photos/{photo_id}",
                    params={"client_id": self.access_key}
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Unsplash API error: {response.text}"
                    )

                return response.json()

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get photo: {str(e)}"
            )

    async def download_photo(self, photo_id: str, download_location: str) -> bool:
        """
        사진 다운로드 트리거 (Unsplash API 규정)

        Args:
            photo_id: Unsplash 사진 ID
            download_location: 다운로드 엔드포인트 URL

        Returns:
            성공 여부
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    download_location,
                    params={"client_id": self.access_key}
                )

                return response.status_code == 200

        except Exception as e:
            print(f"Failed to trigger download: {str(e)}")
            return False

    async def get_collections(
        self,
        page: int = 1,
        per_page: int = 10
    ) -> List[dict]:
        """
        추천 컬렉션 가져오기

        Args:
            page: 페이지 번호
            per_page: 페이지당 결과 수

        Returns:
            컬렉션 리스트
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/collections",
                    params={
                        "page": page,
                        "per_page": min(per_page, 30),
                        "client_id": self.access_key
                    }
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Unsplash API error: {response.text}"
                    )

                return response.json()

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get collections: {str(e)}"
            )

    async def get_category_backgrounds(self, category: str) -> List[dict]:
        """
        카테고리별 배경 추천

        Args:
            category: 상품 카테고리 (예: "fashion", "food", "tech")

        Returns:
            추천 배경 이미지 리스트
        """
        # 카테고리별 검색 키워드 매핑
        category_keywords = {
            "fashion": "minimalist background texture",
            "food": "wooden table background restaurant",
            "tech": "modern gradient abstract background",
            "beauty": "marble background elegant",
            "sports": "stadium court field background",
            "home": "interior living room background",
            "nature": "landscape mountains ocean background",
            "business": "office desk workspace background",
        }

        query = category_keywords.get(category.lower(), "abstract background")

        result = await self.search_photos(
            query=query,
            per_page=20,
            orientation="landscape"
        )

        return result.get("results", [])


# 싱글톤 인스턴스
_unsplash_service: Optional[UnsplashService] = None


def get_unsplash_service() -> UnsplashService:
    """UnsplashService 싱글톤 인스턴스 반환"""
    global _unsplash_service
    if _unsplash_service is None:
        _unsplash_service = UnsplashService()
    return _unsplash_service
