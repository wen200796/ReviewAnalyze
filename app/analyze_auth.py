import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import secrets
import string
import os
from app.service.short_token_manage_service import add_token, get_token, add_usage, get_usage_count
from app.service.short_token_manage_service import change_token_status as change_status

JWT_SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = "HS256"

security = HTTPBearer()

def generate_short_token(length=8):
    characters = string.ascii_letters + string.digits
    while True:
        short_token = ''.join(secrets.choice(characters) for _ in range(length))
        if not get_token(short_token):
            return short_token

def create_token(days: int, usage_limit: int):
    short_token = generate_short_token()  # 生成短的隨機字串
    expiration = datetime.utcnow() + timedelta(days=days)
    jwt_token = jwt.encode({"short_token": short_token, "exp": expiration, "usage_limit": usage_limit}, JWT_SECRET_KEY, algorithm=ALGORITHM)
    add_token(short_token, jwt_token, True)
    return short_token

def get_jwt_token(short_token: str) -> str:
    token_data = get_token(short_token)
    if not token_data or not token_data["is_active"]:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token_data["jwt_token"]

def get_remaining_usage(short_token: str, usage_limit: int) -> int:
    usage_count = get_usage_count(short_token)
    return usage_limit - usage_count

def verify_token(jwt_token: str):
    try:
        payload = jwt.decode(jwt_token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        short_token = payload.get("short_token")
        usage_limit = payload.get("usage_limit")
        token_data = get_token(short_token)
        if not token_data or not token_data["is_active"]:
            raise HTTPException(status_code=401, detail="Invalid token")
        remaining_usage = get_remaining_usage(short_token, usage_limit)
        if (remaining_usage <= 0):
            raise HTTPException(status_code=403, detail="Usage limit exceeded")
        return short_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def record_usage(short_token: str):
    token_data = get_token(short_token)
    if token_data and token_data["is_active"]:
        add_usage(short_token)

def get_token_usage(short_token: str):
    try:
        token_data = get_token(short_token)
        if not token_data or not token_data["is_active"]:
            raise HTTPException(status_code=401, detail="Invalid token")
        jwt_token = get_jwt_token(short_token)
        payload = jwt.decode(jwt_token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        usage_limit = payload.get("usage_limit")
        expiration = payload.get("exp")
        remaining_usage = get_remaining_usage(short_token, usage_limit)
        return {
        "remaining_usage": remaining_usage,
        "expiration": datetime.utcfromtimestamp(expiration).strftime('%Y-%m-%d %H:%M:%S')
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def change_token_status(short_token: str, is_active: bool):
    token_data = get_token(short_token)
    if not token_data:
        raise HTTPException(status_code=404, detail="Token not found")
    change_status(short_token, is_active)
