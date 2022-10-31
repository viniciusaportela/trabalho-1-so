import PySimpleGUI as sg
from constants import TOKENS_COUNT
from core.utils import Position


class Ui:
    def __init__(self) -> None:
        self.window = None
        self.closed = False

    def show_game(self, board, time, eliminated):
        layout = [
            [
                sg.Text(self.__get_time_text(time), key="time_text"),
                sg.Text(self.__get_tokens_text(eliminated), key="tokens_text")
            ]
        ]

        for row in range(10):
            row_layout = []
            for col in range(10):
                has_token = self.__has_token(board, Position(row, col))
                # color = ('white', 'red') if has_token else ('white', 'grey2')
                button_text = 'X' if has_token else ' '

                row_layout.append(sg.Button(button_text, key = (row, col), size=(2,2), disabled=not has_token))
            layout.append(row_layout)
        layout += [[sg.Button('SAIR', font=70)]]
        
        self.__close_if_exists()

        self.window = sg.Window('Trabalho I - S.O.', layout)

    def refresh_game(self, board, time, eliminated):
        self.window["time_text"].update(self.__get_time_text(time))
        self.window["tokens_text"].update(self.__get_tokens_text(eliminated))
    
    def show_victory(self):
        layout = [
            [sg.Text("PARABÉNS, VOCÊ GANHOU!", font=("Helvica",35))],
            [sg.Button("Voltar ao menu", key="back_to_menu")],
        ]

        self.__close_if_exists()
        
        self.window = sg.Window('Vitória', layout, element_justification='c')

    def show_defeat(self):
        layout = [
            [sg.Text("NÃO FOI DESSA VEZ!", font=("Helvica",35))],
            [sg.Button("Voltar ao menu", key="back_to_menu")],
        ]
        
        self.__close_if_exists()

        self.window = sg.Window('Derrota!', layout, element_justification='c')

    def show_menu(self):
        layout = [
            [sg.Text("ESCOLHA UMA OPÇÃO ", font=("Helvica",35))],
            [sg.Text("Níveis de Dificuldade", font=("Helvica",20))],
            [sg.Button("FÁCIL", key="play_easy"), sg.Button("MÉDIO", key="play_medium"), sg.Button("DIFÍCIL", key="play_hard")],
        ]

        self.__close_if_exists()

        self.window = sg.Window('Trabalho I - S.O.', layout, element_justification='c')

    def __close_if_exists(self):
        if (self.window):
            self.window.close()

    def __has_token(self, board, position):
        return bool(board[position.x][position.y])

    def __get_time_text(self, time: int):
        return "Tempo: {time}".format(time=time)
    
    def __get_tokens_text(self, eliminated: int):
        return "Fichas: {tokens}".format(tokens=TOKENS_COUNT - eliminated)