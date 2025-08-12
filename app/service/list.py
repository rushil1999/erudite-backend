from app.service.llm import generate_llm_response
from app.service.logging import log_info, log_error
from app.models.stock_info import Stock_Info_Model
from app.models.response_models import Service_Response_Model
from app.service.mongodb import collection 
from fastapi import HTTPException


async def get_stocks_in_list(name):
  log_info("Stock list name received {name}", name=name)
  try:
    document = collection.find_one({"name": name})
    if document and document['stocks']:
      stock_info_list = parse_stock_info(document['stocks'])
      return Service_Response_Model(data=stock_info_list, is_success=True)
    else:
      return Service_Response_Model(data="", status_code=404, is_success=False)

  except Exception as e:
    log_error("Error fetching stock list: {name}, due to {error}",name=name, error=str(e) )
    raise HTTPException(status_code=500, detail=f"Error fetching stock list list: {str(e)}")




  except Exception as e:
    log_error("Error getting tickers stock list: {stock_list}, due to {error}",stock_list=stock_list, error=str(e) )
    raise HTTPException(status_code=500, detail=f"Error fetching stock list list: {str(e)}")


def parse_stock_info(data):
  stock_info_list = []
  for obj in data:
    stock_info = Stock_Info_Model(name=obj['name'], ticker=obj['ticker'])
    stock_info_list.append(stock_info)
  return stock_info_list
