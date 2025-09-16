# MSR-Analyzer: Ferramenta para Análise de Manutenibilidade de Software

Este projeto é parte do Trabalho Prático da disciplina de Mineração de Repositórios de Software.

## 1. Membros do Grupo

* Artur Fonseca de Souza
* Bruno Soares e Silva
* Lucas Araújo de Macedo e Silva

## 2. Explicação do Sistema

Nossa ferramenta é uma ferramente de linha de comando (CLI) projetada para identificar potenciais problemas de manutenção em repositórios de software. O principal objetivo da ferramenta é localizar "hotspots" de código — arquivos que representam um alto risco para a manutenção do projeto.

Um **hotspot** é definido como um arquivo que possui duas características principais:
1.  **Alta Complexidade:** O código é estruturalmente complexo (ex: muitos `if`s, `for`s, aninhamentos), tornando-o difícil de entender e modificar.
2.  **Alta Frequência de Mudança:** O arquivo é alterado com muita frequência ao longo do histórico do projeto, indicando que ele é uma parte instável ou central do sistema.

Arquivos com ambas as características são os principais candidatos a introduzir bugs e a consumir um esforço desproporcional da equipe de desenvolvimento. Nossa ferramenta irá analisar um repositório Git, calcular essas métricas e apresentar um ranking de arquivos para que os desenvolvedores possam focar seus esforços de refatoração e testes nas áreas mais críticas.

## 3. Tecnologias Utilizadas (Proposta Inicial)

Para o desenvolvimento desta ferramenta, planejamos utilizar o seguinte conjunto de tecnologias:

* **Linguagem de Programação:** **Python 3**, devido ao seu robusto ecossistema de bibliotecas para análise de dados e de código.

* **Análise de Histórico de Repositório (Git):** **Pydriller**. Escolhemos esta biblioteca por sua API de alto nível que simplifica a iteração sobre commits, branches e a extração de metadados de um repositório Git. Ela nos permite, de forma eficiente, calcular a frequência de alteração de cada arquivo.

* **Análise de Complexidade de Código:** **Lizard**. É uma ferramenta leve e rápida para análise de complexidade ciclomática. Por ser uma ferramenta externa que pode ser chamada via linha de comando ou como biblioteca, ela se integra facilmente ao nosso fluxo de trabalho para medir a complexidade dos arquivos identificados pelo Pydriller.

* **Interface de Linha de Comando (CLI):** **Typer**. Baseado no `click` e em type hints do Python, o Typer nos permite criar uma CLI moderna, com autocompletar e uma interface de usuário clara com mínimo esforço de programação.

* **Gerenciamento de Dependências:** `pip` com `requirements.txt` ou `Poetry` para garantir um ambiente de desenvolvimento consistente.
