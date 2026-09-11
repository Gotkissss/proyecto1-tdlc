# Genera imágenes de los autómatas usando graphviz
from graphviz import Digraph
from thompson import EPSILON

# Si un automata tiene mas estados que esto, graphviz puede tardar demasiado
# (o colgarse) intentando calcular el layout, asi que se salta el dibujo.
LIMITE_ESTADOS_GRAFICO = 120


def graficar_afn(afn, nombre):
    n = len(afn.transiciones)
    if n > LIMITE_ESTADOS_GRAFICO:
        print(f'  [!] AFN con {n} estados: se omite el dibujo '
              f'(supera el limite de {LIMITE_ESTADOS_GRAFICO}, tardaria demasiado)')
        return

    dot = Digraph(format='png')
    dot.attr(rankdir='LR')
    dot.node('inicio_ficticio', shape='point')

    for estado in afn.transiciones:
        forma = 'doublecircle' if estado in afn.acepta else 'circle'
        dot.node(str(estado), shape=forma)

    dot.edge('inicio_ficticio', str(afn.inicio))

    for origen, trans in afn.transiciones.items():
        for simbolo, destino in trans:
            etiqueta = 'ε' if simbolo == EPSILON else simbolo
            dot.edge(str(origen), str(destino), label=etiqueta)

    dot.render(nombre, cleanup=True)


def graficar_afd(afd, nombre):
    n = len(afd.transiciones)
    if n > LIMITE_ESTADOS_GRAFICO:
        print(f'  [!] AFD con {n} estados: se omite el dibujo '
              f'(supera el limite de {LIMITE_ESTADOS_GRAFICO}, tardaria demasiado)')
        return

    dot = Digraph(format='png')
    dot.attr(rankdir='LR')
    dot.node('inicio_ficticio', shape='point')

    for estado in afd.transiciones:
        forma = 'doublecircle' if estado in afd.acepta else 'circle'
        dot.node(str(estado), shape=forma)

    dot.edge('inicio_ficticio', str(afd.inicio))

    for origen, trans in afd.transiciones.items():
        for simbolo, destino in trans.items():
            dot.edge(str(origen), str(destino), label=simbolo)

    dot.render(nombre, cleanup=True)