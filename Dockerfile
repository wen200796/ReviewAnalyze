# 使用更小的基礎映像
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 安裝必要的系統依賴
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 複製 requirements.txt 並安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式的源代碼
COPY . .

# 暴露應用程式運行的端口
EXPOSE 8000

# 定義容器啟動時運行的命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
