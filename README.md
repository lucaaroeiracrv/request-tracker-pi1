# 📌 SCSC - Sistema de Controle e Solicitação Corporativa

![Python](https://img.shields.io/badge/Python-3776AB?style=flat\&logo=python\&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-005C84?style=flat\&logo=mysql\&logoColor=white)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-ff9800?style=flat)
![Academic Project](https://img.shields.io/badge/Project-Academic-blue?style=flat)

---

## 📖 Sobre o Projeto

O **SCSC (Sistema de Controle e Solicitação Corporativa)** é um sistema desenvolvido para o **Projeto Integrador I (PI1)** da faculdade.

A proposta simula a contratação de uma equipe de desenvolvimento para resolver problemas internos de uma organização que atualmente enfrenta:

* Registro informal de solicitações (e-mails, mensagens e anotações descentralizadas)
* Perda de informações
* Falta de rastreabilidade
* Dificuldade na priorização de demandas

O sistema tem como objetivo **centralizar, organizar e controlar todas as solicitações internas**.

---

## 🎯 Objetivo do Sistema

* Permitir cadastro de usuários
* Registrar solicitações internas
* Controlar status das demandas
* Garantir rastreabilidade
* Persistir dados em banco MySQL
* Organizar e priorizar solicitações

---

## 🛠️ Tecnologias Utilizadas

* Python
* MySQL
* Git & GitHub
* Trello

---

## 🏗️ Estrutura do Projeto

```
📁 request-tracker-pi1
 ├── main.py
 ├── database.py
 ├── requirements.txt
 └── README.md
```

---

## 🚀 Como Executar o Projeto

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
```

### 2️⃣ Entrar na pasta do projeto

```bash
cd request-tracker-pi1
```

### 3️⃣ Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar o banco de dados

Crie um banco MySQL e atualize as credenciais no arquivo:

```
database.py
```

Exemplo:

```
host="localhost"
user="root"
password="sua_senha"
database="mydatabase"
```

### 5️⃣ Executar o sistema

```bash
python main.py
```

---

## 📊 Status do Projeto

🚧 Em desenvolvimento
Projeto acadêmico — Projeto Integrador I

---

## 📄 Licença

Projeto desenvolvido exclusivamente para fins educacionais.
