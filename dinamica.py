from auxiliares import main, imprimir_resultado
import sys

def dinamica(lista,nro):
	solucion = []
	opt_parciales = []
	for x in range(nro):
		opt_parciales.append([])
	for i in range(nro):
		opt_parciales[i] = obt_opt(i, opt_parciales, lista)
	solucion = ord_sol(opt_parciales[-1], lista)	
	return solucion

def obt_opt(i, opt_parc, lista):
	posibles_sol = []
	for sobre in lista:
		if sobre <= i+1:
			sol_i = [(sobre,1)]
			for sol in opt_parc[i-sobre]:
				sol_i.append(sol)
			posibles_sol.append(sol_i)
	mejor_sol = posibles_sol[0]
	nro_sobres_mejor_sol = 0
	for sobre in mejor_sol:
		nro_sobres_mejor_sol += sobre[1]
	for sol in posibles_sol:
		nro_sobres = 0
		for sobre in sol:
			nro_sobres += sobre[1]
		if nro_sobres < nro_sobres_mejor_sol:
			mejor_sol = sol
			nro_sobres_mejor_sol = nro_sobres
	return mejor_sol
	
def ord_sol(opt, lista):
	sol_ord = []
	for sobre in lista[::-1]:
		nro_sobres = 0
		for sol_i in opt:
			if sol_i[0] == sobre:
				nro_sobres += sol_i[1]
		if nro_sobres == 0:
			continue
		sol_ord.append((sobre, nro_sobres))
	return sol_ord


def ejecutar_prog_dinamica():
	sobres, cant_tarj = main(sys.argv)
	solucion = dinamica(sobres, cant_tarj)
	imprimir_resultado(solucion)

