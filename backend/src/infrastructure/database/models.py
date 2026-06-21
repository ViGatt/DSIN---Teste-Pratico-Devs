from datetime import datetime, timezone
from sqlalchemy import String, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from src.domain.entities.agendamento import StatusAgendamento

# Mapeamento do SQLAlchemy
class Base(DeclarativeBase):
    pass

class AgendamentoModel(Base):
    __tablename__ = "agendamentos"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    
    # Otimizar as buscas por cliente 
    cliente_id: Mapped[str] = mapped_column(String, index=True)
    
    data_hora_agendada: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    
    # Contornar a ausência de tipo Array nativo no SQLite
    servicos: Mapped[list[str]] = mapped_column(JSON)
    
    # Vincula o Enum do domínio diretamente à validação do banco de dados
    status: Mapped[StatusAgendamento] = mapped_column(SQLEnum(StatusAgendamento))
    
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )