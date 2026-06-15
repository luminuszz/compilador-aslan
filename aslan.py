#!/usr/bin/env python3
import argparse
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from code_generator import CodeGenerator
from ir_generator import IRGenerator
from lexer import Lexer
from lexer_narnia import LexerNarnia
from lexer_lotr import LexerLotr
from optimizer import Optimizer
from parser_ import Parser
from semantic import SemanticAnalyzer
from vm import VirtualMachine


def run(source_code, optimize=True, debug=False, use_narnia=False, use_lotr=False):
    try:
        if debug:
            print("--- TOKENS ---")

        if use_narnia:
            lexer = LexerNarnia(source_code)
        elif use_lotr:
            lexer = LexerLotr(source_code)
        else:
            lexer = Lexer(source_code)
            
        tokens = lexer.tokenize()

        if debug:
            for t in tokens:
                print(t)

        if debug:
            print("\n--- PARSING ---")

        parser = Parser(tokens)
        ast = parser.parse()

        if optimize:
            if debug:
                print("\n--- OPTIMIZING ---")
            optimizer = Optimizer()
            ast = optimizer.visit(ast)

        if debug:
            print("\n--- SEMANTIC ANALYSIS ---")

        analyzer = SemanticAnalyzer()
        analyzer.visit(ast)

        if debug:
            print("\n--- IR GENERATION ---")

        ir_gen = IRGenerator()
        tac = ir_gen.visit(ast)

        if debug:
            for instr in tac:
                print(instr)

        if debug:
            print("\n--- CODE GENERATION ---")

        code_gen = CodeGenerator(tac)
        bytecode = code_gen.generate()

        if debug:
            print(bytecode)

        if debug:
            print("\n--- EXECUTION ---")

        vm = VirtualMachine(bytecode)
        vm.run()

    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        if debug:
            import traceback

            traceback.print_exc()
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Compilador e VM da Linguagem Aslan")
    parser.add_argument("filename", help="Arquivo .aslan para executar")
    parser.add_argument(
        "--no-optimize",
        action="store_false",
        dest="optimize",
        help="Desativar otimizações",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Exibir informações de depuração"
    )
    parser.add_argument(
        "--narnia", "-n", action="store_true", help="Usar a sintaxe temática de Nárnia"
    )
    parser.add_argument(
        "--lotr", "-l", action="store_true", help="Usar a sintaxe temática de Senhor dos Anéis"
    )

    args = parser.parse_args()

    if not os.path.exists(args.filename):
        print(f"Erro: Arquivo '{args.filename}' não encontrado.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.filename, "r", encoding="utf-8") as f:
            source_code = f.read()
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}", file=sys.stderr)
        sys.exit(1)

    run(source_code, optimize=args.optimize, debug=args.debug, use_narnia=args.narnia, use_lotr=args.lotr)


if __name__ == "__main__":
    main()
