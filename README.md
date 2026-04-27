# 📌 SCSC - Sistema de Controle e Solicitação Corporativa

![Python](https://img.shields.io/badge/Python-3776AB?style=flat\&logo=python\&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-005C84?style=flat\&logo=mysql\&logoColor=white)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-ff9800?style=flat)
![Academic Project](https://img.shields.io/badge/Project-Academic-blue?style=flat)

---

# 📖 Sobre o Projeto

O **SCSC (Sistema de Controle e Solicitação Corporativa)** é um sistema desenvolvido para o **Projeto Integrador I (PI1)** da faculdade.

A proposta simula a contratação de uma equipe de desenvolvimento para resolver problemas internos de uma organização que atualmente enfrenta:

* Registro informal de solicitações (e-mails, mensagens e anotações descentralizadas)
* Perda de informações importantes
* Falta de rastreabilidade nas demandas
* Dificuldade na priorização de solicitações

O objetivo do sistema é **centralizar, organizar e controlar todas as solicitações internas da organização**, proporcionando maior controle, rastreabilidade e eficiência no atendimento das demandas.

---

# 🎯 Objetivos do Sistema

* Permitir cadastro de usuários
* Registrar solicitações internas
* Controlar status das demandas
* Garantir rastreabilidade das solicitações
* Persistir dados em banco de dados MySQL
* Organizar e priorizar solicitações internas

---

# 🛠️ Tecnologias Utilizadas

* **Python**
* **MySQL**
* **Git**
* **GitHub**
* **Trello**

---

# 🏗️ Estrutura do Projeto

```
📁 request-tracker-pi1
│
├── main.py
├── database.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# ⚙️ Configuração do Ambiente

Este projeto utiliza **variáveis de ambiente** para proteger credenciais de acesso ao banco de dados.

Crie um arquivo `.env` na raiz do projeto baseado no arquivo `.env.example`.

Exemplo de `.env`:

```
DB_HOST=localhost
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=seu_banco
```

⚠️ **Importante:**
O arquivo `.env` não deve ser enviado para o GitHub. Ele já está listado no `.gitignore`.

---

# 🚀 Como Executar o Projeto

## 1️⃣ Clonar o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
```

---

## 2️⃣ Entrar na pasta do projeto

```bash
cd request-tracker-pi1
```

---

## 3️⃣ Instalar as dependências

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configurar as variáveis de ambiente

Crie o arquivo `.env` baseado no `.env.example` e configure as credenciais do banco de dados.

---

## 5️⃣ Executar o sistema

```bash
python main.py
```

---

# 📊 Status do Projeto

🚧 **Em desenvolvimento**

Este projeto está sendo desenvolvido como parte do **Projeto Integrador I (PI1)**.

Funcionalidades atualmente em desenvolvimento:

* Estrutura inicial do sistema
* Conexão com banco de dados
* Criação automática da tabela de usuários

Próximas funcionalidades:

* Cadastro de usuários
* Sistema de login
* Registro de solicitações
* Visualização de solicitações

---

# 📄 Licença

Projeto desenvolvido **exclusivamente para fins educacionais** como parte de atividades acadêmicas.
