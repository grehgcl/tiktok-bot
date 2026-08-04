FROM python:3.11-slim

# Define o diretório de trabalho primeiro
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    unzip \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Instala o Chrome (método atualizado sem apt-key)
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /etc/apt/trusted.gpg.d/google.gpg \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Copia o requirements.txt primeiro (para aproveitar cache)
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código
COPY . .

EXPOSE 8501

CMD streamlit run app.py --server.port=8501 --server.address=0.0.0.0