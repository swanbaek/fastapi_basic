from fastapi import APIRouter, Request, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from memo.model import Memo
from memo import db_oracle

router = APIRouter()
templates = Jinja2Templates(directory="templates")




# GET: 메모장 폼 페이지
@router.get("/memo", response_class=HTMLResponse)
async def read_memo(request: Request):
	memos = await db_oracle.select_memos()
	return templates.TemplateResponse("memo/index.html", {"request": request, "memos": memos})

# GET: 메모 목록 ajax (HTML fragment)
@router.get("/memo/list", response_class=HTMLResponse)
async def memo_list(request: Request):
	memos = await db_oracle.select_memos()
	return templates.TemplateResponse("memo/memo_list.html", {"request": request, "memos": memos})

# POST: JSON 또는 폼 모두 지원
@router.post("/memo")
async def post_memo(memo: Memo = Body(...)):
	await db_oracle.insert_memo(memo.author, memo.content)
	return {"message": "메모가 성공적으로 저장되었습니다.", "memo": memo}

# DELETE: 메모 삭제 (AJAX)
@router.delete("/memo/{id}")
async def delete_memo(id: int):
	await db_oracle.delete_memo(id)
	return {"message": "메모가 삭제되었습니다.", "id": id}

# PUT: 메모 수정 (AJAX)
@router.put("/memo/{id}")
async def update_memo(id: int, memo: Memo = Body(...)):
	await db_oracle.update_memo(id, memo.content)
	return {"message": "메모가 수정되었습니다.", "id": id, "content": memo.content}
	
