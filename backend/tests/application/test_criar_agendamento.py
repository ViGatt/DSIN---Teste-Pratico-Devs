from datetime import datetime
from src.application.use_cases.criar_agendamento import CriarAgendamentoUseCase
from src.domain.entities.agendamento import Agendamento

#  Fake Repository
class FakeAgendamentoRepository:
    def __init__(self):
        self.agendamentos = []

    def salvar(self, agendamento):
        self.agendamentos.append(agendamento)

    def buscar_por_cliente_na_semana(self, cliente_id, data_desejada):
        # Simula a busca: se a Maria já tem um agendamento na nossa lista falsa, devolve
        for ag in self.agendamentos:
            if ag.cliente_id == cliente_id:
                return ag
        return None

def test_deve_criar_agendamento_se_cliente_nao_tiver_nada_na_semana():
    repo = FakeAgendamentoRepository()
    use_case = CriarAgendamentoUseCase(repo)
    data_desejada = datetime(2026, 6, 25, 10, 0)
    
    resposta = use_case.executar("cliente_maria", data_desejada, ["Coloração"])
    
    assert resposta["sucesso"] is True
    assert len(repo.agendamentos) == 1

def test_deve_sugerir_agrupamento_se_cliente_ja_tiver_agendamento_na_semana():
    repo = FakeAgendamentoRepository()
    # Adicionamos um agendamento manualmente no Fake Repo
    agendamento_existente = Agendamento("1", "cliente_maria", datetime(2026, 6, 22, 14, 0), ["Corte"])
    repo.salvar(agendamento_existente)
    
    use_case = CriarAgendamentoUseCase(repo)
    nova_data_desejada = datetime(2026, 6, 25, 10, 0)
    
    resposta = use_case.executar("cliente_maria", nova_data_desejada, ["Manicure"])
    
    # Verifica se o Caso de Uso interceptou corretamente a criação
    assert resposta["sucesso"] is False
    assert resposta["acao_requerida"] == "SUGESTAO_AGRUPAMENTO"
    assert len(repo.agendamentos) == 1