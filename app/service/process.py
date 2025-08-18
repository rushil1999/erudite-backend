from app.service.list import get_stocks_in_list
from app.service.info import get_stock_news, get_stock_info
from app.service.logging import log_info, log_error
from fastapi import HTTPException
from app.service.polygon_integration import get_ticker_specific_data
from app.models.polygon_integration_models import Polygon_Article_Model, Parsed_Article_Model
from app.models.response_models import Service_Response_Model

async def process_news(list_name):
  log_info("List received to process news {list_name}", list_name=list_name)
  try:

    response = await get_stocks_in_list(list_name)
    if not response.is_success:
      return response
    ticker_list = get_tickers_from_list(response.data)

    stock_article_map = {}
    for ticker in ticker_list:
        ticker_specific_response = await get_ticker_specific_data(ticker)
        if not ticker_specific_response.is_success:
          log_error("error getting stock data from polygon integration for ticker: {ticker}", ticker=ticker)
          continue
        article_list = convert_to_polygon_stock(ticker, ticker_specific_response.data).data
        stock_article_map[ticker] = article_list
    return Service_Response_Model(data=stock_article_map, is_success=True)
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
    

def get_tickers_from_list(stock_list):
  ticker_list = []
  for stock in stock_list:
    ticker_list.append(stock.ticker)
  return ticker_list


def convert_to_polygon_stock(ticker, ticker_data):
  log_info("Input Received")
  article_list = []
  try:
    for article in ticker_data:
      for index in range(len(article.insights)):
        if article.insights[index].ticker == ticker:
          sentiment_reasoning = article.insights[index].sentiment_reasoning
          sentiment = article.insights[index].sentiment
          break
      parsed_article = Parsed_Article_Model(id=article.id, title=article.title, article_url=article.article_url, description=article.description, sentiment_reasoning=sentiment_reasoning, sentiment=sentiment, ticker=ticker)
      article_list.append(parsed_article)
    return Service_Response_Model(data=article_list, is_success=True)
  except Exception as e:
    log_error("Error for input: {input}, due to {error}",input=ticker_data, error=str(e) )
    raise HTTPException(status_code=500, detail=f"Error fetching stock list: {str(e)}")
    
    