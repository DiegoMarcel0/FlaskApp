import re
import networkx as nx
import pandas as pd
import math
import matplotlib.pyplot as plt

#print(elementos)

def valencia_elemento(elemento_texto):
    """
    Consulta la el valor de la columna 'Valencia' de un elemento
    de la tabla de elementos (csv)
    Args:
        elemento_texto (str): Simbolo del elemento en la tabla periodica ('H', 'O', 'Au', etc)
    Returns: 
        valencia (int): Valencia del elemento
    Raises:
        No existe: El elemento no existe no aparece en la tabla
        Limites del modelo: La valencia no es muy complicada para este programa
    """
    valencia = elementos.get(elemento_texto, {}).get("NumberofValence")
    if valencia == None:
        print("No existe")
        return
    if math.isnan(valencia):
        print("Excepción: Limites del modelo")
        return
    print(valencia)
    return valencia

def consulta_valencias(elementos_molecula):
    """
    Consulta de las valencias de varios elementos a la vez
    Args:
        elementos_molecula (list): Los elementos para consultar su valencia
    Return:
        elementos_molecula_valores (list): Los valores de valencia
    """
    elementos_molecula_valores = []
    for elemento in elementos_molecula:
        valencia = valencia_elemento(elemento)
        elementos_molecula_valores.append(valencia)
    return elementos_molecula_valores

def datos_elementos(elementos_molecula):
    """
    Crea un diccionario en base a la lista de elementos con los datos del
    diccionario 'elementos' declarada al principio. Se le agrega Numero en molecula.
    Args:
        elementos_molecula: Lista de tuplas ("H", 2). Elemento y numero en molecula
    Returns:
        elem_molecula (Dict): Datos de elementos en la molecula
    Raises:
        No existe elemento: No existe elemento de la lista
        Limites del modelo: No hay numero de valencia valido para este modelo
    """
    datos_molecula =  {k: elementos[k] for k, v in elementos_molecula if k in elementos}
    if (len(elementos_molecula) != len(datos_molecula) or len(elementos_molecula)==0):
        print("Error: Elementos invalidos")
        return
    for elem, cantidad in elementos_molecula:
        datos_molecula[elem]["NumEnMolecula"] = cantidad
        if math.isnan(datos_molecula[elem]["NumberofValence"]):
            print("Excepción: Limites del modelo")
            return
    return datos_molecula
    
    
def formatear_molecula(molecula_texto):
    """
    Transforma un texto de molecula tipo 'H2O' o '(OH)-1' a datos manejables
    Args:
        molecula_texto (str): molecula directa del usuario
    Returns:
        tuple: una lista de tuplas de texto y valor donde cada uno viene de 'H2'-> ('H',2)
               La carga de la molecula '(...)-1' -> -1
    """
    resultado = re.findall(r'[A-Z][a-z]*[0-9]*', molecula_texto)
    molecula_elementos = []
    carga = 0
    try:
        #Desentrañar elementos y su cantidad
        for res in resultado:
            atomicidad = 1
            atomicidad_texto = re.findall(r'[0-9]+', res)
            if atomicidad_texto != []:
                atomicidad = int(atomicidad_texto[0])
            molecula_elementos.append((re.findall(r'[A-Z][a-z]*', res)[0], atomicidad))

        #Desentrañar la carga de la molecula
        carga_texto  = re.sub(r"\s*\(.*?\)", "", molecula_texto)
        if "(" in molecula_texto:
            carga = int(carga_texto)
    except:
        print("Error: Molecula Invalida")
    return molecula_elementos, carga

def generar_atomos(molecula = nx.Graph(), element = ""):
    """
    Inserta de que haya tantos elementos como en 'NumEnMolecula' en el grafo.
    Excepto en el 
    Args:
        molecula (Graph): representa la molecula
        element (str): es el elemento
    Returns:
        creados (list): Nombres de los atomos (nodos) insertados
        molecula (Graph): Donde se insertaron los atomos (nodos)
    """
    creados = []
    n=0
    if element == molecula.graph["elemento_central"]:
        n=1
    for i in range(n,datos_molecula[element]["NumEnMolecula"]):
        molecula.add_node(element+str(i+1), 
                   free_atoms=datos_molecula[element]["NumberofValence"], 
                   elemento = element, 
                   )
        creados.append(element+str(i+1))
    return creados, molecula

def formar_enlaces(molecula_G = nx.Graph(), restantes = []):
    """
    Enlaza los atomos que pueda al atomo central
    Args:
        molecula_G (Graph): Grafo que representa la molecula en 2D
        restantes (list): Elementos restantes a unirse a la molecula
    Returns:
        molecula_G (Graph): Grafo con elementos y enlaces 
    """
    if len(restantes)==0:
        return molecula_G
    # AGREGAR ENLACES
    a_enlazar = restantes[:]
    restantes.insert(0,molecula_G.graph["atomo_central"])
    for atomo in restantes:
        max_octeto =maximos_atomos(molecula_G.nodes[atomo]["elemento"])
        while a_enlazar:
            if molecula_G.nodes[atomo]["free_atoms"] == 0:
                break
            otro_atomo = a_enlazar.pop(0)
            if atomo == otro_atomo or molecula_G.degree(otro_atomo) != 0:
                #a_enlazar.insert(0,otro_atomo)
                continue
            #Caso imposible???
            if  molecula_G.nodes[otro_atomo]["free_atoms"] == 0:
                continue
            molecula_G.nodes[atomo]["free_atoms"] -= 1
            molecula_G.nodes[otro_atomo]["free_atoms"] -= 1
            molecula_G.add_edge(otro_atomo, atomo, weight=2)
    #BUSCAMOS GENERAR ENLACES MULTIPLES
    molecula_G = enlaces_multiples(molecula_G)
    return molecula_G

    
def repartir_cargas(grafo = nx.Graph(), carga = 1,  cargador = ""):
    """
    Reparte una carga al primer atomo apropiado que se encuentre
    Args:
    grafo (Graph): Representa la molecula
    carga (int): La carga negativa o positiva. Es -1 o 1.
    cargador (str): Elemento al que se le dejara la carga
    """
    if carga < 0:
        ion = 1
    else:
        ion = -1
    for node in grafo.nodes:
        if grafo.nodes[node]["elemento"] == cargador and grafo.nodes[node]["free_atoms"]>0:
            grafo.nodes[node]["free_atoms"] += ion
            carga +=ion
        if carga==0:
            break
    return carga, grafo
    """if(carga!=0):
        print(f"Ionización fallida: {carga}")
    else:
        print(f"Ionización exitosa: {carga}")"""

def maximos_atomos(elemento):
    """
    Algoritmo heuristico para encontrar el octeto para todos los elementos
    Args:
        elemento (str): Elemento a analizar
    Returns:
        max_octeto (int): El octeto calculado
    """
    max_octeto = 8
    if (elemento=="H"):
        max_octeto = 2
    elif datos_molecula[elemento]["Period"] >=3:
        max_octeto = 12
    return max_octeto

def enlaces_multiples(grafo = nx.Graph()):
    """
    Genera los enlaces dobles o triples en la molecula según la disponibilidad
    Args:
        grafo (Graph): Representa la molecula
    Returns:
        grafo (Graph): Molecula con enlaces generados
    """
    for node in grafo.nodes:
        node_dic = grafo.nodes[node]
        max_octeto =maximos_atomos(node_dic["elemento"])
        if node_dic["free_atoms"]+ grafo.degree(node) * 2 >= max_octeto:
            continue
        if int(node_dic["free_atoms"]) % 2 != 1:
            continue
        candidato = ""
        for vecino in grafo.neighbors(node):
            vecino_dic = grafo.nodes[vecino]
            if vecino_dic["free_atoms"] + grafo.degree(vecino)*2 >= maximos_atomos(vecino_dic["elemento"]):
                continue
            vecino_dic["weight"] += 2
            #print(f"nodo {node} tiene {grafo.nodes[node]["free_atoms"]} electrones libres")
            #print(f"peso de -- {node} -> {vecino} = {grafo[node][vecino]["weight"]}")
            #print(f"octavidad de { grafo.nodes[vecino]["elemento"]} --> {maximos_atomos(grafo.nodes[vecino]["elemento"])}")
            node_dic["free_atoms"] -= 1
            vecino_dic["free_atoms"] -= 1
    return grafo





#formula = input("Introduce fórmula: ")

##TEXTO DE MOLECULA -> ESTRUCTURA DE DATP DE MOLECULA
""" texto = "(Agua12Bolsa21Casa333)-12"
#molecula = formatear_molecula(texto)
molecula = ([("Na",1), ("Cl",1), ("N", 2)], 0)
molecula = ([("Na",1), ("Cl",1), ("N", 2)], 0)

## EJEMPLOS
molecula = formatear_molecula("CH4")
#molecula = formatear_molecula("NH3")
#molecula = formatear_molecula("H2O")
#molecula = formatear_molecula("CO2")
#molecula = formatear_molecula("CH2O")
molecula = formatear_molecula("(NH4)+1") 
#molecula = formatear_molecula("(OH)-1")
molecula = formatear_molecula("O2")
molecula = formatear_molecula("N2") #NO
molecula = formatear_molecula("H2")
molecula = formatear_molecula("F2")
molecula = formatear_molecula("O3")
molecula = formatear_molecula("HF")
molecula = formatear_molecula("C2H4") #NO
molecula = formatear_molecula("C2H2") #no
molecula = formatear_molecula("(CN)-1")#NO
molecula = formatear_molecula("PCl5")
molecula = formatear_molecula("SF6")
molecula = formatear_molecula("(SO4)-2") #2/3 FALTA SIMETRIA
molecula = formatear_molecula("SO2")
"""
def estructura_lewis(formula):
    global datos_molecula
    #molecula_texto = "H2O"
    molecula, carga = formatear_molecula(formula)
    datos_molecula = datos_elementos(molecula)
    if datos_molecula:
        print ("\n\n\nValidado correctamente\n")
    else:
        print("Invalida - Finalizando...\n\n")
        return
    # ELEGIR ATOMO CENTRAL
    elementos_originales = sorted(
        datos_molecula.keys(),
        key=lambda k: (datos_molecula[k]["NumEnMolecula"], datos_molecula[k]["Electronegativity"])
    )
    elemento_central = elementos_originales[0]
    if elemento_central == "H" and len(elementos_originales)>1:
        elemento_central = elementos_originales[1]
    atomo_central = elemento_central + "1"
    molecula_graph = nx.Graph()
    molecula_graph.add_node(atomo_central, 
                            free_atoms=datos_molecula[elemento_central]["NumberofValence"], 
                            elemento = elemento_central, 
                            )
    molecula_graph.graph["elemento_central"] = elemento_central
    molecula_graph.graph["atomo_central"] = atomo_central
    # AGREGAR ATOMOS
    elementos_originales = sorted(
        elementos_originales,
        key=lambda k: (-datos_molecula[k]["Electronegativity"])
    )
    restantes = []
    for elem in elementos_originales:
        temp, molecula_graph = generar_atomos(molecula_graph, elem)
        restantes.extend(temp)
    #print ("lista restantes: ",restantes)
    # FORMAR ENLACES
    molecula_graph = formar_enlaces(molecula_graph, restantes)
    molecula_graph = enlaces_multiples(molecula_graph)

    #REPARTIR CARGAS
    if carga != 0:
        elementos_originales = sorted(
            elementos_originales,
            key=lambda k: datos_molecula[k]["Electronegativity"],
            reverse=(carga < 0)
        )
        for element in elementos_originales:
            carga, molecula_graph = repartir_cargas(molecula_graph, carga,  element)
            if carga == 0:
                return
    return molecula_graph


datos_molecula = {}
elementos = {}
#import os
if __name__ =="__main__":
    tabla_periodica = pd.read_csv("table/Periodic_Table_of_Elements.csv")
    elementos = tabla_periodica[["AtomicNumber","Symbol", "Electronegativity", "NumberofValence", "Period"]]
    elementos = elementos.set_index("Symbol").to_dict("index")
else:
    #try:
    tabla_periodica = pd.read_csv("views/lewis/table/Periodic_Table_of_Elements.csv")
    elementos = tabla_periodica[["AtomicNumber","Symbol", "Electronegativity", "NumberofValence", "Period"]]
    elementos = elementos.set_index("Symbol").to_dict("index")
    #except:
        #print("Nel Pastel")
        #print("Estás en la carpeta:", os.getcwd())
"""
for nodo, datos in estructura_lewis("CO2").nodes(data=True):
    print(f"Nodo: {nodo} | Datos: {datos}")
    print(f"weight: " )
"""
