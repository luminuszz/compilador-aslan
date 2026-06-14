# Compilador Didático em Python

Este projeto documenta o desenvolvimento de um compilador completo para uma linguagem de programação simples, utilizando apenas Python e suas bibliotecas padrão. O objetivo é aplicar os conceitos teóricos de compiladores de forma prática.

## Estrutura do Projeto

```
/
|-- lexer.py            # Fase 1: Analisador Léxico
|-- parser_.py          # Fase 2: Analisador Sintático e AST
|-- semantic.py         # Fase 3: Analisador Semântico e Tabela de Símbolos
|-- optimizer.py        # Fase de Bônus: Otimizador de AST (Constant Folding)
|-- ir_generator.py     # Fase 4: Gerador de Código Intermediário (TAC)
|-- code_generator.py   # Fase 5: Gerador de Bytecode
|-- vm.py               # Fase 5: Máquina Virtual baseada em pilha
|-- test_runner.py      # Executor de testes automatizados
|-- tests/              # Diretório com os casos de teste (56 testes)
|   |-- test_lexer.py
|   |-- test_parser.py
|   |-- test_semantic.py
|   |-- test_optimizer.py
|   |-- test_ir_generator.py
|   |-- test_vm.py
|   |-- test_regressive.py
|   |-- test_stress.py
|   |-- test_leetcode.py
|-- .gitignore          # Arquivos ignorados pelo Git
|-- requirerimentos-compilador.pdf # O documento original de requisitos
|-- README.md           # Este arquivo
|-- PROJECT_STATUS.md   # Checkpoint final do projeto
```

## Como Executar os Testes

Para validar a implementação a qualquer momento, execute o `test_runner` a partir do diretório raiz. Ele descobrirá e rodará todos os testes unitários, regressivos e de estresse.

```sh
python3 test_runner.py
```

---

## Progresso Atual

Adotamos uma metodologia de Desenvolvimento Orientado a Testes (TDD), garantindo que cada funcionalidade seja validada antes de prosseguirmos.

### ✅ Fase 1: Análise Léxica (Concluída)
Suporte a palavras-chave, operadores, literais e comentários.

### ✅ Fase 2: Análise Sintática (Concluída)
Construção de AST para expressões complexas e estruturas de controle (`if`, `while`, `print`, `read`).

### ✅ Fase 3: Análise Semântica (Concluída)
Gerenciamento de escopos e Verificação de Tipos (Type Checking).

### ✅ Fase de Bônus: Otimização (Concluída)
Implementação de **Constant Folding**. O compilador simplifica expressões constantes (ex: `2 + 2` vira `4`) em tempo de compilação, gerando um código mais eficiente para a VM.

### ✅ Fase 4: Geração de Código Intermediário (Concluída)
Tradução da AST para Código de Três Endereços (TAC) com gerenciamento de temporários e labels.

### ✅ Fase 5: Geração de Código Final e Execução (Concluída)
Tradução para Bytecode customizado e execução em uma Máquina Virtual (VM) robusta.

---

## Conclusão do Projeto

O projeto superou 100% dos requisitos originais, incluindo o bônus de otimização e algoritmos complexos (Fibonacci, Bubble Sort), com um total de **56 testes automatizados** garantindo a integridade do sistema.
