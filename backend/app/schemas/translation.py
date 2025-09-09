from typing import Optional
from pydantic import BaseModel, Field

# ---------- Transcribe ----------
class TranscribeRequest(BaseModel):
    language: Optional[str] = Field(
        default=None,
        description="ISO-639-1 code of the spoken language (e.g. 'en'). Auto-detect if omitted."
    )

class TranscribeResponse(BaseModel):
    transcribed_text: str = Field(
        ..., 
        description="The text extracted from the audio file."
    )

# ---------- Translate ----------
class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to translate.")
    source_language: str = Field(
        ..., 
        regex=r"^[a-z]{2}$", 
        description="ISO-639-1 code of the source language (e.g. 'en')."
    )
    target_language: str = Field(
        ..., 
        regex=r"^[a-z]{2}$", 
        description="ISO-639-1 code of the target language (e.g. 'fr')."
    )

class TranslateResponse(BaseModel):
    translated_text: str = Field(..., description="Translated text.")
    source_language: str
    target_language: str