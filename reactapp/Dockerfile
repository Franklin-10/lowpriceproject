# Usa uma imagem oficial do Node.js, leve e baseada em Alpine
FROM node:20-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de definição de dependências
COPY package*.json ./

# Instala as dependências do projeto
RUN npm install

# Copia o resto do código-fonte do React
COPY . .

# Expõe a porta que o Vite usa para o servidor de desenvolvimento
EXPOSE 3000

# O comando para iniciar o servidor de desenvolvimento do Vite
CMD ["npm", "run", "dev"]