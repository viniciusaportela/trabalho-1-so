def token_thread(self, game, killed_me_ev):
    killed_all_ev = game.threads_killed_ev

    while True:
        if (killed_all_ev.isSet() or killed_me_ev):
            break
