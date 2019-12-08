__author__ = 'Marco Almeida and André Furlan'

from bot.bot import Bot


def main():
    bot = Bot('../files/dialogo.csv')
    print('{h} Bem vindo a SJN Polpas {h}\n'.format(h = '#' * 8))
    print(bot.escolherResposta('saudacao'))

    loop = True

    while loop:
        entrada = input()
        int = bot.predict(entrada)[0]

        if int in 'saudacao':
            print(bot.escolherResposta(int))

        elif int in 'pedido':
            bot.validarPedido(entrada)

        elif int in 'conta':
            bot.fecharConta()

        elif int in 'tabela':
            print(bot.escolherResposta('tabela'))
            bot.showMenu()

        elif int in 'saida':
            bot.fecharConta()
            loop = False

        if loop is True:
            print('\n{}'.format(bot.escolherResposta('continuidade')))


if __name__ == '__main__':
    main()
