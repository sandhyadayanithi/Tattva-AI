from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any

class MessageRecord(BaseModel):
<<<<<<< HEAD
    id: Optional[str] = Field(None, description="Firestore document ID")
    user_number: str = Field(..., description="WhatsApp user phone number")
    audio_file: Optional[str] = Field(None, description="Path or URL to the audio file")
    image_file: Optional[str] = Field(None, description="Path or URL to the image file")
    transcription: Optional[str] = Field(None, description="Whisper STT result")
    claim: Optional[str] = Field(None, description="Extracted claim for fact-checking")
    verdict: Optional[str] = Field(None, description="Fact-checking result (True, Related, False, etc.)")
    explanation: Optional[str] = Field(None, description="Brief explanation of the verdict")
    confidence: float = Field(0.0, description="AI confidence score for the verdict (numeric)")
    confidence_level: Optional[str] = Field(None, description="AI confidence level (High, Medium, Low)")
    virality_score: int = Field(0, description="Virality risk score (1-10)")
    counter_message: Optional[str] = Field(None, description="Localized debunking message")
    evidence_used: Optional[list[str]] = Field(default_factory=list, description="List of evidence snippets used")
    language: Optional[str] = Field("English", description="Detected language of the claim")
    raw_fact_check_response: Optional[Dict[str, Any]] = Field(None, description="Complete JSON response from the fact-checker")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message processing timestamp")
=======
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
>>>>>>> 009a52ca1ffae4c2f23641b736d59688f7687a9b

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
