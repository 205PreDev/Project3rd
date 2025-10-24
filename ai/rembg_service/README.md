# Rembg 배경 제거 서비스

AI 기반 이미지 배경 제거 마이크로서비스

## 로컬 실행

### Docker 사용
```bash
cd ai/rembg_service
docker build -t rembg-service .
docker run -p 5000:5000 rembg-service
```

### Python 직접 실행
```bash
cd ai/rembg_service
pip install rembg[gpu] fastapi uvicorn python-multipart
python main.py
```

## API 사용

### 헬스 체크
```bash
curl http://localhost:5000/
```

### 배경 제거
```bash
curl -X POST http://localhost:5000/remove \
  -F "file=@image.jpg" \
  -o output.png
```

### Alpha Matting (고급)
```bash
curl -X POST http://localhost:5000/remove \
  -F "file=@image.jpg" \
  -F "alpha_matting=true" \
  -F "alpha_matting_foreground_threshold=240" \
  -F "alpha_matting_background_threshold=10" \
  -o output.png
```

## 환경 변수

- `PORT`: 서버 포트 (기본: 5000)

## 배포

### Render.com
1. 새 Web Service 생성
2. Repository 연결
3. Docker 빌드 설정
4. 환경 변수 설정
5. 배포

### Railway
```bash
railway login
railway init
railway up
```

## 성능

- 평균 처리 시간: 2-5초 (이미지 크기에 따라 다름)
- 메모리 사용량: 1-2GB
- GPU 사용 시 더 빠른 처리 가능
