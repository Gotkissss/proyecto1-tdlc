# Tokeniza y convierte una expresión regular en notación infix a postfix (Shunting Yard)

OPERADORES = {'|': 1, '.': 2, '*': 3, '+': 3, '?': 3}
UNARIOS = {'*', '+', '?'}
RESERVADOS = set('|*+?()')


def _expandir_clase(regex, i):
    """Lee una clase de caracteres tipo [a-zA-Z0-9.-] a partir de regex[i] == '['.
    Devuelve (tokens_equivalentes, nuevo_indice), donde tokens_equivalentes es
    la lista de tokens ('OP','(') LIT OP('|') ... ('OP',')') que representa
    la alternancia de todos los caracteres de la clase (rangos ya expandidos).
    """
    j = i + 1
    crudos = []  # lista de (caracter, fue_escapado)
    while j < len(regex) and regex[j] != ']':
        if regex[j] == '\\':
            if j + 1 >= len(regex):
                raise ValueError('Escape incompleto dentro de una clase [...]')
            crudos.append((regex[j + 1], True))
            j += 2
        else:
            crudos.append((regex[j], False))
            j += 1

    if j >= len(regex):
        raise ValueError('Clase de caracteres sin cerrar (falta "]")')

    negada = False
    if crudos and crudos[0] == ('^', False):
        negada = True
        crudos = crudos[1:]
    if negada:
        raise ValueError('Las clases negadas [^...] no estan soportadas')

    # Expandir rangos tipo a-z (el '-' solo cuenta como rango si no esta
    # escapado y no esta al inicio/final, donde se trata como literal)
    caracteres = []
    k = 0
    while k < len(crudos):
        c, esc = crudos[k]
        if (not esc and k + 2 < len(crudos) and
                crudos[k + 1] == ('-', False)):
            fin_c, _ = crudos[k + 2]
            if ord(c) > ord(fin_c):
                raise ValueError(f'Rango invalido en clase: {c}-{fin_c}')
            for code in range(ord(c), ord(fin_c) + 1):
                caracteres.append(chr(code))
            k += 3
        else:
            caracteres.append(c)
            k += 1

    if not caracteres:
        raise ValueError('Clase de caracteres vacia: []')

    # Quitar duplicados preservando el orden (evita ramas de alternancia repetidas)
    vistos = set()
    unicos = []
    for ch in caracteres:
        if ch not in vistos:
            vistos.add(ch)
            unicos.append(ch)

    tokens = [('OP', '(')]
    for idx, ch in enumerate(unicos):
        tokens.append(('LIT', ch))
        if idx != len(unicos) - 1:
            tokens.append(('OP', '|'))
    tokens.append(('OP', ')'))

    return tokens, j + 1  # j es el indice de ']', seguimos justo despues


def tokenizar(regex):
    """Convierte el string crudo en una lista de tokens ('OP', c) o ('LIT', c).
    Un backslash fuerza que el siguiente caracter se trate como literal,
    aunque sea uno de los operadores reservados.
    Una clase de caracteres [abc] o [a-z] se expande a una alternancia
    equivalente, ej. [a-c] se convierte en los tokens de (a|b|c)."""
    tokens = []
    i = 0
    while i < len(regex):
        c = regex[i]
        if c == '\\':
            i += 1
            if i >= len(regex):
                raise ValueError('Escape incompleto al final de la regex')
            tokens.append(('LIT', regex[i]))
        elif c == '[':
            expandidos, i = _expandir_clase(regex, i)
            tokens.extend(expandidos)
            continue
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