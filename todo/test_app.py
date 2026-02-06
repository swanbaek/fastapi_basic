import pytest
from fastapi.testclient import TestClient
from todo.app import todo_router
from fastapi import FastAPI
# pip install pytest httpx
app = FastAPI()
app.include_router(todo_router)
client = TestClient(app)

def test_get_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    assert "todos" in response.json()

def test_create_todo():
    data = {"id": 3, "item": {"item": "새로운 할 일"}}
    response = client.post("/todos", json=data)
    assert response.status_code == 200
    assert response.json()["message"] == "할 일이 추가되었습니다."

def test_get_todo_by_id():
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert "todo" in response.json() or "message" in response.json()

def test_update_todo():
    data = {"item": "수정된 할 일"}
    response = client.put("/todos/1", json=data)
    assert response.status_code == 200
    assert "message" in response.json()

def test_delete_todo():
    response = client.delete("/todos/1")
    assert response.status_code == 200
    assert "message" in response.json()

def test_delete_all_todos():
    response = client.delete("/todos")
    assert response.status_code == 200
    assert response.json()["message"] == "모든 할 일이 삭제되었습니다."

def test_query_string():
    # 예시: /todos/query?keyword=할 일
    response = client.get("/todos/query", params={"keyword": "할 일"})
    assert response.status_code in (200, 404)
    # 실제 구현에 따라 응답 구조가 다를 수 있음

# python -m pytest todo/test_app.py -v
# => 현재 활성화된 venv 환경의 pytest가 실행됨
# pytest -v todo/test_app.py ==>이걸로 하면 에러남 시스템 PATH에 있는 pytest 또는 venv가 아닌 다른 Python 환경을 실행