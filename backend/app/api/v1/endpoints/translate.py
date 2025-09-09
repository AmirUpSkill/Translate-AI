import logging
from typing import Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.schemas.translation import TranscribeRequest, TranscribeResponse, TranslateRequest, TranslateResponse  # Absolute import
from app.services.stt_service import stt_service  # Absolute import + CORRECTED NAME: stt_service
from app.services.translation_service import translation_service  # Absolute import

# Setup logging
logger = logging.getLogger(__name__)

# Create a sub-router for translation endpoints
translate_router = APIRouter()

@translate_router.post("/transcribe", response_model=TranscribeResponse, tags=["transcription"])
async def transcribe_audio(
    audio: UploadFile = File(..., description="Audio file to transcribe (WAV, MP3, etc.)"),
    language: Optional[str] = Form(None, description="Optional ISO-639-1 language code (e.g., 'en')")
):
    """
    Transcribes speech from an audio file to text using Groq's STT model.
    """
    try:
        # Validate file
        if not audio.content_type or audio.content_type not in ["audio/wav", "audio/mpeg", "audio/mp3"]:
            raise HTTPException(status_code=400, detail="Unsupported audio format. Use WAV or MP3.")
        
        # Read audio bytes
        audio_bytes = await audio.read()
        if not audio_bytes:
            raise HTTPException(status_code=400, detail="Empty audio file.")
        
        logger.info(f"Received audio file: {audio.filename}, size: {len(audio_bytes)} bytes")
        
        # Call STT service – CORRECTED USAGE: stt_service (not sst_service)
        transcribed_text = stt_service.transcribe_audio(audio_bytes, language)
        
        # Return response
        return TranscribeResponse(transcribed_text=transcribed_text)
    
    except ValueError as e:
        logger.error(f"Validation error in transcribe: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in transcribe: {e}")
        raise HTTPException(status_code=500, detail="Transcription failed internally.")

@translate_router.post("/translate", response_model=TranslateResponse, tags=["translation"])
async def translate_text(request: TranslateRequest):
    """
    Translates text from source language to target language using Cohere's model.
    """
    try:
        logger.info(f"Received translation request: {request.source_language} -> {request.target_language}, text length: {len(request.text)}")
        
        # Call translation service
        translated_text = translation_service.translate_text(request)
        
        # Return response (echo languages for confirmation)
        return TranslateResponse(
            translated_text=translated_text,
            source_language=request.source_language,
            target_language=request.target_language
        )
    
    except ValueError as e:
        logger.error(f"Validation error in translate: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in translate: {e}")
        raise HTTPException(status_code=500, detail="Translation failed internally.")