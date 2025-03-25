# 中文語句分析 API

這是一個基於 FastAPI 的中文語句分析 API，支援批量處理，目前可分析語句情感。

## 功能

- 生成短 token
- 查詢 short token 的剩餘次數和到期日
- 變更 token 的啟用狀態
- 批量分析中文語句情感

## 安裝

### 使用虛擬環境

1. 克隆此專案到本地端：
    ```bash
    git clone <repository_url>
    cd ReviewAnalyze
    ```

2. 建立並啟動虛擬環境：
    ```bash
    python -m venv venv
    source venv/bin/activate  # 對於 Windows 使用 venv\Scripts\activate
    ```

3. 安裝所需的套件：
    ```bash
    pip install -r requirements.txt
    ```

### 使用 Docker

1. 克隆此專案到本地端：
    ```bash
    git clone <repository_url>
    cd ReviewAnalyze
    ```

2. 使用 Docker Compose 啟動服務：
    ```bash
    docker-compose up --build
    ```

## 使用

1. 啟動 FastAPI 伺服器：
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```

2. 使用瀏覽器或 API 客戶端（如 Postman）訪問 `http://localhost:8000`。

### API 端點

- `GET /` - 根路徑，顯示歡迎訊息
- `POST /token` - 生成短 token
- `GET /token/usage` - 查詢 short token 的剩餘次數和到期日
- `POST /token/status` - 變更 token 的啟用狀態
- `POST /analyze` - 批量分析中文語句情感

### 範例請求

#### 生成短 token

```http
POST /token
Content-Type: application/json

{
    "days": 7,
    "usage_limit": 20
}
```

#### 批量分析中文語句情感

```http
POST /analyze
Content-Type: application/json
short_token: <your_short_token>

{
    "texts": [
        {"id": "1", "text": "上菜速度超級慢，餐點少做，前也算錯"},
        {"id": "2", "text": "這是一家CP值很高的店，東西好吃價格不貴是我經常光顧的店家之一"}
    ]
}
```

## 環境變數

- `SECRET_KEY` - JWT 秘密金鑰（可選，預設為 `default_secret_key`）
