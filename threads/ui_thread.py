def ui_thread(game):
    while True:
        if (game.threads_killed_ev.isSet()):
            break

        if (game.ui.window):
            event, values = game.ui.window.read()

            if event in (None, 'exit'):
                game.ui.closed = True
                break
            
            if (event == 'graph'):
                x, y = values['graph']
                game.thread_safe_click_position(x, y)

            if (event == 'play_easy'):
                # DEV use Enums
                game.start_game('easy')
            
            if (event == 'play_medium'):
                game.start_game('medium')

            if (event == 'play_hard'):
                game.start_game('hard')