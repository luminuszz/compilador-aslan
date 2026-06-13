# Compilador Didático em Python

Este projeto documenta o desenvolvimento de um compilador completo para uma linguagem de programação simples, utilizando apenas Python e suas bibliotecas padrão. O objetivo é aplicar os conceitos teóricos de compiladores de forma prática.

## Estrutura do Projeto

```
/
|-- lexer.py            # Fase 1: Analisador Léxico
|-- parser_.py          # Fase 2: Analisador Sintático e AST
|-- test_runner.py      # Executor de testes automatizados
|-- tests/              # Diretório com os casos de teste
|   |-- test_lexer.py
|   |-- test_parser.py
|-- requirerimentos-compilador.pdf # O documento original de requisitos
|-- README.md           # Este arquivo
```

## Como Executar os Testes

Para validar a implementação a qualquer momento, execute o `test_runner` a partir do diretório raiz. Ele descobrirá e rodará todos os testes unitários das fases concluídas.

```sh
python3 test_runner.py
```

---

## Progresso Atual

Adotamos uma metodologia de Desenvolvimento Orientado a Testes (TDD), garantindo que cada funcionalidade seja validada antes de prosseguirmos.

### ✅ Fase 1: Análise Léxica (Concluída)

-   **Arquivo:** `lexer.py`
-   **Descrição:** O analisador léxico foi implementado e exaustivamente testado. Ele processa o código-fonte e o converte em uma sequência de tokens.
-   **Funcionalidades:**
    -   Reconhecimento de palavras-chave (`if`, `while`, `int`, etc.).
    -   Reconhecimento de operadores aritméticos e de comparação.
    -   Análise de literais (números, strings, booleanos).
    -   Capacidade de ignorar espaços em branco e comentários.
    -   Relatório de erros para caracteres inválidos, com indicação de linha e coluna.

### ✅ Fase 2: Análise Sintática (Concluída)

-   **Arquivo:** `parser_.py`
-   **Descrição:** O analisador sintático valida a sequência de tokens de acordo com a gramática da linguagem e constrói uma Árvore de Sintaxe Abstrata (AST) para representar a estrutura do programa.
-   **Funcionalidades:**
    -   **Análise de Expressões:** Lida com expressões aritméticas e de comparação, respeitando a **precedência de operadores** (ex: `*` antes de `+`) e o uso de **parênteses**.
    -   **Declarações de Variáveis:** Consegue analisar `int x = ...;`.
    -   **Estruturas de Controle:** Implementado o parsing para o comando `if` e blocos de código aninhados (`{...}`).

---

## Próximas Etapas

### ➡️ Fase 3: Análise Semântica

O próximo grande passo é garantir que o código, embora sintaticamente correto, também faça sentido lógico.
-   **Tabela de Símbolos:** Criar uma estrutura para registrar todas as variáveis declaradas, seus tipos e escopos.
-   **Verificação de Tipos:** Garantir que as operações sejam válidas (ex: não permitir `10 + true`).
-   **Verificação de Escopo:** Garantir que uma variável não seja usada fora de onde foi declarada ou antes de ser declarada.

### 🔲 Fase 4: Geração de Código Intermediário (IR)

Após a validação semântica, a AST será traduzida para uma representação de baixo nível, independente de máquina, como o **Código de Três Endereços (TAC)**.

### 🔲 Fase 5: Geração de Código Final

A etapa final será traduzir o código intermediário para algo executável. O plano é gerar um **Bytecode** customizado e construir uma pequena **Máquina Virtual (VM)** em Python para executá-lo.
