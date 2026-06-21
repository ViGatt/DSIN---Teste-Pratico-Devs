from datetime import datetime, timezone
from typing import Optional
from src.application.use_cases.criar_agendamento import CriarAgendamentoUseCase
from src.domain.entities.agendamento import Agendamento
from src.domain.interfaces.agendamento_repository import IAgendamentoRepository

#  Fake Repository 
class FakeAgendamentoRepository(IAgendamentoRepository):
    def __init__(self):
        self.agendamentos = []

    def salvar(self, agendamento: Agendamento) -> None:
        self.agendamentos.append(agendamento)

    # Implementação obrigatória exigida pela interface
    def buscar_por_id(self, id_agendamento: str) -> Optional[Agendamento]:
        for ag in self.agendamentos:
            if ag.id == id_agendamento:
                return ag
        return None

    def buscar_por_cliente_na_semana(self, cliente_id: str, data_desejada: datetime) -> Optional[Agendamento]:
        # Se a Maria já tem um agendamento na nossa lista falsa, devolve
        for ag in self.agendamentos:
            if ag.cliente_id == cliente_id:
                return ag
        return None

def test_deve_criar_agendamento_se_cliente_nao_tiver_nada_na_semana():
    repo = FakeAgendamentoRepository()
    use_case = CriarAgendamentoUseCase(repo)
    data_desejada = datetime(2026, 6, 25, 10, 0, tzinfo=timezone.utc)
    
    resposta = use_case.executar("cliente_maria", data_desejada, ["Coloração"])
    
    assert resposta["sucesso"] is True
    assert len(repo.agendamentos) == 1

def test_deve_sugerir_agrupamento_se_cliente_ja_tiver_agendamento_na_semana():
    repo = FakeAgendamentoRepository()
    # Adicionamos um agendamento manualmente no Fake Repo
    agendamento_existente = Agendamento("1", "cliente_maria", datetime(2026, 6, 22, 14, 0, tzinfo=timezone.utc), ["Corte"])
    repo.salvar(agendamento_existente)
    
    use_case = CriarAgendamentoUseCase(repo)
    nova_data_desejada = datetime(2026, 6, 25, 10, 0, tzinfo=timezone.utc)
    
    resposta = use_case.executar("cliente_maria", nova_data_desejada, ["Manicure"])
    
    # Verifica se o Caso de Uso interceptou corretamente a criação
    assert resposta["sucesso"] is False
    assert resposta["acao_requerida"] == "SUGESTAO_AGRUPAMENTO"
    assert len(repo.agendamentos) == 1

def test_deve_criar_agendamento_mesmo_com_conflito_se_ignorar_sugestao_for_true():
    repo = FakeAgendamentoRepository()
    # Adiciona um agendamento manualmente no Fake Repo
    agendamento_existente = Agendamento("1", "cliente_maria", datetime(2026, 6, 22, 14, 0, tzinfo=timezone.utc), ["Corte"])
    repo.salvar(agendamento_existente)
    
    use_case = CriarAgendamentoUseCase(repo)
    nova_data_desejada = datetime(2026, 6, 25, 10, 0, tzinfo=timezone.utc)
    
    # Passando a flag para ignorar o agrupamento
    resposta = use_case.executar("cliente_maria", nova_data_desejada, ["Manicure"], ignorar_sugestao=True)
    
    # Verificação: O agendamento deve ser criado, resultando em 2 agendamentos no repo
    assert resposta["sucesso"] is True
    assert len(repo.agendamentos) == 2