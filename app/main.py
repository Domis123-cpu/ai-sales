from fastapi import FastAPI
from app.api import leads, conversations, assistant, offers

app = FastAPI(title="AI Sales Assistant")

app.include_router(leads.router)
app.include_router(conversations.router)
app.include_router(assistant.router)
app.include_router(offers.router)
