# Compilador Didático em Python

Este projeto documenta o desenvolvimento de um compilador completo para uma linguagem de programação simples, utilizando apenas Python e suas bibliotecas padrão. O objetivo é aplicar os conceitos teóricos de compiladores de forma prática.

## Estrutura do Projeto

```
/
|-- lexer.py            # Fase 1: Analisador Léxico
|-- parser_.py          # Fase 2: Analisador Sintático e AST
|-- semantic.py         # Fase 3: Analisador Semântico e Tabela de Símbolos
|-- test_runner.py      # Executor de testes automatizados
|-- tests/              # Diretório com os casos de teste
|   |-- test_lexer.py
|   |-- test_parser.py
|   |-- test_semantic.py
|   |-- test_regressive.py # Testes de regressão e fumaça
|-- .gitignore          # Arquivos ignorados pelo Git
|-- requirerimentos-compilador.pdf # O documento original de requisitos
|-- README.md           # Este arquivo
|-- PROJECT_STATUS.md   # Checkpoint de desenvolvimento
```

## Como Executar os Testes

Para validar a implementação a qualquer momento, execute o `test_runner` a partir do diretório raiz. Ele descobrirá e rodará todos os testes unitários e regressivos.

```sh
python3 test_runner.py
```

---

## Progresso Atual

Adotamos uma metodologia de Desenvolvimento Orientado a Testes (TDD), garantindo que cada funcionalidade seja validada antes de prosseguirmos.

### ✅ Fase 1: Análise Léxica (Concluída)

-   **Funcionalidades:** Suporte a todas as palavras-chave, operadores aritméticos/lógicos, literais (int, bool, string) e comentários.

### ✅ Fase 2: Análise Sintática (Concluída)

-   **Funcionalidades:** 
    -   Construção de AST para expressões complexas com precedência.
    -   Suporte a comandos: `if-else`, `while`, `print`, `read` e atribuição simples.
    -   Tratamento de blocos de código `{...}`.

### ✅ Fase 3: Análise Semântica (Concluída)

-   **Arquivo:** `semantic.py`
-   **Descrição:** Valida a lógica do programa e a consistência dos dados.
-   **Funcionalidades:**
    -   **Tabela de Símbolos:** Gerenciamento de escopos aninhados e detecção de redeclaração.
    -   **Verificação de Declaração:** Garante que variáveis sejam declaradas antes do uso.
    -   **Verificação de Tipos (Type Checking):** Valida compatibilidade em atribuições, operações binárias e condições de controle (`if`/`while`).

### ✅ Fase 4: Geração de Código Intermediário (Concluída)

-   **Arquivo:** `ir_generator.py`
-   **Descrição:** Traduz a AST para Código de Três Endereços (TAC).
-   **Funcionalidades:**
    -   **TAC:** Geração de instruções simples como `(OP, arg1, arg2, result)`.
    -   **Temporários:** Alocação dinâmica de variáveis temporárias para expressões.
    -   **Labels e Jumps:** Implementação de controle de fluxo (`if`, `while`) através de saltos condicionais e incondicionais.

### ✅ Fase 5: Geração de Código Final e Execução (Concluída)

-   **Arquivos:** `code_generator.py` e `vm.py`
-   **Descrição:** Traduz o TAC para um Bytecode customizado e o executa em uma Máquina Virtual baseada em pilha.
-   **Funcionalidades:**
    -   **Bytecode:** Conjunto de instruções para manipulação de pilha, aritmética, controle de fluxo e E/S.
    -   **VM:** Máquina Virtual completa com pilha de operandos, memória de variáveis e Program Counter.
    -   **E2E:** Validação completa do pipeline, permitindo a execução real de algoritmos como o Fatorial.

---

## Conclusão do Projeto

O projeto atingiu 100% dos requisitos obrigatórios, com um total de **47 testes automatizados** validando cada etapa do processo de compilação.
