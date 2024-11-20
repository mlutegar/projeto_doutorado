# Doutorado - Back End

## Deploy

Para fazer o deploy do back end, siga os passos abaixo:
```bash
docker build -t mlutegar/doutoradov1:v3 .
docker run -d -p 5000:5000 mlutegar/doutoradov1:v3
```

Enviar para o Docker Hub:
```bash
docker push mlutegar/doutoradov1:v4
```


## Executar

Para executar o back end, siga os passos abaixo:

Para instalar as dependências, execute o comando abaixo:

```bash
pip install -r requirements.txt
```

Para iniciar o servidor, execute o comando abaixo:

```bash
flask --app flaskr run --debug
```

Rode o comando abaixo para criar o banco de dados:

```bash
flask --app flaskr init-db
```