import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_generate_offer():
    payload = {
        "lead_id": 1,
        "items": [
            {"product_id": 1, "quantity": 2}
        ]
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/offers/generate", json=payload)

    assert response.status_code in (200, 500)
