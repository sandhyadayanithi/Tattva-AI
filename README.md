# Tattva-AI 

> **AI-powered misinformation detection via WhatsApp — supports voice, image, and text in Indian regional languages.**

Tattva-AI is a full-stack fact-checking platform built around a WhatsApp bot. Users send a voice note, image, or text message containing a claim; the system transcribes it, extracts the core claim, verifies it against live web evidence, and replies with a verdict, virality risk score, and a suggested counter-message — all in the user's original language.

A companion dashboard (MisInfo Monitor) gives analysts a real-time view of trends, repeat claims, language breakdowns, and model feedback.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Dashboard Pages](#dashboard-pages)

---

## Features

- **Multi-modal input** — accepts WhatsApp voice notes, images, and plain text
- **Regional language support** — auto-detects and responds in Tamil, Hindi, Telugu, Bengali, and more
- **Whisper transcription** — OpenAI Whisper converts voice notes to text locally
- **OCR pipeline** — Tesseract + Gemini refinement extracts text from forwarded screenshots
- **Claim extraction** — Gemini 2.5 Flash isolates the core factual claim and translates it to English
- **Live fact-checking** — Tavily search fetches real-time evidence; Gemini generates a structured verdict
- **Semantic cache** — ChromaDB + SentenceTransformers deduplicate near-identical claims to save API credits
- **Firestore transcript cache** — exact-match caching for repeated transcripts
- **Virality risk scoring** — 1–10 score based on emotional language, urgency, and conspiracy framing
- **Regional TTS replies** — ElevenLabs Multilingual v2 sends voice note responses for non-English verdicts
- **Firebase Storage** — all uploaded media is persisted in Cloud Storage
- **MisInfo Monitor dashboard** — React + Vite frontend with live analytics

---

## Architecture

```
WhatsApp User
     │
     ▼
Meta Cloud API (webhook)
     │
     ▼
FastAPI Backend
     ├── Voice  → Whisper → ClaimExtractor (Gemini) → FactChecker (Tavily + Gemini)
     ├── Image  → OCR (Tesseract + Gemini) → ClaimExtractor → FactChecker
     └── Text   → ClaimExtractor → FactChecker
          │
          ├── ChromaDB (semantic cache)
          ├── Firestore (transcript cache + message history)
          └── ElevenLabs TTS → WhatsApp voice reply
     │
     ▼
React Dashboard (MisInfo Monitor)
     └── Firestore (live claim feed, analytics)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend framework | FastAPI + Uvicorn |
| AI / LLM | Google Gemini 2.5 Flash (`google-genai`) |
| Transcription | OpenAI Whisper (`openai-whisper`) |
| Web search | Tavily API |
| OCR | Tesseract + Pillow |
| TTS | ElevenLabs Multilingual v2 |
| Vector cache | ChromaDB + `sentence-transformers` (`all-MiniLM-L6-v2`) |
| Database | Firebase Firestore + Firebase Storage |
| Messaging | Meta WhatsApp Cloud API |
| Frontend | React 18, Vite, TypeScript, Tailwind CSS, React Router |
| UI components | shadcn/ui, Lucide React, Recharts |

---

## Project Structure

```
tattva-ai/
├── backend/
│   ├── main.py                  # FastAPI app, webhook handlers, pipeline orchestration
│   ├── requirements.txt
│   ├── seed_firestore.py        # Seeds Firestore with mock data on startup
│   ├── ai/
│   │   ├── claim_extractor.py   # Gemini-based claim isolation + language detection
│   │   ├── fact_checker.py      # Tavily search + Gemini verdict generation
│   │   └── transcription.py     # Whisper audio transcription
│   ├── services/
│   │   ├── whatsapp_service.py  # Meta API: send/receive messages and media
│   │   ├── firebase_service.py  # Firestore read/write helpers
│   │   ├── storage_service.py   # Firebase Cloud Storage uploads
│   │   ├── vector_service.py    # ChromaDB semantic cache
│   │   ├── elevenlabs_service.py# TTS generation
│   │   └── ocr_service.py       # Tesseract OCR + optional LLM refinement
│   ├── core/
│   │   └── config.py            # Pydantic settings (env vars)
│   ├── models/
│   │   └── message_model.py     # Pydantic data models
│   ├── utils/
│   │   ├── logger.py
│   │   └── text_utils.py        # Transcript normalisation
│   └── scripts/
│       ├── test_pipeline.py     # End-to-end pipeline test
│       └── test_elevenlabs.py   # Standalone TTS test
│
└── frontend/
    ├── src/
    │   └── app/
    │       ├── features/
    │       │   ├── landing/     # Public landing page
    │       │   ├── dashboard/   # Dashboard overview
    │       │   ├── trends/      # Misinformation trend charts
    │       │   ├── repeat-claims/
    │       │   ├── language/    # Language analytics
    │       │   └── feedback/    # Model feedback
    │       └── shared/
    │           └── components/layout/
    └── package.json
```

---

## Getting Started

### Prerequisites

- Python 3.10+ (3.14 supported with defensive ChromaDB import)
- Node.js 20+
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) installed on your system
- A Meta Developer account with a WhatsApp Business app and webhook configured
- API keys for: Gemini, Tavily, ElevenLabs, Firebase (service account JSON)

---

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Copy and fill in your environment variables
cp .env.example .env

# Start the development server
uvicorn main:app --reload --port 8000
```

The server starts on `http://localhost:8000`. On startup it automatically seeds Firestore with mock data if the database is empty.

To expose your local server to Meta's webhook during development, use a tunnelling tool like [ngrok](https://ngrok.com/):

```bash
ngrok http 8000
```

Set the resulting `https://` URL as your Meta webhook URL, with `/webhook` as the path and your `VERIFY_TOKEN` as the verification token.

---

### Frontend Setup

```bash
cd frontend

npm install
npm run dev
```

The dashboard runs on `http://localhost:5173`.

---

## Environment Variables

Create a `backend/.env` file with the following keys:

```env
# Meta / WhatsApp
WHATSAPP_TOKEN=your_whatsapp_access_token
PHONE_NUMBER_ID=your_phone_number_id
VERIFY_TOKEN=your_webhook_verify_token

# Google Gemini
GEMINI_API_KEY=your_gemini_api_key

# Tavily (web search)
TAVILY_API_KEY=tvly-your_tavily_api_key

# ElevenLabs TTS
ELEVENLABS_API_KEY=your_elevenlabs_api_key

# Firebase (path to your service account JSON)
FIREBASE_CREDENTIALS_PATH=./firebase-service-account.json
FIREBASE_STORAGE_BUCKET=your-project.appspot.com

# Feature flags
USE_LLM=true

# (Optional) for pipeline tests
TEST_WHATSAPP_NUMBER=919876543210
```

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/webhook` | Meta webhook verification |
| `POST` | `/webhook` | Incoming WhatsApp messages (voice / image / text) |
| `GET` | `/messages/recent` | List recent fact-checked messages |
| `GET` | `/messages/user/{number}` | Messages from a specific WhatsApp number |
| `GET` | `/claims` | All claims stored in the vector DB |
| `POST` | `/test-claim-storage` | Debug: manually cache a claim embedding |

---

## Testing

Run the end-to-end pipeline locally (no WhatsApp device needed):

```bash
cd backend
python scripts/test_pipeline.py
```

Test TTS generation in isolation:

```bash
python scripts/test_elevenlabs.py
```

Test Whisper transcription:

```bash
python run_whisper.py
```

---

## Dashboard Pages

| Route | Page | Description |
|---|---|---|
| `/` | Dashboard Overview | KPI cards, welcome panel, quick-access tiles |
| `/trends` | Misinformation Trends | Time-series charts by category |
| `/repeat-claims` | Repeat Claims | Deduplicated high-frequency claims |
| `/language` | Language Analytics | Claim breakdown by detected language |
| `/feedback` | Model Feedback | Flag incorrect verdicts, partner collaboration |
