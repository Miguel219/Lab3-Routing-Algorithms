#Script generador de nombres y Nodos para Lab3-4

##########################################
#Formato
#   {"type":"topo",
#    "config":{"A":["B","C"],
#               "B":["A"],
#               "C":["A"],}
#   }
#   {"type":"names",
#    "config":{"A":"foo@alumchat.xyz",
#               "B":"bar@alumchat.xyz",
#               "C":"yeet@alumchat.xyz",}
#   }
##########################################
import numpy as np
import string, random, traceback, argparse

_EXAMPLE = ["foo", "bar", "yeet", "lol", "woot", "omg", "swag"]
_SECC10 = ["alv15842@uvg.edu.gt","ben18232@uvg.edu.gt","cas18161@uvg.edu.gt","cas18040@uvg.edu.gt",
"cas181202@uvg.edu.gt","cha18562@uvg.edu.gt","con18409@uvg.edu.gt","dele18607@uvg.edu.gt",
"dele18037@uvg.edu.gt","dele17822@uvg.edu.gt","del18221@uvg.edu.gt","fig18306@uvg.edu.gt",
"fue18188@uvg.edu.gt","gar18102@uvg.edu.gt","gon18398@uvg.edu.gt","men18239@uvg.edu.gt",
"men18500@uvg.edu.gt","qua17652@uvg.edu.gt","que18028@uvg.edu.gt","riv18049@uvg.edu.gt",
"ros18676@uvg.edu.gt","san18962@uvg.edu.gt","sol18151@uvg.edu.gt","val18762@uvg.edu.gt",
"vas18250@uvg.edu.gt","zav18893@uvg.edu.gt"]

def generateConfig(dict, fname, t):
    """
    Metodo que recibe un diccionario y escribe un archivo de configuracion names-*.txt

    Recibe: dict - un diccionario
            fname - string, el nombre del archivo
    Retorna: nada
    """
    try:
        with open(fname+'.txt', 'w') as f:
            the_config = str(dict)
            body = '{{"type":"{T}", "config":{PYLD} }}'.format(T = t, PYLD = the_config)
            f.write(body)
    except:
        print("Error Writing file...")
        traceback.print_exc()

def matrix2Dict(m):
    """
    Metodo que recibe una matriz de adjacencia y la convierte en un diccionario con arrays como values, \n
    con los vecinos como elementos del array.

    Recibe: matriz m de ajdacencia (por ende, cuadrada y simetrica), de N x N
    Retorna: Diccionario
    """
    #aprovechamos el uso de numpy y de nonzero para obtener los vecinos de forma eficiente
    #usamos tolist() para volverlo list y usamos dict comprehension para llenar el dict con N
    #usamos de forma astuta chr() para convertir de entero a su ASCII correspondiente + 65 (para que inicie en 'A')
    #el inverso de chr() es ord() y recibe el caracter y devuelve su ascii
    return {chr(i+65): [chr(j+65) for j in np.nonzero(row)[0].tolist()] for i,row in enumerate(m)}

def users2Dict(usrs):
    """
    Metodo que recibe una lista con nombres y la convierte en un diccionario con la asignacion \n

    Recibe: usrs - lista con N usuarios
    Retorna: Diccionario
    """
    #igual, aprovechamos numpy, y el formato ASCII y list comprehension
    return {chr(i+65): row.split("@")[0]+"@alumchat.xyz" for i,row in enumerate(usrs)}

def generateRandomTopology(name_list=[], fname="topo-default"):
    """
    Metodo que genera una topologia aleatoreamente
    """
    if len(name_list)==0:
        name_list = _EXAMPLE
    #generar una matriz de adjacencia
    M = 3   #numero de vecinos promedio (esperado), debe ser menor o igual a N
    N = len(name_list)   #total de nodos
    #se modela ese numero de vecinos esperados sampleando de una distribucion Bernoulli(p)
    #donde p=(0,1) y en nuestro caso representa esa proporcion entre M y N
    #Como su valor esperado es p entonces repitiendo el experimento N veces obtenemos n * M / N = M (conexiones en promedio)

    random_matrix = np.random.binomial(n=1, p=M/N, size=(N,N)) #Binomial con n=1 es Bernouli(p), no encontre metodo bernoulli como tal
    #obtener triangulo de matriz (setea 0 el resto), transpose, sumar, para obtener simetria
    matriz_res = np.tril(random_matrix) + np.tril(random_matrix, -1).T
    np.fill_diagonal(matriz_res, 0) #adjacencia al mismo nodo es 0
    generateConfig(matrix2Dict(matriz_res), fname, 'topo')

def assignRandomNames(name_list=[], fname="names-default"):
    """
    Metodo que genera la asignacion aleatoreamente
    """
    if len(name_list)==0:
        name_list = _EXAMPLE
    all_users = name_list

    random.shuffle(all_users)
    generateConfig(users2Dict(all_users), fname, 'names')


#################################################################################


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", action='store_true',
                    help="Generate random Names")
    parser.add_argument("-t", action='store_true',
                    help="Generate random Topology")
    parser.add_argument("-d", action='store_true',
                    help="Use Demo Values")

    args = parser.parse_args()

    if args.n:
        if args.d:
            assignRandomNames(name_list=_EXAMPLE)
        else:
            assignRandomNames(name_list=_SECC10)
        print("Asignacion de Nombres Generada...")
    if args.t:
        if args.d:
            generateRandomTopology(name_list=_EXAMPLE)
        else:
            generateRandomTopology(name_list=_SECC10)
        print("Topologia Generada...")

    if not args.n and not args.t :
        #no option, default solo nombres
        assignRandomNames(args.d)
        print("Asignacion de Nombres Generada...")
