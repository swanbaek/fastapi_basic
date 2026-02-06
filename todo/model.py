from pydantic import BaseModel
# pydantic을 이용하면 데이터 검증과 설정 관리를 쉽게 할 수 있다

# class Item(BaseModel):
#     item: str
#     status: str
class TodoItem(BaseModel):
    item: str

    model_config = {
        "json_schema_extra" : {
            "example": {
                "item": "Buy groceries",
            }
        }
    }

# pydantic 모델은 중첩해서 정의 가능    
class Todo(BaseModel):
    id: int
    item: TodoItem

    #문서(Swagger UI)에서 보여줄 예시 데이터를 지정하는 옵션
    # FastAPI에서 Todo 모델을 쓸 때 스웨거(/docs)에서 요청/응답 예시(example)가 자동으로 보임.
    # 그걸 직접 지정할 수 있는 게 schema_extra
    model_config = {
        "json_schema_extra" : {
            "example": {
                "id": 1,
                "item": {
                    "item": "Nested models",
                    "status": "completed"
                }
            }
        }
    }
# '''
# {
# "id": 1,
# "item": {
#     "item": "Nested models",
#     "status": "completed"
#     }
# }
# '''