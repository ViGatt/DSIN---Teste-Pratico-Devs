from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from src.domain.entities.agendamento import Agendamento

class IAgendamentoRepository(ABC):

    #Contrato que qualquer banco de dados ou repositório falso 
    # deve seguir para ser aceito pelos Casos de Uso.

    
    @abstractmethod
    def salvar(self, agendamento: Agendamento) -> None:
        pass

    @abstractmethod
    def buscar_por_id(self, id_agendamento: str) -> Optional[Agendamento]:
        pass

    @abstractmethod
    def buscar_por_cliente_na_semana(self, cliente_id: str, data_desejada: datetime) -> Optional[Agendamento]:
        pass