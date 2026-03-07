from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any

class MessageRecord(BaseModel):
    id: Optional[str] = Field(None, description="Firestore document ID")
    audio_file: Optional[str] = Field(None, description="URL to the audio file")
    transcription: Optional[str] = Field(None, description="Whisper STT result")
    claim: Optional[str] = Field(None, description="Extracted claim for fact-checking")
    verdict: Optional[str] = Field(None, description="Fact-checking result")
    explanation: Optional[str] = Field(None, description="Detailed explanation of the verdict")
    counter_message: Optional[str] = Field(None, description="Short debunking message")
    confidence: float = Field(0.0, description="AI confidence score (0.0 to 1.0)")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message processing timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "audio_file": "audio_123.ogg",
                "transcription": "Drinking hot water cures dengue",
                "claim": "Hot water cures dengue",
                "verdict": "True",
                "explanation": "The evidence provided strongly and consistently supports the claim...",
                "confidence": 0.91,
                "timestamp": "2026-03-07T13:10:22"
            }
        }
