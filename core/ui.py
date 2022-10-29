from curses import window
import PySimpleGUI as sg


class Ui:
    def __init__(self) -> None:
        self.window = None
        self.closed = False

    def show_game(self, board):
        layout = [[]]
        for row in range(10):
            row_layout = []
            for col in range(10):
                row_layout.append(sg.Button('', key = (row, col), size=(2,2)))
            layout.append(row_layout)
        layout += [[sg.Button('SAIR', font=70)]]
        
        self.__close_if_exists()

        self.window = sg.Window('Trabalho I - S.O.', layout)

    def refresh_game(self, board):
        pass
    
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

