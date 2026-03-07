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
    
    # Nested sections
    fact_check: Dict[str, Any] = Field(default_factory=dict, description="Processed fact-check result for application use")
    ai_response: Dict[str, Any] = Field(default_factory=dict, description="Raw AI response for debugging")
    
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
