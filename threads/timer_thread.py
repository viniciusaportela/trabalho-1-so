from time import sleep


def timer_thread(killed_me_ev, update_ui_queue):
    while True:
        if (killed_me_ev.isSet()):
            break

        sleep(1)
        # game.time -= 1
        # game.refresh_game()
        # DEV
        update_ui_queue.put({ "command": "timer_update", "args": []})
