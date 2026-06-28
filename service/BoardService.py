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

    # 게시글 조회
    async def getBoardList(self) -> list:
        board_list = await self.repository.boardList();
        return board_list;

    # 게시글 상세 조회
    async def getBoardDetail(self, idx: int) -> dict:
        board = await self.repository.detailBoard(idx);

        if not board:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="해당 게시글을 찾을 수 없습니다"
            )
        return board;

    # 게시글 삭제
    async def deleteBoard(self, idx: int) -> bool:
        row = await self.repository.deleteBoard(idx);
        if row == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"게시글 삭제에 실패하였습니다."}
            )
        else:
            return True;

    # 게시글 수정
    async def updateBoard(self, idx: int, board: BoardUpdate) -> bool:
        row = await self.repository.updateBoard(idx, board);
        if row == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"게시글 수정에 실패하였습니다."}
            )
        else:
            return True