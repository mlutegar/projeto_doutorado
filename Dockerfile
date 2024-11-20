# Use uma imagem base do Python
FROM python:3.12-slim

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie o arquivo de dependências (requirements.txt) para o container
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código para o container
COPY . .

# Exponha a porta em que o Flask irá rodar (geralmente 5000)
EXPOSE 5000

# Comando para iniciar o aplicativo Flask
CMD ["python", "main.py"]
