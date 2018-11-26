# -*- coding: utf-8 -*-
import argparse
import math

def main(file_stations,file_railways,people_per_wagon,min_wagon_per_line,num_wagons_in_system):
    # grapg = create_subway_graph(file_stations,file_railways,people_per_wagon,min_wagon_per_line,num_wagons_in_system)
    # test_graph = [ ["a",[[2,5],[4,20]]] , ["b",[ [5,1],[3,300],[6,100] ]] , ["c",[[0,5],[5,10]]],["d",[[1,300],[4,10]]],["e",[[0,20],[3,10]]],["f",[[1,1],[2,10],[6,100]]],["g",[[5,100],[1,100]]]]
    # print(test_graph)
    # max_f = ford_fulkerson(test_graph,0,1)
    # print(max_f)
    subway_people_graph,station_dict = create_subway_graph(file_stations,file_railways,people_per_wagon)
    necessary_flow_source = 0
    necessary_flow_sink = 0
    for i in subway_people_graph[0][1]:
        necessary_flow_source += i[1]
    for i in subway_people_graph[1][1]:
        necessary_flow_sink += i[1]
    if necessary_flow_source != necessary_flow_sink:
        print("La fuente y el sumidero tienen cantidades distintas. La gente no se crea ni se destruye, solo se transforma (?")
        exit()
    for i in subway_people_graph:
        print(i)
    max_f_people,subway_people_graph_residual = ford_fulkerson(subway_people_graph,0,1)
    for i in subway_people_graph_residual:
        print(i)
    print(max_f_people)
    if max_f_people != necessary_flow_source:
        print("No es factible debido al estado de las vias")
    lines_railways_graph = create_lines_railways_graph(subway_people_graph,station_dict,subway_people_graph_residual,people_per_wagon,min_wagon_per_line)
    for i in lines_railways_graph:
        print(i)
    max_f_trains,res_graph = ford_fulkerson(lines_railways_graph,0,1)
    print(max_f_trains)


    return 

def create_lines_railways_graph(subway_people_graph,station_dict,subway_people_graph_residual,people_per_wagon,min_wagon_per_line):
    # Se creará un grafo para manejar el flujo de vagones
    # Esto consiste en ver cuantos vagones se necesitan para cada tramo, que es
    # la cantidad de gente en el tramo sobre la capacidad de un vagon redondeado
    # para arriba
    # A su vez se debe separar en líneas para cumplir la restricción del mínimo
    # por línea. Para esto se verá si cumplen la cantidad con los que necesitan
    # y si no, se agregará una capacidad al sumidero que es la demanda de la
    # línea
    # Los que son de una línea tienen aristas con capacidades numerables entre
    # ellos. Las combinaciones tienen capacidades infinitas
    visited = [False] * (len(subway_people_graph))
    visited[0] = True
    visited[1] = True # Son fuente y sumidero
    from collections import deque
    queue = deque([2])
    railways_graph = []
    railways_graph.append(["source",[]])
    railways_graph.append(["sink",[]])
    this_line = 2
    railways_graph.append(["Line"+str(this_line),[[0,float("inf")]]])
    railways_graph[0][1].append([this_line,float("inf")])
    lines_nodes_pos = [2]
    num_visited = 2

    while num_visited!=len(subway_people_graph):
        print(num_visited)
        num_visited+=1
        if not queue:
            print(visited)
            next_pos = visited.index(False)
            queue.append(next_pos)
            visited[next_pos] = True
            # num_visited += 1
            # Revisamos si cumple el mínimo de línea
            wagons_needed = 0
            for i in railways_graph[this_line][1]:
                print(i)
                if i[1] != float("inf"):
                    wagons_needed += i[1]
            if wagons_needed < min_wagon_per_line:
                railways_graph[this_line][1].append([1,min_wagon_per_line - wagons_needed])
                railways_graph[1][1].append([this_line,min_wagon_per_line - wagons_needed])
            this_line = len(railways_graph)
            lines_nodes_pos.append(this_line)
            railways_graph.append(["Line"+str(this_line),[[0,float("inf")]]])
            railways_graph[0][1].append([this_line,float("inf")])
        current_pos = queue.popleft()
        for i in range(len(subway_people_graph[current_pos][1])):
            # Cada arista que incide al nodo
            connected_node_pos = subway_people_graph[current_pos][1][i][0]
            edge_cap = subway_people_graph[current_pos][1][i][1]
            if visited[connected_node_pos] == False and edge_cap != float("inf"):
                # Agrego el tramo (arista) al grafo de tramos
                visited[connected_node_pos] = True
                # num_visited += 1
                queue.append(connected_node_pos)
                edge_in_residual = subway_people_graph_residual[current_pos][1][i][1]
                use_of_edge = math.ceil(abs(edge_in_residual-edge_cap)/people_per_wagon)
                name = "railway"+str(len(railways_graph))
                railways_graph.append([name,[[1,use_of_edge],[this_line,use_of_edge]]])
                railways_graph[1][1].append([len(railways_graph)-1,use_of_edge])
                railways_graph[this_line][1].append([len(railways_graph)-1,use_of_edge])
    # Revisamos si cumple el mínimo de línea
    wagons_needed = 0
    for i in railways_graph[this_line][1]:
        if i[1] != float("inf"):
            wagons_needed += i[1]
    if wagons_needed < min_wagon_per_line:
        railways_graph[this_line][1].append([1,min_wagon_per_line - wagons_needed])
        railways_graph[1][1].append([this_line,min_wagon_per_line - wagons_needed])
    return railways_graph



def read_stations(file_stations):
    # Se leerá el archivo de estaciones
    # Se espera un archivo como el siguiente:
    # Estacion1 numero_de_entrantes numero_de_salientes
    # Estacion2 numero_de_entrantes numero_de_salientes
    # Se entiende que, según las conexiones, se verán las líneas
    with open(file_stations) as open_file:
        stations_info = []
        line = open_file.readline().rstrip("\n\r")
        while line:
            parsed_line = line.split(" ")
            if len(parsed_line) == 3:
                parsed_line_list = [parsed_line[0] , int(parsed_line[1]) , int(parsed_line[2])]
                stations_info.append(parsed_line_list)
            else:
                print("Error al parsear estaciones")
                exit()
            line = open_file.readline().rstrip("\n\r")
    return stations_info

def read_railways(file_railways):
    # Se leerá el archivo de tramos de subte
    # Se espera algo como esto
    # estacionA estacionB (max_cantidad_en_tramo)
    # Si es una conexión entre líneas, max_cantidad_en_tramo no va
    with open(file_railways) as open_file:
        railways_info = []
        line = open_file.readline().rstrip("\n\r")
        while line:
            parsed_line = line.split(" ")
            if len(parsed_line) == 3:
                parsed_line_list = [parsed_line[0] , parsed_line[1] , int(parsed_line[2])]
                railways_info.append(parsed_line_list)
            elif len(parsed_line) == 2:
                parsed_line_list = [parsed_line[0] , parsed_line[1] ]
                railways_info.append(parsed_line_list)
            else:
                print("Error al parsear tramos")
                exit()
            line = open_file.readline().rstrip("\n\r")
    return railways_info

def create_subway_graph(file_stations,file_railways,max_people_per_wagon):
    # El grafo es así:
    # TODO explicar como es el grafo
    # El grafo se utiliza con lista de adyacencia:
    # Es una lista de listas. Cada lista aquí contiene, primero, el nombre de
    # la estación y luego una lista con de aristas, las cuales tienen 
    stations_info = read_stations(file_stations)
    railways_info = read_railways(file_railways)
    # subway_people_graph es con todas las cantidades consideradas gente
    subway_people_graph = []
    subway_people_graph.append(["source",[]])
    subway_people_graph.append(["sink",[]])
    station_dict = {"source":0,"sink":1}
    for station in stations_info:
        diff_people = station[2] - station[1]
        station_pos_in_graph = len(subway_people_graph)
        station_dict[station[0]] = station_pos_in_graph
        if diff_people != 0:
            # Ponemos la arista a la fuente o sumidero
            subway_people_graph.append([station[0],[[0 if diff_people<0 else 1, abs(diff_people) ]]])
            # Ponemos la arista desde la fuente o sumidero
            if diff_people<0:
                subway_people_graph[0][1].append([station_pos_in_graph,abs(diff_people)])
            else:
                subway_people_graph[1][1].append([station_pos_in_graph,abs(diff_people)])
        else:
            subway_people_graph.append([station[0],[]])
    for railway in railways_info:
        # Pongo aristas entre los nodos u y v
        u = station_dict[railway[0]]
        v = station_dict[railway[1]]
        capacity = float("inf") if len(railway) == 2 else (railway[2]*max_people_per_wagon)
        subway_people_graph[u][1].append([v,capacity])
        subway_people_graph[v][1].append([u,capacity])
    return subway_people_graph,station_dict




def ford_fulkerson(graph,pos_source,pos_sink):
    # Asumimos que el primer nodo es la fuente y el segundo el sumidero
    import copy
    graph_residual = copy.deepcopy(graph)
    source = graph_residual[pos_source]
    sink = graph_residual[pos_sink]
    max_flow = 0
    path,bottleneck = bfs_path(graph_residual,pos_source,pos_sink)
    while path:
        # Mientra haya camino, actualizo el maximo flujo y el grafo residual, e 
        # intento aumentar
        max_flow+=bottleneck
        # Actualizo el grafo residual moviéndome desde la fuente
        v_pos = pos_source
        path_pos = 1
        while v_pos!=pos_sink:
            # Busco la arista en la lista del grafo
            v_pos_next = path[path_pos]

            edge_in_list_pos = find_index_in_list(graph_residual[v_pos][1],v_pos_next)
            graph_residual[v_pos][1][edge_in_list_pos][1]-=bottleneck
            # Ahora sumo la capacidad para el otro lado
            edge_in_list_pos = find_index_in_list(graph_residual[v_pos_next][1],v_pos)
            graph_residual[v_pos_next][1][edge_in_list_pos][1]+=bottleneck

            v_pos = v_pos_next
            path_pos+=1

        path,bottleneck = bfs_path(graph_residual,pos_source,pos_sink)
    return max_flow,graph_residual


def find_index_in_list(l,index):
    for i in range(len(l)):
        if l[i][0] == index:
            return i
    return -1

def bfs_path(graph,start,finish):
    # Busca un camino de graph[start] a graph[finish] y da su cuello de botella
    # Hace BFS desde graph[start]
    # En la cola van el nodo en el que está, el camino hasta ese y el cuello de
    # botella
    from collections import deque
    queue = deque([[start,[],-1]])
    visited = [False]*len(graph)
    visited[start] = True
    found_path = False
    while queue and found_path is False:
        current = queue.popleft()
        current_node_pos = current[0]
        current_path = current[1]
        current_bottleneck = current[2]
        if current_node_pos == finish :
            # Estoy en el que tengo que llegar
            found_path = True
        else:
            for i in range(len(graph[current_node_pos][1])):
                next_node_pos = graph[current_node_pos][1][i][0]
                edge_value = graph[current_node_pos][1][i][1]
                new_bottleneck = min(current_bottleneck,edge_value)
                if visited[next_node_pos]==False and edge_value>0:
                    new_path = current_path.copy()
                    new_path.append(current_node_pos)
                    visited[next_node_pos] = True
                    if current_bottleneck == -1:
                        queue.append([next_node_pos,new_path,edge_value])
                    else:
                        queue.append([next_node_pos,new_path,new_bottleneck])
    if found_path == True:
        current_path.append(current_node_pos)
        return (current_path,current_bottleneck)
    else:
        return ([],-1)







if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parser.')
    parser.add_argument('file_stations')
    parser.add_argument('file_railways')
    parser.add_argument('people_per_wagon',type=int)
    parser.add_argument('min_wagon_per_line',type=int)
    parser.add_argument('num_wagons_in_system',type=int)
    parsed_args = parser.parse_args()
    file_stations = parsed_args.file_stations
    file_railways = parsed_args.file_railways
    people_per_wagon = parsed_args.people_per_wagon
    min_wagon_per_line = parsed_args.min_wagon_per_line
    num_wagons_in_system = parsed_args.num_wagons_in_system
    main(file_stations,file_railways,people_per_wagon,min_wagon_per_line,num_wagons_in_system)
