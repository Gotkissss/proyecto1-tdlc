# Convierte una expresión regular en notación infix a postfix (algoritmo Shunting Yard)

OPERADORES = {'|': 1, '.': 2, '*': 3, '+': 3, '?': 3}
UNARIOS = {'*', '+', '?'}


def insertar_concatenacion(regex):
    """Inserta el operador explícito '.' donde hay concatenación implícita."""
    resultado = []
    for i in range(len(regex)):
        c1 = regex[i]
        resultado.append(c1)
        if i + 1 < len(regex):
            c2 = regex[i + 1]
            necesita_punto = (
                (c1 not in '(|' and c1 not in OPERADORES or c1 in UNARIOS or c1 == ')')
                and (c2 not in ')|' and (c2 == '(' or c2 not in OPERADORES))
            )
            if necesita_punto:
                resultado.append('.')
    return ''.join(resultado)


def a_postfix(regex):
    regex = insertar_concatenacion(regex)
    salida = []
    pila = []

    for c in regex:
        if c == '(':
            pila.append(c)
        elif c == ')':
            while pila and pila[-1] != '(':
                salida.append(pila.pop())
            pila.pop()  # descarta '('
        elif c in OPERADORES:
            while (pila and pila[-1] != '(' and
                   OPERADORES.get(pila[-1], 0) >= OPERADORES[c]):
                salida.append(pila.pop())
            pila.append(c)
        else:
            salida.append(c)  # literal

    while pila:
        salida.append(pila.pop())

    return ''.join(salida)