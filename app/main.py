from fastapi import FastAPI
from app.routes import auth

app = FastAPI(
    title='User Management API',
    description="API para gerenciamento de doaçoes",
    version='1.1.0'
)

app.include_router(auth.router, prefix='/user', tags=['users'])


@app.get('/')
def health_check():
    return {"msg": 'bem vindo'}
