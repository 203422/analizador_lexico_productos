from flask import Flask, request, render_template
import ply.lex as lex

app = Flask(__name__)

tokens = ('NOMBRE', 'PRECIO')

t_ignore = ' \t'

def t_NOMBRE(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_PRECIO(t):
    r'\d+(\.\d{1,2})?'
    t.value = float(t.value)
    return t

def t_error(t):
    print(f"Caracter no valido '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

productos = []

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form['data']
        lexer.input(data)
        nombre = None
        precio_original = None

        for token in lexer:
            if token.type == 'NOMBRE':
                nombre = token.value
            elif token.type == 'PRECIO':
                precio_original = token.value

        if nombre and precio_original:
            precio_decimal = float(precio_original)
            iva = 0.16
            iva_monto = precio_decimal * iva
            total = precio_decimal + iva_monto
            producto = {
                'nombre': nombre,
                'precio_decimal': precio_decimal,
                'iva': iva_monto,
                'total': total
            }
            productos.append(producto)

    return render_template('index.html', productos=productos)

if __name__ == '__main__':
    app.run(debug=True)
