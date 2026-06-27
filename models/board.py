from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Board:
    idx: Optional[int] = None
    title: Optional[str] = None
    writer: Optional[str] = None
    content: Optional[str] = None
    fileName: Optional[str] = None
    filePath: Optional[str] = None
    created_at: Optional[datetime] = None