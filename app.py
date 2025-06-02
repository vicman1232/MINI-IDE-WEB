from flask import Flask, render_template, request, jsonify
from lexer import Lexer
from parser_custom import Parser
from turing_machine import ejecutar_maquina_turing

app = Flask(__name__)

STUDENT_INFO = {
    "name": "Victor Manuel Dominguez Santiago",
    "professor": "ING Kevin David Molina Gomez",  # Replace with actual professor name
}

@app.route('/')
def index():
    return render_template('index.html', student_info=STUDENT_INFO)

@app.route('/analizar', methods=['POST'])
def analizar():
    codigo = request.json.get('codigo', '')
    
    # Análisis léxico
    lexer = Lexer(codigo)
    tokens_por_linea, errores_lexicos = lexer.analyze()
    
    # Análisis sintáctico
    parser = Parser(tokens_por_linea)
    arbol_sintactico, errores_sintacticos = parser.parse()
    
    return jsonify({
        'tokens_por_linea': tokens_por_linea,
        'errores_lexicos': errores_lexicos,
        'arbol': arbol_sintactico,
        'errores_sintacticos': errores_sintacticos
    })

@app.route('/turing', methods=['POST'])
def turing():
    cadena = request.json.get('cadena', '')
    
    # Ejecutar la máquina de Turing y obtener el resultado
    resultado = ejecutar_maquina_turing(cadena)
    
    # Separar el resultado en líneas para obtener los pasos
    pasos = resultado.split('\n')
    
    # El último paso contiene el resultado final
    resultado_final = pasos[-1] if pasos else "Error: No hay resultado"
    
    return jsonify({
        'resultado': resultado_final,
        'pasos': pasos,
        'tipo': 'humano_robot'
    })

if __name__ == '__main__':
    app.run(debug=True) 