from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class CriarAgendamentoRequest(BaseModel):
    # REMOVIDO o cliente_id (Agora virá do token)
    data_desejada: datetime = Field(..., description="Data e hora exatas do agendamento em UTC")
    servicos: List[str] = Field(..., min_length=1, description="Lista contendo pelo menos um serviço")
    ignorar_sugestao: bool = Field(default=False, description="Flag para forçar o agendamento")

class CriarAgendamentoResponse(BaseModel):
    #Schema para padronizar a resposta de sucesso ou sugestão de agrupamento
    sucesso: bool
    mensagem: str
    acao_requerida: str | None = None
    data_sugerida: datetime | None = None
    agendamento_id: str | None = None

class AlterarAgendamentoClienteRequest(BaseModel):
    # REMOVIDO o cliente_id_token (Agora virá do token)
    nova_data: datetime = Field(..., description="Nova data desejada pelo cliente")

class AlterarAgendamentoAdminRequest(BaseModel):
    nova_data: datetime = Field(..., description="Nova data forçada pela administradora")

class DashboardResponse(BaseModel):
    periodo: dict
    agendamentos_por_dia: dict
    servicos_mais_buscados: list
    horarios_pico: list
    top_clientes: list

class AgendamentoItemResponse(BaseModel):
    id: str
    cliente_id: str
    data_hora_agendada: datetime
    servicos: list[str]
    status: str