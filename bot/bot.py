import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import LeaveOneOut
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score


class Bot:
    def __init__(self, arquivo, classificador = 'knn'):
        self.dialogos = list()
        self.intencoes = list()
        self.classificador = self.setClassificador(classificador)
        self.vectorizer = TfidfVectorizer(sublinear_tf = True, max_df = 0.5, strip_accents = 'unicode')

        self.fit(arquivo)

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
                s = line.replace("\n", "").split('-')
                self.intencoes.append(s[0])
                self.dialogos.append(s[1])

        with open('../files/produtos.csv', 'r', encoding = 'utf-8-sig') as file:
            for line in file:
                s = line.replace("\n", "").split(';')
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