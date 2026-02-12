from pydantic import BaseModel
from typing import Optional

class Memo(BaseModel): 
    id: Optional[int]= None #Optional 필드에 기본값을 명시적으로 줘야 함
    author: str
    content: str