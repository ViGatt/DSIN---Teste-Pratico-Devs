from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.database.database import criar_banco_de_dados
from src.presentation.routers import agendamento_router

# vai gerar o arquivo "salao_da_leila.db" na primeira vez que rodar
criar_banco_de_dados()

app = FastAPI(
    title="API - Salão da Leila",
    description="Backend do sistema de agendamentos",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, mudar para a URL exata do React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agendamento_router.router)