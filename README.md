# FastAPI Todo & Memo Web Project

## 소개
이 프로젝트는 FastAPI를 활용한 Todo 앱과 한줄 메모장 예제입니다. Python 백엔드, Jinja2 템플릿, 정적 파일 관리, RESTful API, 단위 테스트 등 실무에 필요한 다양한 FastAPI 기능을 포함합니다.

## 폴더 구조
```
main.py                # FastAPI 앱 진입점
requirements.txt       # 의존성 관리
static/                # 정적 파일(css 등)
templates/             # Jinja2 템플릿(html)
todo/                  # Todo 앱 모듈 (app.py, model.py, test_app.py)
```

## 주요 기능
- Todo RESTful API (CRUD, Query String 검색)
- 한줄 메모장 (작성자/내용 입력, 스타일 적용)
- Pydantic을 활용한 데이터 검증 및 문서화
- pytest 기반 단위 테스트
- .gitignore로 불필요/민감 파일 관리

## 실행 방법
1. 가상환경 생성 및 패키지 설치
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```
2. 서버 실행
   ```bash
   uvicorn main:app --reload
   ```
3. 브라우저에서 접속
   - http://127.0.0.1:8000/docs (Swagger UI)
   - http://127.0.0.1:8000/memo (메모장 예제)

## 테스트
```bash
python -m pytest todo/test_app.py -v
```

## 참고
- FastAPI 공식문서: https://fastapi.tiangolo.com/ko/
- 실습 예제: https://github.com/hanbit/web-with-fastapi
