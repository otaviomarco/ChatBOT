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
    def __init__(self, arquivo, classificador = 'knn'):
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

        self.fit(arquivo)

    def buildAnswers(self):
        a = dict()

        with open('../files/respostas.csv', 'r', encoding = 'utf-8-sig') as file:
            for line in file:
                intencao = line.replace('\n', '').split(';')[0]
                frase = line.replace('\n', '').split(';')[1]

                if intencao in a.keys():
                    novo = a.get(intencao)
                    novo.append(frase)
                    a[intencao] = novo

                else:
                    a[intencao] = [frase]

        return a

    def escolherResposta(self, intencao):
        if intencao in self.listaRespostas.keys():
            return choice(self.listaRespostas[intencao])

        else:
            return 'Em que posso ser útil?'

    def showMenu(self):
        for key, value in self.listaProdutosPreco.items():
            print('{} -> R$ {:0.2f}'.format(key, float(value)))

    def adicionarCarrinho(self, listaProduto, listaQuantidade):
        for index in range(len(listaProduto)):
            preco = self.listaProdutosPreco.get(listaProduto[index])
            p = dict()
            p[listaProduto[index]] = [listaQuantidade[index], listaQuantidade[index] * preco]
            self.cart.append(p)

    def saida(self):
        # TODO: Fechar carrinho se tiver produtos
        pass

    def validarPedido(self, frase):
        palavras = frase.split(' ')
        quantidade = None
        produto = None
        multiplicador = 1

        lista_quantidades = list()
        lista_produtos = list()
        index = 0
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

                index += 1
                quantidade = None
                produto = None
                multiplicador = 1

        self.adicionarCarrinho(lista_produtos, lista_quantidades)

    def buildProductList(self):
        p = dict()
        with open('../files/produtos.csv', 'r', encoding = 'utf-8-sig') as file:
            for line in file:
                chave, valor = line.replace('\n', '').replace(' ', '').split(';')
                p[chave] = valor

        return p

    def buildNumberList(self):
        n = dict()
        with open('../files/numeros.csv', mode = 'r', encoding = 'utf-8-sig') as file:
            for line in file:
                str, num = line.replace('\n', '').split(';')
                n[str] = int(num)

        return n

    def buildProductsPrice(self):
        p = dict()
        with open('../files/precos.csv', 'r', encoding = 'utf-8-sig') as file:
            for line in file:
                chave, valor = line.replace('\n', '').split(';')
                p[chave] = float(valor)

        return p

    def buildPackages(self):
        p = dict()
        with open('../files/pacotes.csv', 'r', encoding = 'utf-8-sig') as file:
            for line in file:
                str, num = line.replace('\n', '').split(';')
                p[str] = int(num)

        return p

    def fecharConta(self):
        if len(self.cart) > 0:
            print('{h} Pedido número {p} {h}'.format(h = '=' * 8, p = choice(range(1000, 9999))))
            print('#.\tproduto\t\t\tQtd.\tR$')
            index = 1
            total = 0
            for item in self.cart:
                for key, value in item.items():
                    print('{}.\t{} \t\t{}\t\t{:.2f}'.format(index, key, value[0], value[1]))
                    index += 1
                    total += value[1]
            print('-' * 36)
            print('Total.\t\t\t\t\t\t{:.2f}'.format(total))
            print('=' * 36)

    def setClassificador(self, x):
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
        return self.classificador.predict(self.vectorizer.transform([texto]))

    def fit(self, arquivo):
        with open(arquivo, 'r', encoding = 'utf-8-sig') as file:
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
