#!/usr/bin/env python3
"""
🌐 Translation Service Smoke Test
Simple test script to validate that our Translation service works with Cohere API
"""

import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

def test_translation_service():
    """Test the Translation service with various language pairs"""
    try:
        # Import the translation service and schema
        from app.services.translation_service import translation_service
        from app.schemas.translation import TranslateRequest
        
        print("Testing Translation Service...")
        print("-" * 60)
        
        # Test cases with different language pairs
        test_cases = [
            {
                "name": "English to French",
                "text": "Hello, my name is Amir Abdallah and today I want to share with you my plan to build an AI Translation App.",
                "source_language": "en",
                "target_language": "fr",
            },
            {
                "name": "English to Spanish", 
                "text": "Artificial Intelligence is transforming the world of technology.",
                "source_language": "en",
                "target_language": "es",
            },
            {
                "name": "English to Arabic",
                "text": "Machine learning helps computers learn from data.",
                "source_language": "en", 
                "target_language": "ar",
            }
        ]
        
        results = []
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nTest Case {i}: {test_case['name']}")
            print("=" * 40)
            
            # Create request
            request = TranslateRequest(
                text=test_case["text"],
                source_language=test_case["source_language"],
                target_language=test_case["target_language"]
            )
            
            print(f"Original Text ({test_case['source_language']}):")
            print(f"   '{test_case['text']}'")
            print()
            print(f"Translating to {test_case['target_language'].upper()}...")
            
            # Test translation
            translated_text = translation_service.translate_text(request)
            
            print(f"Translation completed!")
            print(f"Translated Text ({test_case['target_language']}):")
            print(f"   '{translated_text}'")
            print(f"Length: {len(translated_text)} characters")
            
            # Basic validation
            if translated_text and len(translated_text.strip()) > 0:
                results.append({"test": test_case['name'], "success": True, "output": translated_text})
                print("Test PASSED")
            else:
                results.append({"test": test_case['name'], "success": False, "error": "Empty translation"})
                print("Test FAILED: No translation received")
            
            print("-" * 40)
        
        # Summary
        print("\nTEST RESULTS SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for r in results if r["success"])
        total = len(results)
        
        for result in results:
            status = "PASS" if result["success"] else "FAIL"
            print(f"{status} - {result['test']}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("ALL TRANSLATION TESTS PASSED! Service is working perfectly!")
            return True
        else:
            print("Some translation tests failed!")
            return False
            
    except Exception as e:
        print(f"SMOKE TEST FAILED: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_edge_cases():
    """Test edge cases and error handling"""
    try:
        from app.services.translation_service import translation_service
        from app.schemas.translation import TranslateRequest
        
        print("\nTesting Edge Cases...")
        print("-" * 40)
        
        # Test with very short text
        print("Edge Case 1: Very short text")
        short_request = TranslateRequest(
            text="Hi",
            source_language="en",
            target_language="fr"
        )
        short_result = translation_service.translate_text(short_request)
        print(f"   Input: 'Hi' → Output: '{short_result}'")
        print("   Short text handled successfully")
        
        # Test with longer text
        print("\nEdge Case 2: Longer paragraph")
        long_text = """
        The field of artificial intelligence has evolved rapidly in recent years. 
        Machine learning algorithms can now process vast amounts of data and make 
        predictions with remarkable accuracy. This technology is being applied 
        across numerous industries, from healthcare to finance to transportation.
        """
        long_request = TranslateRequest(
            text=long_text.strip(),
            source_language="en",
            target_language="es"
        )
        long_result = translation_service.translate_text(long_request)
        print(f"   Input length: {len(long_text.strip())} chars")
        print(f"   Output length: {len(long_result)} chars")
        print("   Long text handled successfully")
        
        return True
        
    except Exception as e:
        print(f"   Edge case test failed: {e}")
        return False

if __name__ == "__main__":
    print("Starting Translation Service Smoke Test")
    print("=" * 70)
    
    # Test main functionality
    main_success = test_translation_service()
    
    # Test edge cases
    edge_success = test_edge_cases()
    
    print("\n" + "=" * 70)
    
    if main_success and edge_success:
        print("ALL TESTS PASSED! Translation service is production-ready!")
        sys.exit(0)
    else:
        print("Some tests failed! Check the errors above.")
        sys.exit(1)
