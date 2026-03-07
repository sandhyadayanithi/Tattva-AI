from tavily import TavilyClient
import os
import json
import sqlite3
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

class FactCheckerEngine:
    def __init__(self, db_path="claims_cache.db"):
        self.tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        self.genai_client = genai.Client()
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database for claim caching."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS claim_cache (
                    claim TEXT PRIMARY KEY,
                    verdict TEXT,
                    confidence_level TEXT,
                    virality_score INTEGER,
                    counter_message TEXT,
                    explanation TEXT
                )
            ''')

    def check_claim(self, claim):
        """Main entry point. Checks cache before running full pipeline."""
        # Check cache first
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT verdict, confidence_level, virality_score, counter_message, explanation FROM claim_cache WHERE claim = ?", 
                (claim,)
            )
            row = cursor.fetchone()
            if row:
                return {
                    "verdict": row[0],
                    "confidence_level": row[1],
                    "virality_score": row[2],
                    "counter_message": row[3],
                    "explanation": row[4],
                    "cached": True
                }

        # If not in cache, run full pipeline
        evidence = self.search_evidence(claim)
        result = self.generate_verdict(claim, evidence)
        
        # Save to cache
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO claim_cache (claim, verdict, confidence_level, virality_score, counter_message, explanation) VALUES (?, ?, ?, ?, ?, ?)",
                (claim, result.get("verdict"), result.get("confidence_level"), result.get("virality_score"), result.get("counter_message"), result.get("explanation"))
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
        """Uses Gemini to evaluate claim against evidence."""
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

if __name__ == "__main__":
    engine = FactCheckerEngine()
    
    print("Welcome to the Fact-Checker Engine!")
    
    claim = input("Enter a claim to fact-check: ")
        
    print("Checking...")
    result = engine.check_claim(claim)
    
    # Remove evidence_used from output to keep terminal clean
    output_result = {k: v for k, v in result.items() if k != "evidence_used"}
    print(json.dumps(output_result, indent=2))
    print("\n" + "-"*40 + "\n")