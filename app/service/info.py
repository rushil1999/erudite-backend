from app.service.llm import generate_llm_response
from app.service.logging import log_info, log_error
from app.models.stock_info import Stock_Info_Model
from app.models.response_models import Service_Response_Model
from fastapi import HTTPException


async def get_stock_info(stock_list):
  log_info("Stock list received for basic information {stock_list}", stock_list=stock_list)
  try:
    ticker_list = get_tickers_from_list(stock_list)
    prompt = f"Given the stock ticker symbols {ticker_list}. Give a brief overview of about the companies, their stock and what they do. This informaiton is for someone who knows nothing about this company. Keep the answer short as it might be either read or converted to speech for the user. Seperate the each stock information with a * delimiter"
    response = await generate_llm_response(prompt)
    if not response.is_success:
      return response
    llm_stock_info = response.data.split('*')
    parsed_stock_info = []
    for index in range(0, len(stock_list)):
      stock_name = stock_list[index].name
      ticker = stock_list[index].ticker
      if ticker in llm_stock_info[index]:
        stock_info = Stock_Info_Model(name=stock_name, ticker=ticker, info=llm_stock_info[index])
        parsed_stock_info.append(stock_info)
      else:
        log_info("Stock ticker and name not found in llm text: {name} {ticker}", name=stock_name, ticker=ticker)
    return Service_Response_Model(data=parsed_stock_info, is_success=True)

  except Exception as e:
    log_error("Error parsing stock information: {stocks}, due to {error}",stocks=stocks, error=str(e) )
    raise HTTPException(status_code=500, detail=f"Error parsing stock information: {str(e)}")


async def get_stock_news(stock_list):
  log_info("Stock list received for latest news {stock_list}", stock_list=stock_list)
  try:
    ticker_list = get_tickers_from_list(stock_list)
    prompt = f"Given the stock ticker symbols {ticker_list}. For each stock, give the latest news that lead to changes in stock prices, and what market conditions lead to those fluctutations. This informaiton is for someone who wants to stay updated about the latest news happening globally, specifically the ones that leads to price changes for a given stock. Keep the answer short as it might be either read or converted to speech for the user. Seperate the each stock information with a * delimiter"
    response = await generate_llm_response(prompt)
    if not response.is_success:
      return response
    llm_stock_info = response.data.split('*')
    parsed_stock_info = []
    for index in range(0, len(stock_list)):
      stock_name = stock_list[index].name
      ticker = stock_list[index].ticker
      if ticker in llm_stock_info[index]:
        stock_info = Stock_Info_Model(name=stock_name, ticker=ticker, info=llm_stock_info[index])
        parsed_stock_info.append(stock_info)
      else:
        log_info("Stock ticker and name not found in llm text: {name} {ticker}", name=stock_name, ticker=ticker)
    return Service_Response_Model(data=parsed_stock_info, is_success=True)
  except Exception as e:
    log_error("Error parsing stock news: {stock_list}, due to {error}",stock_list=stock_list, error=str(e) )
    raise HTTPException(status_code=500, detail=f"Error parsing stock news: {str(e)}")

def get_tickers_from_list(stock_list):
  ticker_list = []
  for stock in stock_list:
    ticker_list.append(stock.ticker)
  return ticker_list