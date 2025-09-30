from typing import Any, Optional

from pydantic import BaseModel


class Response(BaseModel):
    status: bool = False
    message: str = None
    data: Optional[Any] = None
