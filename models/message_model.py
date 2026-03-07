from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any

class MessageRecord(BaseModel):
    id: Optional[str] = Field(None, description="Firestore document ID")
    user_number: str = Field(..., description="WhatsApp user phone number")
    audio_file: Optional[str] = Field(None, description="Path or URL to the audio file")
    image_file: Optional[str] = Field(None, description="Path or URL to the image file")
    transcription: Optional[str] = Field(None, description="Whisper STT or OCR result")
    claim: Optional[str] = Field(None, description="Extracted claim for fact-checking")
    verdict: Optional[str] = Field(None, description="Fact-checking result (True, Related, False, etc.)")
    explanation: Optional[str] = Field(None, description="Brief explanation of the verdict")
    confidence: float = Field(0.0, description="AI confidence score for the verdict (numeric)")
    confidence_level: Optional[str] = Field(None, description="AI confidence level (High, Medium, Low)")
    virality_score: int = Field(0, description="Virality risk score (1-10)")
    counter_message: Optional[str] = Field(None, description="Localized debunking message")
    evidence_used: Optional[list[str]] = Field(default_factory=list, description="List of evidence snippets used")
    raw_fact_check_response: Optional[Dict[str, Any]] = Field(None, description="Complete JSON response from the fact-checker")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message processing timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "user_number": "919840899063",
                "audio_file": "audio_123.ogg",
                "transcription": "Drinking hot water cures dengue",
                "claim": "Hot water cures dengue",
                "fact_check": {
                    "verdict": "False",
                    "explanation": "No scientific evidence supports this...",
                    "counter_message": "Stay hydrated, but hot water is not a cure for dengue.",
                    "confidence": 0.8,
                    "virality_score": 7,
                    "cached": False
                },
                "ai_response": {
                    "verdict_en": "False",
                    "explanation_en": "...",
                    "counter_message_en": "..."
                },
                "timestamp": "2026-03-07T13:10:22"
            }
        }
