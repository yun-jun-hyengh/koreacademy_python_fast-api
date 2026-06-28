from typing import Optional, List
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing import db
from dto.boardDTO import BoardCreate, BoardUpdate

class BoardRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    # 등록
    async def create_board(self, board: BoardCreate) -> int:
        query = text(
            '''
            insert into board(title, writer, content, fileName, filePath, created_at)
            values(:title, :writer, :content, :fileName, :filePath, CURRENT_DATE())
            '''
        )
        insert_data = {
            "title": board.title,
            "writer": board.writer,
            "content": board.content,
            "fileName": board.fileName,
            "filePath": board.filePath
        }
        result = await self.db.execute(query, insert_data)
        await self.db.commit()
        return result.lastrowid

    # 게시글 조회
    async def boardList(self) -> list:
        query = text(
            '''
                SELECT idx, title, writer, content, created_at
                FROM board order by idx desc
            '''
        );
        result = await self.db.execute(query);
        rows = result.mappings().all();
        return list(rows);

    # 게시글 상세조회
    async def detailBoard(self, idx: int) -> dict:
        query = text(
            '''
                SELECT idx, title, writer, content, created_at
                FROM board WHERE idx = :idx
            '''
        )
        result = await self.db.execute(query, {"idx": idx});
        row = result.mappings().first();
        if row:
            return dict(row);
        else:
            return None;

    # 게시글 삭제
    async def deleteBoard(self, idx: int) -> int:
        query = text(
            '''
                delete from board where idx = :idx
            '''
        );
        result = await self.db.execute(query, {"idx": idx});
        await self.db.commit();
        return result.rowcount

    # 게시글 수정
    async def updateBoard(self, idx: int, board: BoardUpdate):
        query = text(
            '''
                update board 
                set title = :title, content = :content,
                fileName = :fileName, filePath = :filePath where idx = :idx
            '''
        )
        data = {
            "idx": idx,
            "title": board.title,
            "content": board.content,
            "fileName": board.fileName,
            "filePath": board.filePath
        };

        result = await self.db.execute(query, data);
        await self.db.commit();
        return result.rowcount;