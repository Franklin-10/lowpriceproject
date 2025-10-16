# Usa uma base Debian (slim-bullseye) que é mais compatível com Playwright
FROM python:3.11.3-slim-bullseye
LABEL mantainer='franklin.oliveira096@gmail.com'

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /djangoapp

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-traditional \
    gosu \
    && rm -rf /var/lib/apt/lists/*

# Cria o ambiente virtual
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Copia apenas o requirements.txt primeiro para usar o cache do Docker
COPY djangoapp/requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- A CORREÇÃO FINAL ESTÁ AQUI ---
# Define um caminho de sistema para os navegadores, em vez de um caminho de usuário
ENV PLAYWRIGHT_BROWSERS_PATH=0

# Roda o comando do playwright para baixar o NAVEGADOR Chromium
RUN playwright install chromium --with-deps

# Copia os scripts e o resto do seu aplicativo
COPY scripts /scripts
COPY djangoapp .

# Cria o usuário não-root e ajusta as permissões
RUN useradd --system --create-home duser && \
    mkdir -p /data/web/static && \
    mkdir -p /data/web/media && \
    chown -R duser:duser /data \
    && chown -R duser:duser /djangoapp \
    && chmod -R 755 /scripts

USER root

#React

# Define o nosso novo script como o ponto de entrada
ENTRYPOINT ["/scripts/commands.sh"]

# Define o comando padrão, que será executado pelo entrypoint
CMD ["web"]