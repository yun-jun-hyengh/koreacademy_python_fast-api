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