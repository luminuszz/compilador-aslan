<p align="center">
  <img src="./images/image-removebg-preview.png" alt="Compiler Logo" width="144">
</p>

# Compilador ASLAN

Este projeto consiste no desenvolvimento de um compilador completo para uma linguagem de programação imperativa simples

## 👥 Integrantes
- Alison Oliveira
- Maria Clara
- Davi Ribeiro

## 🚀 Estrutura do Projeto

```
/
|-- src/
|   |-- lexer.py            # Fase 1: Analisador Léxico (Scanner)
|   |-- parser_.py          # Fase 2: Analisador Sintático (Parser) e AST
|   |-- semantic.py         # Fase 3: Analisador Semântico e Tabela de Símbolos
|   |-- optimizer.py        # Bônus: Otimizador de AST (Constant Folding)
|   |-- ir_generator.py     # Fase 4: Gerador de Código Intermediário (TAC)
|   |-- code_generator.py   # Fase 5: Gerador de Bytecode
|   |-- vm.py               # Fase 5: Máquina Virtual (Stack Machine)
|-- test_runner.py      # Executor central de testes
|-- DOCS.md             # Documentação técnica detalhada
|-- tests/              # Suíte de testes (61 casos automatizados)
|-- .gitignore          # Configurações de repositório
|-- README.md           # Guia de apresentação e visão geral
```

## 🛠️ Como Executar os Testes

Para validar a integridade de todas as fases do compilador, execute:

```sh
python3 test_runner.py
```

## 📝 Documentação Detalhada (Módulos)

Para uma análise profunda de cada classe, método e complexidade Big-O de cada etapa, consulte o arquivo **[DOCS.md](./DOCS.md)**.

