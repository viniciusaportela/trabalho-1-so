from time import sleep


def token_thread(game, killed_me_ev, token_id):
    killed_all_ev = game.killed_all_threads_ev

    while True:
        if (killed_all_ev.isSet() or killed_me_ev.isSet()):
            break
        
        sleep(game.difficulty_config["time_to_change"])

        game.thread_safe_change_token_position(token_id)
        game.messages_queue.put({ "command": "refresh_game", "args": [] })


