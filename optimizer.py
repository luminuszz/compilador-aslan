# optimizer.py
from parser_ import Numero, Booleano, OperacaoBinaria

class Optimizer:
    """Otimiza a AST realizando Constant Folding (simplificação de constantes)."""

    def visit(self, node):
        """Método de despacho para visitar o nó correto."""
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Retorna o nó como está se não houver regra de otimização."""
        return node

    def visit_Programa(self, node):
        node.declaracoes = [self.visit(stmt) for statement in node.declaracoes for stmt in [statement]]
        # A linha acima é um hack simples para manter a lista original, vamos simplificar:
        new_stmts = []
        for stmt in node.declaracoes:
            new_stmts.append(self.visit(stmt))
        node.declaracoes = new_stmts
        return node

    def visit_DeclaracaoVariavel(self, node):
        if node.expressao:
            node.expressao = self.visit(node.expressao)
        return node

    def visit_Atribuicao(self, node):
        node.expressao = self.visit(node.expressao)
        return node

    def visit_ComandoIf(self, node):
        node.condicao = self.visit(node.condicao)
        node.bloco_then = self.visit(node.bloco_then)
        if node.bloco_else:
            node.bloco_else = self.visit(node.bloco_else)
        return node

    def visit_ComandoWhile(self, node):
        node.condicao = self.visit(node.condicao)
        node.bloco = self.visit(node.bloco)
        return node

    def visit_Bloco(self, node):
        node.declaracoes = [self.visit(stmt) for stmt in node.declaracoes]
        return node

    def visit_ComandoPrint(self, node):
        node.expressao = self.visit(node.expressao)
        return node

    def visit_OperacaoBinaria(self, node):
        # 1. Tenta otimizar os filhos primeiro
        node.esquerda = self.visit(node.esquerda)
        node.direita = self.visit(node.direita)

        # 2. Se ambos os filhos forem Numero, faz Constant Folding
        if isinstance(node.esquerda, Numero) and isinstance(node.direita, Numero):
            v1 = node.esquerda.valor
            v2 = node.direita.valor
            op = node.op.type

            res = None
            if op == 'MAIS': res = v1 + v2
            elif op == 'MENOS': res = v1 - v2
            elif op == 'MULT': res = v1 * v2
            elif op == 'DIV': res = v1 // v2 if v2 != 0 else 0
            
            # Se foi uma operação aritmética, retorna um novo nó Numero
            if res is not None:
                # Criamos um novo token falso para o nó Numero (apenas para manter compatibilidade)
                from lexer import Token
                new_token = Token('NUMERO', str(res), node.esquerda.token.line, node.esquerda.token.column)
                return Numero(new_token)

            # Se for uma operação de comparação
            comp_res = None
            if op == 'MAIOR': comp_res = v1 > v2
            elif op == 'MENOR': comp_res = v1 < v2
            elif op == 'IGUAL_COMP': comp_res = v1 == v2
            
            if comp_res is not None:
                from lexer import Token
                t_type = 'TRUE' if comp_res else 'FALSE'
                new_token = Token(t_type, t_type.lower(), node.esquerda.token.line, node.esquerda.token.column)
                return Booleano(new_token)

        return node
