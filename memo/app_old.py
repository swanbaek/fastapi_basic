from fastapi import APIRouter, Request, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from memo.model import Memo

router = APIRouter()
templates = Jinja2Templates(directory="templates")



# GET: 메모장 폼 페이지
@router.get("/memo", response_class=HTMLResponse)
def read_memo(request: Request):
	return templates.TemplateResponse("memo/index.html", {"request": request, "메모장": "여기는 메모장 페이지입니다."})

# POST: JSON 또는 폼 모두 지원
@router.post("/memo")
async def post_memo(memo: Memo = Body(...)):
	print('memo:', memo)
	# AJAX/JSON 요청이면 JSON 반환
	return {"message": "메모가 성공적으로 저장되었습니다.", "memo": memo}
	
