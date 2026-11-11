import os
import tempfile

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.conversation import handle_seller_message
from services.speech_service import transcribe_audio


app = FastAPI(title="Snapdeal Voice KAM")


# Allow frontend to communicate with backend.
# NOTE: browsers reject allow_origins=["*"] together with credentials,
# so credentials are disabled. In production, list your real frontend origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Store conversations temporarily in memory.
conversation_histories = {}

# Content types browsers commonly send for MediaRecorder blobs.
# Chrome sometimes labels audio-only webm as video/webm.
ALLOWED_CONTENT_TYPES = (
    "audio/",
    "video/webm",
    "video/mp4",
    "application/octet-stream",
)


# Request model for chat endpoint.
class ChatRequest(BaseModel):
    session_id: str
    message: str


# -----------------------------------
# 1. Health Check
# -----------------------------------

@app.get("/health")
async def health_check():

    return {
        "status": "healthy",
        "service": "Snapdeal Voice KAM"
    }


# -----------------------------------
# 2. Chat Endpoint
# -----------------------------------

@app.post("/chat")
async def chat(request: ChatRequest):

    session_id = request.session_id
    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    # Create a new conversation if needed.
    if session_id not in conversation_histories:
        conversation_histories[session_id] = []

    history = conversation_histories[session_id]

    try:

        answer = await handle_seller_message(
            message,
            history
        )

        return {
            "session_id": session_id,
            "response": answer
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Chat generation failed: {str(error)}"
        )


# -----------------------------------
# 3. Speech-to-Text Endpoint
# -----------------------------------

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):

    # Validate uploaded audio.
    content_type = (file.content_type or "").lower()

    if not content_type.startswith(ALLOWED_CONTENT_TYPES):
        raise HTTPException(
            status_code=400,
            detail="Please upload a valid audio file."
        )

    temp_path = None

    try:

        audio_bytes = await file.read()

        if not audio_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded audio file is empty."
            )

        # Keep the original extension if available (webm, mp4, wav, ...).
        suffix = os.path.splitext(file.filename or "")[1] or ".webm"

        # Save audio temporarily.
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_file.write(audio_bytes)
            temp_path = temp_file.name

        # Convert audio to text using Faster-Whisper.
        # Runs in a worker thread so it doesn't block other requests.
        transcript = await run_in_threadpool(
            transcribe_audio,
            temp_path
        )

        return {
            "transcript": transcript
        }

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {str(error)}"
        )

    finally:

        # Remove temporary audio file.
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


# -----------------------------------
# 4. Voice Chat (audio in -> reply out, one call)
# -----------------------------------

@app.post("/voice-chat")
async def voice_chat(session_id: str, file: UploadFile = File(...)):

    result = await transcribe(file)
    transcript = result["transcript"]

    if not transcript:
        return {
            "session_id": session_id,
            "transcript": "",
            "response": "Sorry, I couldn't hear that. Could you please repeat?"
        }

    chat_result = await chat(
        ChatRequest(session_id=session_id, message=transcript)
    )

    return {
        "session_id": session_id,
        "transcript": transcript,
        "response": chat_result["response"]
    }