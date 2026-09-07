import os
import sys

from shunting_yard import a_postfix, postfix_legible
from thompson import construir_afn, simular_afn
from subset_construction import construir_afd, simular_afd
from minimization import minimizar_afd, minimizar_afd_particion
from graphs import graficar_afn, graficar_afd

CARPETA_SALIDA = 'salida'


def procesar_regex(r, w, indice):
    os.makedirs(CARPETA_SALIDA, exist_ok=True)

    postfix = a_postfix(r)  # ahora es una lista de tokens, no un string
    afn = construir_afn(postfix)
    afd = construir_afd(afn)
    afd_min_tabla = minimizar_afd(afd)
    afd_min_particion = minimizar_afd_particion(afd)

    graficar_afn(afn, f'{CARPETA_SALIDA}/afn_{indice}')
    graficar_afd(afd, f'{CARPETA_SALIDA}/afd_{indice}')
    graficar_afd(afd_min_tabla, f'{CARPETA_SALIDA}/afd_min_tabla_{indice}')
    graficar_afd(afd_min_particion, f'{CARPETA_SALIDA}/afd_min_particion_{indice}')

    resultado_afn = 'sí' if simular_afn(afn, w) else 'no'
    resultado_afd = 'sí' if simular_afd(afd, w) else 'no'
    resultado_afd_min_tabla = 'sí' if simular_afd(afd_min_tabla, w) else 'no'
    resultado_afd_min_particion = 'sí' if simular_afd(afd_min_particion, w) else 'no'

    print(f'\nRegex: {r}   Postfix: {postfix_legible(postfix)}')
    print(f'Cadena: "{w}"')
    print(f'  AFN                        -> {resultado_afn}')
    print(f'  AFD                        -> {resultado_afd}')
    print(f'  AFD minimo (tabla)         -> {resultado_afd_min_tabla}  '
          f'({len(afd_min_tabla.transiciones)} estados)')
    print(f'  AFD minimo (particion)     -> {resultado_afd_min_particion}  '
          f'({len(afd_min_particion.transiciones)} estados)')


def main():
    with open('regexes.txt', encoding='utf-8') as f:
        regexes = [linea.rstrip('\n') for linea in f if linea.strip()]

    if len(sys.argv) == 3:
        procesar_regex(sys.argv[1], sys.argv[2], 0)
    elif len(sys.argv) == 2:
        w = sys.argv[1]
        for i, r in enumerate(regexes):
            procesar_regex(r, w, i)
    else:
        for i, r in enumerate(regexes):
            w = input(f'Cadena de prueba para "{r}": ')
            procesar_regex(r, w, i)


if __name__ == '__main__':
    main()