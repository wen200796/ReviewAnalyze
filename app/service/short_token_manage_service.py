from datetime import datetime

# 使用內存中的字典模擬資料庫
tokens_db = {}
usage_db = []

def add_token(short_token: str, jwt_token: str, is_active: bool):
    tokens_db[short_token] = {
        "jwt_token": jwt_token,
        "is_active": is_active,
        "created_at": datetime.utcnow()
    }

def get_token(short_token: str) -> dict:
    return tokens_db.get(short_token)

def change_token_status(short_token: str, is_active: bool):
    if short_token in tokens_db:
        tokens_db[short_token]["is_active"] = is_active
    else:
        raise ValueError("Token not found")

def add_usage(short_token: str):
    usage_db.append({"short_token": short_token, "timestamp": datetime.utcnow()})

def get_usage_count(short_token: str) -> int:
    return sum(1 for usage in usage_db if usage["short_token"] == short_token)
