import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_conversation_reply():
    payload = {
        "conversation_id": 1,
        "message": "Dzień dobry, szukam CRM."
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/assistant/reply", json=payload)

    assert response.status_code in (200, 500)
