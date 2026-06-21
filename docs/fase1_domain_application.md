# Processo de Desenvolvimento - Fase 1: Domain & Application

Este documento detalha o processo de pensamento, as decisões arquiteturais e as refatorações realizadas durante a primeira fase do desenvolvimento do **Sistema de Agendamento - Salão da Leila**.

## Objetivo da Fase 1
O objetivo principal desta fase foi construir o "cérebro" da aplicação. Adotando os princípios do **Domain-Driven Design (DDD)** e da **Clean Architecture**, decidindo isolar completamente as regras de negócio de qualquer detalhe de infraestrutura (bancos de dados, APIs ou frameworks web). 

Se a infraestrutura mudar, o núcleo do sistema permanece intacto.

---

## 1. Camada de Domínio (O Coração do Sistema)

A construção começou pela camada mais interna: as Entidades e as Regras Puras.

* **Entidade Rica (`Agendamento`):** Em vez de usar classes anêmicas (apenas com *getters* e *setters*), a entidade controla seu próprio ciclo de vida e estado.
* **Máquina de Estados com `Enum`:** Substituímos *magic strings* ("PENDENTE", "CONCLUIDO") por um enumerador `StatusAgendamento`. Isso previne falhas de digitação e reforça o código contra transições de estado inválidas (ex: tentar concluir um agendamento cancelado).
* **Gestão de Datas (UTC):** O sistema foi padronizado para operar com `datetime` ciente de fuso horário (`timezone.utc`), eliminando uma das categorias mais comuns de bugs em produção.
* **Regra de D-2 (48h):** A validação que impede o cliente de alterar um agendamento em cima da hora foi encapsulada dentro da própria entidade, com precisão de `timedelta(hours=48)`.

---

## 2. Tratamento de Exceções Customizadas

Para evitar o anti-padrão de lançar erros genéricos do Python (`ValueError` ou `PermissionError`), foi criado uma hierarquia de exceções próprias do nosso domínio na pasta `domain/exceptions/`:
* `StatusAgendamentoInvalidoException`
* `RegraAntecedenciaMinimaException`
* `PermissaoNegadaException`

**Por que fiz isso?** Para garantir que, na Fase 2, a camada de API (FastAPI) consiga capturar esses erros específicos e traduzi-los facilmente para os códigos de status HTTP corretos (400, 403, 404).

---

## 3. Camada de Aplicação (Casos de Uso)

Os Casos de Uso (*Use Cases*) comandam as entidades para realizar as vontades do usuário. Foram implementados:

1.  **Criar Agendamento:** Intercepta a criação para buscar agendamentos prévios na mesma semana, sugerindo agrupamentos para otimizar a agenda da Leila. Possui flag `ignorar_sugestao` para forçar a criação.
2.  **Alterar Agendamento (Cliente):** Valida a regra de 48h e garante o controle de acesso (um cliente não pode alterar o agendamento de outro).
3.  **Alterar Agendamento (Admin):** Aplicação de **RBAC** (Role-Based Access Control). O sistema possui um *bypass* de regras que permite à administradora (Leila) remanejar qualquer agendamento sem restrições.
4.  **Dashboard Gerencial:** Caso de uso focado em relatórios que estrutura um pacote de métricas (horários de pico, serviços mais buscados) para a tomada de decisão comercial.

---

## 4. Inversão de Dependência (SOLID)

A maior evolução arquitetural desta fase foi a aplicação do Princípio da Inversão de Dependência (A letra **D** do SOLID).

* **O Problema:** Um Caso de Uso não deve "saber" que o banco de dados é um SQLite.
* **A Solução:** Criamos uma interface (`IAgendamentoRepository` usando o módulo `abc` do Python). 
* Os Casos de Uso exigem apenas o *contrato*. Durante os testes, injetamos um Repositório Falso em memória. Em produção, injetaremos o Repositório do SQLAlchemy.

---

## 5. Cobertura de Testes Unitários

Todas as regras de negócio foram postas à prova.

Utilizando a biblioteca `pytest`, construímos uma suíte de testes rápidos (em memória) que cobre 100% dos fluxos críticos:
* Validações matemáticas da regra de 48 horas.
* Bloqueios da máquina de estados.
* Lógica de sugestão e ignorância de agrupamentos semanais.
* Bloqueios de permissão entre usuários diferentes e acesso irrestrito do Admin.

O terminal verde confirmando os testes rodando com sucesso garante que o motor do sistema é confiável para a próxima etapa.

---
**Status Final da Fase 1:** Sistema completo, padronizado, seguro e coberto por testes. Pronto para elaboração do Banco de Dados e a Interface Web (API).