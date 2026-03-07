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
        self.tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        self.use_llm = use_llm
        if self.use_llm:
            self.genai_client = genai.Client()

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
            verdict=result.get("verdict"), 
            explanation=result.get("explanation")
        )
            
        result["cached"] = False
        result["evidence_used"] = evidence
        return result

    def search_evidence(self, claim):
        """Retrieves evidence using Tavily."""
        response = self.tavily.search(
            query=claim,
            search_depth="advanced",
            max_results=5
        )
        # Deduplicate and truncate snippets to 500 chars each
        snippets = list({e["content"][:500] for e in response["results"]})
        return snippets

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
        2. Confidence Level: High, Medium, or Low
        3. Virality Risk Score: 1-10 based on how emotionally charged and shareable the claim is.
        4. Counter-message: A short, WhatsApp-friendly debunking message in the SAME language as the original claim.

        Return ONLY in this precise JSON format, without any markdown formatting wrappers:

        {{
          "verdict": "",
          "confidence_level": "",
          "virality_score": 0,
          "counter_message": "",
          "explanation": ""
        }}
        """
        response = self.genai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        content = response.text
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
                "confidence_level": "Low",
                "virality_score": 5,
                "counter_message": "We could not verify this claim due to a system error.",
                "explanation": "Failed to parse JSON: " + content
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
