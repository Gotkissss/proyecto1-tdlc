# Genera imágenes de los autómatas usando graphviz
from graphviz import Digraph
from thompson import EPSILON


def graficar_afn(afn, nombre):
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