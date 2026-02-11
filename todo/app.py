from fastapi import APIRouter, HTTPException, Path, Query, Request, Depends
from todo.model import Todo, TodoItem, TodoItems
from fastapi.templating import Jinja2Templates

todo_router = APIRouter()

from todo.model import Todo

# todo_list를 Todo 객체로 통일
todo_list = [
    Todo(id=1, item="할 일 1"),
    Todo(id=2, item="할 일 2")
]

templates = Jinja2Templates(directory="templates/")

#2.응답 모델 지정 (TodoItems 모델)
@todo_router.get("/todos", response_model=TodoItems)
async def get_todos(request: Request)->dict:    
    return templates.TemplateResponse("todo/todo.html", {"request": request, "todos": todo_list})

@todo_router.post("/todos", status_code=201)
async def create_todo(request: Request, todo: Todo = Depends(Todo.as_form)):
    todo.id = len(todo_list) + 1
    todo_list.append(todo)
    print('todo_list:', todo_list)
    # 전체 목록을 todos로 넘겨서 렌더링
    return templates.TemplateResponse("todo/todo.html", {"request": request, "todos": todo_list})

#  더 구체적인 경로를 먼저 등록해야 함
# Query string으로 검색하는 예제
#  /todos/query?keyword=검색어 형식
# @todo_router.get("/todos/query")
# async def query_todos(keyword: str = Query(..., description="검색할 키워드")) -> dict:
#     # ... ellipsis는 필수 파라미터라는 의미
#     # 선택적 파라미터 (기본값 제공)-> keyword: str = Query(None, description="검색할 키워드")
#     result = [todo for todo in todo_list if keyword in todo['item']]
#     if result:
#         return {"result": result}
#     return {"message": f'"{keyword}"(으)로 검색된 할 일이 없습니다.'}
# '''
# 이 경우 /todos/query를 요청하면:
# FastAPI가 /todos/{id} 패턴을 먼저 확인
# "query"를 id 파라미터로 인식하려고 시도
# id는 int 타입인데 "query"는 문자열이라 파싱 실패 → 422 에러
# 따라서 /todos/query 경로를 /todos/{id} 경로보다 먼저 정의해야 함
# '''
@todo_router.get("/todos/{id}")
async def get_todo(request: Request, id: int = Path(...,title="The ID of the todo to be retrieved")):
    for todo in todo_list:
        if todo.id==id:
            # todo_list에 추가된 객체가 딕셔너리(dict)가 아니라 Pydantic 모델(Todo)이기 때문에
            # todo['id']처럼 인덱싱이 아니라, todo.id처럼 속성 접근을 해야 함   
            return templates.TemplateResponse("todo/todo.html", {"request": request, "todo": todo, "todos": todo_list})    
    raise HTTPException(status_code=404, detail=f'{id}번 할 일을 찾을 수 없습니다.')

# 할 일 수정 폼 GET
@todo_router.get("/todos/{id}/edit")
async def edit_todo_form(request: Request, id: int):
    for todo in todo_list:
        if todo.id == id:
            return templates.TemplateResponse("todo/edit.html", {"request": request, "todo": todo})
    raise HTTPException(status_code=404, detail=f'{id}번 할 일을 찾을 수 없습니다.')

# 할 일 수정 POST
from fastapi import Form

@todo_router.post("/todos/{id}/edit")
async def edit_todo_submit(request: Request, id: int, item: str = Form(...)):
    for todo in todo_list:
        if todo.id == id:
            todo.item = item
            return templates.TemplateResponse("todo/todo.html", {"request": request, "todos": todo_list})
    raise HTTPException(status_code=404, detail=f'{id}번 할 일을 찾을 수 없습니다.')

# POST 방식 삭제 엔드포인트 (HTML form용)
@todo_router.post("/todos/{id}/delete")
async def delete_todo_post(request: Request, id: int):
    for todo in todo_list:
        if todo.id == id:
            todo_list.remove(todo)
            return templates.TemplateResponse("todo/todo.html", {"request": request, "todos": todo_list})
    raise HTTPException(status_code=404, detail=f'{id}번 할 일을 찾을 수 없습니다.')

@todo_router.put("/todos/{id}")
async def update_todo(todo_data: TodoItem, id: int=Path(..., title="The ID of to todo to be updated"))->dict:
    # id: int = Path(...) → /todos/3 같은 경로 값을 Path Parameter로 받음
    # → Swagger UI에 "The ID of the todo to be updated" 설명이 뜸
    for todo in todo_list:
        if todo.id==id:
            todo.item=todo_data.item
            return {'message':f'{id}번 할 일이 수정되었습니다.'}
    # return {'message':f'{id}번 할 일을 찾을 수 없습니다.'}
    raise HTTPException(status_code=404, detail=f'{id}번 할 일을 찾을 수 없습니다.')

@todo_router.delete("/todos/{id}")
async def delete_todo(id: int)->dict:
    for todo in todo_list:
        if todo.id==id:
            todo_list.remove(todo)
            return {'message':f'{id}번 할 일이 삭제되었습니다.'}
    # return {'message':f'{id}번 할 일을 찾을 수 없습니다.'}
    raise HTTPException(status_code=404, detail=f'{id}번 할 일을 찾을 수 없습니다.')

@todo_router.delete("/todos")
async def delete_all_todos()->dict:
    todo_list.clear()
    return {'message':'모든 할 일이 삭제되었습니다.'}   

