from typing import Union
from fastapi import APIRouter,HTTPException
from app.service.info import get_stock_info, get_stock_news
from app.service.list import get_stock_list 


router = APIRouter()

@router.get("/stocks/info/")
async def get_stock_info_controller(stocks):
  response = await get_stock_info(stocks)
  if not response.is_success:
    if response.status_code == None:
      response.status_code = 500
    raise HTTPException(status_code=response.status_code, detail=response.message)
  return {"result": response.data}

@router.get("/stocks/news/")
async def get_stock_news_controller(stocks):
  response = await get_stock_news(stocks)
  if not response.is_success:
    if response.status_code == None:
      response.status_code = 500
    raise HTTPException(status_code=response.status_code, detail=response.message)
  return {"result": response.data}

@router.get("/list/{name}")
async def get_stock_list_controller(name):
  response = await get_stock_list(name)
  if not response.is_success:
    if response.status_code == None:
      response.status_code = 500
    raise HTTPException(status_code=response.status_code, detail=response.message)
  return {"result": response.data}