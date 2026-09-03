# Minimización de AFD por el método de llenado de tabla (Myhill-Nerode)
from subset_construction import AFD


def minimizar_afd(afd):
    estados = list(afd.transiciones.keys())
    n = len(estados)

    # tabla[i][j] = True si (i,j) son distinguibles
    distinguibles = {(a, b): False for a in estados for b in estados if a < b}

    # Paso 1: marcar pares donde uno acepta y el otro no
    for (a, b) in distinguibles:
        if (a in afd.acepta) != (b in afd.acepta):
            distinguibles[(a, b)] = True

    # Paso 2: iterar hasta que no haya cambios
    cambiado = True
    while cambiado:
        cambiado = False
        for (a, b) in distinguibles:
            if distinguibles[(a, b)]:
                continue
            for simbolo in afd.alfabeto:
                da = afd.transiciones[a].get(simbolo)
                db = afd.transiciones[b].get(simbolo)
                if da == db:
                    continue
                if da is None or db is None:
                    distinguibles[(a, b)] = True
                    cambiado = True
                    break
                par = (min(da, db), max(da, db))
                if distinguibles.get(par, False):
                    distinguibles[(a, b)] = True
                    cambiado = True
                    break

    # Paso 3: agrupar estados equivalentes
    grupos = {}
    representante = {}
    for s in estados:
        if s in representante:
            continue
        grupo = {s}
        for t in estados:
            if t == s:
                continue
            par = (min(s, t), max(s, t))
            if not distinguibles.get(par, False):
                grupo.add(t)
        for g in grupo:
            representante[g] = s
        grupos[s] = grupo

    # Paso 4: construir AFD minimizado
    afd_min = AFD()
    afd_min.alfabeto = afd.alfabeto
    mapa_nuevo = {rep: i for i, rep in enumerate(sorted(grupos))}

    for rep in grupos:
        nuevo_id = mapa_nuevo[rep]
        afd_min.transiciones[nuevo_id] = {}
        for simbolo, destino in afd.transiciones[rep].items():
            destino_rep = representante[destino]
            afd_min.transiciones[nuevo_id][simbolo] = mapa_nuevo[destino_rep]
        if rep in afd.acepta:
            afd_min.acepta.add(nuevo_id)

    afd_min.inicio = mapa_nuevo[representante[afd.inicio]]
    return afd_min