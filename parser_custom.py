class Parser:
    def __init__(self, tokens_por_linea):
        self.tokens_por_linea = tokens_por_linea
        self.errores = []
        self.arbol = []
        self.current_line = 1
        self.current_token_index = 0
        self.current_tokens = []
    
    def parse(self):
        for linea, tokens in self.tokens_por_linea.items():
            self.current_line = int(linea)
            self.current_token_index = 0
            self.current_tokens = tokens
            
            try:
                while self.current_token_index < len(tokens):
                    nodo = self.parse_statement()
                    if nodo:
                        nodo['linea'] = self.current_line
                        self.arbol.append(nodo)
            except SyntaxError as e:
                self.errores.append({
                    'linea': self.current_line,
                    'mensaje': str(e)
                })
                # Intentar recuperarse del error avanzando al siguiente punto y coma o fin de línea
                self.recuperar_error()
        
        return self.arbol, self.errores
    
    def recuperar_error(self):
        """Intenta recuperarse de un error sintáctico"""
        while self.current_token_index < len(self.current_tokens):
            token = self.current_tokens[self.current_token_index]
            self.current_token_index += 1
            if token['tipo'] == 'PUNTO_COMA':
                break
    
    def peek(self):
        """Mira el siguiente token sin consumirlo"""
        if self.current_token_index < len(self.current_tokens):
            return self.current_tokens[self.current_token_index]
        return None
    
    def consume(self, tipo_esperado=None):
        """Consume un token y verifica su tipo si se especifica"""
        if self.current_token_index >= len(self.current_tokens):
            raise SyntaxError(f"Se esperaba {tipo_esperado}, pero se llegó al final de la línea")
        
        token = self.current_tokens[self.current_token_index]
        self.current_token_index += 1
        
        if tipo_esperado and token['tipo'] != tipo_esperado:
            raise SyntaxError(f"Se esperaba {tipo_esperado}, pero se encontró {token['tipo']}")
        
        return token
    
    def parse_statement(self):
        """Analiza una declaración"""
        token = self.peek()
        if not token:
            return None
        
        # Declaración de variable
        if token['tipo'] in ['VAR', 'LET', 'CONST']:
            return self.parse_variable_declaration()
        
        # Declaración de función
        elif token['tipo'] == 'FUNCTION':
            return self.parse_function_declaration()
        
        # Declaración if
        elif token['tipo'] == 'IF':
            return self.parse_if_statement()
        
        # Declaración while
        elif token['tipo'] == 'WHILE':
            return self.parse_while_statement()
        
        # Expresión
        else:
            return self.parse_expression_statement()
    
    def parse_variable_declaration(self):
        """Analiza una declaración de variable"""
        tipo_declaracion = self.consume()  # VAR, LET o CONST
        identificador = self.consume('IDENTIFICADOR')
        
        # Verificar si hay inicialización
        if self.peek() and self.peek()['tipo'] == 'OPERADOR_ASIGNACION':
            self.consume('OPERADOR_ASIGNACION')
            valor = self.parse_expression()
        else:
            valor = None
        
        # Verificar punto y coma
        if self.peek() and self.peek()['tipo'] == 'PUNTO_COMA':
            self.consume('PUNTO_COMA')
        
        return {
            'tipo': 'declaracion_variable',
            'tipo_declaracion': tipo_declaracion['tipo'],
            'identificador': identificador['valor'],
            'valor': valor
        }
    
    def parse_expression_statement(self):
        """Analiza una expresión como declaración"""
        expresion = self.parse_expression()
        
        # Verificar punto y coma
        if self.peek() and self.peek()['tipo'] == 'PUNTO_COMA':
            self.consume('PUNTO_COMA')
        
        return {
            'tipo': 'expresion_statement',
            'expresion': expresion
        }
    
    def parse_expression(self):
        """Analiza una expresión"""
        return self.parse_assignment()
    
    def parse_assignment(self):
        """Analiza una asignación"""
        expr = self.parse_logical_or()
        
        if self.peek() and self.peek()['tipo'] == 'OPERADOR_ASIGNACION':
            operador = self.consume('OPERADOR_ASIGNACION')
            valor = self.parse_assignment()
            return {
                'tipo': 'asignacion',
                'objetivo': expr,
                'valor': valor
            }
        
        return expr
    
    def parse_logical_or(self):
        """Analiza una expresión OR lógica"""
        expr = self.parse_logical_and()
        
        while self.peek() and self.peek()['tipo'] == 'OPERADOR_LOGICO' and self.peek()['valor'] == '||':
            operador = self.consume('OPERADOR_LOGICO')
            derecho = self.parse_logical_and()
            expr = {
                'tipo': 'operacion_logica',
                'operador': operador['valor'],
                'izquierda': expr,
                'derecha': derecho
            }
        
        return expr
    
    def parse_logical_and(self):
        """Analiza una expresión AND lógica"""
        expr = self.parse_equality()
        
        while self.peek() and self.peek()['tipo'] == 'OPERADOR_LOGICO' and self.peek()['valor'] == '&&':
            operador = self.consume('OPERADOR_LOGICO')
            derecho = self.parse_equality()
            expr = {
                'tipo': 'operacion_logica',
                'operador': operador['valor'],
                'izquierda': expr,
                'derecha': derecho
            }
        
        return expr
    
    def parse_equality(self):
        """Analiza una expresión de igualdad"""
        expr = self.parse_comparison()
        
        while self.peek() and self.peek()['tipo'] == 'OPERADOR_COMPARACION':
            operador = self.consume('OPERADOR_COMPARACION')
            derecho = self.parse_comparison()
            expr = {
                'tipo': 'operacion_comparacion',
                'operador': operador['valor'],
                'izquierda': expr,
                'derecha': derecho
            }
        
        return expr
    
    def parse_comparison(self):
        """Analiza una expresión de comparación"""
        expr = self.parse_term()
        
        while self.peek() and self.peek()['tipo'] == 'OPERADOR_COMPARACION':
            operador = self.consume('OPERADOR_COMPARACION')
            derecho = self.parse_term()
            expr = {
                'tipo': 'operacion_comparacion',
                'operador': operador['valor'],
                'izquierda': expr,
                'derecha': derecho
            }
        
        return expr
    
    def parse_term(self):
        """Analiza una expresión de suma/resta"""
        expr = self.parse_factor()
        
        while self.peek() and self.peek()['tipo'] == 'OPERADOR_ARITMETICO' and self.peek()['valor'] in ['+', '-']:
            operador = self.consume('OPERADOR_ARITMETICO')
            derecho = self.parse_factor()
            expr = {
                'tipo': 'operacion_aritmetica',
                'operador': operador['valor'],
                'izquierda': expr,
                'derecha': derecho
            }
        
        return expr
    
    def parse_factor(self):
        """Analiza una expresión de multiplicación/división"""
        expr = self.parse_unary()
        
        while self.peek() and self.peek()['tipo'] == 'OPERADOR_ARITMETICO' and self.peek()['valor'] in ['*', '/']:
            operador = self.consume('OPERADOR_ARITMETICO')
            derecho = self.parse_unary()
            expr = {
                'tipo': 'operacion_aritmetica',
                'operador': operador['valor'],
                'izquierda': expr,
                'derecha': derecho
            }
        
        return expr
    
    def parse_unary(self):
        """Analiza una expresión unaria"""
        if self.peek() and self.peek()['tipo'] == 'OPERADOR_ARITMETICO' and self.peek()['valor'] in ['+', '-']:
            operador = self.consume('OPERADOR_ARITMETICO')
            expr = self.parse_unary()
            return {
                'tipo': 'operacion_unaria',
                'operador': operador['valor'],
                'expresion': expr
            }
        
        return self.parse_primary()
    
    def parse_primary(self):
        """Analiza una expresión primaria"""
        token = self.peek()
        if not token:
            raise SyntaxError("Se esperaba una expresión")
        
        if token['tipo'] == 'NUMERO':
            return {
                'tipo': 'literal',
                'valor': self.consume('NUMERO')['valor'],
                'tipo_dato': 'numero'
            }
        elif token['tipo'] == 'CADENA':
            return {
                'tipo': 'literal',
                'valor': self.consume('CADENA')['valor'],
                'tipo_dato': 'cadena'
            }
        elif token['tipo'] == 'IDENTIFICADOR':
            return {
                'tipo': 'identificador',
                'valor': self.consume('IDENTIFICADOR')['valor']
            }
        elif token['tipo'] == 'PARENTESIS_IZQ':
            self.consume('PARENTESIS_IZQ')
            expr = self.parse_expression()
            self.consume('PARENTESIS_DER')
            return {
                'tipo': 'grupo',
                'expresion': expr
            }
        elif token['tipo'] in ['TRUE', 'FALSE']:
            token = self.consume()
            return {
                'tipo': 'literal',
                'valor': token['valor'],
                'tipo_dato': 'booleano'
            }
        elif token['tipo'] == 'NULL':
            self.consume()
            return {
                'tipo': 'literal',
                'valor': 'null',
                'tipo_dato': 'null'
            }
        
        raise SyntaxError(f"Token inesperado: {token['valor']}") 