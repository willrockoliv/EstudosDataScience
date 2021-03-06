import random

board = ['''

>>>>>>Hangman<<<<<<<

+---+
|   |
    |
    |
    |
    |
=====''','''
+---+
|   |
0   |
    |
    |
    |
=====''','''
 +---+
 |   |
 0   |
/    |
     |
     |
 =====''','''
 +---+
 |   |
 0   |
/|   |
     |
     |
 =====''','''
 +---+
 |   |
 0   |
/|\  |
     |
     |
 =====''','''
 +---+
 |   |
 0   |
/|\  |
/    |
     |
 =====''','''
 +---+
 |   |
 0   |
/|\  |
/ \  |
     |
 =====''']


class Hangman:

    word = ""
    word_show = ""
    letras_descobertas = []
    chances = 6


    #Método Construtor
    def __init__(self, word):
        self.word = word

    # Método para adivinhar a letra
    def guess(self, latter):
        if self.word.find(latter) != -1:
            self.letras_descobertas.append(latter)
            return True
        else:
            self.chances = self.chances - 1
            return False


    # Método para verificar se o jogo terminou
    def hangman_over(self):
        if self.chances == 0:
            return True
        else:
            return False


    #Método para verificar se o jogador venceu
    def hangman_won(self):

        won = True

        for w in Hangman.word:
            if self.letras_descobertas.count(w) == 0:
                won = False

        return won

    #Método para não mostrar a letra no board
    def hide_word(self):
        self.word_show = ''
        for letra in self.word:
            if letra in self.letras_descobertas:
                self.word_show = self.word_show + letra
            else:
                self.word_show = self.word_show + "_"

    #Mpetodo para checar o status do game e imprimir o board na tela
    def print_game_status(self):
        self.hide_word(self)
        print(board[6-self.chances])
        print(self.word_show)


#Função para ler uma palavra de forma aleatória do banco de palavras
def rand_word():
    with open("palavras.txt", "rt") as f:
        bank = f.readlines()
    return bank[random.randint(0, len(bank))].strip()

# Função Main - Execuçao do Programa
def main():
    #Objeto
    game = Hangman(rand_word())

    #Enquanto o jogo não estiver terminado, print do status, solicita uma letra e faz a leitura do caracter
    while(True):

        print('\nEscolha uma letra:\n')
        _input = input()

        if (len(_input) > 1):
            print('apenas uma letra por favor...')
        else:
            # testa a letra
            game.guess(_input)

            #Verifica o status do jogo
            game.print_game_status()

            # De acordo com o status, imprime mensagem na tela para o usuário
            if game.hangman_won():
                print('\nParabéns! Você venceu!!')
                break
            elif game.hangman_over():
                print('\nGame Over!')
                print('\nA palavra era ' + game.word)
                break

    print('\nFoi bom jogar com você! Agora vá estudar!\n')

# Executa o programa
if __name__ == "__main__":
    main()