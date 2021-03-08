import json
from numpy import random
from typing import Dict, List


def flatten_matrix(m):
    flat = []
    for line in m:
        flat += line
    return flat


def structuration_donnees():
    d: Dict = {}
    with open("data.json", "r") as f:
        data: Dict = json.load(f)

        d = {i: [] for i in range(0, 10)}  # we create a dict with keys from 0 to 9 with an empty list for every key

        for key in data.keys():  # we loop all the matrix in the ref data
            for res_key in d.keys():  # we loop for all the numbers from 1 to 9
                if str(res_key) in key:  # we search to what number the ref matrix corresponds to
                    # we append the data to it's correspondent number in the res dict
                    d[res_key].append(flatten_matrix(data[key]))
    return d


def print_matrix(m: list):
    LINE_LENGTH: int = 5
    print(len(m)/LINE_LENGTH)
    for i, digit in enumerate(m):
        # It prints the number of the matrix in the terminal
        # the i+1 is because the lists starts at index 0 which obviously causes the mod to be 0
        print("#" if digit == 1 else ".", end="\n" if (i+1) % 5 == 0 else "")


def init_poids(dimEntree: int, dimSortie: int) -> List:
    random.seed(2)  # NE PAS TOUCHER CETTE LIGNE QUI REND DETERMINISTE LE RESULTAT
    # create a nxp matrix with values ranging from -50 to 50
    return [[(100*random.random()-50) for n in range(dimSortie)] for i in range(dimEntree)]


def calcul_neurone(j: int, e: List, poids):
    result = 0
    for i in range(len(e)):
        result += e[i] * poids[i][j]
        # resultat = int(result > 0)

    return result


def calcul_reseau(e, poids):
    return [calcul_neurone(neuron, e, poids) for neuron in range(10)]


def apprendre_neurone(e,poids, j, sortie_attendue):
    h = 5
    valeur_calculee = calcul_neurone(j, e, poids)
    for i in range(len(poids)):
        valeur_desiree = 1 if sortie_attendue == j else 0
        poids[i][j] = poids[i][j] + (valeur_desiree - valeur_calculee)*e[i]*h
    return poids


def apprendre_reseau(e, poids, sortie_attendue):
    for neuron in range(10):
        apprendre_neurone(e, poids, neuron, sortie_attendue)


def apprendre(d, poids):
    for key in d: # for every number it should study
        for number_specific in d[key]:  # give every number example to the enctrance to the neuron
            apprendre_reseau(number_specific, poids, key)


def main():
    d = structuration_donnees()
    poids_neurones = init_poids(30, 10)
    print('Learning...')
    for i in range(5000):
        apprendre(d, poids_neurones)
    flat_input = noise(generate_matrix_number(d))
    output = calcul_reseau(flat_input, poids_neurones)
    print(output)


