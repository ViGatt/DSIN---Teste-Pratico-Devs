import pytest
from datetime import datetime, timedelta, timezone
from typing import Optional
from src.domain.entities.agendamento import Agendamento
from src.domain.interfaces.agendamento_repository import IAgendamentoRepository
from src.application.use_cases.alterar_agendamento_cliente import AlterarAgendamentoClienteUseCase
from src.application.use_cases.alterar_agendamento_admin import AlterarAgendamentoAdminUseCase
from src.domain.exceptions.agendamento_exceptions import PermissaoNegadaException, RegraAntecedenciaMinimaException

# Recriei o Fake Repo para manter este arquivo de teste independente
class FakeAgendamentoRepository(IAgendamentoRepository):
    def __init__(self):
        self.agendamentos = []

    def salvar(self, agendamento: Agendamento) -> None:
        self.agendamentos.append(agendamento)
        
    def buscar_por_id(self, id_agendamento: str) -> Optional[Agendamento]:
        for ag in self.agendamentos:
            if ag.id == id_agendamento:
                return ag
        return None

    def buscar_por_cliente_na_semana(self, cliente_id: str, data_desejada: datetime) -> Optional[Agendamento]:
        pass # Não precisamos deste método para alterar agendamento

# --- TESTES DO CLIENTE ---

def test_cliente_nao_pode_alterar_agendamento_de_outro_cliente():
    repo = FakeAgendamentoRepository()
    agendamento = Agendamento("123", "cliente_maria", datetime(2026, 6, 20, 14, 0, tzinfo=timezone.utc), ["Corte"])
    repo.salvar(agendamento)
    
    use_case = AlterarAgendamentoClienteUseCase(repo)
    data_atual = datetime(2026, 6, 10, 10, 0, tzinfo=timezone.utc)
    nova_data = datetime(2026, 6, 21, 14, 0, tzinfo=timezone.utc)
    
    # O token diz que é a Joana tentando mudar o da Maria
    with pytest.raises(PermissaoNegadaException, match="Você não tem permissão"):
        use_case.executar("123", "cliente_joana", nova_data, data_atual)

def test_cliente_nao_pode_alterar_com_menos_de_48h_de_antecedencia():
    repo = FakeAgendamentoRepository()
    agendamento = Agendamento("123", "cliente_maria", datetime(2026, 6, 20, 14, 0, tzinfo=timezone.utc), ["Corte"])
    repo.salvar(agendamento)
    
    use_case = AlterarAgendamentoClienteUseCase(repo)
    # Apenas 1 dia de antecedência
    data_atual = datetime(2026, 6, 19, 14, 0, tzinfo=timezone.utc) 
    nova_data = datetime(2026, 6, 21, 14, 0, tzinfo=timezone.utc)
    
    with pytest.raises(RegraAntecedenciaMinimaException, match="Alterações só podem ser feitas com 48h de antecedência"):
        use_case.executar("123", "cliente_maria", nova_data, data_atual)

#  TESTES DA (LEILA) 

def test_admin_pode_alterar_qualquer_agendamento_ignorando_regras():
    repo = FakeAgendamentoRepository()
    agendamento = Agendamento("123", "cliente_maria", datetime(2026, 6, 20, 14, 0, tzinfo=timezone.utc), ["Corte"])
    repo.salvar(agendamento)
    
    use_case = AlterarAgendamentoAdminUseCase(repo)
    # Leila muda para a semana que vem, sem informar quem é o cliente e nem a data atual
    nova_data = datetime(2026, 6, 27, 10, 0, tzinfo=timezone.utc) 
    
    resposta = use_case.executar("123", nova_data)
    
    assert resposta["sucesso"] is True
    assert agendamento.data_hora_agendada == nova_data