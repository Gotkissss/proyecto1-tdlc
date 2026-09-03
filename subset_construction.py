# Algoritmo de subconjuntos: AFN -> AFD
from thompson import EPSILON


def cerradura_epsilon(afn, estados):
    pila = list(estados)
    cerradura = set(estados)
    while pila:
        s = pila.pop()
        for simbolo, destino in afn.transiciones[s]:
            if simbolo == EPSILON and destino not in cerradura:
                cerradura.add(destino)
                pila.append(destino)
    return cerradura


def mover(afn, estados, simbolo):
    destinos = set()
    for s in estados:
        for sim, dest in afn.transiciones[s]:
            if sim == simbolo:
                destinos.add(dest)
    return destinos


class AFD:
    def __init__(self):
        self.transiciones = {}  # estado(int) -> {simbolo: estado_destino(int)}
        self.inicio = None
        self.acepta = set()
        self.alfabeto = set()


def construir_afd(afn):
    alfabeto = sorted({sim for trans in afn.transiciones.values()
                        for sim, _ in trans if sim != EPSILON})

    afd = AFD()
    afd.alfabeto = set(alfabeto)

    inicial = frozenset(cerradura_epsilon(afn, {afn.inicio}))
    mapa_estados = {inicial: 0}
    afd.inicio = 0
    afd.transiciones[0] = {}
    if inicial & afn.acepta:
        afd.acepta.add(0)

    pendientes = [inicial]
    while pendientes:
        actual = pendientes.pop()
        id_actual = mapa_estados[actual]

        for simbolo in alfabeto:
            destino = frozenset(cerradura_epsilon(afn, mover(afn, actual, simbolo)))
            if not destino:
                continue
            if destino not in mapa_estados:
                nuevo_id = len(mapa_estados)
                mapa_estados[destino] = nuevo_id
                afd.transiciones[nuevo_id] = {}
                if destino & afn.acepta:
                    afd.acepta.add(nuevo_id)
                pendientes.append(destino)
            afd.transiciones[id_actual][simbolo] = mapa_estados[destino]

    return afd


def simular_afd(afd, w):
    actual = afd.inicio
    for c in w:
        if c not in afd.transiciones[actual]:
            return False
        actual = afd.transiciones[actual][c]
    return actual in afd.acepta