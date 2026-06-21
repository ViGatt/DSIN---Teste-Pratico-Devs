class DomainException(Exception):
    """Classe base para todas as exceções de regra de negócio do nosso sistema."""
    pass

class StatusAgendamentoInvalidoException(DomainException):
    """Lançada quando há uma tentativa de ferir a máquina de estados (ex: concluir algo cancelado)."""
    pass

class RegraAntecedenciaMinimaException(DomainException):
    """Lançada quando o cliente tenta alterar o agendamento fora do prazo permitido (D-2)."""
    pass

class AgendamentoNaoEncontradoException(DomainException):
    """Lançada quando a busca no banco de dados não encontra o ID solicitado."""
    pass

class PermissaoNegadaException(DomainException):
    """Lançada quando um usuário tenta alterar um recurso que não pertence a ele."""
    pass