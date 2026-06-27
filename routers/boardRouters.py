from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession
from config.database import get_db
from dto.boardDTO import BoardCreate
from service.BoardService import BoardService

router = APIRouter(tags=["board"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_board(payload: BoardCreate, db: AsyncConnection = Depends(get_db)):
    board_service = BoardService(db)
    await board_service.createBoard(payload)
    return {"success": True, "message": "게시글이 정상적으로 등록되었습니다."}

@router.get("/list", status_code=status.HTTP_200_OK)
async def boardList(db: AsyncSession = Depends(get_db)):
    boardService = BoardService(db);
    result = await boardService.getBoardList();
    return {"data": result};