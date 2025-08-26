from pydantic import BaseModel
from typing import Any, Optional, List

class Polygon_Insight_Model(BaseModel):
  ticker: str
  sentiment: str
  sentiment_reasoning: str

class Article_Model(BaseModel):
  title: str
  description: str
  sentiment_reasoning: str
  sentiment: str
  ticker: str
  article_url: str
  name: Optional[str]= None

class Polygon_Article_Model(BaseModel):
  id: str
  title: str
  article_url: str
  tickers: List[str]
  description: str
  insights: List[Polygon_Insight_Model]

class Polygon_Response(BaseModel):
  results: List[Polygon_Article_Model]

