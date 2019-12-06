__author__ = 'Marco Almeida and André Furlan'

from bot.bot import Bot
import random

produtos = dict()
produtosPrecos = dict()
carrinho = list()
numeros = dict()
frases_saudacao = list()
frases_tabela = list()
frases_pedido = list()
frases_conta = list()
frases_confirmacao = list()
frases_negacao = list()
frases_agradecimento = list()
pacotes = dict()

def controiPacotes():
    with open('../files/pacotes.csv', 'r', encoding = 'utf-8-sig') as file:
        for line in file:
            str, num = line.replace('\n', '').split(';')
            pacotes[str] = int(num)

def constroiRespostas():
    with open('../files/respostas.csv', 'r', encoding = 'utf-8-sig') as file:
        for line in file:
            intencao = line.replace('\n', '').split(';')[0]
            frase = line.replace('\n', '').split(';')[1]
            if intencao == 'saudacao':
                frases_saudacao.append(frase)
            elif intencao == 'tabela':
                frases_tabela.append(frase)
            elif intencao == 'pedido':
                frases_pedido.append(frase)
            elif intencao == 'conta':
                frases_conta.append(frase)
            elif intencao == 'confirmacao':
                frases_confirmacao.append(frase)
            elif intencao == 'negacao':
                frases_negacao.append(frase)
            elif intencao == 'agradecimento':
                frases_agradecimento.append(frase)

def constroiNumeros():
    with open('../files/numeros.csv', mode = 'r', encoding = 'utf-8-sig') as file:
        for line in file:
            str, num = line.replace('\n', '').split(';')
            numeros[str] = int(num)

def somaConta(conta):
    #TODO
    pass

def exibeProdutos():
    print('\n' + random.choice(frases_saudacao))
    for key, value in produtos.items():
        print('{} -> R${}'.format(key, value).replace('\n', ''))

def cardapio():
    with open('../files/precos.csv', 'r', encoding = 'utf-8-sig') as file:
        for line in file:
            produto, valor = line.replace('\n', '').split(';')
            produtosPrecos[produto] = valor

def controiProdutos():
    with open('../files/produtos.csv', 'r', encoding = 'utf-8-sig') as file:
        for line in file:
            chave, valor = line.replace('\n', '').replace(' ', '').split(';')
            produtos[chave] = valor

def adicionaCarrinho(lista_produto, lista_quantidade):
    index = 0
    #FIXME Corregir multiplicacao de pacotes
    for index in range(len(lista_produto)):
        preco = produtosPrecos.get(lista_produto[index])
        print(preco)
        p = {'{}:{}:{}'.format(lista_produto[index], lista_quantidade[index], lista_quantidade[index] * preco )}
        carrinho.append(p)

    print(carrinho)
    print(random.choice(frases_pedido))

def saida():
    if len(produtos) > 0:
        somaConta(carrinho)
        print('sua conta total eh de xxxx')

    print('\n'+ random.choice(frases_agradecimento))

    return False


def verificarPedido(entrada):
    palavras = entrada.split(' ')
    quantidade = None
    produto = None
    multiplicador = 1
    print(palavras)

    lista_quantidades = list()
    lista_produtos = list()
    index = 0
    for palavra in palavras:
        if pacotes.get(palavra): multiplicador = pacotes.get(palavra)
        if quantidade is None: quantidade = numeros.get(palavra)
        if produto is None: produto = produtos.get(palavra)
        if palavra.isdigit(): quantidade = palavra
        quantidade = 1 if quantidade is None else quantidade

        if produto is not None:
            lista_quantidades.append(int(quantidade) * multiplicador)
            lista_produtos.append(produto)

            index += 1
            quantidade = None
            produto = None
            multiplicador = 1

    adicionaCarrinho(lista_produtos, lista_quantidades)

def main():
    bot = Bot('../files/dialogo.csv')
    constroiNumeros()
    cardapio()
    constroiRespostas()
    controiPacotes()
    controiProdutos()

    print('{h} Bem vindo a SJN Polpas {h}\n'.format(h = '#'* 8))
    print(random.choice(frases_saudacao))

    loop = True

    while loop:
        entrada = input()
        int = bot.predict(entrada)[0]

        print('Intencao {}'.format(int))

        if int in 'saudacao':
            print(random.choice(frases_saudacao))

        elif int in 'pedido':
            verificarPedido(entrada)
            print(carrinho)

        elif int in 'conta':
            somaConta(carrinho)

        elif int in 'tabela':
            exibeProdutos()

        elif int in 'saida':
            loop = saida()

        if loop is True:
            print('Deseja algo mais?')

if __name__ == '__main__':
    main()