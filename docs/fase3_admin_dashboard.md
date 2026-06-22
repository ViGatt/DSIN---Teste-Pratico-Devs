# Fase 3: Dashboard Administrativo e RBAC(Role-Based Access Control)

Nesta fase, separamos o contexto de uso do cliente do contexto administrativo . Focamos em proteger os dados da aplicação garantindo que apenas a proprietária (Leila) tenha acesso à visualização e controle avançado de agenda.

## Decisões Arquiteturais

1. **Role-Based Access Control (RBAC) no Backend:**
   - Foi criado uma dependência estrita `obter_admin_logado` no FastAPI.
   - Rotas de gestão (`GET /desempenho` e `PUT /admin`) agora exigem validação específica do ID do usuário, retornando `403 Forbidden` para clientes comuns.

2. **Separação de Contextos (Frontend):**
   - **Camada de Rede Isolada:** Foi criado o `src/services/api.ts` para isolar requisições do painel administrativo. Não poluímos o `useSchedulingStore` (focado na jornada do cliente) com dados estáticos de dashboard.
   - **Renderização Condicional Segura:** Utilizado o hook `useUser` do Clerk para identificar o ID da usuária e renderizar o `<AdminDashboard />` apenas se o perfil corresponder à administradora, evitando vazamento de UI.

3. **Integração de Dados:**
   - A comunicação Ponta a Ponta (End-to-End) foi validada. O JSON de métricas (Agendamentos por dia, Serviços mais buscados, etc.) transita com segurança e é mapeado para a interface `DashboardData` no TypeScript.