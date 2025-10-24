# Rembg 배경 제거 서비스 Docker 이미지
FROM python:3.11-slim

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치
RUN pip install --no-cache-dir \
    rembg[gpu]==2.0.56 \
    fastapi==0.109.0 \
    uvicorn[standard]==0.27.0 \
    python-multipart==0.0.6

# API 서버 코드
COPY main.py .

# 포트 노출
EXPOSE 5000

# 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
