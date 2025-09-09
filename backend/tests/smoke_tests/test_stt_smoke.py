#!/usr/bin/env python3
"""
🧪 STT Service Smoke Test
Simple test script to validate that our STT service works with demo.wav
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

def load_demo_audio():
    """Load the demo.wav file as bytes"""
    demo_path = backend_dir / "demo.wav"
    
    if not demo_path.exists():
        raise FileNotFoundError(f"Demo audio file not found at: {demo_path}")
    
    print(f"Loading audio file: {demo_path}")
    with open(demo_path, "rb") as f:
        audio_bytes = f.read()
    
    print(f"Audio loaded successfully: {len(audio_bytes)} bytes")
    return audio_bytes

def test_stt_service():
    """Test the STT service with demo.wav"""
    try:
        # Import the STT service
        from app.services.stt_service import sst_service
        
        print("Testing STT Service...")
        print("-" * 50)
        
        # Load demo audio
        audio_bytes = load_demo_audio()
        
        # Test transcription
        print("Starting transcription...")
        transcribed_text = sst_service.transcribe_audio(
            audio_bytes=audio_bytes,
            language="en"  # Assuming English audio
        )
        
        print("Transcription completed!")
        print("-" * 50)
        print("Transcribed Text:")
        print(f"'{transcribed_text}'")
        print("-" * 50)
        print(f"Text length: {len(transcribed_text)} characters")
        
        # Basic validation
        if transcribed_text and len(transcribed_text.strip()) > 0:
            print("SMOKE TEST PASSED: STT service is working!")
            return True
        else:
            print("SMOKE TEST FAILED: No text transcribed")
            return False
            
    except Exception as e:
        print(f"SMOKE TEST FAILED: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    print("Starting STT Service Smoke Test")
    print("=" * 60)
    
    success = test_stt_service()
    
    print("=" * 60)
    if success:
        print("All tests passed! STT service is ready.")
        sys.exit(0)
    else:
        print("Tests failed! Check the error above.")
        sys.exit(1)
