from datetime import datetime, timezone
from src.application.use_cases.obter_desempenho_semanal import ObterDesempenhoSemanalUseCase

# Repositório Fake exclusivo para os Relatórios Gerenciais
class FakeRelatorioRepository:
    def contar_agendamentos_por_dia(self, inicio, fim):
        return {"Segunda": 2, "Terça": 5, "Quarta": 6}
        
    def buscar_servicos_mais_realizados(self, inicio, fim):
        return [{"nome": "Corte Feminino", "quantidade": 18}]
        
    def buscar_horarios_de_pico(self, inicio, fim):
        return ["14:00", "18:00"]
        
    def buscar_top_clientes(self, inicio, fim):
        return ["Maria Silva"]

def test_deve_retornar_metricas_semanais_corretamente():
    # Preparação
    repo = FakeRelatorioRepository()
    use_case = ObterDesempenhoSemanalUseCase(repo)
    
    # Simulando uma quarta-feira exata para garantir que a lógica de datas não quebra
    data_base = datetime(2026, 6, 17, 10, 0, tzinfo=timezone.utc)
    
    # Ação
    resposta = use_case.executar(data_referencia=data_base)
    
    # Verificação
    assert "periodo" in resposta
    assert "inicio" in resposta["periodo"]
    assert "fim" in resposta["periodo"]
    assert resposta["agendamentos_por_dia"]["Terça"] == 5
    assert resposta["servicos_mais_buscados"][0]["nome"] == "Corte Feminino"
    assert "18:00" in resposta["horarios_pico"]
    assert resposta["top_clientes"][0] == "Maria Silva"