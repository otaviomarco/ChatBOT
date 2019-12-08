__author__ = 'Marco Almeida and André Furlan'

from bot.bot import Bot
import datetime
import random

def tratarSaudacao():
    """
    Função de tratamento horário
    """
    now = datetime.datetime.now()
    hour = now.hour

    if hour < 12:
        greeting = "Bom dia"
    elif hour < 18:
        greeting = "Boa tarde"
    else:
        greeting = "Boa noite"

    return greeting

def main():
    """
    Função main
    """
    bot = Bot()
    print('{h} Bem vindo a SJN Polpas {h}\n'.format(h = '#' * 8))
    print(bot.escolherResposta('boasvindas'))

    loop = True

    while loop:
        entrada = input()
        int = bot.predict(entrada)[0]

        if int in 'saudacao':
            primeiraSaudacao = random.choice(range(0, 9))
            segundaSaudacao = random.choice(range(0, 9))
            saudacao = ''

            if primeiraSaudacao % 2 == 0:
                 saudacao += tratarSaudacao()

            if segundaSaudacao % 2 ==0:
                if saudacao != '':
                    saudacao += ", "
                saudacao += bot.escolherResposta(int)

            if saudacao == '':
                saudacao = tratarSaudacao() + "!"

            print(saudacao)

        if int in 'inicio':
            print(bot.escolherResposta(int))

        elif int in 'pedido':
            if bot.validarPedido(entrada):
                print(bot.escolherResposta('pedido'))
            else:
                print('Não entendi o seu pedido, poderia repetir?')

        elif int in 'conta':
            bot.fecharConta()
            print(bot.escolherResposta('continuidade'))

        elif int in 'tabela':
            print(bot.escolherResposta('tabela'))
            bot.showMenu()

        elif int in 'agradecimento':
            print(bot.escolherResposta('agradecimento'))

        elif int in 'cancelar':
            print(bot.escolherResposta('agradecimento'))
            loop = False

        elif int in 'saida':
            print('Deseja realmente sair?')
            entrada = input()

            int = bot.predict(entrada)[0]

            if int in ['confirmar', 'saida']:
                if bot.totalItemsInCart() > 0:
                    bot.fecharConta()
                    print('Favor dirigir-se ao caixa!')

                print(bot.escolherResposta('agradecimento'))
                loop = False

            else:
                print(bot.escolherResposta('continuidade'))


if __name__ == '__main__':
    main()
