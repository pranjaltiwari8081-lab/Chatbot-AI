from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")
client = genai.Client()
app = FastAPI()

class ChatRequest(BaseModel):
    messages: list[dict]

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    chat_history = "\n".join([f"{'User' if m['role']=='user' else 'Gemini'}: {m['content']}" for m in chat_request.messages])
    response = client.models.generate_content(model="gemini-2.0-flash", contents=chat_history)
    return {"reply": response.text}
