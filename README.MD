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

O backend foi/será estruturado seguindo os princípios táticos do DDD, garantindo isolamento total das regras de negócio:

- **Domain Layer:** Regras de negócio e lógica central.
. Contém as entidades de negócio, Objetos de Valor e as regras puras (Validação de data retroativa D-2 e Agrupamento Semanal), sem dependência externa.
- **Application Layer:** Orquestração de casos de uso e fluxos do sistema .
- **Infrastructure Layer:** Implementações técnicas e persistência. Implementação de repositórios (SQLAlchemy), adaptadores de banco de dados (SQLite) e decodificação de tokens do Clerk.
- **Presentation Layer (API):** Interface com usuário e entrada de dados. Componentes como Controladores FastAPI que expõem os endpoints REST.

---

## Como Executar o Projeto

*Instruções detalhadas de setup de ambiente, variáveis .env do Clerk e inicialização do banco serão adicionadas aqui*

---

## Estratégia de Testes

Foco em testes unitários na camada de **Domínio** para garantir a integridade das seguintes regras críticas:
- Trava de alteração de agendamentos com menos de 48h de antecedência.
- Algoritmo de sugestão de agrupamento na mesma semana.