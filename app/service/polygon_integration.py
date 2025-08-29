import httpx
from datetime import datetime, timedelta, date
from app.models.polygon_integration_models import Polygon_Response, Polygon_Insight_Model, Article_Model
from app.models.response_models import Service_Response_Model
import os
from dotenv import load_dotenv
from typing import List
from app.service.logging import log_info, log_error
from fastapi import HTTPException
import json


# Load environment variables from .env
load_dotenv()

# Function to get the API key from the environment
def get_api_key():
    return os.getenv("POLYGON_API_KEY")
  
async def get_ticker_specific_data(ticker: str):
  log_info("Received Ticker Input: {ticker}", ticker=ticker)
  try:
    key = get_api_key()
    current_date = date.today()
    current_date = current_date.strftime('%Y-%m-%d')
    host = os.getenv("POLYGON_NEWS_URL")
    url = f"{host}?ticker={ticker}&published_utc={current_date}&order=asc&limit=10&sort=published_utc&apiKey={key}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = httpx.get(url, headers=headers)
    if response.status_code != httpx.codes.OK:
      log_error("Error fetching data from Polygon API, status code: {status_code}", status_code=response.status_code )
    json_data = response.json()
    polygon_response = Polygon_Response(**json_data)
    if len(polygon_response.results) == 0:
      log_info("Cannot fetch any articles from Polygon API for ticker: {ticker}", ticker=ticker)
      return Service_Response_Model(data=[], is_success=False, message="Cannot fetch news data")
    log_info("Called Polygon API to get {count} articles for ticker: {ticker}", count=len(polygon_response.results), ticker=ticker)

    parsed_articles = parse_polygon_articles(ticker, polygon_response)
    return Service_Response_Model(data=parsed_articles, is_success=True)
  except Exception as e:
    log_error("Error getting specific ticker news: {ticker}, due to {error}",ticker=ticker, error=str(e) )
    raise HTTPException(status_code=500, detail=f"Error generating vector: {str(e)}")


def parse_polygon_articles(ticker: str, polygon_response: Polygon_Response) -> List[Article_Model]:
  parsed_articles = []
  
  for article in polygon_response.results:
    sentiment = ''
    sentiment_reasoning = ''
    for insight in article.insights:
      if insight.ticker == ticker:
        sentiment_reasoning = insight.sentiment_reasoning
        sentiment = insight.sentiment
        break

    article = Article_Model(title=article.title, article_url=article.article_url, description=article.description, ticker=ticker, sentiment=sentiment, sentiment_reasoning=sentiment_reasoning)

    parsed_articles.append(article)

  return parsed_articles
     

