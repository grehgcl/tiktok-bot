FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir playwright streamlit pandas plotly python-dotenv
RUN playwright install chromium
RUN playwright install-deps

WORKDIR /app
COPY . .

EXPOSE 8501

CMD streamlit run app.py --server.port=8501 --server.address=0.0.0.0