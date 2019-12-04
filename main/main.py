__author__ = 'Marco Almeida and André Furlan'

from bot.bot import Bot

def somaConta(conta):
    #TODO
    pass

def exibePreco():
    with open('../files/precos.csv', 'r', encoding = 'utf-8-sig') as file:
        for line in file:
            print(line.replace("\n", ""))

def main():
    bot = Bot('../files/dialogo.csv')

    print('Bem vindo a porra toda')

    while True:
        conta = list()
        print('O que deseja?')
        int = bot.predict(input())[0]

        if int in 'pedido':
            #TODO
            pass
        elif int in 'conta':
            somaConta(conta)
            pass
        elif int in 'tabela':
            exibePreco()
            pass
        elif int in 'saida':
            #TODO
            pass

if __name__ == '__main__':
    main()