from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import List, Dict
from app.api_models import TextInput, EmotionResult

class EmotionAnalyzer:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_path = "Johnson8187/Chinese-Emotion-Small"
        self.label_mapping = {
            0: "平淡語氣",
            1: "關切語調",
            2: "開心語調",
            3: "憤怒語調",
            4: "悲傷語調",
            5: "疑問語調",
            6: "驚奇語調",
            7: "厭惡語調"
        }
        self.tokenizer = None
        self.model = None

    def load_model(self):
        if self.tokenizer is None or self.model is None:
            print("正在載入模型...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path).to(self.device)
            print("模型載入完成！")

    def analyze_text(self, text: str) -> str:
        self.load_model()
        # 將文本轉換為模型輸入格式
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(self.device)
        
        # 進行預測
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # 取得預測結果
        predicted_class = torch.argmax(outputs.logits).item()
        return self.label_mapping[predicted_class]
    
    def analyze_batch(self, texts: List[TextInput]) -> List[EmotionResult]:
        results = []
        # 檢查 ID 是否重複
        id_set = set()
        for text_input in texts:
            if text_input.id in id_set:
                raise ValueError(f"重複的文本 ID: {text_input.id}")
            id_set.add(text_input.id)
            
            emotion = self.analyze_text(text_input.text)
            results.append(EmotionResult(
                id=text_input.id,
                emotion=emotion
            ))
        return results

# 創建全局實例
emotion_analyzer = EmotionAnalyzer()