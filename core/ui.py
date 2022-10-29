from curses import window
import PySimpleGUI as sg


class Ui:
    def initialize(self):
        layout = [[]]
        for row in range(10):
            row_layout = []
            for col in range(10):
                row_layout.append(sg.Button('', key = (row, col), size=(2,2)))
            layout.append(row_layout)
        layout += [[sg.Button('SAIR', font=70)]]
        window = sg.Window('Trabalho I - S.O.', layout)
    
    def winning_screen(self):
        layout = [
            [sg.Text("PARABÉNS, VOCÊ GANHOU!", font=("Helvica",35))],
            [sg.Text("Deseja Jogar Novamente?", font=("Helvica",20))],
            [sg.Button("SIM"), sg.Button("NÃO")],
        ]
        window = sg.Window('Trabalho I - S.O.', layout, element_justification='c')

    def loser_screen(self):
        layout = [
            [sg.Text("NÃO FOI DESSA VEZ!", font=("Helvica",35))],
            [sg.Text("Deseja Jogar Novamente?", font=("Helvica",20))],
            [sg.Button("SIM"), sg.Button("NÃO")],
        ]
        window = sg.Window('Trabalho I - S.O.', layout, element_justification='c')
    
    def level_screen(self):
        layout = [
            [sg.Text("ESCOLHA UMA OPÇÃO ", font=("Helvica",35))],
            [sg.Text("Níveis de Dificuldade", font=("Helvica",20))],
            [sg.Button("FÁCIL"), sg.Button("MÉDIO"), sg.Button("DIFÍCIL")],
        ]
        window = sg.Window('Trabalho I - S.O.', layout, element_justification='c')

    def refresh(self, board):
        pass


