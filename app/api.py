import logging

from fastapi import FastAPI
from pydantic import BaseModel

from app.agent import TravelXAgent
from app.logging_config import setup_logging


setup_logging()

logger = logging.getLogger("travelx.api")


app = FastAPI(
    title="TravelX Customer Service Agent",
    description="A simple TravelX AI customer service agent with state and tools",
    version="0.1.0"
)


agent = TravelXAgent()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def health_check():
    logger.info("Health check requested")

    return {
        "status": "ok",
        "service": "Welcome to Travelx Ai Agent"
    }

    
@app.get("/health")
def health_check():
    logger.info("Health check requested")

    return {
        "status": "ok",
        "service": "travelx-agent"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    logger.info("Chat request received")

    reply = agent.run(request.message)

    logger.info("Chat response generated")

    return {
        "reply": reply,
        "state": agent.state.to_dict()
    }


@app.post("/reset")
def reset_conversation():
    global agent

    logger.info("Conversation state reset requested")

    agent = TravelXAgent()

    return {
        "status": "reset",
        "message": "Conversation state has been reset."
    }