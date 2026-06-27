from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from repository.BoardRepository import BoardRepository
from dto.boardDTO import BoardCreate, BoardUpdate

class BoardService:

    def __init__(self, db: AsyncSession):
        self.repository = BoardRepository(db)

    # 게시글 등록
    async def createBoard(self, board: BoardCreate) -> dict:
        # Repository를 통해 DB에 INSERT 치고 자동 증가된 id 값을 받아옴
        new_id = await self.repository.create_board(board);

        # 반환된 id가 없거나 0 이하면 등록 실패
        if not new_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="게시글 등록에 실패했습니다."
            )
        return True;