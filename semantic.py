class SemanticError(Exception):
    pass

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def define(self, name, type):
        if name in self.symbols:
            raise SemanticError(f"Erro Semântico: Variável '{name}' já declarada neste escopo.")
        self.symbols[name] = type

    def lookup(self, name):
        symbol_type = self.symbols.get(name)
        if symbol_type:
            return symbol_type
        if self.parent:
            return self.parent.lookup(name)
        return None

class SemanticAnalyzer:
    def __init__(self):
        self.current_scope = SymbolTable()

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'Não há método visit_{type(node).__name__} definido.')

    def visit_Programa(self, node):
        for decl in node.declaracoes:
            self.visit(decl)

    def visit_DeclaracaoVariavel(self, node):
     
        tipo = node.tipo.value 
        self.current_scope.define(node.nome_variavel.nome, tipo)
        if node.expressao:
            expr_type = self.visit(node.expressao)
            if expr_type != tipo:
                raise SemanticError(f"Erro de Tipo: Tentativa de atribuir {expr_type} a uma variável {tipo}.")

    def visit_Identificador(self, node):
        tipo = self.current_scope.lookup(node.nome)
        if tipo is None:
            raise SemanticError(f"Erro Semântico: Variável '{node.nome}' não declarada.")
        return tipo

    def visit_Numero(self, node):
        return 'int'

    def visit_OperacaoBinaria(self, node):
        esq_tipo = self.visit(node.esquerda)
        dir_tipo = self.visit(node.direita)
        
   
        if node.op.type in ('MAIS', 'MENOS', 'MULT', 'DIV'):
            if esq_tipo == 'int' and dir_tipo == 'int':
                return 'int'
            raise SemanticError(f"Operação {node.op.value} exige operandos do tipo int.")
        
        
        if node.op.type in ('MAIOR', 'MENOR', 'IGUAL_COMP', 'DIFERENTE'):
            return 'bool'
            
        return esq_tipo

    def visit_Bloco(self, node):
    
        self.current_scope = SymbolTable(parent=self.current_scope)
        for decl in node.declaracoes:
            self.visit(decl)
       
        self.current_scope = self.current_scope.parent

    def visit_ComandoIf(self, node):
        cond_type = self.visit(node.condicao)
        if cond_type != 'bool' and cond_type != 'int': 
             pass 
        self.visit(node.bloco_then)
        if node.bloco_else:
            self.visit(node.bloco_else)