import re

class Token:
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna
    
    def to_dict(self):
        return {
            'tipo': self.tipo,
            'valor': self.valor,
            'linea': self.linea,
            'columna': self.columna
        }

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.linea = 1
        self.columna = 1
        self.tokens = []
        self.errores = []
        
        # Palabras reservadas
        self.palabras_reservadas = {
            'if': 'IF',
            'else': 'ELSE',
            'while': 'WHILE',
            'for': 'FOR',
            'return': 'RETURN',
            'function': 'FUNCTION',
            'var': 'VAR',
            'let': 'LET',
            'const': 'CONST',
            'true': 'TRUE',
            'false': 'FALSE',
            'null': 'NULL'
        }
        
        # Definición de patrones para tokens
        self.token_specs = [
            ('NUMERO', r'\d+(\.\d+)?'),
            ('CADENA', r'"[^"]*"'),
            ('OPERADOR_ARITMETICO', r'[\+\-\*/]'),
            ('OPERADOR_ASIGNACION', r'='),
            ('OPERADOR_COMPARACION', r'[<>]=?|==|!='),
            ('OPERADOR_LOGICO', r'&&|\|\|'),
            ('PARENTESIS_IZQ', r'\('),
            ('PARENTESIS_DER', r'\)'),
            ('LLAVE_IZQ', r'\{'),
            ('LLAVE_DER', r'\}'),
            ('CORCHETE_IZQ', r'\['),
            ('CORCHETE_DER', r'\]'),
            ('PUNTO_COMA', r';'),
            ('COMA', r','),
            ('IDENTIFICADOR', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('ESPACIO', r'[ \t]+'),
            ('SALTO_LINEA', r'\n'),
            ('COMENTARIO_LINEA', r'//.*'),
            ('COMENTARIO_BLOQUE', r'/\*[\s\S]*?\*/'),
        ]
        
        # Compilar patrones
        self.token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_specs)
        self.regex = re.compile(self.token_regex)
    
    def analyze(self):
        tokens_por_linea = {}
        errores_lexicos = []
        linea_actual = 1
        tokens_linea = []
        
        for match in self.regex.finditer(self.text):
            tipo = match.lastgroup
            valor = match.group()
            columna = match.start() - self.text.rfind('\n', 0, match.start())
            
            if tipo == 'ESPACIO':
                continue
            elif tipo == 'SALTO_LINEA':
                if tokens_linea:
                    tokens_por_linea[str(linea_actual)] = tokens_linea
                linea_actual += 1
                tokens_linea = []
                continue
            elif tipo == 'COMENTARIO_LINEA' or tipo == 'COMENTARIO_BLOQUE':
                continue
            elif tipo == 'IDENTIFICADOR' and valor in self.palabras_reservadas:
                tipo = self.palabras_reservadas[valor]
            
            token = {
                'tipo': tipo,
                'valor': valor,
                'columna': columna
            }
            tokens_linea.append(token)
            
            # Verificar errores específicos
            if tipo == 'CADENA' and not valor.endswith('"'):
                errores_lexicos.append({
                    'linea': linea_actual,
                    'valor': valor,
                    'mensaje': 'Cadena no cerrada'
                })
            elif tipo == 'NUMERO' and not re.match(r'^\d+(\.\d+)?$', valor):
                errores_lexicos.append({
                    'linea': linea_actual,
                    'valor': valor,
                    'mensaje': 'Número mal formado'
                })
        
        # Agregar últimos tokens si existen
        if tokens_linea:
            tokens_por_linea[str(linea_actual)] = tokens_linea
        
        # Buscar caracteres inválidos
        pos = 0
        linea = 1
        for char in self.text:
            if char == '\n':
                linea += 1
                continue
            
            if not any(re.match(pattern, char) for _, pattern in self.token_specs):
                errores_lexicos.append({
                    'linea': linea,
                    'valor': char,
                    'mensaje': f'Carácter inválido: {char}'
                })
            pos += 1
        
        return tokens_por_linea, errores_lexicos 