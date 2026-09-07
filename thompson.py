# Construccion de Thompson: de postfix (lista de tokens) a AFN

EPSILON = '\uE000'  # caracter de area privada Unicode: imposible que choque con un simbolo real del alfabeto


class AFN:
    def __init__(self):
        self.transiciones = {}
        self.inicio = None
        self.acepta = None
        self.contador = 0

    def nuevo_estado(self):
        s = self.contador
        self.contador += 1
        self.transiciones[s] = []
        return s

    def agregar_transicion(self, origen, simbolo, destino):
        self.transiciones[origen].append((simbolo, destino))


def construir_afn(postfix):
    """postfix es una lista de tokens ('OP', c) / ('LIT', c), como la que devuelve a_postfix."""
    afn = AFN()
    pila = []

    for tipo, val in postfix:
        if tipo == 'LIT':
            s = afn.nuevo_estado()
            e = afn.nuevo_estado()
            afn.agregar_transicion(s, val, e)
            pila.append((s, e))
            continue

        if val == '.':
            f2 = pila.pop()
            f1 = pila.pop()
            afn.agregar_transicion(f1[1], EPSILON, f2[0])
            pila.append((f1[0], f2[1]))

        elif val == '|':
            f2 = pila.pop()
            f1 = pila.pop()
            s = afn.nuevo_estado()
            e = afn.nuevo_estado()
            afn.agregar_transicion(s, EPSILON, f1[0])
            afn.agregar_transicion(s, EPSILON, f2[0])
            afn.agregar_transicion(f1[1], EPSILON, e)
            afn.agregar_transicion(f2[1], EPSILON, e)
            pila.append((s, e))

        elif val == '*':
            f = pila.pop()
            s = afn.nuevo_estado()
            e = afn.nuevo_estado()
            afn.agregar_transicion(s, EPSILON, f[0])
            afn.agregar_transicion(s, EPSILON, e)
            afn.agregar_transicion(f[1], EPSILON, f[0])
            afn.agregar_transicion(f[1], EPSILON, e)
            pila.append((s, e))

        elif val == '+':
            f = pila.pop()
            s = afn.nuevo_estado()
            e = afn.nuevo_estado()
            afn.agregar_transicion(s, EPSILON, f[0])
            afn.agregar_transicion(f[1], EPSILON, f[0])
            afn.agregar_transicion(f[1], EPSILON, e)
            pila.append((s, e))

        elif val == '?':
            f = pila.pop()
            s = afn.nuevo_estado()
            e = afn.nuevo_estado()
            afn.agregar_transicion(s, EPSILON, f[0])
            afn.agregar_transicion(s, EPSILON, e)
            afn.agregar_transicion(f[1], EPSILON, e)
            pila.append((s, e))

    inicio, fin = pila.pop()
    afn.inicio = inicio
    afn.acepta = {fin}
    return afn


def simular_afn(afn, w):
    def cerradura_epsilon(estados):
        pila = list(estados)
        cerradura = set(estados)
        while pila:
            s = pila.pop()
            for simbolo, destino in afn.transiciones[s]:
                if simbolo == EPSILON and destino not in cerradura:
                    cerradura.add(destino)
                    pila.append(destino)
        return cerradura

    actuales = cerradura_epsilon({afn.inicio})
    for c in w:
        siguientes = set()
        for s in actuales:
            for simbolo, destino in afn.transiciones[s]:
                if simbolo == c:
                    siguientes.add(destino)
        actuales = cerradura_epsilon(siguientes)

    return len(actuales & afn.acepta) > 0