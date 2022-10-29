def ui_thread(game):
    while True:
        if (game.threads_killed_ev.isSet()):
            break

        if (game.ui.window):
            event, values = game.ui.window.read()

            if event in (None, 'exit'):
                break
            
            if (event == 'graph'):
                x, y = values['graph']
                game.thread_safe_click_position(x, y)
            
