from tavily import TavilyClient
import os
import json
from dotenv import load_dotenv
from google import genai
from services.vector_service import vector_service
from utils.logger import logger

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

class FactCheckerEngine:
    def __init__(self, use_llm=True):
        from tavily import TavilyClient
        self.tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        self.use_llm = use_llm
        if self.use_llm:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                logger.error("GEMINI_API_KEY not set")
                self.use_llm = False
            else:
                self.client = genai.Client(api_key=api_key)
                self.model_name = "gemini-2.5-flash"

    def check_claim(self, claim, language="English"):
        """Main entry point. Checks semantic cache before running full pipeline."""
        if not claim:
            logger.error("Claim is empty or None. Fact-checking bypassed.")
            return {
                "verdict": "Uncertain",
                "category": "general",
                "explanation_en": "No clear claim was identified to fact-check.",
                "explanation_reg": "No clear claim was identified to fact-check.",
                "virality_score": 0,
                "virality_reason_en": "No actionable claim found.",
                "virality_reason_reg": "No actionable claim found.",
                "counter_message_en": "Could you please explain what you want me to check?",
                "counter_message_reg": "Could you please explain what you want me to check?",
                "cached": False,
                "evidence_used": []
            }
        # 1. Pipeline check: See if similar claim already exists in Vector DB
        logger.info(f"Checking semantic cache for: {claim}")
        similar_claim = vector_service.find_similar_claim(claim)
        
        if similar_claim:
            logger.info(f"Pipeline hit: Similar claim found in semantic cache.")
            return {
                **similar_claim,
                "cached": True
            }

        # 2. Else: Run full fact-check pipeline via external API
        logger.info(f"Cache miss. Running full fact-check via external Search and LLM.")
        evidence = self.search_evidence(claim)
        result = self.generate_verdict(claim, evidence, language)
        
        # 3. Store result in Vector Cache for future hits
        vector_service.store_claim(
            claim_text=claim, 
            fact_check_result=result
        )
            
        result["cached"] = False
        result["evidence_used"] = evidence
        return result

    def search_evidence(self, claim):
        """Retrieves evidence using Tavily."""
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key or not api_key.startswith("tvly-"):
             logger.error("Invalid Tavily API Key format. Expected starting with 'tvly-'.")
             return ["Error: Invalid Tavily API Key. Please provide a valid key from tavily.com."]

        try:
            response = self.tavily.search(
                query=claim,
                search_depth="advanced",
                max_results=5
            )
            # Deduplicate and truncate snippets to 500 chars each
            snippets = list({e["content"][:500] for e in response["results"]})
            return snippets
        except Exception as e:
            logger.error(f"Tavily Search Error: {e}")
            return [f"Error searching for evidence: {e}"]

    def generate_verdict(self, claim, evidence, language="English"):
        """Uses Gemini to evaluate claim against evidence (if enabled)."""
        if not self.use_llm:
            return {
                "verdict": "Uncertain (LLM Disabled)",
                "confidence_level": "Low",
                "virality_score": 0,
                "counter_message": "[MOCK] LLM Fact Checking is disabled to save credits.",
                "explanation": "Fact-checking bypassed."
            }

        evidence_text = "\n".join(evidence)

        prompt = f"""
        You are a professional fact checker.

        Claim:
        {claim}

        Evidence:
        {evidence_text}

        Determine the validity of the claim based on the evidence.
        
        Rules:
        1. The verdict must be ONLY one of the following: TRUE or FALSE.
        2. Provide a short plain-language explanation in both English and {language}.
        3. Assign a Virality Risk Score (1-10) based on linguistic cues: emotional language, urgency, conspiracy framing, authority claims, or encouragement to forward.
        4. Provide a short reason explaining the virality score in both English and {language}.
        5. Classify the claim into ONE of these categories: health, election, religion, finance.
        6. Generate a "Suggested Counter Message" ONLY if the verdict is FALSE. This message must be short, clear, WhatsApp-friendly, and written in the same language as the original claim/detected language.

        Return ONLY in this precise JSON format, without any markdown formatting wrappers:

        {{
          "verdict": "TRUE or FALSE",
          "category": "health or election or religion or finance",
          "explanation_en": "short explanation in English",
          "explanation_reg": "short explanation in {language}",
          "virality_score": 0,
          "virality_reason_en": "reason for virality score in English",
          "virality_reason_reg": "reason for virality score in {language}",
          "counter_message_en": "short counter message in English (null if TRUE)",
          "counter_message_reg": "short counter message in {language} (null if TRUE)"
        }}
        """
        import time
        max_retries = 3
        retry_delay = 5 # Increased initial delay for Free Tier stability

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                content = response.text
                break # Success, exit retry loop
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    logger.warning(f"Quota exceeded (429). Retrying in {retry_delay}s... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    retry_delay *= 2 # Exponential backoff
                else:
                    logger.error(f"Error calling Gemini for verdict: {e}")
                    return {
                        "verdict": "FALSE", # Default to false for safety if error
                        "category": "health", # Default
                        "explanation_en": f"API Error: {e}",
                        "explanation_reg": f"API பிழை: {e}",
                        "virality_score": 5,
                        "virality_reason_en": "Service capacity limit reached.",
                        "virality_reason_reg": "சேவை திறன் வரம்பை எட்டியது.",
                        "counter_message_en": "Service is currently unstable. Please try again later.",
                        "counter_message_reg": "சேவை தற்போது நிலையற்றதாக உள்ளது. பிறகு முயற்சிக்கவும்."
                    }

        clean_content = content.strip()
        if clean_content.startswith("```json"):
            clean_content = clean_content[7:]
        if clean_content.startswith("```"):
            clean_content = clean_content[3:]
        if clean_content.endswith("```"):
            clean_content = clean_content[:-3]
        clean_content = clean_content.strip()

        try:
            verdict_json = json.loads(clean_content)
        except json.JSONDecodeError:
            verdict_json = {
                "verdict": "FALSE",
                "category": "health",
                "explanation_en": "Failed to parse JSON response.",
                "explanation_reg": "பதிலைச் செயல்படுத்த முடியவில்லை.",
                "virality_score": 5,
                "virality_reason_en": "System parsing error.",
                "virality_reason_reg": "அமைப்பு பிழை.",
                "counter_message_en": "An error occurred while processing the result.",
                "counter_message_reg": "முடிவைச் செயலாக்குவதில் பிழை ஏற்பட்டது."
            }
        return verdict_json

# Example usage for testing the pipeline
if __name__ == "__main__":
    from services.vector_service import initialize_vector_db
    initialize_vector_db() # Ensure DB is ready
    
    engine = FactCheckerEngine()
    test_claim = "Drinking hot lemon water cures all forms of cancer."
    print(f"Checking claim: {test_claim}")
    result = engine.check_claim(test_claim)
    print(json.dumps(result, indent=2, ensure_ascii=False))
