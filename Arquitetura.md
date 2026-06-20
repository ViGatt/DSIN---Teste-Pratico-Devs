# Estrutura do Projeto - Salao da Leila

Este documento apresenta a arquitetura do projeto, detalhando a responsabilidade de cada diretorio no sistema. O projeto foi planejado dividindo-se entre Backend (regras de negocio e persistencia) e Frontend (interface do usuario).

---

## 1. O Backend (/backend) - Arquitetura DDD 

O backend utiliza os principios do DDD para garantir que as regras de negocio fiquem completamente isoladas de detalhes de infraestrutura, como frameworks web ou bancos de dados.

* **src/domain/**
  Contem apenas codigo Python puro, sem dependencias externas. Aqui moram as Entidades (como a classe Agendamento) e as regras de negocio essenciais (como a validacao de antecedencia minima de 48h para alteracoes).

* **src/application/**
  Contem os Casos de Uso (Use Cases), que definem o fluxo das operacoes do sistema (ex: CriarAgendamento, CancelarServico). Esta camada interage com as interfaces do dominio e coordena a execucao das tarefas.

* **src/infrastructure/**
  Aqui e implementado tudo o que faz comunicacao com o mundo externo. Contem a configuracao do banco de dados SQLite via SQLAlchemy, os repositorios reais de dados e a integracao com o Clerk para validacao de tokens.

* **src/api/**
  Contem os roteadores e endpoints do FastAPI (ex: rotas HTTP para /agendamentos). Sua funcao e estritamente receber as requisicoes, extrair os dados necessarios, invocar a camada de aplicacao e retornar a resposta em formato JSON.

---

## 2. O Frontend (/frontend) - React + Vite

O frontend foi organizado de forma a ser utilizado módulos para promover a reutilizacao de componentes e a clara separacão na interface.

* **src/pages/**
  Representa as telas completas do sistema. As interfaces sao divididas por contexto de utilizacao: a area do Cliente (historico e realizacao de agendamentos) e a area Admin (ferramentas operacionais e gerenciais da Leila).

* **src/components/**
  Componentes visuais reaproveitaveis por diferentes telas da aplicacao, como botoes customizados, modais de confirmacao e cards de listagem de servicos.

* **src/services/**
  Camada de integracao com o backend. Centraliza as chamadas HTTP (API), configuracoes de clientes de requisicao (como Axios ou Fetch) e o envio de tokens de autenticacao.

* **src/contexts/ e src/hooks/**
  Gerenciamento de estado global e encapsulamento de logicas especificas da interface, como o controle de autenticacao do usuario logado e estados compartilhados entre componentes.
