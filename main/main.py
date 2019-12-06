__author__ = 'Marco Almeida and André Furlan'

from bot.bot import Bot
import random

produtos = dict()
carrinho = list()
numeros = dict()
frases_saudacao = list()
frases_tabela = list()
frases_pedido = list()
frases_conta = list()
frases_confirmacao = list()
frases_negacao = list()
frases_agradecimento = list()

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
            str, num = line.split(';')
            numeros[str] = num

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
            produto, valor = line.split(';')
            produtos[produto] = valor



def adicionaCarrinho(produto, quantidade):
    encontrou = False

    for item in carrinho:
        if item.get(produto) is not None:
            item['quantidade'] += quantidade
            encontrou = True
            break

    if not encontrou:
        p = {'{}:{}'.format(produto, quantidade)}
        carrinho.append(p)

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
    print(palavras)

    for palavra in palavras:
        #TODO se for pedido 2 produtos na mesma frase?
        quantidade = numeros.get(palavra)
        produto = produtos.get(palavra)

        if palavra.isdigit(): quantidade = palavra

    if quantidade is not None and produto is not None:
        quantidade = max(1, quantidade)
        adicionaCarrinho(produto, quantidade)

    else:
        print('Não entendi seu pedido')



def main():
    bot = Bot('../files/dialogo.csv')
    constroiNumeros()
    cardapio()
    constroiRespostas()

    print('{h} Bem vindo a loja {h}\n'.format(h = '#'* 8))
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