from app.service.llm import generate_llm_response
from app.service.logging import log_info, log_error
from app.models.stock_info import Stock_Info_Model
from app.models.response_models import Service_Response_Model
from fastapi import HTTPException


async def get_stock_info(stocks):
  try:
    log_info("Stock list received for basic information {stocks}", stocks=stocks)
    prompt = f"Given the stock ticker symbols {stocks}. Give a brief overview of about the companies, their stock and what they do. This informaiton is for someone who knows nothing about this company. Keep the answer short as it might be either read or converted to speech for the user. Seperate the each stock information with a * delimiter"
    response = await generate_llm_response(prompt)
    if not response.is_success:
      return response
    ticker_list = stocks.split(',')
    llm_stock_info = response.data.split('*')
    parsed_stock_info = []
    for index in range(0, len(ticker_list)):
      ticker = ticker_list[index]
      if ticker in llm_stock_info[index]:
        stock_info = Stock_Info_Model(name="", ticker=ticker, info=llm_stock_info[index])
        parsed_stock_info.append(stock_info)
    return Service_Response_Model(data=parsed_stock_info, is_success=True)

  except Exception as e:
    log_error("Error parsing stock information: {stocks}, due to {error}",stocks=stocks, error=str(e) )
    raise HTTPException(status_code=500, detail=f"Error parsing stock information: {str(e)}")


async def get_stock_news(stocks):
  try:
    log_info("Stock list received for latest news {stocks}", stocks=stocks)
    prompt = f"Given the stock ticker symbols {stocks}. For each stock, give the latest news that lead to changes in stock prices, and what market conditions lead to those fluctutations. This informaiton is for someone who wants to stay updated about the latest news happening globally, specifically the ones that leads to price changes for a given stock. Keep the answer short as it might be either read or converted to speech for the user. Seperate the each stock information with a * delimiter"
    response = await generate_llm_response(prompt)
    if not response.is_success:
      return response
    ticker_list = stocks.split(',')
    llm_stock_info = response.data.split('*')
    parsed_stock_info = []
    for index in range(0, len(ticker_list)):
      ticker = ticker_list[index]
      if ticker in llm_stock_info[index]:
        stock_info = Stock_Info_Model(name="", ticker=ticker, info=llm_stock_info[index])
        parsed_stock_info.append(stock_info)
    return Service_Response_Model(data=parsed_stock_info, is_success=True)
  except Exception as e:
    log_error("Error parsing stock news: {stocks}, due to {error}",stocks=stocks, error=str(e) )
    raise HTTPException(status_code=500, detail=f"Error parsing stock news: {str(e)}")
