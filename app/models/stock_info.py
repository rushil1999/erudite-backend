
from pydantic import BaseModel
from typing import Any, Optional

class Stock_Info_Model(BaseModel):
    name: Optional[str]= None
    ticker: str
    info: Optional[Any] = None
    timestamp: Optional[str] = None
    
