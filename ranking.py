import csv

def CSVReader():
    pontos = []
    nomes = []
    lista = []
    with open('rankingfile.csv', newline = '') as csvfile:
        leitor = csv.reader(csvfile, delimiter = '\t')
        lista = list(leitor)
        lista_ordenada = sorted(lista, key = lambda dado: int(dado[1]), reverse = True)
        csvfile.close()
        return lista_ordenada

def organizaDados(dados):
    lista_nome = []
    lista_pontos = []
    try:
        #só serão mostrados as 10 melhores pontuações
        for i in range(11):
            lista_nome.append(dados[i][0])
            lista_pontos.append(dados[i][1])
    except(IndexError):
        print('-------------------------\n')
    print(lista_nome)
    print(lista_pontos)
    return lista_nome, lista_pontos

def CSVWriter(nome,pontos):
    with open('rankingfile.csv','a',newline = '') as csvfile:
        escritor = csv.writer(csvfile, delimiter='\t')
        escritor.writerow([nome, pontos])
        csvfile.close()

organizaDados(CSVReader())