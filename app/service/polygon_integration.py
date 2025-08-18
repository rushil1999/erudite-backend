import httpx
from datetime import datetime
from app.models.polygon_integration_models import Polygon_Response, Polygon_Insight_Model
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
    current_date = datetime.today().strftime('%Y-%m-%d')
    host = os.getenv("POLYGON_NEWS_URL")
    url = f"{host}?ticker={ticker}&published_utc={current_date}&order=asc&limit=10&sort=published_utc&apiKey={key}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = httpx.get(url, headers=headers)
    if response.status_code != httpx.codes.OK :
        log_error("Error fetching data from Polygon API, status code: {status_code}", status_code=response.status_code )
    print(response)
    json_data = response.json()
    polygon_response = Polygon_Response(**json_data)
    log_info("Called Polygon API to get data: {polygon_response}", polygon_response=polygon_response)
    if len(polygon_response.results) == 0 :
        return Service_Response_Model(data=[], is_success=False, message="Cannot fetch news data")
    return Service_Response_Model(data=polygon_response.results, is_success=True)
  except Exception as e:
    log_error("Error getting specific ticker news: {ticker}, due to {error}",ticker=ticker, error=str(e) )
    raise HTTPException(status_code=500, detail=f"Error generating vector: {str(e)}")
