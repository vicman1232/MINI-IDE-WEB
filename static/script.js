let editor;

const ejemplosValidos = `// ===== ANÁLISIS LÉXICO =====
// Tokens válidos:
numero = 42          // IDENTIFICADOR, OPERADOR, NUMERO
texto = "Hola"      // IDENTIFICADOR, OPERADOR, CADENA
x = y + z           // IDENTIFICADOR, OPERADOR, IDENTIFICADOR

// ===== ANÁLISIS SINTÁCTICO =====
// Asignaciones simples
variable = 100
nombre = "Juan"

// Expresiones aritméticas
resultado = 10 + 5 * 3
promedio = (nota1 + nota2) / 2

// ===== MÁQUINA DE TURING =====
// Solo acepta cadenas de 'a' y 'b'
aaa     // → Humano (termina en 'a')
aaab    // → Robot (termina en 'b')
ab      // → Robot (termina en 'b')
a       // → Humano (termina en 'a')`;

const ejemplosInvalidos = `// ===== ANÁLISIS LÉXICO =====
// Caracteres no permitidos
x@ = 10             // @ no es un carácter válido
y# = 20             // # no es un carácter válido

// Tokens mal formados
123abc              // número seguido de letras
"cadena sin cerrar  // comilla sin cerrar

// ===== ANÁLISIS SINTÁCTICO =====
// Falta identificador
= 5                 // no hay variable a la izquierda

// Operadores mal usados
x + = y             // operador mal formado
variable =          // falta valor después del =

// Paréntesis sin cerrar
(x + y * (z - 1    // falta paréntesis de cierre

// ===== MÁQUINA DE TURING =====
// Solo acepta 'a' y 'b'
abc     // Error: 'c' no es válido
123     // Error: números no válidos
áéíóú   // Error: acentos no válidos
        // Error: cadena vacía`;

document.addEventListener('DOMContentLoaded', function() {
    editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
        lineNumbers: true,
        mode: "javascript",
        theme: "monokai",
        autoCloseBrackets: true,
        matchBrackets: true,
        indentUnit: 4,
        tabSize: 4,
        lineWrapping: true
    });
});

function cargarEjemplo(tipo) {
    const contenido = tipo === 'valido' ? ejemplosValidos : ejemplosInvalidos;
    editor.setValue(contenido);
}

// Función para marcar error en el editor
function marcarError(mensaje, linea) {
    // Crear el marcador de error
    const marker = document.createElement("div");
    marker.className = "error-marker";
    marker.style.color = "red";
    marker.style.marginLeft = "10px";
    marker.innerHTML = `❌ ${mensaje}`;
    
    // Agregar el marcador en la línea correspondiente
    editor.addLineWidget(linea - 1, marker, { above: false });
}

// Función para limpiar errores
function limpiarErrores() {
    // Limpiar todos los widgets de error existentes
    editor.getAllMarks().forEach(mark => mark.clear());
    editor.clearGutter("error-gutter");
}

async function analizarLexico() {
    try {
        limpiarErrores();
        const codigo = editor.getValue();
        const res = await fetch("/analizar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ codigo })
        });
        
        if (!res.ok) {
            throw new Error(`Error HTTP: ${res.status}`);
        }
        
        const data = await res.json();
        
        // Si hay errores léxicos, mostrarlos en el editor
        if (data.errores_lexicos && data.errores_lexicos.length > 0) {
            data.errores_lexicos.forEach(error => {
                marcarError(`Error léxico: carácter inválido '${error.valor}'`, error.linea);
            });
            return; // No mostrar nada en la salida si hay errores
        }
        
        // Si no hay errores, mostrar los tokens
        let salida = "📌 TOKENS POR LÍNEA:\n";
        for (const linea in data.tokens_por_linea) {
            const tokens = data.tokens_por_linea[linea].map(t => `[${t.tipo}: ${t.valor}]`).join(" ");
            salida += `Línea ${linea}: ${tokens}\n`;
        }
        
        document.getElementById("salida").textContent = salida;
    } catch (error) {
        document.getElementById("salida").textContent = `Error: ${error.message}`;
    }
}

async function analizarSintactico() {
    try {
        limpiarErrores();
        const codigo = editor.getValue();
        const res = await fetch("/analizar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ codigo })
        });
        
        if (!res.ok) {
            throw new Error(`Error HTTP: ${res.status}`);
        }
        
        const data = await res.json();
        
        // Si hay errores sintácticos, mostrarlos en el editor
        if (data.errores_sintacticos && data.errores_sintacticos.length > 0) {
            data.errores_sintacticos.forEach(error => {
                marcarError(`Error sintáctico: ${error.mensaje}`, error.linea);
            });
            return; // No mostrar nada en la salida si hay errores
        }
        
        // Si no hay errores, mostrar el árbol sintáctico
        let salida = "🌳 ÁRBOL SINTÁCTICO:\n";
        if (data.arbol && data.arbol.length > 0) {
            salida += data.arbol.map(e => 
                `Línea ${e.linea}:\n${JSON.stringify(e, null, 2)}`
            ).join("\n\n");
        }
        
        document.getElementById("salida").textContent = salida;
    } catch (error) {
        document.getElementById("salida").textContent = `Error: ${error.message}`;
    }
}

async function simularTuring() {
    try {
        limpiarErrores();
        const cadena = editor.getValue().trim();
        
        // Validación previa de la cadena
        if (!cadena) {
            marcarError("Error: La cadena está vacía", 1);
            return;
        }
        
        if (!/^[ab]+$/.test(cadena)) {
            marcarError("Error: La cadena solo puede contener 'a' y 'b'", 1);
            return;
        }
        
        const res = await fetch("/turing", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ cadena })
        });
        
        if (!res.ok) {
            throw new Error(`Error HTTP: ${res.status}`);
        }
        
        const data = await res.json();
        
        // Si el resultado indica error, mostrarlo en el editor
        if (data.resultado && data.resultado.includes("Desconocido")) {
            marcarError(data.resultado, 1);
            return;
        }
        
        // Si no hay errores, mostrar los pasos de ejecución
        let salida = "⚙️ MÁQUINA DE TURING:\n\n";
        salida += "Entrada: " + cadena + "\n\n";
        salida += "Pasos de ejecución:\n";
        data.pasos.forEach(paso => {
            salida += paso + "\n";
        });
        
        document.getElementById("salida").textContent = salida;
    } catch (error) {
        document.getElementById("salida").textContent = `Error: ${error.message}`;
    }
} 