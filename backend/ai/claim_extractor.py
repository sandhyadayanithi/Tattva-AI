import os
from google import genai

class ClaimExtractor:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.5-flash"
    
    def extract_claim(self, transcription):
        """
        Extracts the core factual claim from the transcription text and translates it to English.
        Also detects the original language of the transcription.
        Returns a dict: {"claim": "English claim", "language": "Detected Language Name"}
        """
        prompt = (
            "You are a fact-checking assistant for a WhatsApp bot. "
            "Your job is to read the following input transcription and extract the core factual claim(s) from it. "
            "Ignore opinions, greetings, or conversational filler. Extract only the factual statement being made.\n\n"
            "CRITICAL INSTRUCTIONS:\n"
            "1. Output the extracted claim translated into ENGLISH.\n"
            "2. Detect the original language of the input transcription (e.g., 'Tamil', 'Hindi', 'English', 'Bengali').\n"
            "3. Return the results ONLY in the following JSON format:\n"
            "{\n"
            "  \"claim\": \"The extracted claim in English\",\n"
            "  \"language\": \"The name of the detected language\"\n"
            "}\n\n"
            f"Input transcription:\n{transcription}\n\n"
            "JSON Output:"
        )
        
        import time
        import json
        max_retries = 3
        retry_delay = 5 # Start with a longer delay for Free Tier

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                content = response.text.strip()
                
                # Cleanup JSON formatting if present
                if content.startswith("```json"):
                    content = content[7:]
                if content.startswith("```"):
                    content = content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                content = content.strip()
                
                result = json.loads(content)
                return {
                    "claim": result.get("claim", "").strip(),
                    "language": result.get("language", "English").strip()
                }
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    print(f"Quota exceeded (429) in ClaimExtractor. Retrying in {retry_delay}s... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    retry_delay *= 2 # Exponential backoff
                else:
                    print(f"Error calling Gemini API for claim extraction: {e}")
                    # Fallback for manual parsing or simple failure
                    return {"claim": None, "language": "English"}
