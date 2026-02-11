from fastapi import FastAPI, Request,Form   
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from todo.app import todo_router
from jinja_ex.example_app import app as jinja2_app
from memo.app import router as memo_router


# venv 안에서 FastAPI 설치
# pip install fastapi uvicorn[standard] python-dotenv jinja2 python-multipart

app= FastAPI()

templates= Jinja2Templates(directory="templates/")
# static 폴더 제공
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def get_root_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "메인 페이지"})

@app.get("/test")
def read_root()->dict:
    return {"안녕?": "FASTAPI 세계!"}
# 실행 명령어
# uvicorn main:app --reload
# http://127.0.0.1:8000





app.include_router(todo_router)
app.include_router(memo_router)

app.mount("/jinja_ex", jinja2_app)