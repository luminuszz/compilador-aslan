# 🚀 Guia do Meu Compilador

Este documento explica como o nosso compilador funciona, como se fosse uma "receita de bolo" dividida em etapas.

## O que é este projeto?
Estamos criando um tradutor que pega um código escrito por nós (em uma linguagem simples que criamos) e o valida para que, no futuro, ele possa ser executado.

---

## 🛠 As Engrenagens (Fases Concluídas)

### 1. O Analisador Léxico (`lexer.py`) - "O Leitor de Palavras"
Imagine que você está lendo um livro. Antes de entender a história, seu cérebro identifica o que é uma palavra, o que é um ponto e o que é um número.
*   **O que ele faz:** Ele lê o arquivo de texto caractere por caractere e agrupa tudo em **Tokens**.
*   **Exemplo:** Se ele vê `int x = 10;`, ele gera os tokens: `[INT, IDENTIFICADOR(x), IGUAL, NUMERO(10), PONTO_VIRGULA]`.
*   **O que ele ignora:** Espaços em branco e comentários (como o `// comentário`).

### 2. O Analisador Sintático (`parser_.py`) - "O Gramático"
Aqui, o compilador verifica se a ordem das palavras faz sentido segundo as regras da nossa língua.
*   **O que ele faz:** Ele pega os tokens do Lexer e monta uma **AST (Árvore de Sintaxe Abstrata)**. É como um mapa que mostra que o `10` pertence à variável `x`.
*   **Exemplo:** Ele garante que você não escreveu `= 10 x int;`, pois isso não faz sentido gramatical.
*   **Precedência:** Ele sabe que `2 + 3 * 4` deve calcular a multiplicação primeiro.

### 3. O Analisador Semântico (`semantic.py`) - "O Inspetor de Lógica"
Um código pode estar gramaticalmente correto, mas ser um absurdo lógico. Exemplo: "O gato bebeu o carro". A frase está certa, mas a lógica está errada.
*   **Tabela de Símbolos:** É um "caderninho" onde o compilador anota o nome de toda variável que você criou e o tipo dela (`int` ou `bool`).
*   **Verificação de Erros:**
    *   Ele avisa se você tentar usar uma variável que nunca declarou.
    *   Ele avisa se você tentar somar um número com um valor booleano (ex: `10 + true`).
    *   Ele impede que você crie duas variáveis com o mesmo nome no mesmo lugar.

---

## 📂 Resumo dos Arquivos

| Arquivo | Função |
| :--- | :--- |
| `lexer.py` | Transforma texto em "peças" (tokens). |
| `parser_.py` | Organiza as peças em uma estrutura de árvore (AST). |
| `semantic.py` | Checa se as operações e variáveis fazem sentido lógico. |
| `main.py` | O "botão de ligar" que executa todas as fases acima em sequência. |
| `test_runner.py` | Roda testes automáticos para garantir que nada quebrou. |

---

## 🏃‍♂️ Como usar agora?

1.  **Para testar um código seu:**
    Abra o arquivo `main.py`, coloque o seu código na variável `exemploDeTravestir` e execute:
    ```bash
    python main.py
    ```

2.  **Para conferir se tudo está funcionando bem:**
    Execute o comando abaixo para rodar todos os testes de segurança:
    ```bash
    python test_runner.py
    ```

---

## 🚩 O que falta?
Agora que já sabemos que o código é válido, precisamos de um **Gerador de Código** (`codegen.py`), que vai transformar essa árvore em instruções que o computador realmente consiga rodar (Bytecode).