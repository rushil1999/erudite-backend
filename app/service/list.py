from app.service.llm import generate_llm_response
from app.service.logging import log_info, log_error
from app.models.stock_info import Stock_Info_Model
from app.models.response_models import Service_Response_Model
from app.service.mongodb import collection 
from fastapi import HTTPException


async def get_stock_list(name):
  log_info("Stock list name received {name}", name=name)
  try:
    document = collection.find_one({"name": name})
    if document:
      print(document)
      return Service_Response_Model(data=document['stocks'], is_success=True)
    else:
      print(document)
      return Service_Response_Model(data="", status_code=404, is_success=False)

  except Exception as e:
    log_error("Error fetching stock list: {name}, due to {error}",name=name, error=str(e) )
    raise HTTPException(status_code=500, detail=f"Error fetching stock list list: {str(e)}")
