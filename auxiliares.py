def main(vector_parametros):
	if len(vector_parametros) != 3:
		print("El programa solo debe recibir 2 parametros")
		exit()
	sobres = leer_archivo(vector_parametros[1])
	cant_tarj = leer_cant_tarj(vector_parametros[2])
	return sobres,cant_tarj


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


def leer_cant_tarj(parametro):
	try:
		nro = int(parametro)
	except ValueError:
		print("La cantidad de tarjetas debe ser un nro entero")
		exit()
	if nro <= 0:
		print("El nro ingresado debe ser positivo")
		exit()
	return nro	
	
	
def imprimir_resultado(solucion):
	print("Solucion:")
	print("Capacidad del sobre - Nro de sobres")
	print("-----------------------------------")
	nro_sobres_total = 0
	for linea in solucion:
		print("        {}          -       {}     ".format(linea[0],linea[1]))
		nro_sobres_total += linea[1]
	print("Nro total de sobres: {}".format(nro_sobres_total))