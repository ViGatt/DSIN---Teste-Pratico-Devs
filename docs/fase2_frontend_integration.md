# Processo de Desenvolvimento - Fase 2: Frontend & Integração

Este documento detalha as decisões arquiteturais da camada de apresentação (Frontend) do **Sistema de Agendamento - Salão da Leila**, construído em React/Vite, e a sua integração com a infraestrutura de backend desenvolvida na Fase 1.

## Objetivo da Fase 2
O objetivo principal desta etapa foi criar uma interface de usuário altamente reativa e responsiva, mantendo a responsabilidade estrita da camada visual. O frontend atua apenas como um cliente de apresentação, delegando toda a lógica de negócio, persistência de dados e regras complexas (como a regra de antecedência de 48h) para a Clean Architecture do nosso backend Python.

---

## 1. Gestão de Estado Global (Zustand)
Para evitar o anti-padrão de *prop drilling* (passar parâmetros por dezenas de componentes filhos), adotamos o **Zustand** para o gerenciamento de estado da aplicação. 

O fluxo de agendamento foi modelado no `useSchedulingStore`, dividindo a jornada em passos reativos:
1.  **Captura de Identidade:** Nome e Telefone (`clientData`).
2.  **Seleção de Data:** Integração com bibliotecas de calendário, tipando as seleções estritamente com objetos `Date`.
3.  **Seleção de Serviço:** Atualização de UI condicional baseada na confirmação das etapas anteriores.

---

## 2. Arquitetura de Componentes e UI
O projeto adotou o ecossistema moderno do React com foco em acessibilidade e consistência visual:
*   **Tailwind CSS:** Utilizado para estilização utilitária, garantindo um design *mobile-first* com animações fluídas (`animate-in fade-in`).
*   **Radix / Base UI:** Empregado para primitivas de UI complexas (como `Popover` no `DatePicker`).
*   **Resolução de Conflitos de DOM:** Durante o desenvolvimento, resolvemos anomalias de hidratação (como `<button>` aninhados indevidamente em componentes *Trigger*) mantendo o controle explícito sobre propriedades `asChild` e a tipagem estrita do TypeScript.

---

## 3. Identidade e Segurança (Clerk)
A autenticação não foi construída do zero. O provedor de identidade **Clerk** foi integrado como solução de *Identity as a Service* (IDaaS).
*   Componentes como `<SignedIn>` e `<SignedOut>` gerenciam o acesso às rotas protegidas diretamente na camada visual.
*   O identificador único (`user_id`) é extraído do token e repassado para o backend, garantindo que as regras de controle de acesso (RBAC) do backend saibam exatamente quem está manipulando os dados.

---

## 4. Decisão Arquitetural Crítica: Rejeição de BaaS (Supabase)
Durante o desenvolvimento, a adoção do **Supabase** (Backend as a Service) foi prototipada e testada com sucesso para conexão direta com o banco PostgreSQL. No entanto, a decisão técnica final foi **reverter e remover** a integração direta pelo frontend.

**Motivo:** Conectar o React diretamente ao banco de dados violaria o princípio de Inversão de Dependência implementado na Fase 1. Ao dar *bypass* na API FastAPI, o sistema:
1.  Ignoraria completamente a validação matemática da máquina de estados.
2.  Tornaria as exceções de domínio criadas (ex: `RegraAntecedenciaMinimaException`) inúteis.
3.  Impediria a contabilização correta de métricas gerenciais exigidas pelo Caso de Uso do Dashboard.

A arquitetura foi corrigida para manter o fluxo padrão de Sistemas Distribuídos: `React (Client) -> HTTP REST -> FastAPI (Application) -> SQLAlchemy (Repository)`.

---

## 5. Integração com a Camada de Aplicação (API REST)
O método final de persistência (`handleFinalize`) foi estruturado em uma requisição `fetch` assíncrona apontando diretamente para o Swagger do backend. 

*   O payload é serializado no formato nativo exigido pelo backend (`snake_case`).
*   Possíveis falhas retornadas pela API (baseadas nas Exceções Customizadas mapeadas para erros HTTP 400/403) são interceptadas e apresentadas como feedback claro ao cliente na interface do React.

---
**Status Final da Fase 2:** Cliente React concluído, fluxo de checkout operante e arquitetura frontend conectada de forma segura e não acoplada às regras de negócio contidas no backend estruturado em Domain-Driven Design.