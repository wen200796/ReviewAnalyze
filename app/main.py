from fastapi import FastAPI, HTTPException, Depends, Header
from app.api_models import TextRequest, EmotionResponse
from app.service.emotion_analyze_service import emotion_analyzer
from app.analyze_auth import create_token, verify_token, record_usage, get_jwt_token, get_token_usage, change_token_status
import uvicorn

app = FastAPI(
    title="中文語句分析 API",
    description="分析中文語句，支援批量處理，目前可分析語句情感",
    version="1.0.0"
)

@app.get("/")
async def read_root():
    """根路徑處理程序"""
    return {"message": "歡迎使用中文語句分析 API"}

@app.post("/token")
async def generate_token(days: int, usage_limit: int):
    """
    生成短 token
    - days: token 的有效期（天）
    - usage_limit: token 的使用次數限制
    """
    if days > 7:  # 最多設置1周
        raise HTTPException(status_code=400, detail="Token expiration time cannot exceed 1 week")
    if usage_limit > 20:  # 最多設置20次
        raise HTTPException(status_code=400, detail="Usage limit cannot exceed 20")
    short_token = create_token(days, usage_limit)
    return {"token": short_token}

@app.get("/token/usage")
async def get_token_usage_api(short_token: str = Header(...)):
    """
    查詢 short token 的剩餘次數和到期日(utc)
    """
    usage_info = get_token_usage(short_token)
    return usage_info

@app.post("/token/status")
async def update_token_status(short_token: str, is_active: bool):
    """
    變更 token 的啟用狀態
    - short_token: 要變更的 token
    - is_active: 新的啟用狀態
    """
    try:
        change_token_status(short_token, is_active)
        return {"message": "Token status updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze", response_model=EmotionResponse)
async def analyze_text(request: TextRequest, short_token: str = Header(...)):
    """
    批量分析中文語句
    
    - 每個中文語句必須有唯一的 ID
    - 回傳結果只包含 ID 和對應的情感
    """
    jwt_token = get_jwt_token(short_token)
    verify_token(jwt_token)
    try:
        results = emotion_analyzer.analyze_batch(request.texts)
        record_usage(short_token)
        return EmotionResponse(results=results)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # 修改 uvicorn.run 配置
    uvicorn.run(app, host="0.0.0.0", port=8000)