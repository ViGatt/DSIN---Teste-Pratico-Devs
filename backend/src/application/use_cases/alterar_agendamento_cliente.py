from datetime import datetime

class AlterarAgendamentoClienteUseCase:
    def __init__(self, agendamento_repository):
        self.repository = agendamento_repository

    def executar(self, id_agendamento: str, cliente_id_token: str, nova_data: datetime, data_atual_requisicao: datetime):
        # 1. Busca o agendamento no banco
        agendamento = self.repository.buscar_por_id(id_agendamento)
        
        if not agendamento:
            raise ValueError("Agendamento não encontrado.")
            
        # 2.  Garante que o cliente só pode alterar o PRÓPRIO agendamento
        if agendamento.cliente_id != cliente_id_token:
            raise PermissionError("Você não tem permissão para alterar este agendamento.")

        # 3. A trava D-2 da nossa Entidade
        if not agendamento.pode_ser_alterado_pelo_cliente(data_atual_requisicao):
            raise ValueError("Alterações só podem ser feitas com 48h de antecedência. Por favor, ligue para o salão.")

        # 4. Aplica a alteração e salva
        agendamento.data_hora_agendada = nova_data
        self.repository.salvar(agendamento)
        
        return {"sucesso": True, "mensagem": "Agendamento alterado com sucesso."}