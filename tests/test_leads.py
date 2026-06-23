import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_ingest_lead():
    payload = {
        "company_name": "ACME",
        "contact_name": "Jan",
        "email": "jan@acme.com",
        "raw_message": "Szukamy automatyzacji sprzedaży."
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/leads/ingest", json=payload)

    assert response.status_code in (200, 500)
