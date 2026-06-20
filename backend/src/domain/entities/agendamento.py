from datetime import datetime, timedelta
from typing import List

class Agendamento:
    def __init__(self, id_agendamento: str, cliente_id: str, data_hora_agendada: datetime, servicos: List[str]):
        self.id = id_agendamento
        self.cliente_id = cliente_id
        self.data_hora_agendada = data_hora_agendada
        self.servicos = servicos
        self.status = "PENDENTE" # Ciclo : PENDENTE -> CONFIRMADO -> CONCLUIDO ou CANCELADO
        self.criado_em = datetime.now()

    def pode_ser_alterado_pelo_cliente(self, data_atual_da_requisicao: datetime) -> bool:
        tempo_restante = self.data_hora_agendada - data_atual_da_requisicao
        return tempo_restante >= timedelta(days=2) # True >= 48h Agenda | False < 48h Ligar no salão
        
    def confirmar(self):
        if self.status == "CANCELADO":
            raise ValueError("Não é possível confirmar um agendamento cancelado.")
        self.status = "CONFIRMADO"

    def concluir(self):
        if self.status != "CONFIRMADO":
            raise ValueError("O agendamento precisa estar confirmado antes de ser concluído.")
        self.status = "CONCLUIDO"

    def cancelar(self):
        if self.status == "CONCLUIDO":
            raise ValueError("Não é possível cancelar um serviço que já foi concluído.")
        self.status = "CANCELADO"