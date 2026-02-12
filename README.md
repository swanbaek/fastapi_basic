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
memo/                  # Memo 앱 모듈 (app.py,model.py,db_oracle.py, oracle_test.py)
```


## 주요 기능
- Todo RESTful API (CRUD, Query String 검색)
- 한줄 메모장 (작성자/내용 입력, 스타일 적용, Oracle DB 연동, AJAX 페이징)
- Pydantic을 활용한 데이터 검증 및 문서화
- pytest 기반 단위 테스트
- .gitignore로 불필요/민감 파일 관리

## Memo(메모장) 기능 요약

- **비동기 FastAPI + 오라클 DB 연동**
- **AJAX로 등록/삭제/목록/페이징 처리**
- **ThreadPoolExecutor로 동기 DB를 비동기로 래핑**
- **Oracle ROW_NUMBER()로 페이징**
- **스타일 통일(css), 새로고침 없는 UX**

### 처리 흐름
1. 메모 등록: JS에서 AJAX로 /memo POST → FastAPI에서 DB insert → 성공시 목록 ajax 갱신
2. 메모 목록: JS에서 /memo/list?page=1 등으로 AJAX → FastAPI에서 page/size로 DB 조회 → fragment 반환, JS가 테이블에 삽입, 페이지 버튼 클릭시 ajax 재요청
3. 메모 삭제: 삭제 버튼 클릭시 /memo/{id} DELETE ajax → FastAPI에서 DB 삭제 → 목록 ajax 갱신

### 핵심 로직
- db_oracle.py: select_memos_paged_sync(page, size), count_memos_sync(), ThreadPoolExecutor 래핑
- app.py: /memo, /memo/list, /memo(POST), /memo/{id}(DELETE) 등 라우트
- static/js/memo.js: 폼 submit, 삭제, 페이지 버튼 클릭 모두 ajax, loadMemoList(page) 함수로 일원화
- templates/memo/index.html, memo_list.html: 폼+목록+페이징 fragment

자세한 구조와 흐름은 memo.md 참고

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
   - http://127.0.0.1:8000/todos (Todo 예제 : 동기방식)
   - http://127.0.0.1:8000/memo (메모장 예제 : 비동기방식/oracle DB연동)

## 테스트
```bash
python -m pytest todo/test_app.py -v
```

## 참고
- FastAPI 공식문서: https://fastapi.tiangolo.com/ko/
- 실습 예제: https://github.com/hanbit/web-with-fastapi
