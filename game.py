from queue import Queue
import threading
from constants import BOARD_SIZE, TOKENS_COUNT
from core.ui import Ui
from core.utils import Utils
from threads.token_thread import token_thread
from threads.ui_thread import ui_thread


class Game:
    def __init__(self) -> None:
        self.board = None
        self.eliminated = 0
        self.threads = {}
        self.kill_evs = {}

        self.tokens_event_queue = Queue()
        self.ui_events_queue = Queue()
        self.threads_killed_ev = threading.Event()

        self.ui = Ui()
        self.board_lock = threading.Lock()

    def initialize(self):
        self.__initialize_ui_thread()

        self.ui.show_menu()

        self.__wait_for_exit()

    def thread_safe_change_token_position(self, token_id, from_position, to_position):
        with self.board_lock:
            self.clear_position(from_position.x, from_position.y)
            self.board[to_position.x][to_position] = token_id

    def thread_safe_click_position(self, x, y):
        with self.board_lock:
            has_in_position = self.has_in_position()
            if (has_in_position):
                self.clear_position(x, y)
                self.eliminated += 1

        if (self.eliminated == TOKENS_COUNT):
            self.win()
    
    def has_in_position(self, x, y):
        return bool(self.board[x][y])

    def clear_position(self, x, y):
        self.board[x][y] = 0

    def start_game(self):
        self.__wait_for_threads_to_finish()
        self.__reset_variables()
        self.__initialize_board()
        self.__initialize_tokens()
        self.__initialize_token_threads()

        self.ui.show_game(self.board)

    def refresh_game(self):
        self.ui.refresh_game(self.board)

    def win(self):
        self.threads_killed_ev.set()
        
        self.ui.show_victory()

    def defeat(self):
        self.threads_killed_ev.set()

        self.ui.show_defeat()

    def __initialize_board(self):
        self.board = []

        for row in range(BOARD_SIZE):
            self.board.append([])
            for _ in range(BOARD_SIZE):
                self.board[row].append(0)

    def __initialize_tokens(self):
        fulfilled_positions_count = 0
        while(fulfilled_positions_count < TOKENS_COUNT):
            position = Utils.get_random_position()
            has_in_position = self.has_in_position(position.x, position.y)

            if (not has_in_position):
                current_token_id = fulfilled_positions_count + 1
                self.board[position.x][position.y] = current_token_id
                fulfilled_positions_count += 1

    def __initialize_token_threads(self):
        for index in range(TOKENS_COUNT):
            key = "token_" + index

            kill_event = threading.Event()
            self.kill_evs[key] = kill_event

            token_thread = threading.Thread(target=token_thread, args=(self, kill_event))
            self.threads[key] = token_thread
            token_thread.start()

    def __initialize_ui_thread(self):
        self.threads["ui"] = threading.Thread(target=ui_thread, args=(self,))
        self.threads["ui"].start()

    def __wait_for_threads_to_finish(self):
        print("Waiting for threads to finish...")
        for thread in self.threads.values():
            thread.join()

    def __reset_variables(self):
        self.board = []
        self.eliminated = 0
        self.threads = {}
        self.kill_evs = {}
        self.tokens_event_queue = Queue()
        self.ui_events_queue = Queue()
        self.threads_killed_ev.clear()
    
    def __wait_for_exit(self):
        while (True):
            if (self.ui.closed):
                break