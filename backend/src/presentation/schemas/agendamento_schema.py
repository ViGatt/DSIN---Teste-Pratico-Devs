from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class CriarAgendamentoRequest(BaseModel):
    # Schema para validar os dados que chegam do Frontend no momento da criação
    cliente_id: str = Field(..., description="ID do cliente logado (vindo do token do Clerk)")
    data_desejada: datetime = Field(..., description="Data e hora exatas do agendamento em UTC")
    servicos: List[str] = Field(..., min_length=1, description="Lista contendo pelo menos um serviço")
    ignorar_sugestao: bool = Field(default=False, description="Flag para forçar o agendamento ignorando o agrupamento")

class CriarAgendamentoResponse(BaseModel):
    #Schema para padronizar a resposta de sucesso ou sugestão de agrupamento
    sucesso: bool
    mensagem: str
    acao_requerida: str | None = None
    data_sugerida: datetime | None = None
    agendamento_id: str | None = None