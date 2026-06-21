from datetime import datetime, timedelta
from typing import List
from enum import Enum

# Criação de Enum para otimização
class StatusAgendamento(Enum):
    PENDENTE = "PENDENTE"
    CONFIRMADO = "CONFIRMADO"
    CONCLUIDO = "CONCLUIDO"
    CANCELADO = "CANCELADO"

class Agendamento:
    def __init__(self, id_agendamento: str, cliente_id: str, data_hora_agendada: datetime, servicos: List[str]):
        self.id = id_agendamento
        self.cliente_id = cliente_id
        self.data_hora_agendada = data_hora_agendada
        self.servicos = servicos
        self.status = StatusAgendamento.PENDENTE # Ciclo : PENDENTE -> CONFIRMADO -> CONCLUIDO ou CANCELADO / Atualizado para utilizar o Enum
        self.criado_em = datetime.now()

    def pode_ser_alterado_pelo_cliente(self, data_atual_da_requisicao: datetime) -> bool:
        tempo_restante = self.data_hora_agendada - data_atual_da_requisicao
        return tempo_restante >= timedelta(days=2) # True >= 48h Agenda | False < 48h Ligar no salão
        
    def confirmar(self):
        # Comparações atualizadas para usar Enum
        if self.status == StatusAgendamento.CANCELADO:
            raise ValueError("Não é possível confirmar um agendamento cancelado.")
        self.status = StatusAgendamento.CONFIRMADO

    def concluir(self):
        if self.status != StatusAgendamento.CONFIRMADO:
            raise ValueError("O agendamento precisa estar confirmado antes de ser concluído.")
        self.status = StatusAgendamento.CONCLUIDO

    def cancelar(self):
        if self.status == StatusAgendamento.CONCLUIDO:
            raise ValueError("Não é possível cancelar um serviço que já foi concluído.")
        self.status = StatusAgendamento.CANCELADO