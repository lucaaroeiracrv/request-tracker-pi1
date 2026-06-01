# Documentação Pessoal de Participação no Projeto

## Introdução

Neste documento, apresento minha participação individual no desenvolvimento do projeto **request-tracker-pi1**, com base exclusivamente na análise do histórico de commits do repositório, considerando as branches disponíveis e os registros atribuídos ao meu usuário no GitHub (**lucaaroeiracrv**).

A partir dessa análise, foi possível identificar minhas contribuições principalmente na **estruturação inicial do sistema**, na **configuração e integração com banco de dados**, na **evolução das funcionalidades centrais da aplicação**, na **organização da documentação técnica** e na **melhoria da clareza do código por meio de comentários internos**.

Ressalto que esta documentação foi elaborada apenas com base no que pode ser deduzido objetivamente pelos commits e arquivos alterados. Quando alguma interpretação depende de inferência limitada, isso é indicado de forma explícita.

---

## Objetivo da minha participação no projeto

Minha participação no projeto teve como objetivo contribuir para a construção da base técnica da aplicação, estruturando o sistema em Python, organizando a conexão com o banco de dados e implementando funcionalidades relacionadas ao gerenciamento de usuários e de solicitações.

Além disso, atuei na melhoria da configuração do ambiente de execução, na documentação do projeto e na organização interna do código, de modo a tornar o sistema mais utilizável, compreensível e próximo de uma versão funcional.

---

## Principais atividades realizadas

Com base nos commits identificados em meu nome, minhas principais atividades no projeto foram:

- criação da estrutura inicial do projeto;
- implementação da conexão com o banco de dados;
- definição e criação das tabelas principais do sistema;
- evolução da lógica de cadastro e autenticação de usuários;
- implementação do gerenciamento completo de solicitações;
- criação de regras de validação e priorização automática;
- adição de consultas e estatísticas relacionadas às solicitações;
- configuração do ambiente com variáveis externas;
- melhoria da documentação do repositório;
- inserção de comentários explicativos em múltiplos arquivos para facilitar manutenção e entendimento.

---

## Tecnologias e ferramentas que utilizei

Pelos commits e pelos arquivos modificados, é possível afirmar que utilizei as seguintes tecnologias e ferramentas:

- **Python** como linguagem principal do projeto;
- **MySQL** como sistema de banco de dados;
- **SQL** para definição do schema e estrutura das tabelas;
- **python-dotenv** para carregamento de variáveis de ambiente;
- **bcrypt** para hash e verificação de senhas;
- **Git e GitHub** para versionamento, organização em branches e registro das entregas;
- arquivos de apoio como **README.md**, **.gitignore**, **.env.example** e **schema.sql** para documentação e configuração do ambiente.

Também é possível identificar o uso de uma arquitetura simples separada por responsabilidades, com arquivos como:

- `main.py`
- `database.py`
- `services.py`
- `auth.py`
- `schema.sql`

---

## Alterações implementadas com base nos commits

A análise dos commits atribuídos ao meu usuário indica a seguinte sequência de contribuições relevantes:

### 1. Estruturação inicial do projeto

Nos commits iniciais, fui responsável por estabelecer a base do sistema. Isso inclui:

- criação da estrutura inicial do projeto;
- definição da conexão com banco de dados;
- organização dos primeiros arquivos do sistema.

Essa etapa demonstra minha atuação na fundação técnica da aplicação, permitindo que as demais funcionalidades fossem desenvolvidas posteriormente.

### 2. Implementação da camada de banco de dados

Também identifiquei contribuição direta na evolução do arquivo `database.py`, especialmente para:

- adaptação da execução de queries com parâmetros;
- distinção entre consultas `SELECT` e operações de escrita;
- tratamento mais adequado da execução das instruções SQL;
- suporte ao commit em operações que modificam dados.

Com isso, a interação com o banco de dados passou a ser mais segura e funcional para o restante do sistema.

### 3. Criação e ajuste da tabela de usuários

Nos commits analisados, há evidência de implementação da tabela `users`, incluindo campos como:

- identificador;
- nome;
- e-mail;
- senha;
- telefone.

Posteriormente, também houve evolução da lógica relacionada ao armazenamento da senha e ao tratamento de cadastro de usuários.

### 4. Configuração do ambiente com variáveis externas

Uma contribuição importante foi a substituição de credenciais fixas no código por variáveis de ambiente, com:

- uso de `dotenv`;
- leitura de `DB_HOST`, `DB_USER`, `DB_PASSWORD` e `DB_NAME`;
- criação de `.env.example`;
- criação de `.gitignore` para evitar versionamento indevido de arquivos sensíveis.

Essa alteração melhorou a organização do projeto e tornou a aplicação mais adequada para execução em diferentes ambientes.

### 5. Implementação do gerenciamento de usuários e solicitações

A contribuição mais expressiva identificada no histórico foi a implementação de um conjunto amplo de funcionalidades relacionadas ao fluxo principal do sistema. Entre elas, destaco:

- cadastro de usuários com validações;
- login de usuários com verificação de senha;
- listagem de usuários;
- criação de solicitações;
- listagem geral de solicitações;
- filtragem por status;
- filtragem por prioridade;
- filtragem por usuário;
- atualização de status;
- geração de estatísticas por status;
- geração de estatísticas por prioridade.

Essa etapa evidencia minha participação direta no desenvolvimento das regras de negócio mais relevantes do sistema.

### 6. Implementação de validações de negócio

Pelos commits, também é possível observar minha atuação em validações importantes, como:

- verificação de nome obrigatório no cadastro;
- exigência de pelo menos um meio de contato;
- validação de formato de e-mail;
- validação de senha mínima;
- prevenção de duplicidade de e-mail;
- validação de categoria da solicitação;
- validação de descrição obrigatória;
- validação de urgência e impacto em faixa numérica definida;
- restrições para transição de status.

Essas implementações contribuíram para maior consistência dos dados e previsibilidade do comportamento do sistema.

### 7. Priorização automática das solicitações

Identifiquei ainda a implementação de uma regra de negócio para cálculo automático da prioridade das solicitações com base em:

- urgência;
- impacto.

A prioridade passou a ser classificada em níveis como:

- **Baixa**
- **Média**
- **Alta**

Essa funcionalidade mostra participação não apenas estrutural, mas também na modelagem da lógica funcional do sistema.

### 8. Modelagem e documentação do banco de dados

Houve também contribuição direta na criação do arquivo `schema.sql`, com definição das tabelas principais do sistema, incluindo:

- tabela `users`;
- tabela `requests`;
- relacionamento entre as tabelas com chave estrangeira;
- uso de `ON DELETE CASCADE`.

Além disso, o README foi ampliado com explicações sobre:

- estrutura do projeto;
- setup do ambiente;
- configuração das variáveis;
- modelagem do banco;
- regras de prioridade;
- estado atual do sistema.

### 9. Organização e legibilidade do código

Em commit posterior, adicionei comentários explicativos em múltiplos arquivos, como:

- `auth.py`
- `database.py`
- `main.py`
- `services.py`

Esses comentários tiveram função de tornar o código mais legível, compreensível e fácil de manter, o que também representa uma contribuição importante em contexto acadêmico e colaborativo.

---

## Desafios encontrados e como foram resolvidos

Com base nos commits, alguns desafios enfrentados durante minha participação podem ser identificados de forma objetiva:

### 1. Estruturar corretamente a persistência de dados

No início do projeto, foi necessário organizar a conexão com o banco e a execução das queries. Isso foi resolvido por meio da evolução da classe de banco de dados, com melhoria no método de execução e no tratamento entre leitura e escrita.

### 2. Evitar exposição de credenciais no código

O uso inicial de dados fixos de conexão representava uma limitação técnica. Esse problema foi resolvido com a adoção de variáveis de ambiente, do arquivo `.env.example` e do carregamento via `dotenv`.

### 3. Garantir consistência no cadastro de usuários

O cadastro precisou ser ajustado para validar nome, senha, e-mail e duplicidade de registro. A solução foi implementar verificações específicas e tratamento para erro de unicidade no banco.

### 4. Organizar a lógica de solicitações com regras claras

O sistema precisava deixar de ser apenas estrutural e passar a oferecer um fluxo funcional de uso. Isso foi resolvido com a implementação de operações completas para criação, consulta, filtragem, atualização e estatísticas das solicitações.

### 5. Melhorar a compreensão e manutenção do código

À medida que o projeto cresceu, tornou-se importante tornar o código mais fácil de entender. Esse desafio foi enfrentado com a inclusão de comentários internos e com o reforço da documentação do projeto no README.

---

## Conclusão sobre a minha contribuição no projeto

Com base na análise do histórico de commits em meu nome, concluo que minha contribuição no projeto foi significativa principalmente na **base estrutural e funcional da aplicação**.

Participei desde a etapa inicial de organização do sistema até a implementação de funcionalidades centrais, com destaque para:

- estruturação do projeto;
- integração com banco de dados;
- criação da lógica de usuários;
- desenvolvimento do gerenciamento de solicitações;
- validações de negócio;
- configuração de ambiente;
- documentação técnica;
- melhoria da legibilidade do código.

De forma geral, minha atuação esteve concentrada em transformar o projeto em uma aplicação mais completa, organizada e executável, contribuindo tanto para o funcionamento do sistema quanto para sua documentação e manutenção.

Por fim, também é importante registrar que a análise dos commits permite identificar com clareza várias entregas técnicas realizadas por mim, mas não permite afirmar, com total precisão, aspectos subjetivos como decisões de equipe, discussões internas ou autoria compartilhada de ideias que não tenham ficado registradas diretamente no histórico do repositório.