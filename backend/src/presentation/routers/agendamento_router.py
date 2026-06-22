from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from src.application.use_cases.listar_agendamentos import ListarAgendamentosUseCase
from src.presentation.schemas.agendamento_schema import AgendamentoItemResponse
from datetime import timedelta

from src.infrastructure.database.database import get_db
from src.infrastructure.repositories.agendamento_repository import AgendamentoRepository
from src.infrastructure.security.auth import obter_usuario_logado, obter_admin_logado

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
    db: Session = Depends(get_db),  # FastAPI injeta a sessão do banco automaticamente aqui
    cliente_id_token: str = Depends(obter_usuario_logado) # NOVO: Extrai o ID direto do Header!
):
    # Injeção de Dependências manual
    repository = AgendamentoRepository(db)
    use_case = CriarAgendamentoUseCase(repository)

    try:
        # Executa a nossa regra de negócio pura
        resultado = use_case.executar(
            cliente_id=cliente_id_token, # NOVO: Usando o ID inviolável do token
            data_desejada=requisicao.data_desejada,
            servicos=requisicao.servicos,
            ignorar_sugestao=requisicao.ignorar_sugestao
        )

        # Retorna a resposta empacotada
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
    db: Session = Depends(get_db),
    cliente_id_token: str = Depends(obter_usuario_logado) #Cadeado na alteração
):
    repository = AgendamentoRepository(db)
    use_case = AlterarAgendamentoClienteUseCase(repository)
    
    try:
        # Pega a hora exata da requisição para a entidade calcular a regra de 48h
        data_atual = datetime.now(timezone.utc)
        resultado = use_case.executar(
            id_agendamento=id_agendamento,
            cliente_id_token=cliente_id_token, # Já usando o ID inviolável
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
    db: Session = Depends(get_db),
    admin_id: str = Depends(obter_admin_logado) # CADEADO APLICADO
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
    db: Session = Depends(get_db),
    admin_id: str = Depends(obter_admin_logado) # CADEADO APLICADO
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
    
@router.get("/", response_model=list[AgendamentoItemResponse])
def listar_agendamentos(
    inicio: datetime = None,
    fim: datetime = None,
    db: Session = Depends(get_db),
    admin_id: str = Depends(obter_admin_logado) # CADEADO DA LEILA ATIVADO
):
    repository = AgendamentoRepository(db)
    use_case = ListarAgendamentosUseCase(repository)
    
    # Se não filtrar por data, mostramos os últimos 7 dias e os próximos 30
    if not inicio:
        inicio = datetime.now(timezone.utc) - timedelta(days=7)
    if not fim:
        fim = datetime.now(timezone.utc) + timedelta(days=30)
        
    try:
        agendamentos = use_case.executar(inicio, fim)
        
        # Mapeia as Entidades para o Schema do Pydantic
        return [
            {
                "id": ag.id,
                "cliente_id": ag.cliente_id,
                "data_hora_agendada": ag.data_hora_agendada,
                "servicos": ag.servicos,
                "status": ag.status
            }
            for ag in agendamentos
        ]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao listar: {str(e)}")

@router.delete("/{id_agendamento}/admin", status_code=status.HTTP_204_NO_CONTENT)
def cancelar_agendamento_forcado(
    id_agendamento: str,
    db: Session = Depends(get_db),
    admin_id: str = Depends(obter_admin_logado)
):
    repository = AgendamentoRepository(db)
    agendamento = repository.buscar_por_id(id_agendamento)
    
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")
        
    # SOFT DELETE: Apenas mudamos o status em vez de apagar do banco
    agendamento.status = "CANCELADO"
    repository.salvar(agendamento)
    
    return None

@router.patch("/{id_agendamento}/restaurar/admin", status_code=status.HTTP_200_OK)
def restaurar_agendamento(
    id_agendamento: str,
    db: Session = Depends(get_db),
    admin_id: str = Depends(obter_admin_logado)
):
    repository = AgendamentoRepository(db)
    agendamento = repository.buscar_por_id(id_agendamento)
    
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")
        
    # RESTAURAR: Volta o status para pendente
    agendamento.status = "PENDENTE"
    repository.salvar(agendamento)
    
    return {"message": "Agendamento restaurado com sucesso."}

@router.get("/meus", response_model=list[AgendamentoItemResponse])
def listar_meus_agendamentos(
    db: Session = Depends(get_db),
    cliente_id: str = Depends(obter_usuario_logado) # CADEADO DO CLIENTE COMUM
):
    repository = AgendamentoRepository(db)
    agendamentos = repository.listar_por_cliente(cliente_id)
    
    return [
        {
            "id": ag.id,
            "cliente_id": ag.cliente_id,
            "data_hora_agendada": ag.data_hora_agendada,
            "servicos": ag.servicos,
            "status": ag.status
        }
        for ag in agendamentos
    ]

@router.patch("/{id_agendamento}/confirmar/admin", status_code=status.HTTP_200_OK)
def confirmar_agendamento(
    id_agendamento: str,
    db: Session = Depends(get_db),
    admin_id: str = Depends(obter_admin_logado)
):
    repository = AgendamentoRepository(db)
    agendamento = repository.buscar_por_id(id_agendamento)
    
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")
        
    if agendamento.status == "CANCELADO":
        raise HTTPException(status_code=400, detail="Não é possível confirmar um agendamento cancelado.")
        
    agendamento.status = "CONFIRMADO"
    repository.salvar(agendamento)
    
    return {"message": "Agendamento confirmado com sucesso."}