from time import sleep

def timer_thread(game, killed_me_ev):
    killed_all_ev = game.killed_all_threads_ev

    while True:
        if (killed_all_ev.isSet() or killed_me_ev.isSet()):
            break
        
        sleep(1)

        game.time -= 1
        if game.time == 0:
            game.finished_game = True
            game.messages_queue.put({ "command": "defeat", "args": [] })
        else:
            game.messages_queue.put({ "command": "refresh_game", "args": [] })
