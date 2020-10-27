import networkx as nx
import matplotlib.pyplot as plt
import re


class Vertice:

    def __init__(self, key):
        self.id = key
        self.vertices_ady = {}
        self.color = 'blanco'
        self.distancia = 0
        self.padre = None

    def __str__(self):
        return f'{self.id}: Color: {self.color}, Padre: {self.padre} ->\n' \
               f' {str([v.id for v in self.vertices_ady.keys()])}'

    def agregar_vertice_ady(self, vertice, ponderacion=0):
        self.vertices_ady[vertice] = ponderacion

    def obtener_vertices_ady(self):
        arreglo_nodos = []
        {arreglo_nodos.append(v.id) for v in self.vertices_ady.keys()}
        return arreglo_nodos

    def obtener_ponderacion_vertice(self, vertice):
        return self.vertices_ady[vertice]

    def eliminar_vertice_ady(self, nodo):
        for element in self.vertices_ady.keys():
            if element.id == nodo:
                del self.vertices_ady[element]
                break


class Grafo:

    def __init__(self):
        self.vertices = {}
        self.total_vertices = 0
        self.G = nx.Graph()

    def agregar_vertice(self, vertice_id):
        self.total_vertices += 1
        self.G.add_node(vertice_id, color='white')
        nuevo_vertice = Vertice(vertice_id)
        self.vertices[vertice_id] = nuevo_vertice
        return nuevo_vertice

    def obtener_vertice(self, vertice_id):
        try:
            return self.vertices[vertice_id]
        except KeyError:
            return None

    def agregar_arista(self, vertice_origen, vertice_destino, ponderacion=0):
        if vertice_origen not in self.vertices:
            self.agregar_vertice(vertice_origen)
        if vertice_destino not in self.vertices:
            self.agregar_vertice(vertice_destino)

        self.vertices[vertice_origen].agregar_vertice_ady(
            self.vertices[vertice_destino], ponderacion)
        self.G.add_edge(vertice_origen, vertice_destino, weight=ponderacion)

    def obtener_vertices(self):
        return [state for state in self.vertices.keys()]

    def dibujar_grafo(self, time):

        val_map = {'::CCCMMM': 1,
                   'CCCMMM::': .10}
        values = [val_map.get(str(node), 0.25) for node in self.G.nodes()]
        plt.cla()  # Limpia el plot para superponer figuras
        nx.draw_circular(self.G, cmap=plt.cm.Dark2, with_labels=True, node_color=values, font_color='black', font_size=5)
        plt.show()
        plt.pause(time)

    def eliminar_conexion(self, nodo, nodo_siguiente):
        self.vertices[nodo].eliminar_vertice_ady(nodo_siguiente)
        self.G.remove_edge(nodo, nodo_siguiente)

    def activar_interactivo_plot(self):
        plt.ion()

    def add_multi_nodes(self, conjunto_elementos):
        for node in conjunto_elementos:
            self.agregar_vertice(node)

    def clean_ady_node(self, node):
        self.vertices[node]
        for element in self.vertices[node].vertices_ady:
            del self.vertices[node].vertices_ady[element]

    def __contains__(self, item):
        return item in self.vertices

    def __iter__(self):
        return iter(self.vertices.values())


class LogicSolution(Grafo):
    def __init__(self):
        Grafo.__init__(self)
        self.Bote = ['izq']

    def verificar_cambio_unico(self, state, previus_state):
        # Movimiento canival origen -> bote
        if abs(len(re.findall("C", state.split(':')[0])) - len(re.findall("C", previus_state.split(':')[0]))) == 1 and abs(len(re.findall("C", state.split(':')[1])) - len(re.findall("C", previus_state.split(':')[1]))) == 1 and abs(len(re.findall("C", state.split(':')[2])) - len(re.findall("C", previus_state.split(':')[2]))) == 0 and \
        abs(len(re.findall("M", state.split(':')[0])) - len(re.findall("M", previus_state.split(':')[0]))) == 0 and abs(len(re.findall("M", state.split(':')[1])) - len(re.findall("M", previus_state.split(':')[1]))) == 0 and abs(len(re.findall("M", state.split(':')[2])) - len(re.findall("M", previus_state.split(':')[2]))) == 0 and\
        'izq' in self.Bote:
            if len(state.split(':')[1]) >= 1:
                self.Bote = ['der', 'izq']
            else:
                self.Bote = ['izq']
            return True
        # Movimiento misionero origen -> bote
        if abs(len(re.findall("C", state.split(':')[0])) - len(re.findall("C", previus_state.split(':')[0]))) == 0 and abs(len(re.findall("C", state.split(':')[1])) - len(re.findall("C", previus_state.split(':')[1]))) == 0 and abs(len(re.findall("C", state.split(':')[2])) - len(re.findall("C", previus_state.split(':')[2]))) == 0 and \
        abs(len(re.findall("M", state.split(':')[0])) - len(re.findall("M", previus_state.split(':')[0]))) == 1 and abs(len(re.findall("M", state.split(':')[1])) - len(re.findall("M", previus_state.split(':')[1]))) == 1 and abs(len(re.findall("M", state.split(':')[2])) - len(re.findall("M", previus_state.split(':')[2]))) == 0 and\
        'izq' in self.Bote:
            if len(state.split(':')[1]) >= 1:
                self.Bote = ['der', 'izq']
            else:
                self.Bote = ['izq']
            return True
        # Movimiento canival bote -> meta
        if abs(len(re.findall("C", state.split(':')[1])) - len(re.findall("C", previus_state.split(':')[1]))) == 1 and abs(len(re.findall("C", state.split(':')[2])) - len(re.findall("C", previus_state.split(':')[2]))) == 1 and abs(len(re.findall("C", state.split(':')[0])) - len(re.findall("C", previus_state.split(':')[0]))) == 0 and \
        abs(len(re.findall("M", state.split(':')[1])) - len(re.findall("M", previus_state.split(':')[1]))) == 0 and abs(len(re.findall("M", state.split(':')[2])) - len(re.findall("M", previus_state.split(':')[2]))) == 0 and abs(len(re.findall("M", state.split(':')[0])) - len(re.findall("M", previus_state.split(':')[0]))) == 0 and \
        'der' in self.Bote:
            if len(state.split(':')[1]) >= 1:
                self.Bote = ['der', 'izq']
            else:
                self.Bote = ['der']
            return True
        # Movimiento misionero bote -> meta
        if abs(len(re.findall("C", state.split(':')[1])) - len(re.findall("C", previus_state.split(':')[1]))) == 0 and abs(len(re.findall("C", state.split(':')[2])) - len(re.findall("C", previus_state.split(':')[2]))) == 0 and abs(len(re.findall("C", state.split(':')[0])) - len(re.findall("C", previus_state.split(':')[0]))) == 0 and \
        abs(len(re.findall("M", state.split(':')[1])) - len(re.findall("M", previus_state.split(':')[1]))) == 1 and abs(len(re.findall("M", state.split(':')[2])) - len(re.findall("M", previus_state.split(':')[2]))) == 1 and abs(len(re.findall("M", state.split(':')[0])) - len(re.findall("M", previus_state.split(':')[0]))) == 0 and\
        'der' in self.Bote:
            if len(state.split(':')[1]) >= 1:
                self.Bote = ['der', 'izq']
            else:
                self.Bote = ['der']
            return True
        # Movimiento canival bote -> origen
        if abs(len(re.findall("C", state.split(':')[1])) - len(re.findall("C", previus_state.split(':')[1]))) == 1 and abs(len(re.findall("C", state.split(':')[2])) - len(re.findall("C", previus_state.split(':')[2]))) == 1 and abs(len(re.findall("C", state.split(':')[0])) - len(re.findall("C", previus_state.split(':')[0]))) == 0 and \
        abs(len(re.findall("M", state.split(':')[1])) - len(re.findall("M", previus_state.split(':')[1]))) == 0 and abs(len(re.findall("M", state.split(':')[2])) - len(re.findall("M", previus_state.split(':')[2]))) == 0 and abs(len(re.findall("M", state.split(':')[0])) - len(re.findall("M", previus_state.split(':')[0]))) == 0 and \
        'der' in self.Bote:
            if len(state.split(':')[1]) >= 1:
                self.Bote = ['der', 'izq']
            else:
                self.Bote = ['izq']
            return True
        # Movimiento misionero bote -> origen
        if abs(len(re.findall("C", state.split(':')[1])) - len(re.findall("C", previus_state.split(':')[1]))) == 0 and abs(len(re.findall("C", state.split(':')[2])) - len(re.findall("C", previus_state.split(':')[2]))) == 0 and abs(len(re.findall("C", state.split(':')[0])) - len(re.findall("C", previus_state.split(':')[0]))) == 0 and \
        abs(len(re.findall("M", state.split(':')[1])) - len(re.findall("M", previus_state.split(':')[1]))) == 1 and abs(len(re.findall("M", state.split(':')[2])) - len(re.findall("M", previus_state.split(':')[2]))) == 1 and abs(len(re.findall("M", state.split(':')[0])) - len(re.findall("M", previus_state.split(':')[0]))) == 0 and\
        'der' in self.Bote:
            if len(state.split(':')[1]) >= 1:
                self.Bote = ['der', 'izq']
            else:
                self.Bote = ['izq']
            return True
        return False

    def verificar(self, state, previus_state):
        # Verificar camino sin solucion
        if self.vertices[state].color == 'gris':
            return False
        # Revision del mismo elemento
        if state == previus_state:
            return False
        # Verificar no recorrido
        if len(self.vertices[state].obtener_vertices_ady()) > 0:
            return False
        # Revision capacidad bote
        if len(state.split(':')[1]) > 2:
            return False
        # Revision condicion canivales origen
        if len(re.findall("C", state.split(':')[0])) > len(re.findall("M", state.split(':')[0])) and len(re.findall("M", state.split(':')[0])) != 0:
            return False
        # Revision condicion canivales meta
        if len(re.findall("C", state.split(':')[2])) > len(re.findall("M", state.split(':')[2])) and len(re.findall("M", state.split(':')[2])) != 0:
            return False
        # Revision de cambio unico
        return self.verificar_cambio_unico(state, previus_state)

    def indicar_camino(self):
        initial_element = 'CCCMMM::'
        array_solucion = []
        while len(self.vertices[initial_element].obtener_vertices_ady()) != 0:
            if len(initial_element) == 8:
                array_solucion.append(initial_element)
            initial_element = self.vertices[initial_element].obtener_vertices_ady()[0]
        array_solucion.append(self.vertices[initial_element].id)
        return array_solucion

    def back_to_the_past(self, cola_pasado):
        if len(self.indicar_camino()) > 1:
            self.eliminar_conexion(self.indicar_camino()[-2], self.indicar_camino()[-1])
            self.Bote = cola_pasado[-2]
            cola_pasado.pop()
        return cola_pasado

    def resolver_problema(self, actual_element):
        contador = 0
        cola = [self.Bote]
        while True:
            contador += 1
            if actual_element == '::CCCMMM':
                print('\nterminando iteracion debido a encontrar respuesta\n')
                contador = 0
                for element in self.indicar_camino():
                    print(f'{contador} {" " * contador}{element}')
                    contador += 1
                break
            if contador > 200:
                print('terminando while por mas de 200 iteraciones')
                break
            # Se cumplen correctamente verificaciones
            for element in self.obtener_vertices():
                # verifica si elementos cumplen condiciones
                if self.verificar(element, actual_element):
                    self.agregar_arista(actual_element, element)
                    print(actual_element, element)
                    cola.append(self.Bote)
                    actual_element = element
                    break
            # Retroceso por imposibilidad de movimientos
            else:
                self.vertices[actual_element].color = 'gris'
                actual_element = self.indicar_camino()[-2]
                cola = self.back_to_the_past(cola)


if __name__ == '__main__':
    # Estados posibles donde se verificaran condiciones para resolver problema
    Estados = [
        # Elementos sin nada en el bote
        'CCCMMM::',
        'CCCMM::M', 'CCMMM::C',
        'CCCM::MM', 'CCMM::MC', 'CMMM::CC',
        'CCC::MMM', 'CCM::MMC', 'CMM::MCC', 'MMM::CCC',
        'CC::MMMC', 'CM::MMCC', 'MM::MCCC',
        'C::MMMCC', 'M::MMCCC',
        '::CCCMMM',
        # Elementos solo un misionero en el bote
        'CCCMM:M:',
        'CCCM:M:M', 'CCMM:M:C',
        'CCC:M:MM', 'CCM:M:MC', 'CMM:M:CC',
        'CC:M:MMC', 'CM:M:MCC', 'MM:M:MCC',
        'M:M:MCCC', 'C:M:MMCC',
        ':M:CCCMM',
        # Elementos solo un canival en el bote
        'CCMMM:C:',
        'CCMM:C:M', 'CMMM:C:C',
        'CCM:C:MM', 'CMM:C:MC', 'MMM:C:CC',
        'CC:C:MMM', 'CM:C:MMC', 'MM:C:MCC',
        'M:C:MMCC', 'C:C:MMMC',
        ':C:CCMMM',
        # Elementos con dos misioneros en el bote
        'MCCC:MM:',
        'MCC:MM:C', 'CCC:MM:M',
        'MC:MM:CC', 'CC:MM:MC',
        'M:MM:CCC', 'C:MM:MCC',
        ':MM:MCCC',
        # Elementos con un misionero y un canival en el bote
        'MMCC:MC:',
        'MCC:MC:M', 'MMC:MC:C',
        'MM:MC:CC', 'MC:MC:MC', 'CC:MC:MM',
        'M:MC:MCC', 'C:MC:MMC',
        ':MC:MMCC',
        # Elementos con dos canivales en el bote
        'MMMC:CC:',
        'MMM:CC:C', 'MMC:CC:M',
        'MM:CC:MC', 'MC:CC:MM',
        'C:CC:MMM', 'M:CC:MMC',
        ':CC:MCCC',
    ]

    # Llamado a instancias y metodos en las clases para la resolucion del problema
    print('')
    ig = LogicSolution()  # instance_grafo = ig se instancia la clase LogicSolution
    # activar_interactivo_plot permite el refresco del grafico en caso de ser necesario
    ig.activar_interactivo_plot()
    # add_multi_nodes añade los estados en la variable Estados como nodos a ser representados en el grafico final
    ig.add_multi_nodes(Estados)
    # resolver_problema indica de donde se desea  resolve el problema
    ig.resolver_problema('CCCMMM::')
    # dibujar_grafo recibe el tiempo que se desea mostrar el plot de los nodos
    ig.dibujar_grafo(1)