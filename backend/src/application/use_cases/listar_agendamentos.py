from datetime import datetime
from src.domain.interfaces.agendamento_repository import IAgendamentoRepository

class ListarAgendamentosUseCase:
    def __init__(self, repository: IAgendamentoRepository):
        self.repository = repository

    def executar(self, inicio: datetime, fim: datetime):
        agendamentos = self.repository.listar_agendamentos(inicio, fim)
        
        # Ordena para que os agendamentos mais próximos apareçam primeiro na tabela
        agendamentos.sort(key=lambda x: x.data_hora_agendada)
        return agendamentos