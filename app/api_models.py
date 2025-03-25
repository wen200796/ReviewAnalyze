from pydantic import BaseModel, Field
from typing import List

class TextInput(BaseModel):
    id: str
    text: str

class TextRequest(BaseModel):
    texts: List[TextInput]

class EmotionResult(BaseModel):
    id: str
    emotion: str

class EmotionResponse(BaseModel):
    results: List[EmotionResult] 