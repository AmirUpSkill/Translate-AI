import logging
from typing import Optional
from io import BytesIO
from groq import Groq
from ..core.config import settings
from fastapi import HTTPException
# --- Setup logging --- 
logger = logging.getLogger(__name__)
# ---- Main Class ---
class STTService:
    """
        Servivce for Speech-to-Text transcription using Groq's Whisper Model . 
    """
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)
        self.model="whisper-large-v3-turbo"
    def transcribe_audio(self, audio_bytes: bytes, language: Optional[str] = None) -> str:
        """
        Transcribes audio bytes to text using Groq API.
        
        Args:
            audio_bytes (bytes): Raw audio data (e.g., WAV/MP3 from upload).
            language (Optional[str]): ISO-639-1 code (e.g., 'en') for language hint.
        
        Returns:
            str: Transcribed text.
        
        Raises:
            ValueError: If audio_bytes is empty.
            HTTPException: If Groq API fails (status 500).
        """
        # --- Validate input ---
        if not audio_bytes:
            logger.error("Empty audio data provided for transcription.")
            raise ValueError("Audio data cannot be empty.")
        try:
            logger.info(f"Starting transcription for audio (length : {len(audio_bytes)} bytes ) , language : {language}")

            # --- Create file-like object from bytes --- 
            audio_file = BytesIO(audio_bytes)
            audio_file.name = "audio.wav"  

            # --- Call Groq API --- 
            transcription = self.client.audio.transcriptions.create(
                file=audio_file,
                model=self.model,
                language=language, 
                response_format="verbose_json",
            )
            transcribed_text = transcription.text.strip()
            logger.info(f"Transcription completed successfully. Text length: {len(transcribed_text)}")
            return transcribed_text
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise HTTPException(status_code=500, detail="Transcription failed.")
# --- Instance of this Service --- 
sst_service = STTService()
