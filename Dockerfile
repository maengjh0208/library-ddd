FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# RUN : 이미지 빌드시 컨테이너 안에서 명령어 실행
# --no-cache-dir : pip은 기본적으로 한번 다운받은 패키지를 캐시 폴더에 저장함. 나중에 다시 설치할때 빠르게 쓰려고 그런건데, Docker 이미지 안에서는 이 캐시가 쓸모 없음. 그래서 캐시 저장을 하지 않게끔 하는 옵션임.
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD : 컨테이너가 실행될때 수행되는 명령어 (RUN은 패키지 설치 등 환경구성을 할때 사용하고, CMD는 앱 시작할때 사용)
# uvicorn : ASGI 서버 (FastAPI 실행기)
# main : main.py 파일
# app : main.py 파일 안의 FastAPI() 인스턴스 변수명
# --host 0.0.0.0 : 기본값은 127.0.0.1 (localhost)인데, 이러면 컨테이너 내부에서만 접근이 가능하다. 0.0.0.0 으로 설정해야 외부(로컬 브라우저)에서도 접근할 수 있다.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]