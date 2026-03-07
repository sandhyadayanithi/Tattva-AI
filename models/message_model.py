from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class MessageRecord(BaseModel):
    id: Optional[str] = Field(None, description="Firestore document ID")
    user_number: str = Field(..., description="WhatsApp user phone number")
    audio_file: Optional[str] = Field(None, description="Path or URL to the audio file")
    transcription: Optional[str] = Field(None, description="Whisper STT result")
    claim: Optional[str] = Field(None, description="Extracted claim for fact-checking")
    verdict: Optional[str] = Field(None, description="Fact-checking result (True, Related, False, etc.)")
    explanation: Optional[str] = Field(None, description="Brief explanation of the verdict")
    confidence: float = Field(0.0, description="AI confidence score for the verdict")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message processing timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "user_number": "1234567890",
                "audio_file": "audio/msg_001.mp3",
                "transcription": "Drinking lemon water cures everything.",
                "claim": "Lemon water cures all diseases.",
                "verdict": "False",
                "explanation": "Lemon water is healthy but doesn't cure all diseases.",
                "confidence": 0.95
            }
        }
