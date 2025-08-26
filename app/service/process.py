from app.service.list import get_stocks_in_list
from app.service.info import get_stock_news, get_stock_info
from app.service.logging import log_info, log_error
from fastapi import HTTPException
from app.service.polygon_integration import get_ticker_specific_data
from app.models.polygon_integration_models import Polygon_Article_Model, Article_Model
from app.models.response_models import Service_Response_Model
from app.models.stock_info import Stock_Info_Model
from app.service.llm import generate_llm_response
import json
from datetime import datetime, timedelta, date
from app.service.mongodb import db, summaries
from fastapi.encoders import jsonable_encoder

async def process_news(list_name):
  log_info("List received to process news {list_name}", list_name=list_name)
  try: 
    response = await get_stocks_in_list(list_name)
    if not response.is_success:
      return response
    # 1. Get a ticker list from the list name
    ticker_list = get_tickers_from_list(response.data)

    stock_article_map = {}
    llm_article_map = {} # Similar to stock article map, but with article list converted to json string
    for ticker in ticker_list:
      # 2. Get Ticker specific data
      ticker_specific_response = await get_ticker_specific_data(ticker)
      if not ticker_specific_response.is_success:
        log_error("error getting stock data from polygon integration for ticker: {ticker}", ticker=ticker)
        continue

      stock_article_map[ticker] = ticker_specific_response.data

      jsonable_dict = jsonable_encoder(ticker_specific_response.data)
      json_string = json.dumps(jsonable_dict)
      llm_article_map[ticker] = json_string

    if len(stock_article_map) == 0:
      log_info("No data could be mapped. Returning")
      return Service_Response_Model(data=[], is_success=False)

    llm_prompt = generate_llm_prompt(llm_article_map)
    llm_response = await generate_llm_response(llm_prompt)
    llm_object = json.loads(llm_response.data) #Map containing Key as the ticker and summary as the value
    
    for ticker in ticker_list:
      print("Here", llm_object)
      summary = llm_object[ticker]
      date_string = "2025-23-08"
      log_info("saving data for ticker: {ticker} with summary: {summary}", ticker=ticker, summary=summary)

      stock_info = Stock_Info_Model(ticker=ticker, info=summary, timestamp=date_string)
      print("Something")
      data_dump = stock_info.model_dump(by_alias=True)
      result = summaries.insert_one(data_dump).inserted_id
      log_info("inserted summary for ticker with symbol: {ticker}, and mongodb id: {result}", ticker=ticker, result=result)

    return Service_Response_Model(data=llm_object, is_success=True)
  except Exception as e:
    log_error("Error processing news for list: {list_name}, due to {error}",list_name=list_name, error=str(e) )
    raise HTTPException(status_code=500, detail=f"Error processing stock list: {str(e)}")
    

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
    

def get_tickers_from_list(stock_list):
  ticker_list = []
  for stock in stock_list:
    ticker_list.append(stock.ticker)
  return ticker_list

    
def generate_llm_prompt(stock_article_map):
  prompt = f"You are a news summarizer. Summarize the news for a layman person, keeping it concise but not too short and just return the response in json format with key as the ticker and value as the summary. Here is the json objects for articles with their title, description, and sentiment attached which fetched from 3rd party news provider. {stock_article_map}"
  return prompt
