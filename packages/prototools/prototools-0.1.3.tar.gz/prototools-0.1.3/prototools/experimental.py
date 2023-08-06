"""
Modulo Experimental
"""
import re
from inspect import getmembers, isfunction
import sys
from textwrap import dedent
from typing import Tuple
from prototools.config import RELLENOS, MARGENES, BORDES, TIPOS_BORDES

tipo = TIPOS_BORDES[1]

_Relleno = type("Relleno", (), RELLENOS)
_Margenes = type("Margenes", (), MARGENES)
_Borde = type(
    "Borde", (), {atributo:valor[tipo] for atributo, valor in BORDES.items()}
    )

class Margen:
    def __init__(self) -> None:
        for atributo, valor in MARGENES.items():
            setattr(self, atributo, valor)


def partir(predicado, valores) -> Tuple[list, list]:
    """
    Separa los valores en dos conjuntos, basado en el retorno de la 
    función (True/False):

        >>> t = partir(lambda x: x < 4, range(9))
        ([4, 5, 6, 7, 8], [0, 1, 2, 3])
    """
    resultado = ([], [])
    for item in valores:
        resultado[predicado(item)].append(item)
    return resultado

def strip_ansi(s):
    t = re.compile(r"""
    \x1b     # caracter ESC
    \[       # caracter [
    [;\d]*   # 0 or mas digitios or punto y comas
    [A-Za-z] # una letra
    """, re.VERBOSE).sub
    return t("",s)


def run_loop(funcion, indicacion, error, args):
    operador_relacional, valor = args
    while True:
        n =int(input(indicacion))
        condicion = {
            '>': n > valor,
            '>=': n >= valor,
            '<': n < valor,
            '<=': n <= valor,
            '==': n == valor,
            '!=': n != valor,
        }
        if condicion[operador_relacional]:
            print(funcion(n)); break
        else:
            print(error)

def create_func(name, args, unique):
    """
    """
    template = dedent(f'''
    def {name}({", ".join(args.split())}):
        print('algo')
        {unique}
        print('algo')
    ''').strip()
    ns = {}
    exec(template, ns)
    return ns[name]

def __f():
    return [n for n in globals() if not n.startswith("__")]

def obtener_funciones(modulo):
    return [
        funcion for nombre, funcion in getmembers(modulo, isfunction) 
        if nombre not in ('getmembers', 'getmodule', 'isfunction') 
        and not nombre.startswith("_")
        ]

def modulo():
    return __import__(__name__)

class Modulo:
    def get(self):
        return __import__(__name__)

def crear_enlace(lista):
    return {k:v for k,v in enumerate(lista, 1)}

def return_names():
    return [n for n in sys.modules[__name__].__dir__() if not n.startswith("__")]