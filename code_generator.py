# code_generator.py

class CodeGenerator:
    """Traduz TAC (Código de Três Endereços) para Bytecode baseado em pilha."""

    def __init__(self, tac):
        self.tac = tac
        self.bytecode = []
        self.labels = {} # Mapeia nome do label para índice no bytecode

    def is_literal(self, value):
        """Verifica se o valor é um literal (número ou booleano)."""
        if value in ('true', 'false'):
            return True
        try:
            int(value)
            return True
        except (ValueError, TypeError):
            return False

    def get_value(self, value):
        """Gera instrução para colocar o valor na pilha (PUSH ou LOAD)."""
        if self.is_literal(value):
            val = int(value) if value not in ('true', 'false') else (value == 'true')
            self.bytecode.append(('PUSH', val))
        else:
            self.bytecode.append(('LOAD', value))

    def generate(self):
        # Primeira passagem: Gerar bytecode básico e mapear labels
        for instr in self.tac:
            opcode = instr[0]
            arg1 = instr[1]
            arg2 = instr[2]
            result = instr[3]

            if opcode == 'LABEL':
                self.labels[arg1] = len(self.bytecode)
            
            elif opcode == 'ASSIGN':
                self.get_value(arg1)
                self.bytecode.append(('STORE', result))

            elif opcode in ('MAIS', 'MENOS', 'MULT', 'DIV', 'MAIOR', 'MENOR', 'IGUAL_COMP'):
                self.get_value(arg1)
                self.get_value(arg2)
                
                op_map = {
                    'MAIS': 'ADD', 'MENOS': 'SUB', 'MULT': 'MUL', 'DIV': 'DIV',
                    'MAIOR': 'CMP_GT', 'MENOR': 'CMP_LT', 'IGUAL_COMP': 'CMP_EQ'
                }
                self.bytecode.append((op_map[opcode],))
                self.bytecode.append(('STORE', result))

            elif opcode == 'PRINT':
                self.get_value(arg1)
                self.bytecode.append(('PRINT',))

            elif opcode == 'READ':
                self.bytecode.append(('READ', result))

            elif opcode == 'JUMP':
                # Segunda passagem resolverá o endereço
                self.bytecode.append(('JUMP', result))

            elif opcode == 'JUMP_IF_FALSE':
                self.get_value(arg1)
                self.bytecode.append(('JUMP_IF_FALSE', result))

        # Segunda passagem: Resolver endereços de labels
        resolved_bytecode = []
        for instr in self.bytecode:
            opcode = instr[0]
            if opcode in ('JUMP', 'JUMP_IF_FALSE'):
                label_name = instr[1]
                addr = self.labels[label_name]
                resolved_bytecode.append((opcode, addr))
            else:
                resolved_bytecode.append(instr)

        return resolved_bytecode
