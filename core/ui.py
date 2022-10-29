import PySimpleGUI as sg


class Ui:
    def __init__(self) -> None:
        self.window = None
        self.closed = False

    def show_game(self, board):
        layout = [
            [sg.Graph(
                canvas_size=(400, 400),
                graph_bottom_left=(0, 0),
                graph_top_right=(400, 400),
                enable_events=True,
                key='graph'
            )]
        ]

        self.game.on_game_start()
        self.__close_if_exists()

        self.window = sg.Window('Trabalho I - S.O. - Jogo', layout)

    def refresh_game(self, board):
        pass

    def show_victory(self):
        layout = [
            [sg.Text("Parabéns, você venceu!")],
            [sg.Button("Voltar ao menu")]
        ]

        self.__close_if_exists()
        
        self.window = sg.Window('Vitória!', layout)

    def show_menu(self):
        layout = [
            [sg.Text('Jogo')],
            [sg.Button('Jogar Fácil', key="play_easy")],
            [sg.Button('Jogar Médio', key="play_medium")],
            [sg.Button('Jogar Difícil', key="play_hard")],
            [sg.Exit('Sair', key="exit")],
        ]

        self.__close_if_exists()

        self.window = sg.Window('Derrota!', layout)

    def show_defeat(self):
        layout = [
            [sg.Text("Você perdeu! que tal tentar de novo?")],
            [sg.Button("Voltar ao menu")]
        ]
        
        self.__close_if_exists()

        self.window = sg.Window('Derrota!', layout)

    def __close_if_exists(self):
        if (self.window):
            self.window.close()
