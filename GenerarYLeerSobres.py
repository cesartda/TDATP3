import random

def generar_archivo_sobres(cantidad_sobres):
    nombre_archivo = "SOBRES.txt"
    max_tarjetas_en_sobre = 100
    with open(nombre_archivo, 'w+') as archivo_sobres:
        sobres = random.sample(range(1, max_tarjetas_en_sobre + 1), cantidad_sobres)
        for sobre in sobres:
            archivo_sobres.write(str(sobre))
            archivo_sobres.write(str('\n'))
                
def leer_archivo_sobres(nombre_archivo_de_sobres):
    with open(nombre_archivo_de_sobres, 'r') as archivo_sobres:
        sobres = archivo_sobres.read().splitlines()
    return sobres


