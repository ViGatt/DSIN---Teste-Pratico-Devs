from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.infrastructure.database.database import get_db
from src.infrastructure.repositories.agendamento_repository import AgendamentoRepository
from src.application.use_cases.criar_agendamento import CriarAgendamentoUseCase
from src.presentation.schemas.agendamento_schema import CriarAgendamentoRequest, CriarAgendamentoResponse

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