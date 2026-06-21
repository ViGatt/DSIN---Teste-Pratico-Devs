from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.domain.entities.agendamento import Agendamento
from src.domain.interfaces.agendamento_repository import IAgendamentoRepository
from src.infrastructure.database.models import AgendamentoModel

class AgendamentoRepository(IAgendamentoRepository):
    # O repositório recebe a sessão do banco de dados (injetada pelo FastAPI posteriormente)
    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, model: AgendamentoModel) -> Agendamento:
        # Método para converter o Modelo do SQLAlchemy 
        agendamento = Agendamento(
            id_agendamento=model.id,
            cliente_id=model.cliente_id,
            data_hora_agendada=model.data_hora_agendada,
            servicos=model.servicos
        )
        agendamento.status = model.status
        agendamento.criado_em = model.criado_em
        return agendamento

    def salvar(self, agendamento: Agendamento) -> None:

        # Se o registro já existe faz um UPDATE. Se não existir, fazemos um INSERT
        model = self.db.execute(
            select(AgendamentoModel).where(AgendamentoModel.id == agendamento.id)
        ).scalars().first()
        
        if not model:
            # INSERT: Cria um novo modelo espelhando os dados da entidade
            novo_model = AgendamentoModel(
                id=agendamento.id,
                cliente_id=agendamento.cliente_id,
                data_hora_agendada=agendamento.data_hora_agendada,
                servicos=agendamento.servicos,
                status=agendamento.status,
                criado_em=agendamento.criado_em
            )
            self.db.add(novo_model)
        else:
            # UPDATE: Atualiza os campos que podem ter sido alterados
            model.data_hora_agendada = agendamento.data_hora_agendada
            model.servicos = agendamento.servicos
            model.status = agendamento.status
            
        # Efetiva no SQLite
        self.db.commit()

    def buscar_por_id(self, id_agendamento: str) -> Optional[Agendamento]:
        model = self.db.execute(
            select(AgendamentoModel).where(AgendamentoModel.id == id_agendamento)
        ).scalars().first()
        
        if model:
            return self._to_entity(model)
        return None

    def buscar_por_cliente_na_semana(self, cliente_id: str, data_desejada: datetime) -> Optional[Agendamento]:

        # Calcula o início (segunda) e o fim (domingo) da semana com base na data_desejada,
        # e busca se o cliente já possui algum agendamento neste intervalo de tempo.

        # data_desejada.weekday() retorna 0 para Segunda, 1 para Terça, etc.
        inicio_semana = data_desejada - timedelta(days=data_desejada.weekday())
        inicio_semana = inicio_semana.replace(hour=0, minute=0, second=0, microsecond=0)
        
        fim_semana = inicio_semana + timedelta(days=6, hours=23, minutes=59, seconds=59)

        model = self.db.execute(
            select(AgendamentoModel).where(
                AgendamentoModel.cliente_id == cliente_id,
                AgendamentoModel.data_hora_agendada >= inicio_semana,
                AgendamentoModel.data_hora_agendada <= fim_semana
            )
        ).scalars().first()
        
        if model:
            return self._to_entity(model)
        return None