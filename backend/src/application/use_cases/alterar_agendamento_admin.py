from datetime import datetime
from src.domain.interfaces.agendamento_repository import IAgendamentoRepository

class AlterarAgendamentoAdminUseCase:
    def __init__(self, agendamento_repository: IAgendamentoRepository):
        self.repository = agendamento_repository

    # Não tem 'cliente_id_token' e nem 'data_atual_requisicao' porque a Leila pode alterar tudo.
    def executar(self, id_agendamento: str, nova_data: datetime):
        agendamento = self.repository.buscar_por_id(id_agendamento)
        
        if not agendamento:
            raise ValueError("Agendamento não encontrado.")

        # Ignora a regra de 48h e a checagem de dono do agendamento.
        agendamento.data_hora_agendada = nova_data
        
        self.repository.salvar(agendamento)
        
        return {"sucesso": True, "mensagem": "Agendamento alterado pelo Administrador."}