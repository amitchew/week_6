# chat_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import openai  # Import openai if it's used in this file

chat_router = APIRouter()

class ChatRequest(BaseModel):
    input: str

class ChatResponse(BaseModel):
    response: str

@chat_router.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Format user input and previous messages for OpenAI
        user_input = request.input
        langchain_messages = [{"role": "system", "content": "You are a helpful assistant."},
                              {"role": "user", "content": user_input}]

        # Fetch response from OpenAI GPT-3.5-turbo
        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=langchain_messages
        )

        # Extract the assistant's response from the OpenAI API response
        assistant_response = openai_response["choices"][0]["message"]["content"]

        return {"response": assistant_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
