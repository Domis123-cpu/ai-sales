import httpx
import json
import os
from typing import Dict, Any

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")
        self.base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com")

    async def classify_lead(self, lead_payload: Dict[str, Any]) -> Dict[str, Any]:
        prompt = self._build_lead_classification_prompt(lead_payload)
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{self.base_url}/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": "gpt-4o-mini",
                    "response_format": {"type": "json_object"},
                    "messages": [
                        {"role": "system", "content": "You are a B2B sales qualification assistant."},
                        {"role": "user", "content": prompt},
                    ],
                },
            )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        return json.loads(content)

    def _build_lead_classification_prompt(self, lead_payload: Dict[str, Any]) -> str:
        return (
            "Oceń poniższy lead i zwróć JSON z polami: "
            "score (0-100), tier (hot/warm/cold), intent_summary, "
            "budget_signal, timeline_signal, recommended_action.\n\n"
            f"LEAD:\n{lead_payload}"
        )

def get_llm_client() -> LLMClient:
    return LLMClient()
