FROM python:3.10-slim

# 필수 패키지
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg \
    chromium chromium-driver

# 환경변수 설정
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER=/usr/bin/chromedriver

# 작업 디렉토리
WORKDIR /app
COPY . .

# 파이썬 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]