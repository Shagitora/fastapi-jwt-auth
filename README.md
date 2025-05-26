````markdown
# Auth через FastAPI с JWT согласно OAuth2

## Запуск

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/ваш-логин/fastapi-jwt-auth.git
cd fastapi-jwt-auth
````

### 2. Установите зависимости

```bash
pip install -r requirements.txt
```

### 3. Создайте `.env` файл

```env
SECRET_KEY=ваш_секретный_ключ
DATABASE_URL=sqlite:///./app.db
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_MINUTES=1440
```

### 4. Запустите сервер

```bash
uvicorn app.main:app --reload
```

Интерфейс Swagger будет доступен по адресу [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


