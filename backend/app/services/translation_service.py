import logging
from typing import Optional
from cohere import ClientV2
from ..core.config import settings
from ..schemas.translation import TranslateRequest 

# --- SetUp Logging --- 
logger = logging.getLogger(__name__)
# --- Main Class ---
class TranslationService:
    """
        Service for text translation using Cohere API
    """ 
    def __init__(self):
        self.client = ClientV2(api_key=settings.cohere_api_key)
        self.model = "command-a-translate-08-2025"
        self.temperature = 0.3 
    def translate_text(self, request: TranslateRequest) -> str:
        """
        Translates text from source to target language using Cohere API.
        
        Args:
            request (TranslateRequest): Validated request with text, source_language, target_language.
        
        Returns:
            str: Translated text.
        
        Raises:
            ValueError: If text is empty.
            HTTPException: If Cohere API fails (status 500).
        """
        text = request.text.strip()
        source_lang = request.source_language
        target_lang = request.target_language
        if not text:
            raise ValueError("Text cannot be empty.")
        try:
            logger.info(f"Starting translation from {source_lang} to {target_lang} (text length: {len(text)})")
            # --- Using Cohere API Example --- 
            messages = [
                {
                    "role": "system",
                    "content": f"Translate this to {target_lang}."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": text
                        }
                    ]
                }
            ]
            # --- One Shot Translation --- 
            response = self.client.chat(
                messages=messages,
                temperature=self.temperature,
                model=self.model,
            )
            translated_text = response.message.content[0].text.strip()
            logger.info(f"Translation successful: {translated_text[:50]}...")
            return translated_text
        except Exception as e:
            logger.error(f"Translation API error: {str(e)}")
            from fastapi import HTTPException
            raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

translation_service = TranslationService()