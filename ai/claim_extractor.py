import os
from google import genai
from google.genai import types

class ClaimExtractor:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set. Please set it in a .env file or environment.")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.5-flash"
    
    def extract_claim(self, transcription_text):
        """
        Extracts the core factual claim from the transcription text and translates it to English.
        """
        prompt = (
            "You are a fact-checking assistant for a WhatsApp bot. "
            "Your job is to read the following input transcription and extract the core factual claim(s) from it. "
            "Ignore opinions, greetings, or conversational filler. Extract only the factual statement being made.\n\n"
            "CRITICAL INSTRUCTION: No matter what language the input transcription is in, you MUST output the extracted claim translated into ENGLISH.\n\n"
            "Output the extracted claim as a single clear sentence. Provide no other text or explanation in your output.\n\n"
            f"Input transcription:\n{transcription_text}\n\n"
            "Extracted claim (in English):"
        )
        
        import time
        max_retries = 3
        retry_delay = 5 # Start with a longer delay for Free Tier

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                claim = response.text.strip()
                return claim
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    print(f"Quota exceeded (429) in ClaimExtractor. Retrying in {retry_delay}s... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    retry_delay *= 2 # Exponential backoff
                else:
                    print(f"Error calling Gemini API for claim extraction: {e}")
                    return None
