# Imagem leve para rodar apenas o compilador
FROM python:3.11-alpine

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto para o contêiner
COPY . .

# Comando padrão ao rodar o contêiner (abre o demo interativo)
CMD ["python3", "demo.py"]
