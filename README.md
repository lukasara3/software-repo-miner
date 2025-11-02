# PR-Profiler: O Perfilador de Processos do GitHub
## 1. Membros do Grupo

* Artur Fonseca de Souza
* Bruno Soares e Silva
* Lucas Araújo de Macedo e Silva

Este projeto é parte do Trabalho Prático da disciplina de Mineração de Repositórios de Software. Nosso objetivo é identificar problemas de manutenção de software através da mineração do *processo* de desenvolvimento, em vez de apenas do código-fonte.

## 2. Explicação do Sistema

O **PR-Profiler** é uma ferramenta de linha de comando (CLI) que minera repositórios do GitHub para diagnosticar problemas de fluxo de trabalho (workflow) que impactam a manutenção.

Enquanto ferramentas tradicionais focam no *código* (complexidade, bugs), nossa ferramenta foca no *processo* (colaboração, gargalos).

**O Diferencial: Métricas vs. Diagnósticos**

Nossa ferramenta não se limita a exibir métricas básicas (como "tempo médio de review"). O `PR-Profiler` ativamente classifica Pull Requests (PRs) em **Anti-Padrões de Processo** — diagnósticos claros de problemas de manutenção que consomem o tempo da equipe.

Nossa CLI irá se conectar à API do GitHub e identificar padrões como:

* **Anti-Padrão 1: "O PR Muro de Texto" (The Wall-of-Text PR)**
    * **Diagnóstico:** PRs gigantescos (ex: > 1000 linhas alteradas).
    * **Problema de Manutenção:** Impossíveis de revisar com qualidade, alto risco de injetar bugs, desestimulam revisores.

* **Anti-Padrão 2: "O PR Fantasma" (The Ghost PR)**
    * **Diagnóstico:** PRs abertos há muito tempo (ex: > 10 dias) sem *nenhum* comentário ou revisão.
    * **Problema de Manutenção:** Trabalho abandonado? Falta de visibilidade? Desperdício de esforço de desenvolvimento.

* **Anti-Padrão 3: "O PR Bicicleta" (The Bikeshedding PR)**
    * **Diagnóstico:** PRs com um número desproporcional de comentários para pouquíssimas linhas alteradas.
    * **Problema de Manutenção:** O time está gastando energia em debates triviais (bikeshedding) em vez de focar no que importa.

* **Anti-Padrão 4: "O PR Vácuo" (The Review Vacuum)**
    * **Diagnóstico:** PRs que solicitam revisão (review requested) mas ficam dias sem a primeira resposta.
    * **Problema de Manutenção:** Gargalo claro no processo; desenvolvedores ficam bloqueados esperando por feedback.

Ao focar em diagnósticos acionáveis, o `PR-Profiler` cumpre o objetivo de identificar "problemas de manutenção" de forma muito mais direta.

## 3. Tecnologias Utilizadas (Proposta Inicial)

* **Linguagem de Programação:** Python 3
* **Fonte de Dados:** GitHub API 
* **Interação com API:** **PyGithub** (para facilitar a autenticação e chamadas à API REST)
* **Interface de Linha de Comando (CLI):** **Typer** (para criar a CLI de forma rápida e moderna)
* **Apresentação de Dados (Opcional):** Biblioteca `rich` (para tabelas e cores bonitas no terminal)
* **Autenticação:** Token de Acesso Pessoal (PAT) do GitHub, fornecido pelo usuário.
