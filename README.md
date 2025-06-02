# Mini IDE Web

## Estudiante
- **Nombre:** Victor Manuel Dominguez Santiago
- **Materia:** Lenguajes y Automatas
- **Profesor:** ING Kevin David Molina Gomez

## Descripción del Proyecto
Este proyecto implementa un IDE web que incluye:
- Análisis léxico con detección de tokens y errores
- Análisis sintáctico con generación de árbol
- Simulación de Máquina de Turing para clasificación Humano/Robot

## Requisitos
- Python 3.x
- Flask
- Navegador web moderno

## Instalación
1. Clonar el repositorio
2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   ```
3. Activar el entorno virtual:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
4. Instalar dependencias:
   ```bash
   pip install flask
   ```

## Ejecución
1. Activar el entorno virtual (si no está activo)
2. Ejecutar el servidor:
   ```bash
   python app.py
   ```
3. Abrir en el navegador: http://localhost:5000

## Lenguaje Personalizado

### Tokens
- **NUMERO**: Números enteros o decimales (`\d+(\.\d+)?`)
- **IDENTIFICADOR**: Nombres de variables (`[a-zA-Z_][a-zA-Z0-9_]*`)
- **OPERADOR**: Operadores aritméticos y lógicos (`[\+\-\*/=<>!]=?|&&|\|\|`)
- **PARENTESIS**: Paréntesis (`[\(\)]`)
- **LLAVE**: Llaves (`[\{\}]`)
- **CORCHETE**: Corchetes (`[\[\]]`)
- **PUNTUACION**: Símbolos de puntuación (`[,;:]`)
- **CADENA**: Cadenas de texto (`"[^"]*"`)
- **COMENTARIO**: Comentarios de línea y bloque (`//.*|/\*[\s\S]*?\*/`)

### Gramática
```
programa    → declaracion*
declaracion → variable_decl | expresion
variable_decl → IDENTIFICADOR "=" expresion
expresion   → literal | IDENTIFICADOR | operacion
operacion   → expresion OPERADOR expresion
literal     → NUMERO | CADENA
```

### Ejemplos Válidos
```javascript
x = 42
nombre = "Juan"
resultado = 10 + 5 * 3
```

### Ejemplos Inválidos
```javascript
42x = 10  // Identificador inválido
= 5       // Falta identificador
x = "texto incompleto  // Cadena sin cerrar
```

## Máquina de Turing
La implementación incluye una Máquina de Turing que clasifica entre Humano y Robot:

### Descripción
- La máquina procesa cadenas compuestas únicamente por los símbolos 'a' y 'b'
- Convierte cada 'a' en 'X' y cada 'b' en 'Y'
- Clasifica la entrada basándose en el último símbolo de la cadena original

### Reglas de Clasificación
- Si termina en 'a': Clasifica como "Humano 🧍"
- Si termina en 'b': Clasifica como "Robot 🤖"
- Cualquier otro caso: "Desconocido ❓"

### Ejemplos Válidos
```
Entrada: "aaab"
Pasos:
1. Posición 0: 'a' → 'X'
2. Posición 1: 'a' → 'X'
3. Posición 2: 'a' → 'X'
4. Posición 3: 'b' → 'Y'
Cinta final: XXXY
Resultado: Robot 🤖

Entrada: "aaa"
Pasos:
1. Posición 0: 'a' → 'X'
2. Posición 1: 'a' → 'X'
3. Posición 2: 'a' → 'X'
Cinta final: XXX
Resultado: Humano 🧍
```

### Ejemplos Inválidos
```
Entrada: "abc"  // Contiene caracteres no válidos
Resultado: Desconocido ❓ (caracteres inválidos)

Entrada: ""     // Cadena vacía
Resultado: Desconocido ❓
```

## Características
- Editor de código con resaltado de sintaxis
- Detección de errores léxicos en tiempo real
- Visualización de tokens por línea
- Árbol sintáctico para código válido
- Simulador de Máquina de Turing integrado
- Interfaz moderna y responsive con Bootstrap
- Tema oscuro para el editor (Monokai) 
