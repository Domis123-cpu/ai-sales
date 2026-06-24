AI Sales Assistant — FastAPI + PostgreSQL + LLM
Inteligentny system CRM wspierany przez AI, zbudowany w oparciu o FastAPI, SQLAlchemy, PostgreSQL, OpenAI GPT‑4o‑mini oraz automatyczne testy GitHub Actions.

System obsługuje:

zarządzanie leadami

analizę rozmów

generowanie ofert

podsumowania konwersacji

klasyfikację leadów przez AI

integrację z LLM (OpenAI / Mock / Local)

To kompletny backend CRM gotowy do wdrożenia.

🚀 Funkcjonalności
🔹 Lead Ingestion & Qualification
zapis leadów do bazy

automatyczna klasyfikacja AI (hot / warm / cold)

podsumowanie intencji klienta

rekomendacje kolejnych kroków

🔹 AI Conversation Assistant
generowanie odpowiedzi

analiza kontekstu rozmowy

wsparcie handlowca w czasie rzeczywistym

🔹 Offer Generator
generowanie ofert handlowych

obliczenia cen, rabatów i wartości końcowych

generowanie treści ofert (markdown)

🔹 Conversation Summaries
podsumowanie rozmów

potrzeby klienta

obiekcje

next steps

🔹 Modularna architektura
Oddzielone moduły:

/api/leads

/api/conversations

/api/offers

Każdy moduł ma własne modele, schematy i logikę.

🧠 Technologie
Obszar	Technologia
Backend	FastAPI, Uvicorn
ORM	SQLAlchemy 2.0
Baza danych	PostgreSQL 15
Migracje	Alembic
LLM	OpenAI GPT‑4o‑mini / Mock
Testy	pytest, httpx
CI/CD	GitHub Actions
Konteneryzacja	Docker + docker-compose
Język	Python 3.11


🧱 Architektura systemu
Kod
                         ┌──────────────────────────┐
                         │        Frontend          │
                         │ (CRM / React / Postman)  │
                         └─────────────┬────────────┘
                                       │ HTTP/JSON
                                       ▼
                         ┌──────────────────────────┐
                         │         FastAPI          │
                         │       app/main.py        │
                         └─────────────┬────────────┘
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        │                              │                              │
        ▼                              ▼                              ▼
┌────────────────┐        ┌──────────────────────┐        ┌──────────────────────┐
│  Leads Module   │        │ Conversations Module │        │   Offers Module      │
│ /api/leads      │        │ /api/conversations   │        │ /api/offers          │
└───────┬─────────┘        └──────────┬───────────┘        └──────────┬──────────┘
        │                              │                               │
        ▼                              ▼                               ▼
┌────────────────┐        ┌──────────────────────┐        ┌──────────────────────┐
│ Lead Model     │        │ Conversation Model    │        │ Offer + OfferItems   │
│ SQLAlchemy ORM │        │ SQLAlchemy ORM        │        │ SQLAlchemy ORM        │
└───────┬─────────┘        └──────────┬───────────┘        └──────────┬──────────┘
        │                              │                               │
        └──────────────┬───────────────┴───────────────┬──────────────┘
                       ▼                                 ▼
              ┌────────────────┐               ┌────────────────┐
              │ PostgreSQL 15  │               │ Alembic Migrations │
              │   (appdb)      │               │  versions/         │
              └────────────────┘               └────────────────┘
                       ▲
                       │ async HTTP
                       ▼
              ┌──────────────────────────┐
              │       LLM Client         │
              │ OpenAI / Mock / Local    │
              └──────────────────────────┘
🗄️ Struktura bazy danych
Migracje Alembica tworzą tabele:

leads

lead_qualification

products

offers

offer_items

conversations

conversation_summaries

🧪 Testy automatyczne (pytest + GitHub Actions)
Projekt zawiera:

testy endpointów FastAPI (httpx + pytest)

testy integracyjne z PostgreSQL

workflow CI:

Kod
.github/workflows/tests.yml
Testy uruchamiają się automatycznie przy każdym:

pushu

pull requeście

🐳 Uruchamianie projektu (Docker)
Otwórz plik:

Kod
notepad docker-compose.yml
Wklej swój klucz API:

Kod
LLM_API_KEY="your_key_here"
Uruchom:

Kod
docker-compose up --build
Dokumentacja API:

👉 http://localhost:8000/docs
