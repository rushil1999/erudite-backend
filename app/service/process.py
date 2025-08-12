from app.service.list import get_stocks_in_list
from app.service.info import get_stock_news, get_stock_info
from app.service.logging import log_info, log_error
from fastapi import HTTPException

async def process_news(list_name):
  log_info("List received to process news {list_name}", list_name=list_name)
  try:
    response = await get_stocks_in_list(list_name)
    if not response.is_success:
      return response
    print("Results1", response.data)
    return await get_stock_news(response.data)
    print("Results2", response)
    return response
  except Exception as e:
    log_error("Error processing news for list: {list_name}, due to {error}",list_name=list_name, error=str(e) )
    raise HTTPException(status_code=500, detail=f"Error fetching stock list: {str(e)}")
    

async def process_info(list_name):
  log_info("List received to process info {list_name}", list_name=list_name)
  try:
    response = await get_stocks_in_list(list_name)
    if not response.is_success:
      return response
    return await get_stock_info(response.data)
  except Exception as e:
    log_error("Error processing news for list: {list_name}, due to {error}",list_name=list_name, error=str(e) )
    raise HTTPException(status_code=500, detail=f"Error fetching stock list: {str(e)}")
    



