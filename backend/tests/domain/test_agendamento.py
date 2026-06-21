import pytest
from datetime import datetime, timedelta
from src.domain.entities.agendamento import Agendamento

def test_deve_permitir_alteracao_com_mais_de_48h_de_antecedencia():
    # Preparação
    data_agendada = datetime(2026, 6, 20, 14, 0) # 20 de Junho
    agendamento = Agendamento("123", "cliente_1", data_agendada, ["Corte"])
    data_requisicao = datetime(2026, 6, 17, 14, 0) # 17 de Junho (3 dias antes)
    
    # Ação / Verificação
    assert agendamento.pode_ser_alterado_pelo_cliente(data_requisicao) is True

def test_deve_bloquear_alteracao_com_menos_de_48h_de_antecedencia():
    # Preparação
    data_agendada = datetime(2026, 6, 20, 14, 0)
    agendamento = Agendamento("123", "cliente_1", data_agendada, ["Corte"])
    data_requisicao = datetime(2026, 6, 19, 14, 0) # 19 de Junho (Apenas 1 dia antes)
    
    # Ação / Verificação
    assert agendamento.pode_ser_alterado_pelo_cliente(data_requisicao) is False

def test_maquina_de_estados_nao_deve_concluir_agendamento_sem_estar_confirmado_ou_pendente():
    agendamento = Agendamento("123", "cliente_1", datetime.now(), ["Manicure"])
    agendamento.cancelar() # Forçar o estado para CANCELADO
    
    # Ação / Verificação
    with pytest.raises(ValueError, match="O agendamento precisa estar confirmado"):
        agendamento.concluir()