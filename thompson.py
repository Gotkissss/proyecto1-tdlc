# Construcción de Thompson: de postfix a AFN

EPSILON = '~'


class AFN:
    def __init__(self):
        self.transiciones = {}  # estado -> [(simbolo, estado_destino), ...]
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
    afn = AFN()
    pila = []  # cada elemento es (estado_inicial_fragmento, estado_final_fragmento)

    for c in postfix:
        if c == '.':
            f2 = pila.pop()
            f1 = pila.pop()
            afn.agregar_transicion(f1[1], EPSILON, f2[0])
            pila.append((f1[0], f2[1]))

        elif c == '|':
            f2 = pila.pop()
            f1 = pila.pop()
            s = afn.nuevo_estado()
            e = afn.nuevo_estado()
            afn.agregar_transicion(s, EPSILON, f1[0])
            afn.agregar_transicion(s, EPSILON, f2[0])
            afn.agregar_transicion(f1[1], EPSILON, e)
            afn.agregar_transicion(f2[1], EPSILON, e)
            pila.append((s, e))

        elif c == '*':
            f = pila.pop()
            s = afn.nuevo_estado()
            e = afn.nuevo_estado()
            afn.agregar_transicion(s, EPSILON, f[0])
            afn.agregar_transicion(s, EPSILON, e)
            afn.agregar_transicion(f[1], EPSILON, f[0])
            afn.agregar_transicion(f[1], EPSILON, e)
            pila.append((s, e))

        elif c == '+':
            f = pila.pop()
            s = afn.nuevo_estado()
            e = afn.nuevo_estado()
            afn.agregar_transicion(s, EPSILON, f[0])
            afn.agregar_transicion(f[1], EPSILON, f[0])
            afn.agregar_transicion(f[1], EPSILON, e)
            pila.append((s, e))

        elif c == '?':
            f = pila.pop()
            s = afn.nuevo_estado()
            e = afn.nuevo_estado()
            afn.agregar_transicion(s, EPSILON, f[0])
            afn.agregar_transicion(s, EPSILON, e)
            afn.agregar_transicion(f[1], EPSILON, e)
            pila.append((s, e))

        else:  # literal
            s = afn.nuevo_estado()
            e = afn.nuevo_estado()
            afn.agregar_transicion(s, c, e)
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