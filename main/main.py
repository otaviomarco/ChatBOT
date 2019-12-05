__author__ = 'Marco Almeida and André Furlan'

from bot.bot import Bot

produtos = dict()
carrinho = list()
numeros = dict()

def constroiNumeros():
    with open('../files/numeros.csv', mode = 'r', encoding = 'utf-8-sig') as file:
        for line in file:
            str, num = line.split(';')
            numeros[str] = num


def somaConta(conta):
    #TODO
    pass

def exibeProdutos():
    print('\nOs produtos que temos hoje são')
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

def saida():
    if len(produtos) > 0:
        somaConta(carrinho)
        print('sua conta total eh de xxxx')

    print('Agradecemos sua visita!')

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
    print('{h} Bem vindo a loja {h}\n'.format(h = '#'* 8))
    print('Em que posso ajudar?')

    loop = True

    while loop:
        entrada = input()
        int = bot.predict(entrada)[0]

        print('Intencao {}'.format(int))

        if int in 'pedido':
            verificarPedido(entrada)
            print(carrinho)

        elif int in 'conta':
            somaConta(carrinho)

        elif int in 'tabela':
            exibeProdutos()

        elif int in 'saida':
            loop = saida()

        if loop is True: print('Deseja algo mais?')

if __name__ == '__main__':
    main()