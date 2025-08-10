
from pydantic import BaseModel
from typing import Any, Optional

class Stock_Info_Model(BaseModel):
    name: str
    ticker: str
    info: str
    