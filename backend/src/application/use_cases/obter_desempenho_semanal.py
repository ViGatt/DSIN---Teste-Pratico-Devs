from datetime import datetime, timedelta

class ObterDesempenhoSemanalUseCase:
    def __init__(self, relatorio_repository):
        self.repository = relatorio_repository

    def executar(self, data_referencia: datetime = None):
        if not data_referencia:
            data_referencia = datetime.now()
            
        # Calcula a semana
        inicio_semana = data_referencia - timedelta(days=data_referencia.weekday())
        fim_semana = inicio_semana + timedelta(days=6)

        # Delega e faz contagem para o BD
        agendamentos_por_dia = self.repository.contar_agendamentos_por_dia(inicio_semana, fim_semana)
        servicos_top = self.repository.buscar_servicos_mais_realizados(inicio_semana, fim_semana)
        horarios_pico = self.repository.buscar_horarios_de_pico(inicio_semana, fim_semana)
        top_clientes = self.repository.buscar_top_clientes(inicio_semana, fim_semana)

        return {
            "periodo": {
                "inicio": inicio_semana.isoformat(),
                "fim": fim_semana.isoformat()
            },
            "agendamentos_por_dia": agendamentos_por_dia,
            "servicos_mais_buscados": servicos_top,
            "horarios_pico": horarios_pico,
            "top_clientes": top_clientes
        }