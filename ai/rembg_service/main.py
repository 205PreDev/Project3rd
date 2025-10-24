"""
Rembg 배경 제거 API 서버
"""
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import Response
from rembg import remove
from PIL import Image
from io import BytesIO

app = FastAPI(title="Rembg Background Removal API")


@app.get("/")
async def health_check():
    """헬스 체크"""
    return {"status": "ok", "service": "rembg"}


@app.post("/remove")
async def remove_background(
    file: UploadFile = File(...),
    alpha_matting: str = Form(default="false"),
    alpha_matting_foreground_threshold: int = Form(default=240),
    alpha_matting_background_threshold: int = Form(default=10)
):
    """
    이미지 배경 제거 API

    Args:
        file: 업로드된 이미지 파일
        alpha_matting: Alpha matting 활성화 ("true" or "false")
        alpha_matting_foreground_threshold: 전경 임계값 (0-255)
        alpha_matting_background_threshold: 배경 임계값 (0-255)

    Returns:
        배경이 제거된 PNG 이미지
    """
    try:
        # 이미지 읽기
        image_bytes = await file.read()
        input_image = Image.open(BytesIO(image_bytes))

        # Alpha matting 파라미터 변환
        use_alpha_matting = alpha_matting.lower() == "true"

        # 배경 제거
        output_image = remove(
            input_image,
            alpha_matting=use_alpha_matting,
            alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
            alpha_matting_background_threshold=alpha_matting_background_threshold
        )

        # PNG로 변환
        output_buffer = BytesIO()
        output_image.save(output_buffer, format="PNG")
        output_bytes = output_buffer.getvalue()

        return Response(
            content=output_bytes,
            media_type="image/png",
            headers={
                "Content-Disposition": f"attachment; filename=removed_{file.filename}"
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process image: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
