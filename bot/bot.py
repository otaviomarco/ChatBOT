from random import choice
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import LeaveOneOut
from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import accuracy_score
# from sklearn.metrics import precision_score
# from sklearn.metrics import recall_score

class Bot:
    """
    Classe responsável por predizer a inteção do usuário e validar as entradas conforme essa intenção
    """
    def __init__(self, classificador = 'knn'):
        """
        Construtor da classe
        :param classificador: classificador que será utilizando, sendo possíveis o KNN (knn default), Regressão Logística (logre) e Árvore de Decisão (tree)
        """
        self.dialogos = list()
        self.intencoes = list()
        self.cart = list()
        self.listaProdutos = self.buildProductList()
        self.listaNumeros = self.buildNumberList()
        self.listaPacotes = self.buildPackages()
        self.listaProdutosPreco = self.buildProductsPrice()
        self.listaRespostas = self.buildAnswers()
        self.classificador = self.setClassificador(classificador)
        self.vectorizer = TfidfVectorizer(sublinear_tf = True, max_df = 0.5, strip_accents = 'unicode')
        self.numeroConta = choice(range(1000, 9999))
        self.fit()

    def buildAnswers(self):
        """
        Compila as respostas em uma estrutura de dicionário para que seja possível randomizar a conversa com o usuário
        """
        a = dict()

        with open('../files/respostas.csv', 'r', encoding = 'utf-8-sig') as file:
            for line in file:
                intencao = line.replace('\n', '').split(';')[0]
                frase = line.replace('\n', '').split(';')[1]

                """
                Intenção = chave
                Frase = valor
                """
                if intencao in a.keys():
                    novo = a.get(intencao)
                    novo.append(frase)
                    a[intencao] = novo

                else:
                    a[intencao] = [frase]

        return a

    def escolherResposta(self, intencao):
        """
        Define a resposta para o usuário
        """
        if intencao in self.listaRespostas.keys():
            return choice(self.listaRespostas[intencao])

        else:
            return 'Em que posso ser útil?'

    def showMenu(self):
        """
        Imprime o menu/cardárpio para o usuário
        """
        explode = 36
        print('{h} Tabela de produtos {h}'.format(h='=' * 8, ))
        print('Produto\t\t\t\t\t\t\tR$')
        print('-' * explode)

        for key, value in self.listaProdutosPreco.items():
            print('{}\t\t\t{:.2f}'.format(key.ljust(20, ' ').capitalize(), value))

        print('-' * explode)

    def adicionarCarrinho(self, listaProduto, listaQuantidade):
        """
        Adiciona no carrinho e define os preços de uma lista de produtos
        :param listaProduto: Lista de produtos que estão na fila
        :param listaQuantidade: Lista de quantidades de cada produto
        """
        for index in range(len(listaProduto)):
            preco = self.listaProdutosPreco.get(listaProduto[index].lower())
            p = dict()
            p[listaProduto[index]] = [listaQuantidade[index], listaQuantidade[index] * preco]
            self.cart.append(p)

    def validarPedido(self, frase):
        """
        Valida se a entrada no usuário é um pedido de um produto
        :param frase: entrada do usuário
        """
        palavras = frase.lower().split(' ')
        quantidade = None
        produto = None
        multiplicador = 1
        adicionou = False

        lista_quantidades = list()
        lista_produtos = list()
        index = 0

        """
        Laço força bruta para identificação do pedido do usuário
        """
        for palavra in palavras:
            if self.listaPacotes.get(palavra):
                multiplicador = self.listaPacotes.get(palavra)

            if quantidade is None:
                quantidade = self.listaNumeros.get(palavra)

            if produto is None:
                produto = self.listaProdutos.get(palavra)

            if palavra.isdigit():
                quantidade = palavra

            quantidade = 1 if quantidade is None else quantidade

            if produto is not None:
                lista_quantidades.append(int(quantidade) * multiplicador)
                lista_produtos.append(produto)
                adicionou = True

                index += 1
                quantidade = None
                produto = None
                multiplicador = 1

        self.adicionarCarrinho(lista_produtos, lista_quantidades)

        return adicionou

    def buildProductList(self):
        """
        Construção da lista de produtos para que o usuário possa escolher
        """
        p = dict()
        with open('../files/produtos.csv', 'r', encoding = 'utf-8-sig') as file:
            for line in file:
                chave, valor = line.replace('\n', '').replace(' ', '').split(';')
                p[chave.lower()] = valor

        return p

    def buildNumberList(self):
        """
        Construção da lista de número para predição do usuário
        """
        n = dict()
        with open('../files/numeros.csv', mode = 'r', encoding = 'utf-8-sig') as file:
            for line in file:
                str, num = line.replace('\n', '').split(';')
                n[str] = int(num)

        return n

    def buildProductsPrice(self):
        """
        Construção da lista de preços para cada produto existente
        """
        p = dict()
        with open('../files/precos.csv', 'r', encoding = 'utf-8-sig') as file:
            for line in file:
                chave, valor = line.replace('\n', '').split(';')
                p[chave] = float(valor)

        return p

    def buildPackages(self):
        """
        Construção da lista de pacotes (10 unidades do produto)
        """
        p = dict()
        with open('../files/pacotes.csv', 'r', encoding = 'utf-8-sig') as file:
            for line in file:
                str, num = line.replace('\n', '').split(';')
                p[str] = int(num)

        return p

    def totalItemsInCart(self):
        """
        Retorna a quantidade de itens no carrinho do usuário
        """
        return len(self.cart)

    def fecharConta(self):
        """
        Método para fechamento de conta.
        """
        print(self.escolherResposta('conta'))
        explode = 36

        if self.totalItemsInCart() == 0:
            print('Você não possui itens no carrinho. Que tal realizar algumas compras?')

        else:
            print('{h} Pedido número {p} {h}'.format(h = '=' * 8, p = self.numeroConta))
            print('#.\tProduto\t\t\tQtd.\t R$')
            print('-' * explode)
            index = 1
            total = 0

            for item in self.cart:
                for key, value in item.items():
                    print('{}.\t{}\t\t{}\t\t{:.2f}'.format(index, key.ljust(10, ' '), value[0], value[1]))
                    index += 1
                    total += value[1]

            print('-' * explode)
            print('Total.\t\t\t\t\t\t{:.2f}'.format(total))
            print('=' * explode)

    def setClassificador(self, x):
        """
        Define o classificador que será utilizado para a predição da entrada
        """
        if x in 'tree':
            classificador = DecisionTreeClassifier(random_state = 2)

        elif x in 'logre':
            classificador = LogisticRegression(random_state = 0, solver = 'lbfgs', multi_class = 'auto')

        else:
            if x not in 'knn':
                print('Classificador não mapeado. Utlizando KNN')

            classificador = KNeighborsClassifier(n_neighbors = 2)

        return classificador

    def predict(self, texto):
        """
        Método de predição da intenção do usuário
        """
        return self.classificador.predict(self.vectorizer.transform([texto]))

    def fit(self):
        """
        Método de treinamento do algoritmo de predição a partir de diversos diálogos
        """
        with open('../files/dialogo.csv', 'r', encoding = 'utf-8-sig') as file:
            for line in file:
                s = line.replace('\n', '').split(';')
                self.intencoes.append(s[0])
                self.dialogos.append(s[1])

        with open('../files/produtos.csv', 'r', encoding = 'utf-8-sig') as file:
            for line in file:
                s = line.replace('\n', '').split(';')
                self.intencoes.append('pedido')
                self.dialogos.append(s[0])

        y = np.array(self.intencoes)
        x = self.vectorizer.fit_transform(self.dialogos)

        y_true = list()
        predict = list()

        loo = LeaveOneOut()
        loo.get_n_splits(x)

        for train_index, test_index in loo.split(x):
            x_train, x_test = x[train_index], x[test_index]
            y_train, y_test = y[train_index], y[test_index]
            y_true.append(y_test)

            self.classificador.fit(x_train, y_train)
            predict.append(self.classificador.predict(x_test))

        # print('== {}'.format(self.classificador))
        # print('\t= Acuracy: {}'.format(accuracy_score(y_true, predict)))
        # print('\t= Presision: {}'.format(precision_score(y_true, predict, average = 'macro')))
        # print('\t= Recall: {}'.format(recall_score(y_true, predict, average = 'macro')))
