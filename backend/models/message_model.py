from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any

class MessageRecord(BaseModel):
    transcript: str = Field(..., description="The original transcription or OCR text")
    claim: str = Field(..., description="The extracted claim")
    verdict: str = Field(..., description="TRUE or FALSE")
    explanation: str = Field(..., description="Simplified fact-check explanation")
    virality_score: int = Field(..., description="Virality score (1-10)")
    virality_reason: str = Field(..., description="Explanation for the virality score")
    counter_message: Optional[str] = Field(None, description="Suggested counter message (if FALSE)")
    language: str = Field(..., description="Detected language")
    category: str = Field(..., description="Claim category (health, election, religion, finance)")
    created_at: datetime = Field(default_factory=datetime.now, description="Firestore timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "transcript": "Drinking hot water cures dengue",
                "claim": "Hot water cures dengue",
                "verdict": "FALSE",
                "explanation": "No scientific evidence supports this...",
                "virality_score": 7,
                "virality_reason": "High emotional language and medical misinformation.",
                "counter_message": "Stay hydrated, but hot water is not a cure for dengue.",
                "language": "English",
                "category": "health",
                "created_at": "2026-03-08T04:53:24"
            }
        }
