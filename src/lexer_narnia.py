import re

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', L{self.line}:C{self.column})"

class LexerError(Exception):
    pass

class LexerNarnia:
    def __init__(self, code):
        self.code = code
        self.line = 1
        self.column = 1
        self.token_specs = [
            ('COMENTARIO',  r'//[^\n]*'),
            ('NOVALINHA',   r'\n'),
            ('ESPACO',      r'[ \t]+'),
            ('STRING',      r'"[^"]*"'),
            ('NUMERO',      r'\d+(\.\d*)?'),
            ('IF',          r'\bpela_juba_do_leao\b'),
            ('ELSE',        r'\bpelo_rei_caspian\b'),
            ('WHILE',       r'\bdurante_o_reinado\b'),
            ('PRINT',       r'\bproclamar\b'),
            ('READ',        r'\bouvir_conselho\b'),
            ('TRUE',        r'\bverdade_de_aslan\b'),
            ('FALSE',       r'\bmentira_de_edmundo\b'),
            ('INT',         r'\brei_pedro\b'),
            ('BOOL',        r'\brainha_lucia\b'),
            ('IDENTIFICADOR', r'[A-Za-z_][A-Za-z0-9_]*'),
            ('IGUAL_COMP',  r'=='),
            ('DIFERENTE',   r'!='),
            ('MAIOR_IGUAL', r'>='),
            ('MENOR_IGUAL', r'<='),
            ('MAIOR',       r'>'),
            ('MENOR',       r'<'),
            ('IGUAL',       r'='),
            ('MAIS',        r'\+'),
            ('MENOS',       r'-'),
            ('MULT',        r'\*'),
            ('DIV',         r'/'),
            ('LPAREN',      r'\('),
            ('RPAREN',      r'\)'),
            ('LCHAVE',      r'{'),
            ('RCHAVE',      r'}'),
            ('PONTO_VIRGULA', r';'),
            ('ERRO',        r'.'),
        ]
        self.token_regex = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_specs))

    def tokenize(self):
        tokens = []
        while self.code:
            match = self.token_regex.match(self.code)
            if not match:
                raise LexerError(f"Caractere inesperado na linha {self.line}, coluna {self.column}")

            kind = match.lastgroup
            value = match.group()
            
            if kind == 'NOVALINHA':
                self.line += 1
                self.column = 1
            elif kind not in ['ESPACO', 'COMENTARIO']:
                if kind == 'ERRO':
                     raise LexerError(f"Caractere inválido '{value}' na linha {self.line}, coluna {self.column}")
                tokens.append(Token(kind, value, self.line, self.column))
                self.column += len(value)
            else:
                self.column += len(value)

            self.code = self.code[match.end():]
        
        tokens.append(Token('EOF', '', self.line, self.column))
        return tokens
