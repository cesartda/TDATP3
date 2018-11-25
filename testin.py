import random
def leer_archivo(nombre_archivo):
    try:
        with open(nombre_archivo) as f:
            linea = f.readline().rstrip("\n")
            sobres = []
            while linea:
                try:
                    sobres.append(int(linea))
                except ValueError:
                    print("El archivo solo debe contener nros enteros")
                    exit()
                linea = f.readline().rstrip("\n")
    except IOError:
        print("Hubo un problema con el archivo")
        exit()
    if len(sobres) == 0:
        print("El archivo esta vacio")
        exit()
    sobres.sort()
    for nro in sobres:
        if nro <= 0:
            print("Las capacidades de los sobres deben ser positivas")
            exit()
        else:
            break
    if sobres[0] != 1:
        sobres.insert(0,1)
    return sobres


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

a  = leer_archivo_sobres("SOBRES.txt")
a = map(int, a)
a.sort()
print a
a  = leer_archivo("SOBRES.txt")
print a