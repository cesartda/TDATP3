from auxiliares import main, imprimir_resultado
import sys

def greedy(lista,nro):
	solucion = []
	for sobre in lista[::-1]:
		if nro == 0:
			break
		if nro//sobre > 0:	
			solucion.append((sobre,nro//sobre))
		nro = nro % sobre
	return solucion


sobres, cant_tarj = main(sys.argv)
solucion = greedy(sobres, cant_tarj)
imprimir_resultado(solucion)