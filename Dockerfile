# ---- Base Image ----
FROM python:3.11-slim

# ---- Set working directory ----
WORKDIR /app

# ---- Install system dependencies (optional, e.g. psycopg2, curl) ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---- Install Python dependencies ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy project files ----
COPY . .

# ---- Expose port ----
EXPOSE 8000

# ---- Run FastAPI with Uvicorn ----
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]