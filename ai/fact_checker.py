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
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel("gemini-2.5-flash")

    def check_claim(self, claim):
        """Main entry point. Checks semantic cache before running full pipeline."""
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
        result = self.generate_verdict(claim, evidence)
        
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

    def generate_verdict(self, claim, evidence):
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
        Evaluate the claim for the following:
        1. Verdict: True, False, or Uncertain
        2. Confidence Score: A floating point number between 0.0 and 1.0 (e.g., 0.91).
        3. Virality Risk Score: 1-10 based on how emotionally charged and shareable the claim is.
        4. Explanation: A detailed, consistent synthesis of the evidence supporting the verdict.
        5. Counter-message: A short, WhatsApp-friendly debunking message in the SAME language as the original claim.

        Return ONLY in this precise JSON format, without any markdown formatting wrappers:

        {{
          "verdict": "",
          "confidence_score": 0.0,
          "virality_score": 0,
          "explanation": "",
          "counter_message": ""
        }}
        """
        import time
        max_retries = 3
        retry_delay = 5 # Increased initial delay for Free Tier stability

        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
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
                        "verdict": "Uncertain",
                        "confidence_level": "Low",
                        "virality_score": 5,
                        "counter_message": "Service reached its capacity limit. Please try again in 1 minute.",
                        "explanation": f"API Error: {e}"
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
                "verdict": "Uncertain",
                "confidence_score": 0.0,
                "virality_score": 5,
                "explanation": "Failed to parse JSON: " + content,
                "counter_message": "We could not verify this claim due to a system error."
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
    print(json.dumps(result, indent=2))
