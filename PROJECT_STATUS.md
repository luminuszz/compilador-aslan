# Checkpoint do Projeto Compilador

Este documento salva o estado do desenvolvimento para referência futura.

**Data do Checkpoint:** 13 de Junho de 2026

## Resumo

Finalizamos com sucesso as duas primeiras fases do compilador (Análise Léxica e Sintática), seguindo uma metodologia TDD. O projeto está em um estado estável, com todos os 14 testes passando.

## Última Etapa Concluída: Fase 2 (Análise Sintática)

O parser foi a última parte implementada. Ele é capaz de:
- Analisar expressões aritméticas e de comparação complexas.
- Respeitar a precedência de operadores (ex: `*` antes de `+`).
- Lidar com o agrupamento forçado por parênteses.
- Analisar estruturas de controle `if` e blocos de código aninhados (`{...}`).
- Construir uma Árvore de Sintaxe Abstrata (AST) que reflete a estrutura do código.

## Estado dos Arquivos

- **`lexer.py`**: Concluído e estável.
- **`parser_.py`**: Concluído e estável para os requisitos atuais.
- **`test_runner.py`**: Concluído e funcional.
- **`tests/test_lexer.py`**: Concluído, 8 testes passando.
- **`tests/test_parser.py`**: Concluído, 6 testes passando.

## Próximo Passo Imediato

O trabalho será retomado no início da **Fase 3: Análise Semântica**.

1.  **Ação a ser tomada:** Criar o arquivo `semantic.py`.
2.  **Primeira Tarefa:** Dentro de `semantic.py`, implementar as classes `TabelaDeSimbolos` (para gerenciar escopos e variáveis) e `AnalisadorSemantico` (que irá percorrer a AST).
3.  **Primeiro Teste:** Criar o arquivo `tests/test_semantic.py` e adicionar um caso de teste que verifique se o `AnalisadorSemantico` levanta um `SemanticError` ao tentar usar uma variável que não foi declarada.



```sh
gemini --resume 685c0e7f-f9d3-4178-8401-78c070c60687
```
