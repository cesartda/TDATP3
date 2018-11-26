import sys
from auxiliares import main_factibilidad
from dinamica import dinamica
from greedy import greedy


#Retorna True o False si es factible con greedy, respectivamente. #En caso de ser False, muestra un contraejemplo por pantalla.
def factibilidad(sobres):
    if len(sobres) < 3: #Solo tiene el 1 y a lo sumo un elemento mas. Siempre se va a obtener el optimo.
        return True
    for x in range((sobres[2] + 1) + 1, sobres[len(sobres) - 2] + sobres[len(sobres) - 1]):
        #dinamica u optima:
        sobres = main_factibilidad(sys.argv) #Si no llamo al main en cada llamada, falla.
        solucion_prog_dinamica = dinamica(sobres, x)
        cantidad_de_sobres_prog_dinamica = 0
        for tarjetas, sobres in solucion_prog_dinamica:
            cantidad_de_sobres_prog_dinamica += sobres
        #greedy:
        sobres = main_factibilidad(sys.argv)
        solucion_greedy = greedy(sobres, x)
        cantidad_de_sobres_greedy = 0
        for tarjetas, sobres in solucion_greedy:
            cantidad_de_sobres_greedy += sobres
        if cantidad_de_sobres_greedy > cantidad_de_sobres_prog_dinamica:
            print 'No es factible obtener una solucion optima con Greedy para los sobres dados.'
            print 'Contraejemplo =', x, 'tarjetas. Con Greedy se obtienen', cantidad_de_sobres_greedy, 'sobres mientras que la cantidad optima es', cantidad_de_sobres_prog_dinamica
            break
    return True
    
def ejecutar_factibilidad():
    sobres = main_factibilidad(sys.argv)
    factibilidad(sobres)


