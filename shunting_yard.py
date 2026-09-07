# Tokeniza y convierte una expresión regular en notación infix a postfix (Shunting Yard)

OPERADORES = {'|': 1, '.': 2, '*': 3, '+': 3, '?': 3}
UNARIOS = {'*', '+', '?'}
RESERVADOS = set('|*+?()')


def tokenizar(regex):
    """Convierte el string crudo en una lista de tokens ('OP', c) o ('LIT', c).
    Un backslash fuerza que el siguiente caracter se trate como literal,
    aunque sea uno de los operadores reservados."""
    tokens = []
    i = 0
    while i < len(regex):
        c = regex[i]
        if c == '\\':
            i += 1
            if i >= len(regex):
                raise ValueError('Escape incompleto al final de la regex')
            tokens.append(('LIT', regex[i]))
        elif c in RESERVADOS:
            tokens.append(('OP', c))
        else:
            tokens.append(('LIT', c))
        i += 1
    return tokens


def insertar_concatenacion(tokens):
    """Inserta el token de concatenacion ('OP', '.') donde es implicita."""
    resultado = []
    for i, tok in enumerate(tokens):
        resultado.append(tok)
        if i + 1 < len(tokens):
            actual = tok
            siguiente = tokens[i + 1]

            cierra_subexpr = (
                actual[0] == 'LIT' or
                actual == ('OP', ')') or
                (actual[0] == 'OP' and actual[1] in UNARIOS)
            )
            abre_subexpr = (
                siguiente[0] == 'LIT' or
                siguiente == ('OP', '(')
            )

            if cierra_subexpr and abre_subexpr:
                resultado.append(('OP', '.'))
    return resultado


def a_postfix(regex):
    """Recibe el string crudo de la regex, devuelve una lista de tokens en postfix."""
    tokens = tokenizar(regex)
    tokens = insertar_concatenacion(tokens)

    salida = []
    pila = []

    for tok in tokens:
        tipo, val = tok
        if tipo == 'LIT':
            salida.append(tok)
        elif val == '(':
            pila.append(tok)
        elif val == ')':
            while pila and pila[-1][1] != '(':
                salida.append(pila.pop())
            pila.pop()  # descarta '('
        else:  # operador
            while (pila and pila[-1][1] != '(' and
                   OPERADORES.get(pila[-1][1], 0) >= OPERADORES[val]):
                salida.append(pila.pop())
            pila.append(tok)

    while pila:
        salida.append(pila.pop())

    return salida


def postfix_legible(postfix):
    """Solo para imprimir en pantalla: convierte la lista de tokens a un string legible."""
    return ''.join(val for _, val in postfix)