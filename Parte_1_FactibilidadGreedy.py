#Recibe por parametro el nombre del archivo.
#Retorna True o False si es factible con greedy, respectivamente.
#En caso de ser False, imprime un contraejemplo.
def factibilidad(nombre_del_archivo_de_sobres):
    with open(nombre_del_archivo_de_sobres, 'r') as archivo_sobres:
        sobres = archivo_sobres.read().splitlines()


Algorithm 1: IsCanonical
Require: a tight coin system
$ = h1, c2, · · · , cm, cm+1i with m >= 5
1: if 0 < r < c2 - q with c3 = qc2 + r then
2: return $ is non-canonical
3: else
4: for i = m downto 1 do
5: for j = i downto 1 do
6: if ci + cj > cm+1 and |GRD$(ci + cj)| > 2
then
7: return $ is non-canonical
8: end if
9: end for
10: end for
11: return $ is canonical
12: end if