import keras

import csv
import math
import random
import numpy as np
from sklearn import preprocessing
from sklearn import model_selection

def reLU(entrada):
    return np.maximum(0.0,entrada);
    #entrada[entrada > 100.0] = 100.0;
    #entrada[entrada < -100.0] = -100.0;

def sigmoide(entrada):
    return 1 / (1 + np.exp(-entrada));

def derivada_sigmoide(entrada):
    return entrada * (1 - entrada);

def derivada_reLU(entrada):
    return 1.0 * (entrada > 0.0);
    #return np.where(entrada>0, 1, 0.01);
def cria_matriz_entrada(arquivo, primeiro_parametro, ultimo_parametro, entradas):
    matriz_entrada = np.empty((entradas, ultimo_parametro - primeiro_parametro + 1));
    for i in range (0, entradas):
        for j in range(0, ultimo_parametro - primeiro_parametro + 1):
            matriz_entrada[i][j] = arquivo[i][primeiro_parametro + j];
    return matriz_entrada;

def cria_matriz_peso(input_num, output_num):
    pesos = np.empty((output_num,input_num));
    for i in range (0, output_num):
        for j in range(0, input_num):
            pesos[i][j] = random.uniform(0,2)-1;
            pesos[i][j] = round(pesos[i][j],3);

    print('matriz peso:', pesos);
    return pesos;

def cria_matriz_objetivo(arquivo, primeiro_parametro, ultimo_parametro, entradas):
    matriz_entrada = np.empty((entradas, ultimo_parametro - primeiro_parametro + 1));
    for i in range(0, entradas):
        for j in range(0, ultimo_parametro - primeiro_parametro + 1):
            matriz_entrada[i][j] = arquivo[i][primeiro_parametro + j];
    print('matriz objetivo', matriz_entrada)
    return matriz_entrada;

#def norm(x):
#    return (x - train)

def main():
    arq = open("treino_sinais_vitais_com_label.txt", "r")
    #arq = open("C:/Users/nitro5/PyCharmProjects/Implementação AM/.venv/Amostra.txt", "r")
    linha = arq.readline()
    tabela = []
    i = 0
    scaler = preprocessing.StandardScaler()
    #principal = Node()
    while len(linha) != 0:
        tabela.append(linha.split(sep=","))
        #tabela.append(linha.split(sep=", ")[:-1])
        tabela[i][len(tabela[i])-1] = tabela[i][len(tabela[i])-1][0]
        print(tabela[i])
        i += 1
        linha = arq.readline()

    arq2 = open("treino_sinais_vitais_sem_label.txt", "r")
    # arq2 = open("C:/Users/nitro5/PyCharmProjects/Implementação AM/.venv/Amostra2.txt", "r")
    # arq2 = open("C:/Users/nitro5/PyCharmProjects/Implementação AM/.venv/treino_sinais_vitais_com_label.txt", "r")

    # teste = arq2.readline()
    # teste = teste.split(sep=",")
    # print(classificar_item(teste, principal))

    linha = arq2.readline()
    tabela2 = []
    i = 0
    # principal = Node()
    while len(linha) != 0:
        tabela2.append(linha.split(sep=", "))
        tabela2[i][len(tabela2[i]) - 1] = tabela2[i][len(tabela2[i]) - 1][:-1]
        i += 1
        linha = arq2.readline()
    # (tabela2[2])
    #treinamento_mcp(tabela, tabela2, 4);
    entrada_parametros = cria_matriz_entrada(tabela, 3, 5, 1500);
    #min_entrada = np.min(entrada_parametros);
    #max_entrada = np.max(entrada_parametros);
    entrada_parametros_norm = scaler.fit_transform(entrada_parametros)
    objetivos = cria_matriz_objetivo(tabela, 6,7, 1500);
    #objetivos_regressao, objetivos_categoria = np.hsplit(objetivos,2)
    #print(objetivos_categoria, objetivos_regressao)
    #min_objetivos = np.min(objetivos);
    #max_objetivos = np.max(objetivos);
    #objetivos_norm = (objetivos - min_objetivos) / (max_objetivos - min_objetivos);

    #categorias = cria_matriz_objetivo(tabela, 7, 1500);
    entradas_treino, entradas_teste, objetivos_treino, objetivos_teste = model_selection.train_test_split(entrada_parametros_norm, objetivos, test_size=0.66, random_state=33)
    objetivos_regressao_teste, objetivos_categoria_teste = np.hsplit(objetivos_teste, 2)
    objetivos_regressao_treino, objetivos_categoria_treino = np.hsplit(objetivos_treino, 2)
    resultados_categoria = []


    rede_neural = keras.Sequential(
        [
            keras.layers.Input(shape=(entradas_treino.shape[1],)),
            keras.layers.Dense(16, activation='sigmoid'),
            keras.layers.Dense(8, activation='sigmoid'),
            keras.layers.Dense(1)
        ]
    )

    rede_neural.compile(
        optimizer=keras.optimizers.RMSprop(0.01, momentum=0.1),
        loss='mse',
        metrics=['mse','mae']
    )

    batelada = 100
    epoch = 1000

    historico = rede_neural.fit(
        entradas_treino, objetivos_regressao_treino,
        batch_size=batelada,
        epochs=epoch,
        validation_split=0.1,
        verbose=1,
    )

    pontuacao = rede_neural.evaluate(entradas_treino, objetivos_regressao_treino, verbose=0)
    print(pontuacao)
    print('Test Loss', pontuacao[0])
    print('test mse', pontuacao[1])

    previsoes = rede_neural.predict(entradas_teste)
    print('previsoes:', previsoes);
    previsoes_categorias = np.ceil(previsoes / 25)
    for i in range(0, len(previsoes_categorias)):
        if previsoes_categorias[i] == objetivos_categoria_teste[i]:
            resultados_categoria.append(1);
        else:
            resultados_categoria.append(0);
    categoria_test = np.mean(resultados_categoria);
    print('acuracia', categoria_test)

if __name__ == "__main__":
    main()