from time import sleep


def timer_thread(game, killed_me_ev):
    while True:
        if (killed_me_ev.isSet()):
            break

        sleep(1)
        game.time -= 1
        game.refresh_game()
