# Sistema de Chamados Help – API

Este projeto é uma **API REST para gerenciamento de chamados de suporte de TI**, desenvolvida como um projeto de estudo prático para consolidar conhecimentos em:

- Desenvolvimento de APIs REST
- Arquitetura de sistemas backend
- Controle de fluxo de chamados (ticket lifecycle)
- Autenticação, autorização e controle de papéis
- Persistência de dados e rastreabilidade de eventos

O sistema simula um **cenário real de help desk**, onde usuários podem abrir chamados, técnicos podem assumir e resolver problemas, e todo o histórico fica registrado no sistema.

O projeto está sendo desenvolvido **de forma incremental**, com versionamento contínuo e foco em boas práticas.

---

## 🚀 Funcionalidades implementadas

### Autenticação e usuários
- Cadastro e login de usuários
- Autenticação via JWT
- Controle de papéis:
  - `user` (usuário final)
  - `technician` (técnico de suporte)
  - `admin` (administrador)

---

### Chamados (Tickets)
- Criação de chamados por usuários
- Listagem de chamados conforme o papel do usuário
- Atribuição de chamados a técnicos
- Estados do chamado:
  - `open`
  - `in_progress`
  - `resolved`
  - `closed`

---

### Comentários (Chat por chamado)
- Comentários vinculados a um chamado
- Comunicação entre usuário, técnico e administrador
- Ordenação cronológica das mensagens
- Histórico completo da conversa preservado

---

### Histórico de eventos do chamado
- Registro automático de eventos importantes, como:
  - Atribuição de técnico
  - Resolução do chamado
  - Encerramento do chamado
- Cada evento armazena:
  - Quem realizou a ação
  - Status anterior e novo status
  - Data e hora do evento

Esse histórico permite **auditoria e rastreabilidade** do ciclo de vida do chamado.

---

## 🧱 Tecnologias utilizadas

- Python
- FastAPI
- SQLAlchemy
- Alembic (migrations)
- SQLite (ambiente de desenvolvimento)

### Tecnologias planejadas
- PostgreSQL (produção)
- RabbitMQ (eventos assíncronos)
- Docker (containerização)
- Docker Compose

---

## 🏗️ Arquitetura (visão geral)

- API REST desenvolvida com FastAPI
- Camada de modelos usando SQLAlchemy
- Controle de regras de negócio nos serviços
- Banco de dados relacional
- Migrations versionadas com Alembic

A arquitetura foi pensada para **facilitar evolução**, permitindo a adição futura de mensageria, notificações e integração com outros serviços.

---

## 📌 Status do projeto

🟢 **Funcional (MVP)**  
O fluxo principal de chamados está completo e funcional.

Próximos passos incluem:
- Timeline unificada do chamado
- Notificações baseadas em eventos
- Integração com mensageria
- Melhorias de segurança e testes automatizados


