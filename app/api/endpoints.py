from typing import Union
from fastapi import APIRouter,HTTPException


router = APIRouter()

@router.get("/stock/news/{input}")
async def get_stock_news(input: str):
  # data = await generate_vector_embeddings(input)
  return {"result": input}