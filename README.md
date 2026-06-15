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
|-- aslan.py             # Script principal de execução
|-- demo.py              # Script interativo de demonstração
|-- test_runner.py       # Executor central de testes
|-- DOCS.md              # Documentação técnica detalhada
|-- examples/            # Galeria de exemplos (.aslan)
|-- tests/               # Suíte de testes (74 casos automatizados)
|-- .gitignore           # Configurações de repositório
|-- README.md            # Guia de apresentação e visão geral
```

## 🎮 Demonstração Interativa e Temas

Para explorar os exemplos da linguagem e criar seus próprios códigos de forma interativa, execute:

```sh
python3 demo.py
```

O script permite listar exemplos clássicos (Fibonacci, Ordenação, etc.), visualizar o código-fonte e rodá-los imediatamente na VM. Você também pode alternar entre os **Temas de Sintaxe**:

1. **Padrão**: Inglês tradicional (int, if, while).
2. **Nárnia**: Inspirado nas Crônicas de Nárnia (rei_pedro, pela_juba_do_leao). Pode ser rodado no terminal com `python3 aslan.py arquivo.aslan --narnia`
3. **Senhor dos Anéis**: Inspirado na luta de Gandalf e o Balrog (poder_maia, nao_passara). Pode ser rodado no terminal com `python3 aslan.py arquivo.aslan --lotr`

## 🛠️ Como Executar os Testes

Para validar a integridade de todas as fases do compilador, execute:

```sh
python3 test_runner.py
```

## 📝 Documentação Detalhada (Módulos)

Para uma análise profunda de cada classe, método e complexidade Big-O de cada etapa, consulte o arquivo **[DOCS.md](./DOCS.md)**.

