# Snapdeal AI Voice KAM

A voice-first AI Key Account Manager that helps marketplace sellers understand their business performance, identify potential issues, and receive actionable recommendations through natural conversations.

## Overview

Marketplace sellers often struggle to understand why their business metrics change and what actions they should take to improve performance.

Snapdeal AI Voice KAM provides a conversational interface where sellers can ask questions about their business using voice or text. The assistant analyzes available seller performance metrics, asks relevant follow-up questions, and provides practical recommendations.

This project is a working prototype built using mock seller data.

## Features

- **Voice-based interaction:** Speak naturally with the AI assistant using the browser microphone.
- **Speech-to-text:** Converts recorded audio into text using Faster-Whisper.
- **AI-powered conversations:** Uses Qwen 2.5 7B through Ollama to understand seller queries and generate responses.
- **Seller performance analytics:** Calculates changes in sales, orders, cancellation rates, average selling price, and out-of-stock products.
- **Context-aware conversations:** Maintains recent conversation history to support follow-up questions.
- **Voice responses:** Reads AI-generated responses aloud using the browser's Speech Synthesis API.
- **Text interaction:** Supports typing questions as an alternative to voice input.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| Language Model | Qwen 2.5 7B |
| Local Model Runtime | Ollama |
| Speech-to-Text | Faster-Whisper |
| Text-to-Speech | Browser Speech Synthesis API |
| Audio Recording | Browser MediaRecorder API |
| API Communication | HTTP / REST |

## System Architecture

```text
             SELLER
                |
                v
       Browser Frontend
        HTML / CSS / JS
                |
        Microphone Audio
                |
                v
       Browser MediaRecorder
                |
                v
         FastAPI Backend
                |
                v
          Faster-Whisper
          Speech-to-Text
                |
          Transcribed Text
                |
                v
       Conversation Service
                |
         +------+------+
         |             |
         v             v
   Seller Analytics  Conversation
       (Python)       History
         |             |
         +------+------+
                |
                v
          Ollama API
                |
                v
          Qwen 2.5 7B
                |
         Generated Response
                |
                v
          FastAPI Backend
                |
                v
          Browser Frontend
                |
          +-----+------+
          |            |
          v            v
      Chat Display  Speech Synthesis
                       |
                       v
                 Spoken Response
```

## Project Structure

```text
snapdeal-voice-kam/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   │
│   ├── data/
│   │   └── seller.json
│   │
│   ├── services/
│   │   ├── analytics.py
│   │   ├── conversation.py
│   │   ├── ollama_service.py
│   │   └── speech_service.py
│   │
│   └── prompts/
│       └── system_prompt.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
└── README.md
```

## Seller Data

The prototype uses the following mock seller performance data:

| Metric | Previous Month | Current Month |
|---|---:|---:|
| Sales | ₹2,00,000 | ₹1,35,000 |
| Orders | 400 | 270 |
| Cancellation Rate | 8% | 14% |
| Average Selling Price | ₹500 | ₹500 |
| Out-of-Stock Products | 5 | 18 |

### Key Observations

- Sales declined by 32.5%.
- Orders declined by 32.5%.
- Cancellation rate increased by 6 percentage points.
- Average selling price remained unchanged.
- Out-of-stock products increased from 5 to 18.

The assistant uses these observations to guide conversations and suggest possible actions. It does not assume that any single metric is the confirmed cause of the sales decline.

## Getting Started

### Prerequisites

Install the following:

- Python
- Ollama
- Google Chrome or another browser supporting MediaRecorder and Speech Synthesis

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd snapdeal-voice-kam
```

### 2. Set Up Ollama

Install Ollama from:

https://ollama.com/

Download the required model:

```bash
ollama pull qwen2.5:7b
```

Start Ollama:

```bash
ollama serve
```

Ollama runs locally and exposes its API at:

```text
http://localhost:11434
```

If Ollama is already running in the background, you do not need to start another instance.

### 3. Set Up the Backend

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows Git Bash:

```bash
source venv/Scripts/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

If needed, install the audio transcription dependencies:

```bash
python -m pip install faster-whisper python-multipart
```

### 4. Start the Backend

From the backend directory, run:

```bash
uvicorn main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

FastAPI interactive documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Start the Frontend

Open another terminal and navigate to the frontend directory:

```bash
cd frontend
```

Start a local development server:

```bash
python -m http.server 5500
```

Open the application in your browser:

```text
http://localhost:5500
```

Allow microphone access when prompted.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Checks backend health |
| POST | `/transcribe` | Converts uploaded audio into text |
| POST | `/chat` | Processes seller queries and generates AI responses |

### Chat Request Example

```json
{
  "session_id": "demo-session",
  "message": "Why have my sales dropped this month?"
}
```

### Chat Response Example

```json
{
  "session_id": "demo-session",
  "response": "Your sales have declined by 32.5% compared to last month..."
}
```

## How It Works

1. The seller records a voice message through the browser.
2. The MediaRecorder API captures the audio.
3. The audio is uploaded to the FastAPI backend.
4. Faster-Whisper transcribes the recording into text.
5. The conversation service combines the seller's query, recent conversation history, and calculated performance metrics.
6. The Ollama API sends the contextual prompt to Qwen 2.5 7B.
7. The generated response is returned to the frontend.
8. The browser displays the response and converts it into speech using Speech Synthesis.

## Design and Implementation Decisions

- **Local inference:** Ollama and Faster-Whisper run locally, avoiding dependency on paid cloud AI APIs.
- **Lightweight architecture:** The application uses a simple FastAPI backend and vanilla JavaScript frontend.
- **Python-based analytics:** Business metrics are calculated in Python rather than relying on the language model for arithmetic.
- **Conversation context:** Recent messages are maintained in backend memory to support follow-up interactions.
- **Data accuracy:** The assistant is instructed to distinguish observed business metrics from possible explanations and avoid inventing missing information.

## Current Limitations

- Uses mock seller data rather than live Snapdeal APIs.
- Conversation history is stored in application memory and is not persistent across backend restarts.
- Does not include authentication or multi-seller account management.
- Speech recognition performance depends on audio quality and local hardware.
- Text-to-speech uses the browser's available speech synthesis voice.
- The prototype is not production-ready.

## Future Improvements

- Integrate real seller dashboards and marketplace APIs.
- Add product-level inventory and cancellation analysis.
- Introduce persistent conversation storage.
- Support multiple sellers and personalized performance history.
- Improve multilingual speech recognition and voice responses.
- Add evaluation mechanisms to measure response accuracy and recommendation quality.

## Demo

- **Screen Recording:** ADD_YOUR_LOOM_LINK
- **GitHub Repository:** ADD_YOUR_GITHUB_LINK

---

**Built by Vedant Dubey**

A practical prototype exploring conversational AI for marketplace seller support.
