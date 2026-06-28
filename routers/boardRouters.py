from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession
from starlette.status import HTTP_200_OK

from config.database import get_db
from dto.boardDTO import BoardCreate, BoardUpdate
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

@router.get("/{idx}", status_code=HTTP_200_OK)
async def boardDetail(idx: int, db: AsyncSession = Depends(get_db)):
    boardService = BoardService(db);
    result = await boardService.getBoardDetail(idx);
    return {"data": result};

@router.put("/{idx}", status_code=status.HTTP_200_OK)
async def boardUpdate(idx: int, payload: BoardUpdate, db: AsyncSession = Depends(get_db)):
    boardService = BoardService(db);
    await boardService.updateBoard(idx, payload);
    return {"success": True, "message": "게시글이 수정되었습니다."};

@router.delete("/{idx}", status_code=status.HTTP_200_OK)
async def deleteBoard(idx: int, db: AsyncSession = Depends(get_db)):
    boardService = BoardService(db);
    await boardService.deleteBoard(idx);
    return {"success": True, "message": "게시글이 삭제되었습니다."};