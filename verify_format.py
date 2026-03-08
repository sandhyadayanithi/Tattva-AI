import os
import json
import asyncio
from ai.fact_checker import FactCheckerEngine
from dotenv import load_dotenv

load_dotenv()

async def verify():
    engine = FactCheckerEngine()
    
    # Test case 1: False claim
    false_claim = "Drinking hot lemon water cures all forms of cancer."
    print(f"\nTesting FALSE claim: {false_claim}")
    result_false = engine.check_claim(false_claim)
    print(json.dumps(result_false, indent=2, ensure_ascii=False))
    
    # Test case 2: True claim
    true_claim = "The Earth revolves around the Sun."
    print(f"\nTesting TRUE claim: {true_claim}")
    result_true = engine.check_claim(true_claim)
    print(json.dumps(result_true, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(verify())
