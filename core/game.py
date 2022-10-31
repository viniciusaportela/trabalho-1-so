from queue import Queue
import threading
from constants import BOARD_SIZE, DIFFICULTIES_CONFIG, TOKENS_COUNT
from core.ui import Ui
from core.utils import Utils
from threads.timer_thread import timer_thread
from threads.token_thread import token_thread
from threads.ui_thread import ui_thread

class Game:
    def __init__(self) -> None:
        self.board = None
        self.eliminated = 0
        self.threads = {}
        self.kill_evs = {}
        self.difficulty_config = {}
        self.time = 0

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
            position_value = self.get_in_position(x, y)
            if position_value:
                self.clear_position(x, y)
                self.__kill_token_thread(position_value)
                self.eliminated += 1

        if (self.eliminated == TOKENS_COUNT):
            self.win()
    
    def has_in_position(self, x, y):
        return bool(self.board[x][y])

    def get_in_position(self, x, y):
        return self.board[x][y]

    def clear_position(self, x, y):
        self.board[x][y] = 0

    def start_game(self, difficulty):
        self.__select_difficulty(difficulty)
        self.__wait_for_threads_to_finish()
        self.__reset_variables()
        self.__initialize_board()
        self.__initialize_tokens()
        self.__initialize_game_threads()
        self.__set_timer()

        self.ui.show_game(
            self.board, 
            self.time,
            self.eliminated
        )
    
    # DEV
    def exit_game(self):
        pass

    def __select_difficulty(self, difficulty):
        self.difficulty_config = DIFFICULTIES_CONFIG[difficulty]

    def refresh_game(self):
        self.ui.refresh_game(
            self.board,
            self.time,
            self.eliminated
        )

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
                self.board[position.x][position.y] = fulfilled_positions_count
                fulfilled_positions_count += 1

    def __initialize_game_threads(self):
        for index in range(TOKENS_COUNT):
            key = "token_" + str(index)

            kill_event = threading.Event()
            self.kill_evs[key] = kill_event

            thread = threading.Thread(target=token_thread, args=(self, kill_event), daemon=True)
            self.threads[key] = thread
            thread.start()
        
        kill_event = threading.Event()
        self.kill_evs["timer"] = kill_event

        self.threads["timer"] = threading.Thread(target=timer_thread, args=(self, kill_event), daemon=True)
        self.threads["timer"].start()

    def __initialize_ui_thread(self):
        self.threads["ui"] = threading.Thread(target=ui_thread, args=(self,), daemon=True)
        self.threads["ui"].start()

    def __wait_for_threads_to_finish(self):
        for thread_key in self.threads.keys():
            if (thread_key in ("ui")):
                continue
            
            thread = self.threads[thread_key]
            thread.join()

    def __reset_variables(self):
        self.board = []
        self.eliminated = 0
        self.threads = {}
        self.kill_evs = {}
        self.tokens_event_queue = Queue()
        self.ui_events_queue = Queue()
        self.threads_killed_ev.clear()
    
    def __set_timer(self):
        self.time = self.difficulty_config.get("limit_time")

    def __wait_for_exit(self):
        while (True):
            if (self.ui.closed):
                break
    
    def __kill_token_thread(self, token_id):
        self.kill_evs["token_" + str(token_id)].set()