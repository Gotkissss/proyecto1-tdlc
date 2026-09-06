import os
import sys

from shunting_yard import a_postfix
from thompson import construir_afn, simular_afn
from subset_construction import construir_afd, simular_afd
from minimization import minimizar_afd
from graphs import graficar_afn, graficar_afd

CARPETA_SALIDA = 'salida'


def procesar_regex(r, w, indice):
    os.makedirs(CARPETA_SALIDA, exist_ok=True)

    postfix = a_postfix(r)
    afn = construir_afn(postfix)
    afd = construir_afd(afn)
    afd_min = minimizar_afd(afd)

    graficar_afn(afn, f'{CARPETA_SALIDA}/afn_{indice}')
    graficar_afd(afd, f'{CARPETA_SALIDA}/afd_{indice}')
    graficar_afd(afd_min, f'{CARPETA_SALIDA}/afd_min_{indice}')

    resultado_afn = 'sí' if simular_afn(afn, w) else 'no'
    resultado_afd = 'sí' if simular_afd(afd, w) else 'no'
    resultado_afd_min = 'sí' if simular_afd(afd_min, w) else 'no'

    print(f'\nRegex: {r}   Postfix: {postfix}')
    print(f'Cadena: "{w}"')
    print(f'  AFN         -> {resultado_afn}')
    print(f'  AFD         -> {resultado_afd}')
    print(f'  AFD minimo  -> {resultado_afd_min}')


def main():
    if len(sys.argv) == 3:
        # modo: python main.py "regex" "cadena"
        procesar_regex(sys.argv[1], sys.argv[2], 0)
        return

    # modo batch: lee regexes.txt, pide la cadena para cada línea
    with open('regexes.txt', encoding='utf-8') as f:
        regexes = [linea.strip() for linea in f if linea.strip()]

    for i, r in enumerate(regexes):
        w = input(f'Cadena de prueba para "{r}": ')
        procesar_regex(r, w, i)


if __name__ == '__main__':
    main()