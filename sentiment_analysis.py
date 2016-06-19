###############################################################################
# Univesidade Federal de Pernambuco -- UFPE (http://www.ufpe.br)
# Centro de Informatica -- CIn (http://www.cin.ufpe.br)
# Bacharelado em Sistemas de Informacao
# IF968 -- Programacao 1
#
# Autor:    Lucas Eduardo Lira de Oliveira
#           Márcio Belarmino de Arruda
#
# Email:    lelo@cin.ufpe.br
#           mba5@cin.ufpe.br
#
# Data:        2016-06-18
#
# Descricao:  O objetivo deste trabalho é praticar a escrita de funções e programas em Python,
#             em particular, programas envolvendo strings, vetores, listas, tuplas, 
#             dicionários e arquivos.
#
# Licenca: The MIT License (MIT)
#            Copyright(c) 2016 Fulano de Tal, Beltrano do Cin
#
###############################################################################

import sys
import re

def clean_up(s):
    ''' Retorna uma versao da string 's' na qual todas as letras sao
        convertidas para minusculas e caracteres de pontuacao sao removidos
        de ambos os extremos. A pontuacao presente no interior da string
        e' mantida intacta.
    '''    
    punctuation = ''''!"'`´,;:.-?)([]<>*#\n\t\r'''
    result = s.lower().strip(punctuation)

    return result

 

def split_on_separators(original, separators):
    '''    Retorna um vetor de strings nao vazias obtido a partir da quebra
        da string original em qualquer dos caracteres contidos em 'separators'.
        'separtors' e' uma string formada com caracteres unicos a serem usados
        como separadores. Por exemplo, '^$' e' uma string valida, indicando que
        a string original sera quebrada em '^' e '$'.
    '''            

    return filter(lambda x: x != '',re.split('[{0}]'.format(separators),original))


def stopWords(lista):

    fileStop = open ('stopWords.txt','r')
    stop = fileStop.readlines()
    fileStop.close()
    stopWords=[]
    filteredWords=[]
    for word in stop:
        stopWords.append(clean_up(word))
    for word in lista:
        word=clean_up(word)
        if word in lista and word not in stopWords:
            filteredWords.append(word)

    return filteredWords
        

def readTrainingSet(fname):
    '''    Recebe o caminho do arquivo com o conjunto de treinamento como parametro
        e retorna um dicionario com triplas (palavra,freq,escore) com o escore
        medio das palavras no comentarios.
    '''

    treino=open(fname,'r')
    comentarios=treino.readlines()
    treino.close()
    limpa=[]
    words = {}

    #limpando as frases
    for frase in comentarios:
        limpa.append(clean_up(frase))
    for review in limpa:
        palavras = stopWords(list(split_on_separators(review, ' '))) # cria a lista sem stopWords
        scoreComentario = int(palavras.pop(0))
        frequencia = 0
        scorePalavra = 0
        scoreMedia = 0
        for word in palavras:
            if len(word)>2 and word.isdigit()==False:
                word = clean_up(word)
                if word not in words: #verifica se a palavra já está adicionada ao dicionário
                    words[word] = [1,scoreComentario]
                    # words[palavra] = [frequencia, score]
                else: #caso a palavra já esteja no dicionário, adiciona na frequencia e atribui o score
                    words[word][0] += 1 # acrescenta na frequencia
                    words[word][1] += scoreComentario #atribui o score à palavra
    for word in words:
        words[word] = (word,words[word][0],(words[word][1]//words[word][0])) #cria o dicionário, usando as palavras como chaves

    return words

def readTestSet(fname):
    ''' Esta funcao le o arquivo contendo o conjunto de teste
        retorna um vetor/lista de pares (escore,texto) dos
        comentarios presentes no arquivo.
    '''
    file = open(fname,'r')
    teste = file.readlines()
    file.close()
    reviews = []
    limpa=[]

    #limpando as frases
    for frase in teste:
        limpa.append(clean_up(frase))
    for frases in limpa:
        frasePartida = stopWords(list(split_on_separators(frases, ' '))) #pra cada frase, se converte em lista para extrair o score
        scoreFrase = int(frasePartida.pop(0))
        fraseLimpa = []
        for palavra in frasePartida:
                palavra = clean_up(palavra)
                fraseLimpa.append(palavra)
        reviews.append((scoreFrase,fraseLimpa))#adiciona-se a nova lista uma tupla com o score e a converção da lista anterior em frase

    return reviews

def computeSentiment(review,words):
    ''' Retorna o sentimento do comentario recebido como parametro.
        O sentimento de um comentario e' a media dos escores de suas
        palavras. Se uma palavra nao estiver no conjunto de palavras do
        conjunto de treinamento, entao seu escore e' 2.
        Review e' a parte textual de um comentario.
        Words e' o dicionario com as palavras e seus escores medios no conjunto
        de treinamento.
    '''
    score = 0.0
    count = 0
    
    for word in review: 
        if word in words: #se o comentário pussuir alguma palavra contida no dicionário
            score=score+words[word][2] #atribui a nota da palavra ao score
            count+=1
        else:
            score=score+2 #se o comentário não possuir nenhuma palavra do dicionário, a nota 2 é atribuída
            count+=1
    if count == 0: #caso o comentário seja vazio
        return 0
    
    return score/count

def computeSumSquaredErrors(reviews,words): ###estudar###
    '''    Computa a soma dos quadrados dos erros dos comentarios recebidos
        como parametro. O sentimento de um comentario e' obtido com a
        funcao computeSentiment. 
        Reviews e' um vetor de pares (escore,texto)
        Words e' um dicionario com as palavras e seus escores medios no conjunto
        de treinamento.    
    '''    
    sse = 0
    for review in reviews: #para cada comentário
        scoreReview = computeSentiment(review[1],words)
        diferenca = review[0]-scoreReview
        sse = sse + (diferenca)**2

    return sse/len(reviews)



def main():
    
    
    if len(sys.argv) < 3:
        print('Numero invalido de argumentos')
        print('O programa deve ser executado como python sentiment_analysis.py <arq-treino> <arq-teste>')
        sys.exit(0)

    # Lendo conjunto de treinamento e computando escore das palavras
    words = readTrainingSet(sys.argv[1])
    
    # Lendo conjunto de teste
    reviews = readTestSet(sys.argv[2])
    
    # Inferindo sentimento e computando soma dos quadrados dos erros
    sse = computeSumSquaredErrors(reviews,words)
    
    print('A soma do quadrado dos erros e\': {0}'.format(sse))
            

if __name__ == '__main__':
   main()
