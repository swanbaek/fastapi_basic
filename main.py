from fastapi import FastAPI, Request,Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from todo.app import todo_router


# venv 안에서 FastAPI 설치
# pip install fastapi uvicorn[standard] python-dotenv jinja2 python-multipart

app= FastAPI()

# static 폴더 제공
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root()->dict:
    return {"안녕?": "FASTAPI 세계!"}
# 실행 명령어
# uvicorn main:app --reload
# http://127.0.0.1:8000


templates = Jinja2Templates(directory="templates")

# templates 폴더의 "index.html" 응답
@app.get("/memo", response_class=HTMLResponse)
def read_memo(request: Request):
    return templates.TemplateResponse("memo/index.html", {"request": request, "메모장": "여기는 메모장 페이지입니다."})
# http://127.0.0.1:8000/memo

@app.post("/memo", response_class=HTMLResponse)
async def post_memo(request: Request, content: str = Form(...)):
    return templates.TemplateResponse("memo/result.html", {"request": request, "content": content})

app.include_router(todo_router)