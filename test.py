from queue import Empty, Queue
import time
import PySimpleGUI as sg

start = time.time()

queue = Queue()

layout = [
    [
        sg.Text("Tempo: 40", key="time_text"),
        sg.Text("5", key="tokens_text")
    ]
]

for row in range(10):
    row_layout = []
    for col in range(10):
        has_token = True
        button_text = 'X' if has_token else ' '

        row_layout.append(sg.Button(button_text, key = (row, col), size=(2,2), disabled=not has_token))
    layout.append(row_layout)
layout += [[sg.Button('SAIR', font=70)]]

window = sg.Window('Trabalho I - S.O.', layout)

while True:
    try:
        queue.get(block=False)
    except Empty:
        pass

    event, values = window.read(timeout=0)
    print("first event: ", event)
    end = time.time()
    print(str(end - start))

