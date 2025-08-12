from typing import Union
from fastapi import APIRouter,HTTPException
from app.service.process import process_news, process_info
from app.service.list import get_stocks_in_list 


router = APIRouter()

@router.get("/stocks/info/{list_name}")
async def get_stock_info_controller(list_name: str):
  response = await process_info(list_name)
  if not response.is_success:
    if response.status_code == None:
      response.status_code = 500
    raise HTTPException(status_code=response.status_code, detail=response.message)
  return {"result": response.data}

@router.get("/stocks/news/{list_name}")
async def process_stock_news_controller(list_name: str):
  response = await process_news(list_name)
  if not response.is_success:
    if response.status_code == None:
      response.status_code = 500
    raise HTTPException(status_code=response.status_code, detail=response.message)
  return {"result": response.data}

@router.get("/list/{name}")
async def get_stock_list_controller(name):
  response = await get_stocks_in_list(name)
  if not response.is_success:
    if response.status_code == None:
      response.status_code = 500
    raise HTTPException(status_code=response.status_code, detail=response.message)
  return {"result": response.data}