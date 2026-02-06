# 1. FastAPI 개발 환경 설정

## 1.1. FastAPI 프로젝트 구조 설계 및 폴더 구성 방법

- main.py: FastAPI 앱의 진입점
- requirements.txt: 의존성 관리 파일
- templates/: Jinja2 템플릿 폴더
- static/: 정적 파일(css, js 등) 폴더
- todo/: 기능별 모듈 폴더 (예: todo 앱)

프로젝트를 기능별로 폴더로 분리하면 유지보수와 확장성이 좋아집니다.

## 1.2. 가상환경(venv) 및 의존성 관리 (requirements.txt 작성)

- Python venv로 프로젝트별 독립 환경 구성
- 필요한 패키지 설치 후 pip freeze > requirements.txt로 의존성 기록
- 예시:
	```bash
	python -m venv .venv
	.venv\Scripts\activate  # Windows
	pip install fastapi uvicorn jinja2 pytest
	pip freeze > requirements.txt
	```
가상환경을 사용하면 패키지 충돌 없이 안정적으로 개발할 수 있습니다.

# 2. FastAPI 기본 사용법 및 서버 실행

## 2.1. FastAPI 기본 라우팅 및 서버 실행 방법

- main.py에서 FastAPI 인스턴스 생성 후 라우트(엔드포인트) 정의
- 예시:
	```python
	from fastapi import FastAPI
	app = FastAPI()

	@app.get("/")
	def read_root():
			return {"message": "Hello, FastAPI!"}
	```
- 서버 실행:
	```bash
	uvicorn main:app --reload
	```

## 2.2. 개발용 자동 리로드 설정 (uvicorn --reload)

- uvicorn 실행 시 --reload 옵션을 사용하면 코드 변경 시 서버가 자동으로 재시작되어 개발이 편리함
- 예시:
	```bash
	uvicorn main:app --reload
	```

# 3. Restful 방식의 todo 앱 구현 및 테스트

## 3.1. todo 폴더 구성 및 주요 코드

	- CRUD 엔드포인트: /todos (GET, POST, PUT, DELETE), /todos/{id}, /todos/query (query string 검색)
	- 예시: /todos/query?keyword=검색어

#### Pydantic 기능 설명

- Pydantic은 데이터 검증과 직렬화(Serialization)를 쉽게 해주는 Python 라이브러리. 
- FastAPI에서 입력 데이터의 타입과 유효성을 자동으로 검사해주며, 
- API 문서(Swagger UI)에서 예시 데이터와 스키마를 자동 생성해준다. 
  예를 들어, Todo와 TodoItem 모델을 정의하면 클라이언트가 보낸 데이터가 올바른지 자동으로 체크하고, 
  잘못된 데이터는 422 에러로 응답한다.

#### pytest 단위 테스트 설명

- pytest는 Python에서 널리 쓰이는 테스트 프레임워크로, 간단한 함수 작성만으로 API의 각 엔드포인트 동작을 자동으로 검증할 수 있다. 
- FastAPI의 TestClient와 함께 사용하면 실제 서버를 띄우지 않고도 HTTP 요청/응답 테스트가 가능. 
- 예를 들어, CRUD 및 쿼리 검색 기능이 정상 동작하는지 빠르게 확인할 수 있다.

### 3.2. 주요 엔드포인트

- GET /todos: 전체 할 일 목록 조회
- POST /todos: 할 일 추가
- GET /todos/{id}: 특정 할 일 조회
- PUT /todos/{id}: 할 일 수정
- DELETE /todos/{id}: 할 일 삭제
- DELETE /todos: 모든 할 일 삭제
- GET /todos/query?keyword=검색어: Query string으로 할 일 검색

### 3.3. 테스트 예제 (pytest)

```python
def test_query_string():
	response = client.get("/todos/query", params={"keyword": "할 일"})
	assert response.status_code in (200, 404)
```

기타 CRUD 테스트 코드도 포함되어 있음.

# 4. 응답 모델과 오류 처리

- FastAPI의 response_model 사용 가능
- Pydantic으로 데이터 형태 보장
- HTTPException을 활용한 에러 처리 구현 가능

### 4.1. FastAPI의 응답

- FastAPI는 다양한 방식으로 응답을 반환할 수 있습니다.
- dict, list, Pydantic 모델, HTMLResponse 등 다양한 타입 지원
- 예시:
	```python
	@app.get("/hello")
	def hello():
			return {"message": "안녕하세요!"}
	```

### 4.2. 응답 모델 작성

- response_model 파라미터를 사용하면 응답 데이터의 타입과 구조를 명확히 지정할 수 있습니다.
- Pydantic 모델을 활용해 API 응답의 데이터 검증 및 문서화 가능
- 예시:
	```python
	from pydantic import BaseModel
	class HelloResponse(BaseModel):
			message: str

	@app.get("/hello", response_model=HelloResponse)
	def hello():
			return {"message": "안녕하세요!"}
	```

### 4.3. 오류 처리 

- FastAPI에서는 HTTPException을 활용해 에러 응답을 쉽게 처리할 수 있습니다.
- HTTPException 클래스는 다음 세 개의 인수를 받는다.
    * **status_code** : 예외 처리 시 반환할 상태 코드
    *  **detail** : 클라이언트에게 전달한 메시지
    *  **headers** : 헤더를 요구하는 응답을 위한 선택적 인수
- 예시:
	```python
	from fastapi import HTTPException
	@app.get("/error")
	def error():
			raise HTTPException(status_code=404, detail="페이지를 찾을 수 없습니다.")
	```

## 참고 사이트
- https://github.com/hanbit/web-with-fastapi