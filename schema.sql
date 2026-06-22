sql
-- Criação da tabela principal de Agendamentos
CREATE TABLE IF NOT EXISTS agendamentos (
    id VARCHAR(36) PRIMARY KEY,
    cliente_id VARCHAR(255) NOT NULL,
    data_hora_agendada DATETIME NOT NULL,
    servicos TEXT NOT NULL, /* Armazenado via SQLAlchemy como Array JSON serializado */
    status VARCHAR(50) DEFAULT 'PENDENTE' NOT NULL
);

-- Índices gerados para otimização de buscas do Dashboard e Histórico
CREATE INDEX IF NOT EXISTS idx_agendamentos_cliente_id ON agendamentos(cliente_id);
CREATE INDEX IF NOT EXISTS idx_agendamentos_data_hora ON agendamentos(data_hora_agendada);