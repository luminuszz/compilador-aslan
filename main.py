from lexer import Lexer, LexerError
from parser_ import Parser, ParserError
from semantic import SemanticAnalyzer, SemanticError

def compilar(codigo_fonte):
    print("--- Iniciando Compilação ---")
    
    try:
      
        print("[1] Executando Análise Léxica...")
        lexer = Lexer(codigo_fonte)
        tokens = lexer.tokenize()
        
        
        print("[2] Executando Análise Sintática (Gerando AST)...")
        parser = Parser(tokens)
        ast = parser.parse()
        
      
        print("[3] Executando Análise Semântica...")
        analyzer = SemanticAnalyzer()
        analyzer.visit(ast)
        
        print("\n Sucesso: O código é válido léxica, sintática e semanticamente!")
        
    except (LexerError, ParserError, SemanticError) as e:
        print(f"\n❌ Erro durante a compilação:\n{e}")
    except Exception as e:
        print(f"\n Erro inesperado: {e}")

if __name__ == "__main__":
    
    exemploDeTravestir = """
    int x = 10;
    int y = x + 5;
    if (y > 10) {
        int z = 1;
    }
    """
    
    compilar(exemploDeTravestir)