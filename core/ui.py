import PySimpleGUI as sg


class Ui:
    def initialize(self, board):
        layout = [
            sg.Graph(
                canvas_size=(400, 400),
                graph_bottom_left=(0, 0),
                graph_top_right=(400, 400),
                background_color='red', # DEV to white
                enable_events=True,
                key='graph'
            )
        ]

        self.window = sg.Window('Trabalho I - S.O.', layout)

    def refresh(self, board):
        pass
