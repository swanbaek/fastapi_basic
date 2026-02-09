from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
# vscode 확장 설치: Better Jinja, jinja2 enhanced

app = FastAPI()
# main.py의 app = FastAPI()는 전체 프로젝트의 메인 앱
# jinja_ex/example_app.py의 app = FastAPI()는 jinja_ex 하위 경로만 담당하는 서브 앱
# 으로 동작합니다.
templates = Jinja2Templates(directory="templates/example")

# 사용자 정의 필터: 천단위 콤마 (filter예제서 사용)
def comma_filter(value):
    try:
        return f"{value:,}"
    except Exception:
        return value
templates.env.filters["comma"] = comma_filter

app.mount("/static", StaticFiles(directory="static"), name="static")

# 목차 페이지
@app.get("/", response_class=HTMLResponse)
def jinja2_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 각 예제 라우트
@app.get("/basic", response_class=HTMLResponse)
def jinja2_basic(request: Request):
    obj={"name": "FastAPI 학생 홍길동", "score": 85}
    return templates.TemplateResponse("ex01_basic.html", {"request": request, **obj})
    

@app.get("/condition", response_class=HTMLResponse)
def jinja2_condition(request: Request):
    return templates.TemplateResponse("ex02_condition.html",  {"request": request, "name":"김철수", "score": 60})

@app.get("/loop", response_class=HTMLResponse)
def jinja2_loop(request: Request):
    items = ["사과", "바나나", "딸기"]
    return templates.TemplateResponse("ex03_loop.html", {"request": request,"title":"홍길동 님의 장바구니", "items": items})

@app.get("/filter", response_class=HTMLResponse)
def jinja2_filter(request: Request):
    text = "FastAPI와 Jinja2"
    return templates.TemplateResponse("ex04_filter.html", {"request": request, "text": text, "items": ["a", "b", "c"],"num1": 1234.5678, "num2": 9876543})

@app.get("/inherit", response_class=HTMLResponse)
def jinja2_inherit(request: Request):
    return templates.TemplateResponse("child.html", {"request": request, "title": "템플릿 상속 예제"})


# 🔹 홈 페이지
@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    obj = {"message": "Welcome to FastAPI World!!"}
    return templates.TemplateResponse("home.html", {"request": request, **obj})

# 🔹 소개 페이지
@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    info = {"title": "소개 페이지", "content": "FastAPI와 Jinja2 템플릿 상속 예제"}
    return templates.TemplateResponse("about.html", {"request": request, **info})

@app.get("/macro", response_class=HTMLResponse)
def jinja2_macro(request: Request):
    return templates.TemplateResponse("macro.html", {"request": request, "fruits": ["사과", "바나나", "딸기"]})

if __name__ == "__main__":
    uvicorn.run("jinja2.example_app:app", host="127.0.0.1", port=8000, reload=True)
