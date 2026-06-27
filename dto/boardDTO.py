from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class BoardCreate(BaseModel):
    title: Optional[str] = None
    writer: Optional[str] = None
    content: Optional[str] = None
    fileName: Optional[str] = None
    filePath: Optional[str] = None

class BoardUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    fileName: Optional[str] = None
    filePath: Optional[str] = None

class BoardResponse(BaseModel):
    idx: int
    title: Optional[str]
    writer: Optional[str]
    content: Optional[str]
    fileName: Optional[str]
    filePath: Optional[str]
    created_at: Optional[str]

    class Config:
        # DB 결과(RowMapping)를 Pydantic 객체로 쉽게 변환할 수 있도록 설정
        from_attributes = True


