import math
import random

numDivisoes = [4, 6, 6, 6, 6, 6, 4, 4]  # Qtd. de divisões para cada variável, em ordem.


class Node:

    def __init__(self):
        self.varClas = None
        self.listaIndices = []
        self.divisores = []
        self.filhos = []
        self.pai = None
        self.vars_passadas = []
        self.classe = 0
        self.pureza = 0
        self.mediaReg = -1


def proper_round_og(num, dec=0):
    num = str(num)[:str(num).index('.')+dec+2]
    if num[-1]>='5':
        return float(num[:-2-(not dec)]+str(int(num[-2-(not dec)])+1))
    return float(num[:-1])

def proper_round(num):
    i = math.trunc(num)
    if num - i > 0.42:
        return i + 1
    else:
        return i


def calcEntropiaAbsoluta(tabela, listaIndices, indVar):
    n = len(tabela)
    divisores = []
    resultados = []
    for x in range(0, numDivisoes[indVar] - 1):  # Inicializa o vetor de divisores
        divisores.append(0)
        resultados.append(0)
    max = -9999
    min = 9999
    i = -1
    for linha in tabela:
        i += 1
        if i not in listaIndices:
            continue
        if float(linha[indVar]) > max:
            max = float(linha[indVar])
        if float(linha[indVar]) < min:
            min = float(linha[indVar])

    amplitude = max - min  # Calcula a amplitude dos dados na variável selecionada.
    #print(min)
    #print(max)

    for i in range(0, numDivisoes[indVar]-1):   #Calcula os divisores.
        divisores[i] = min + (i+1) * amplitude / numDivisoes[indVar]

    divisores.append(max)
    #divisores = determinaDivisores(indVar, listaIndices)
    resultados.append(0)

    #print(divisores)

    j = -1
    for linha in tabela:  # Retorna a quantidade de registros em cada divisão (vetor de resultados)
        j += 1
        if j not in listaIndices:
            continue
        x = abs(float(linha[indVar]))

        escolhido = 0
        i = 0

        for divisor in divisores:
            if float(divisor) >= x:
                escolhido = i
                break
            i += 1

        resultados[escolhido] += 1

    #print("Resultados: {}".format(resultados))

    soma_final = 0

    for item in resultados:
        if item == 0:
            continue
        soma_final -= (item / n) * math.log2(item / n)

    #print("ENTROPIA FINAL: {}".format(soma_final))

    return (soma_final, min, amplitude, resultados)


def classificar(tabela, listaIndices, indVar, min, amplitude):
    res = []
    divisores = []
    for i in range(0, numDivisoes[indVar]):
        res.append([])
    for x in range(0, numDivisoes[indVar]):  # Inicializa o vetor de divisores
        divisores.append(0)
    if indVar == 7:
        for i in range(0, numDivisoes[indVar]):  # Calcula os divisores.
            divisores[i] = min + (i + 1) * amplitude / numDivisoes[indVar]
    else:
        divisores = determinaDivisores(tabela, indVar, listaIndices)
    i = -1
    for linha in tabela:
        i += 1
        if i not in listaIndices:
            continue
        divisaoEncontrada = 0
        for divisor in divisores:
            if divisor < abs(float(linha[indVar])):
                divisaoEncontrada += 1
                continue
            else:
                res[divisaoEncontrada].append(i)
                break

    return res

def calcEntropiaNova(tabela, listaIndices, indVar):
    divisoes = classificar(tabela, listaIndices, indVar, 0, 0)
    somas = [0] * 4
    soma_final = 0
    for i in range(0, len(divisoes)):
        for j in range(0, len(divisoes[i])):
            if len(divisoes[i]) == 0:
                continue
            somas[int(tabela[divisoes[i][j]][7]) - 1] += 1
        for item in somas:
            if item == 0:
                continue
            soma_final -= (item / len(divisoes[i])) * math.log2(item / len(divisoes[i]))
        #print(somas)
        somas = [0] * 4
    #print("VAR - {}, ENTROPIA - {}".format(indVar, soma_final))
    return soma_final



def iteracao_id3(tabela, listaIndices, pai, vetorCaracteristicas):
    novo = Node()
    novo.listaIndices = listaIndices
    # print("ÍNDICES: {}".format(listaIndices))
    novo.pai = pai
    if pai is not None:
        for item in pai.vars_passadas:
            novo.vars_passadas.append(item)
        novo.vars_passadas.append(pai.varClas)

    cont1 = 0
    for item in vetorCaracteristicas:
        if item == 1:
            cont1 += 1

    if cont1 == 2:
        numDivisoes[3] = numDivisoes[3] + 6
        numDivisoes[4] = numDivisoes[4] + 6
        numDivisoes[5] = numDivisoes[5] + 6

    ########## BLOCO 1: VERIFICA SE É NECESSÁRIA MAIS UMA DIVISÃO
    classificações = classificar(tabela, listaIndices, 7, 1, 3)
    #print("à: {}".format(classificações))
    divisao = 0
    contagem = 0
    for i in range(0, len(classificações)):
        if len(classificações[i]) > 0:
            contagem += 1
            divisao = i

    if contagem == 1:
        novo.classe = int(tabela[int(classificações[divisao][0])][7])
        novo.filhos = []
        novo.divisores = []
        novo.varClas = None
        novo.pureza = 1
        media_final = 0
        for item in listaIndices:
            media_final += float(tabela[item][6])
        novo.mediaReg = media_final / len(listaIndices)
        return novo

    ########## BLOCO 2: ENTROPIA
    x = None
    min = 9999
    sel = 0
    selx = None
    for i in range(3, 6):
        if i in novo.vars_passadas:
            continue
        if vetorCaracteristicas[i-3] == 0:
            continue
        x = calcEntropiaNova(tabela, listaIndices, i)
        if x < min:
            min = x
            sel = i
            selx = x

    ########## BLOCO 3: TRATAMENTO
    if min == 9999:
        novo.filhos = []
        novo.divisores = []
        novo.varClas = -1
        max = -9999
        for j in range(0, len(classificações)):
            if len(classificações[j]) > max:
                max = len(classificações[j])
                novo.classe = j + 1

        novo.pureza = max / len(listaIndices)
        media_final = 0
        for item in listaIndices:
            media_final += float(tabela[item][6])
        novo.mediaReg = media_final / len(listaIndices)

    else:
        novo.varClas = sel
        divisoresTemp = determinaDivisores(tabela, sel, listaIndices)
        indicesFilhos = classificar(tabela, listaIndices, sel, 0, 0)
        #print("INDICES_F: {}".format(indicesFilhos))
        for t in range(0, len(indicesFilhos)):
            if len(indicesFilhos[t]) == 0:
                continue
            novo.divisores.append(divisoresTemp[t])
            if numDivisoes[3] > numDivisoes[2]:
                numDivisoes[3] = numDivisoes[2]
                numDivisoes[4] = numDivisoes[2]
                numDivisoes[5] = numDivisoes[2]
            novo.filhos.append(iteracao_id3(tabela, indicesFilhos[t], novo, vetorCaracteristicas))
    return novo


def classificar_item(item, arvore):
    # print("ITEM = {}; VAR = {}; DIVISORES = {}".format(item, arvore.varClas, arvore.divisores))
    if arvore.divisores == [] and arvore.classe != 0:
        #print("NÓ {}, CLASSIFICAÇÃO {}".format(item[0], arvore.classe))
        return arvore.classe
    if arvore.filhos == [] or arvore.filhos == None:
        #print("NÓ {}, CLASSIFICAÇÃO {}".format(item[0], arvore.classe))
        return arvore.classe
    filho = 0
    # print("VAR = {}; VALOR = {}; DIVISORES: {}".format(arvore.varClas, item[arvore.varClas], arvore.divisores))
    for divisor in arvore.divisores:
        if abs(float(item[arvore.varClas])) > divisor:
            filho += 1

            if filho >= len(arvore.filhos):
                filho = len(arvore.filhos) - 1
                # print("FILHO = {}; ARVORE.FILHOS = {}".format(filho, len(arvore.filhos)))
                res = classificar_item(item, arvore.filhos[filho])
                # print("PARA NÓ COM VAR = {}; LEN(FILHOS) = {}; CLASSIFICAÇÃO = {}".format(arvore.varClas, len(arvore.filhos), res))
                return res

            continue
        else:
            if filho >= len(arvore.filhos):
                filho = len(arvore.filhos) - 1
            #print("FILHO = {}; ARVORE.FILHOS = {}".format(filho, len(arvore.filhos)))
            res = classificar_item(item, arvore.filhos[filho])
            # print("PARA NÓ COM VAR = {}; LEN(FILHOS) = {}; CLASSIFICAÇÃO = {}".format(arvore.varClas, len(arvore.filhos), res))
            return res


def regredir_item(item, arvore):
    if arvore.divisores == [] and arvore.classe != 0:
        #print("NÓ {}, CLASSIFICAÇÃO {}".format(item[0], arvore.classe))
        return arvore.mediaReg
    if arvore.filhos == [] or arvore.filhos == None:
        #print("NÓ {}, CLASSIFICAÇÃO {}".format(item[0], arvore.classe))
        return arvore.mediaReg
    filho = 0
    # print("VAR = {}; VALOR = {}; DIVISORES: {}".format(arvore.varClas, item[arvore.varClas], arvore.divisores))
    for divisor in arvore.divisores:
        if float(item[arvore.varClas]) > divisor: #abs(
            filho += 1

            if filho >= len(arvore.filhos):
                filho = len(arvore.filhos) - 1
                # print("FILHO = {}; ARVORE.FILHOS = {}".format(filho, len(arvore.filhos)))
                res = regredir_item(item, arvore.filhos[filho])
                # print("PARA NÓ COM VAR = {}; LEN(FILHOS) = {}; CLASSIFICAÇÃO = {}".format(arvore.varClas, len(arvore.filhos), res))
                return res

            continue
        else:
            if filho >= len(arvore.filhos):
                filho = len(arvore.filhos) - 1
            #print("FILHO = {}; ARVORE.FILHOS = {}".format(filho, len(arvore.filhos)))
            res = regredir_item(item, arvore.filhos[filho])
            # print("PARA NÓ COM VAR = {}; LEN(FILHOS) = {}; CLASSIFICAÇÃO = {}".format(arvore.varClas, len(arvore.filhos), res))
            return res


rcont = 0
fcont = 0


def imprimir_arvore(no, fc):
    global rcont
    global fcont
    print("VAR = {}; CLASSE = {}; PUREZA = {}; PAIS ANTERIORES: {}; RF = {} {}; DIVISORES: {}; LISTA = {}".format(
        no.varClas, no.classe, no.pureza, len(no.vars_passadas), rcont, fc, no.divisores, no.listaIndices))
    if no.filhos is not None and no.filhos != []:
        fcont = 0
        for item in no.filhos:
            rcont += 1
            fcont += 1
            imprimir_arvore(item, fcont)
            rcont -= 1
    else:
        print("Este nó não possui filhos.")

    print("\n")


def determinaDivisores_og(indVar, listaIndices):
    arqTabelaOrdenada = open("C:/Users/nitro5/PyCharmProjects/Implementação AM/.venv/Tabela Ordenada.txt", "r")
    iterador = 0
    soma = 0
    flag = 0
    res = []
    temp = []
    res_mediana = []
    max = -9999
    linha = arqTabelaOrdenada.readline().split(sep=", ")
    #print("DETERMINA_DIVISORES: VAR = {}".format(indVar))
    for i in range(1, 5):
        while int(linha[7]) == i:
            if int(linha[0]) not in listaIndices and len(listaIndices) > 10:
                linha = arqTabelaOrdenada.readline().split(sep=", ")
                if linha[0] == '':
                    break
                continue
            soma += abs(float(linha[indVar]))
            temp.append(float(linha[indVar]))
            iterador += 1
            if float(linha[indVar]) > max:
                max = float(linha[indVar])
            linha = arqTabelaOrdenada.readline().split(sep=", ")
            if linha[0] == '':
                break
        if iterador == 0:
            iterador = 1
        res.append(soma / iterador)
        # if iterador > 1 and flag < 4:
        #    if flag == 0:
        #        res.append(0.33 * soma / iterador)
        #    else:
        #        res.append(0.87 * soma / iterador)
        #    flag += 1
        #print(soma / iterador)
        temp.sort()
        # print("TEMP = {}".format(temp))
        if temp != []:
            res_mediana.append(temp[21 * len(temp) // 40])
            if len(temp) > 0 and flag < 6:
                if flag % 4 == 0:
                    res_mediana.append(temp[1 * len(temp) // 10])
                elif flag % 4 == 1:
                    res_mediana.append(temp[6 * len(temp) // 10])
                #elif flag % 4 == 3:
                #    res_mediana.append(temp[6 * len(temp) // 10])
                #else:
                #    res_mediana.append(temp[19 * len(temp) // 20])
                elif flag % 4 == 2:
                    res_mediana.append(temp[19 * len(temp) // 20])
                    res_mediana.append(temp[14 * len(temp) // 20])
                    flag += 1
                flag += 1
        else:
            res_mediana.append(0)
        temp = []
        soma = 0
        iterador = 0
    # res.sort()
    #print(res_mediana)
    # print("RES_MEDIANA = {}".format(res_mediana))
    res2 = []
    for t in range(0, len(res_mediana) - 1):
        res2.append((res_mediana[t] + res_mediana[t + 1]) / 2)
    res2.sort()

    arqTabelaOrdenada.seek(0)
    tabelaOrdenada = arqTabelaOrdenada.readlines()
    for item in tabelaOrdenada:
        item = item.split(sep=", ")[:-1]
        if float(item[indVar]) > max:
            # print("atualizado")
            max = float(item[indVar])
    # print("MAX = {}".format(max))
    res2.append(max)
    #print("RES2 = {}".format(res2))
    arqTabelaOrdenada.close()
    return res2


def determinaDivisores(tabela, indVar, listaIndices):
    n = len(tabela)
    divisores = []
    resultados = []
    for x in range(0, numDivisoes[indVar] - 1):  # Inicializa o vetor de divisores
        divisores.append(0)
        resultados.append(0)
    max = -9999
    min = 9999
    i = -1
    for linha in tabela:
        i += 1
        if i not in listaIndices:
            continue
        if float(linha[indVar]) > max:
            max = float(linha[indVar])
        if float(linha[indVar]) < min:
            min = float(linha[indVar])

    amplitude = max - min  # Calcula a amplitude dos dados na variável selecionada.
    # print(min)
    # print(max)

    for i in range(0, numDivisoes[indVar] - 1):  # Calcula os divisores.
        divisores[i] = min + (i + 1) * amplitude / numDivisoes[indVar]

    divisores.append(max)

    return divisores


def main():
    arq = open("C:/Users/nitro5/PyCharmProjects/Implementação AM/.venv/treino_sinais_vitais_com_label.txt", "r")
    #arq = open("C:/Users/nitro5/PyCharmProjects/Implementação AM/.venv/Amostra.txt", "r")
    linha = arq.readline()
    tabela = []
    i = 0
    # principal = Node()
    while len(linha) != 0:
        tabela.append(linha.split(sep=","))
        #tabela.append(linha.split(sep=", ")[:-1])
        tabela[i][len(tabela[i]) - 1] = tabela[i][len(tabela[i]) - 1][0]
        i += 1
        linha = arq.readline()
    print(tabela[1])

    n = len(tabela[0])
    min = 9999
    var = -1
    sel = None
    indicesTotais = []
    for i in range(0, len(tabela)):
        indicesTotais.append(i)

    floresta = []
    novo = None
    vetorCaracteristicas = []
    n = 0
    while n < 50:
        i = random.randint(3, 7)
        if i == 4:
            continue
        if i // 4 > 0:
            vetorCaracteristicas.append(1)
        else:
            vetorCaracteristicas.append(0)

        if i % 4 > 1:
            vetorCaracteristicas.append(1)
        else:
            vetorCaracteristicas.append(0)

        if i % 2 == 1:
            vetorCaracteristicas.append(1)
        else:
            vetorCaracteristicas.append(0)

        indices = []
        for j in range(0, 500):
            indices.append(random.randint(0, 999))

        print("INDICES = {}".format(indices))
        novo = iteracao_id3(tabela, indices, None, vetorCaracteristicas)
        floresta.append(novo)
        vetorCaracteristicas = []
        n += 1

    arq2 = open("C:/Users/nitro5/PyCharmProjects/Implementação AM/.venv/treino_sinais_vitais_sem_label.txt", "r")
    #arq2 = open("C:/Users/nitro5/PyCharmProjects/Implementação AM/.venv/Amostra.txt", "r")
    # arq2 = open("C:/Users/nitro5/PyCharmProjects/Implementação AM/.venv/treino_sinais_vitais_com_label.txt", "r")

    linha = arq2.readline()
    tabela2 = []
    i = 0
    # principal = Node()
    while len(linha) != 0:
        if i > 999:
            tabela2.append(linha.split(sep=", "))
            tabela2[i - 1000][len(tabela2[i - 1000]) - 1] = tabela2[i - 1000][len(tabela2[i - 1000]) - 1][:-1]
        i += 1
        linha = arq2.readline()
    print(tabela2[2])

    listaClassificacoes = []
    listaRegressoes = []
    for arvore in floresta:
        imprimir_arvore(arvore, 0)
        listaClassificacoes.append([])
        listaRegressoes.append([])

    for registro in tabela2:
        for i in range(0, len(floresta)):
            listaClassificacoes[i].append(classificar_item(registro, floresta[i]))
            listaRegressoes[i].append(regredir_item(registro, floresta[i]))

    listaClassificacoesFinal = [0] * len(listaClassificacoes[0])
    listaRegressoesFinal = [0] * len(listaRegressoes[0])

    somaC = 0
    somaR = 0
    cont = 0
    vetClas = [0] * 4
    vetReg = [0] * len(listaClassificacoes)
    for i in range(0, len(listaClassificacoes[0])):
        somaC = 0
        somaR = 0
        for j in range(0, len(listaClassificacoes)):
            somaC += listaClassificacoes[j][i]
            somaR += listaRegressoes[j][i]
            vetClas[listaClassificacoes[j][i]-1] += 1
            vetReg[j] = listaRegressoes[j][i]
        #listaClassificacoesFinal[i] = (proper_round(somaC / len(listaClassificacoes)))
        #listaRegressoesFinal[i] = (somaR / len(listaRegressoes))
        vetReg.sort()
        listaRegressoesFinal[i] = vetReg[len(vetReg) // 2]
        if vetClas[3] > 0.07 * len(listaClassificacoes):
            listaClassificacoesFinal[i] = 4
        elif vetClas[0] > 0.36 * len(listaClassificacoes):
            listaClassificacoesFinal[i] = 1
        #elif vetClas[1] > vetClas[2]:
        #    listaClassificacoesFinal[i] = 2
        else:
            #listaClassificacoesFinal[i] = 3
            listaClassificacoesFinal[i] = (proper_round(somaC / len(listaClassificacoes)))
        vetClas = [0] * 4

    print(len(listaClassificacoesFinal))

    for k in range(0, len(listaClassificacoesFinal)):
        if listaClassificacoesFinal[k] == 1 and float(tabela2[k][6]) <= 25:
            cont += 1
        elif listaClassificacoesFinal[k] == 2 and float(tabela2[k][6]) <= 50 and float(tabela2[k][6]) > 25:
            cont += 1
        elif listaClassificacoesFinal[k] == 3 and float(tabela2[k][6]) <= 75 and float(tabela2[k][6]) > 50:
            cont += 1
        elif listaClassificacoesFinal[k] == 4 and float(tabela2[k][6]) <= 100 and float(tabela2[k][6]) > 75:
            cont += 1
        else:
            print("CLASSIFICAÇÃO ERRADA NO NÓ {}".format(k + 1))

    print(cont / len(tabela2))
    print(listaClassificacoesFinal)
    #print(listaRegressoesFinal)

if __name__ == "__main__":
    main()