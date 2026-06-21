import uuid
from datetime import datetime
from src.domain.entities.agendamento import Agendamento
from src.domain.interfaces.agendamento_repository import IAgendamentoRepository

#Injeção de dependência
class CriarAgendamentoUseCase:
    def __init__(self, agendamento_repository: IAgendamentoRepository):
        self.repository = agendamento_repository

    def executar(self, cliente_id: str, data_desejada: datetime, servicos: list, ignorar_sugestao: bool = False):
        
        # Estabelecimento de variáveis e Consulta
        # Só fazemos a busca se o cliente NÃO marcou a caixinha de "ignorar sugestão"
        if not ignorar_sugestao:
            # Buscamos no banco de dados se a cliente já tem algo na semana
            agendamento_existente = self.repository.buscar_por_cliente_na_semana(cliente_id, data_desejada)
            
            # Etapa de validação
            if agendamento_existente:
                return {
                    "sucesso": False,
                    "acao_requerida": "SUGESTAO_AGRUPAMENTO",
                    "mensagem": "Você já possui um agendamento nesta semana.",
                    "data_sugerida": agendamento_existente.data_hora_agendada
                }

        # Se não tinha nada na semana OU se ignorou a sugestão
        novo_id = str(uuid.uuid4())
        
        novo_agendamento = Agendamento(
            id_agendamento=novo_id,
            cliente_id=cliente_id,
            data_hora_agendada=data_desejada,
            servicos=servicos
        )

        self.repository.salvar(novo_agendamento)

        return {
            "sucesso": True,
            "mensagem": "Agendamento confirmed com sucesso!",
            "agendamento_id": novo_agendamento.id
        }