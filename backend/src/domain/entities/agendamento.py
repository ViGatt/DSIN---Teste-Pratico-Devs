from datetime import datetime, timedelta
from typing import List

class Agendamento:
    def __init__(self, id_agendamento: str, cliente_id: str, data_hora_agendada: datetime, servicos: List[str]):
        self.id = id_agendamento
        self.cliente_id = cliente_id
        self.data_hora_agendada = data_hora_agendada
        self.servicos = servicos
        self.status = "PENDENTE" 
        self.criado_em = datetime.now()

    def pode_ser_alterado_pelo_cliente(self, data_atual_da_requisicao: datetime) -> bool:
        tempo_restante = self.data_hora_agendada - data_atual_da_requisicao
        return tempo_restante >= timedelta(days=2) # True >= 48h Agenda | False < 48h Ligar no salão
        
    def confirmar_pela_leila(self):
        self.status = "CONFIRMADO"