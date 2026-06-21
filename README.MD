# Sistema de Agendamento - Salão da Leila

Este projeto é uma solução fullstack para o gerenciamento de agendamentos online do salão de beleza da Leila, permitindo que clientes marquem mais de um serviço, visualizem históricos e que a Leila tenha uma melhor otimização de sua agenda.

--- 

## Stack Tecnológica

- **Backend:** Python (FastAPI / Dynamic Typings)
- **Frontend:** React + Vite + TypeScript
- **Autenticação:** Clerk Auth (JWT integrado no Backend)
- **Banco de Dados:** SQLite (com SQLAlchemy)
- **Arquitetura:** Domain-Driven Design (DDD) + Clean Architecture

---

## Arquitetura do Sistema (DDD)

O backend foi estruturado seguindo os princípios do DDD e do SOLID (Inversão de Dependência), garantindo isolamento total das regras de negócio:

- **Domain Layer:** Lógica central. Contém as Entidades de negócio (com Máquina de Estados), Objetos de Valor, Interfaces de Contrato (`IAgendamentoRepository`) e **Exceções Customizadas** do domínio. Padronizado com datas cientes de fuso horário (UTC).
- **Application Layer:** Orquestração de casos de uso e fluxos do sistema. Totalmente agnóstico a banco de dados, dependendo apenas de interfaces de repositório.
- **Infrastructure Layer:** Implementações técnicas e persistência. Implementação de repositórios reais (SQLAlchemy com mapeamento de JSON), adaptadores de banco de dados (SQLite) e decodificação de tokens do Clerk.
- **Presentation Layer (API):** Interface com usuário e entrada de dados. Componentes como Controladores FastAPI que expõem os endpoints REST.

---

## Como Executar o Projeto

*Instruções detalhadas de setup de ambiente, variáveis .env do Clerk e inicialização do banco serão adicionadas aqui após a finalização da infraestrutura.*

---

## Estratégia de Testes

Foco em testes unitários automatizados com `pytest` na camada de **Domínio e Aplicação** para garantir a integridade das seguintes regras críticas:
- Máquina de estados: bloqueio de transições inválidas (ex: concluir um serviço cancelado).
- Trava de segurança para alteração de agendamentos com menos de 48h de antecedência.
- Algoritmo de sugestão de agrupamento na mesma semana e bypass caso o cliente decida ignorar.
- Validação de RBAC (Role-Based Access Control): Bypass de segurança de regras para o Perfil Admin (Leila).
- Geração de pacote de dados para o Dashboard Gerencial.

---

## Progresso do Desenvolvimento

**Backend (Core Domain & Application) - CONCLUÍDO**
- [x] Modelagem da Entidade `Agendamento`.
- [x] Implementação da Máquina de Estados (Pendente, Confirmado, Concluído, Cancelado) utilizando `Enum`.
- [x] Regra de Negócio: Trava de 48h (D-2) para alteração por clientes.
- [x] Caso de Uso: Criação com interceptação inteligente (Sugestão de agrupamento).
- [x] Caso de Uso: Alteração com Bypass de Segurança (RBAC) para Admin (Leila).
- [x] Caso de Uso: Dashboard Gerencial (Extração de métricas de desempenho semanal).
- [x] **Refactor:** Padronização de datas para Timezone UTC.
- [x] **Refactor:** Implementação de Exceções Customizadas de Domínio.
- [x] **Refactor:** Aplicação do Princípio de Inversão de Dependência (SOLID) com `IAgendamentoRepository`.
- [x] Cobertura de Testes Unitários nas regras de negócio (11 testes rodando, 100% Passed).

**Backend (Infraestrutura e API) - CONCLUÍDO**
- [x] Configuração do SQLite e SQLAlchemy.
- [x] Repositório físico com Mapeamento de Arrays para JSON.
- [x] Métodos de agregação analítica em Python (Dashboard).
- [x] Endpoints REST (FastAPI) documentados via Swagger.
- [x] **Segurança:** Integração de Auth Bearer e blindagem de Schemas.

**Frontend (React) - NA FILA**
- [ ] Setup do Vite + React + TypeScript.
- [ ] Integração de Autenticação (Clerk).
- [ ] Telas de Cliente e Dashboard Admin.