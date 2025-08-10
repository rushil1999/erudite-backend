from typing import Union
from fastapi import APIRouter,HTTPException
from app.service.info import get_stock_info, get_stock_news


router = APIRouter()

@router.get("/stocks/info/")
async def get_stock_info_controller(stocks):
  print("HERERR", stocks)
  data = await get_stock_info(stocks)
  return {"result": data}

@router.get("/stocks/news/")
async def get_stock_news_controller(stocks):
  data = await get_stock_news(stocks)
  return {"result": data}