#!/usr/bin/env python3
import os
import subprocess
import sys

# Caminhos padrão
EXAMPLES_DIR = 'examples'
COMPILER_SCRIPT = 'aslan.py'

def clear_screen():
    """Limpa o terminal de forma multiplataforma."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_examples():
    """Retorna uma lista de arquivos .aslan no diretório de exemplos."""
    if not os.path.exists(EXAMPLES_DIR):
        return []
    return sorted([f for f in os.listdir(EXAMPLES_DIR) if f.endswith('.aslan')])

def run_example(filepath, theme='PADRAO'):
    """Exibe o código e executa um arquivo Aslan."""
    clear_screen()
    print(f"--- Visualizando Código: {os.path.basename(filepath)} ---")
    print("-" * 50)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            print(f.read())
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        input("\nPressione [ENTER] para voltar...")
        return

    print("-" * 50)
    input("\nPressione [ENTER] para executar o código...")
    print("\n--- Saída da Máquina Virtual Aslan ---")
    print("-" * 50)
    
    try:
        # Chama o compilador aslan.py via subprocesso
        cmd = [sys.executable, COMPILER_SCRIPT, filepath]
        if theme == 'NARNIA':
            cmd.append("--narnia")
        elif theme == 'LOTR':
            cmd.append("--lotr")
        result = subprocess.run(cmd, text=True)
    except Exception as e:
        print(f"\nFalha crítica ao executar o compilador: {e}")
        
    print("-" * 50)
    input("\nPressione [ENTER] para voltar ao menu principal...")

def create_custom_code(theme='PADRAO'):
    """Interface para digitar e rodar código Aslan customizado."""
    clear_screen()
    print("--- Editor Aslan Rápido ---")
    print("Instruções:")
    print("1. Digite seu código linha por linha.")
    print("2. Para finalizar e rodar, digite 'RUN' em uma linha vazia.")
    print("3. Para cancelar, digite 'QUIT' em uma linha vazia.")
    print("-" * 50)
    
    lines = []
    while True:
        try:
            line = input("> ")
            if line.strip().upper() == 'RUN':
                break
            if line.strip().upper() == 'QUIT':
                return
            lines.append(line)
        except EOFError:
            break
            
    if not lines:
        input("\nCódigo vazio. Pressione [ENTER] para voltar...")
        return

    custom_path = os.path.join(EXAMPLES_DIR, 'custom_temp.aslan')
    try:
        with open(custom_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        run_example(custom_path, theme)
    except Exception as e:
        print(f"Erro ao salvar arquivo temporário: {e}")
        input("\nPressione [ENTER] para voltar...")

def main():
    """Loop principal do menu."""
    themes = ['PADRAO', 'NARNIA', 'LOTR']
    current_theme_index = 0
    
    while True:
        theme = themes[current_theme_index]
        clear_screen()
        print("========================================")
        print("      ASLAN COMPILER - DEMO CLI         ")
        print("========================================")
        
        examples = get_examples()
        if not examples:
            print("\nNenhum arquivo .aslan encontrado em 'examples/'")
        else:
            print("\nExemplos Disponíveis:")
            for i, ex in enumerate(examples, 1):
                print(f" [{i}] {ex}")
                
        print("-" * 40)
        print(f" [M] Tema Atual: {theme}")
        print(" [N] Novo código (Criar e Rodar)")
        print(" [Q] Sair")
        print("-" * 40)
        
        try:
            choice = input("\nEscolha uma opção: ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\nSaindo...")
            break
            
        if choice == 'Q':
            print("Saindo do demo. Até logo!")
            break
        elif choice == 'M':
            current_theme_index = (current_theme_index + 1) % len(themes)
        elif choice == 'N':
            create_custom_code(theme)
        elif choice.isdigit() and 1 <= int(choice) <= len(examples):
            selected_file = examples[int(choice) - 1]
            run_example(os.path.join(EXAMPLES_DIR, selected_file), theme)
        else:
            print("\nOpção inválida!")
            import time
            time.sleep(1)

if __name__ == '__main__':
    main()
