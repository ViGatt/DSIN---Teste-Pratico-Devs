from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from src.infrastructure.database.database import get_db
from src.infrastructure.repositories.agendamento_repository import AgendamentoRepository

# Imports dos Casos de Uso
from src.application.use_cases.criar_agendamento import CriarAgendamentoUseCase
from src.application.use_cases.alterar_agendamento_cliente import AlterarAgendamentoClienteUseCase
from src.application.use_cases.alterar_agendamento_admin import AlterarAgendamentoAdminUseCase
from src.application.use_cases.obter_desempenho_semanal import ObterDesempenhoSemanalUseCase

# Imports dos Schemas
from src.presentation.schemas.agendamento_schema import (
    CriarAgendamentoRequest, 
    CriarAgendamentoResponse,
    AlterarAgendamentoClienteRequest, 
    AlterarAgendamentoAdminRequest,
    DashboardResponse
)

# A importação da classe mãe de erros facilita o tratamento
from src.domain.exceptions.agendamento_exceptions import DomainException 

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])

@router.post("/", response_model=CriarAgendamentoResponse, status_code=status.HTTP_200_OK)
def criar_agendamento(
    requisicao: CriarAgendamentoRequest,
    db: Session = Depends(get_db)  # FastAPI injeta a sessão do banco automaticamente aqui
):
    # Injeção de Dependências manual
    repository = AgendamentoRepository(db)
    use_case = CriarAgendamentoUseCase(repository)

    try:
        # Executa a nossa regra de negócio pura
        resultado = use_case.executar(
            cliente_id=requisicao.cliente_id,
            data_desejada=requisicao.data_desejada,
            servicos=requisicao.servicos,
            ignorar_sugestao=requisicao.ignorar_sugestao
        )

        # 3. Retorna a resposta empacotada
        # Se a ação for uma "SUGESTAO", o status HTTP continua sendo 200, 
        # pois não é um erro do servidor, é apenas um caminho alternativo .
        return CriarAgendamentoResponse(**resultado)

    except DomainException as e:
        # Qualquer erro de regra de negócio vira um Bad Request (400) para o Frontend.
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        # Erro genérico (ex: banco caiu)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor.")

@router.put("/{id_agendamento}/cliente")
def alterar_agendamento_cliente(
    id_agendamento: str,
    requisicao: AlterarAgendamentoClienteRequest,
    db: Session = Depends(get_db)
):
    repository = AgendamentoRepository(db)
    use_case = AlterarAgendamentoClienteUseCase(repository)
    
    try:
        # Capturamos a hora exata da requisição para a entidade calcular a regra de 48h
        data_atual = datetime.now(timezone.utc)
        resultado = use_case.executar(
            id_agendamento=id_agendamento,
            cliente_id_token=requisicao.cliente_id_token,
            nova_data=requisicao.nova_data,
            data_atual_requisicao=data_atual
        )
        return resultado
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{id_agendamento}/admin")
def alterar_agendamento_admin(
    id_agendamento: str,
    requisicao: AlterarAgendamentoAdminRequest,
    db: Session = Depends(get_db)
):
    repository = AgendamentoRepository(db)
    use_case = AlterarAgendamentoAdminUseCase(repository)
    
    try:
        resultado = use_case.executar(
            id_agendamento=id_agendamento,
            nova_data=requisicao.nova_data
        )
        return resultado
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/desempenho", response_model=DashboardResponse)
def obter_desempenho_semanal(
    data_referencia: datetime = None,
    db: Session = Depends(get_db)
):
    repository = AgendamentoRepository(db)
    use_case = ObterDesempenhoSemanalUseCase(repository)
    
    # Se o Frontend não mandar data específica, assume a data de hoje
    if not data_referencia:
        data_referencia = datetime.now(timezone.utc)
        
    try:
        resultado = use_case.executar(data_referencia)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao gerar relatório.")