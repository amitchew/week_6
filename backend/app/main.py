from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import openai  # Install using: pip install openai
import os

from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

# Allow CORS for all domains in this example.
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI API key
openai.api_key = openai.api_key = os.getenv("OPENAI_API_KEY")

@main_app.get('/')
def home():
    return 'THis is 10 Academy promptly API '

class ChatRequest(BaseModel):
    input: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat")
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

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
