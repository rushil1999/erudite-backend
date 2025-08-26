from app.service.llm_setup import chat
from fastapi import HTTPException
from app.models.response_models import Service_Response_Model
from app.service.logging import log_info,log_error


async def generate_llm_response(prompt_input):
  log_info("User Data received for LLM")
  try: 
    response = chat.invoke(prompt_input)
    if len(response.content) > 0:
      log_info("Response generate from llm: {result}", result=response.content)
      return Service_Response_Model(data=response.content, is_success=True)
    return Service_Response_Model(data="", is_success=False, status_code=404, message="No data received from the API")
  except Exception as e:
    log_error("Error generating chat response with payload: {user_chat_payload}, due to {error}",user_chat_payload=user_chat_payload, error=str(e) )
    raise HTTPException(status_code=500, detail=f"Error getting response from Grok: {str(e)}")
