from queue import Empty, Queue
import threading
from constants import BOARD_SIZE, DIFFICULTIES_CONFIG, TOKENS_COUNT
from core.ui import Ui
from core.utils import Position, Utils
from threads.timer_thread import timer_thread
from threads.token_thread import token_thread

class Game:
    def __init__(self) -> None:
        self.board = None
        # DEV add a new variable to store position of tokens, to find more easily
        self.eliminated = 0
        self.threads = {}
        self.kill_evs = {}
        self.difficulty_config = {}
        self.time = 0
        self.finished_game = False

        self.messages_queue = Queue()

        self.killed_all_threads_ev = threading.Event()

        self.ui = Ui()
        self.board_lock = threading.Lock()

    def initialize(self):
        self.ui.show_menu()

        self.__event_loop()

    def thread_safe_change_token_position(self, token_id):
        with self.board_lock:
            from_position = self.__get_token_position(token_id)

            if (from_position):
                new_position = self.__find_random_free_position()
                self.clear_position(from_position.x, from_position.y)
                self.board[new_position.x][new_position.y] = token_id

    def thread_safe_click_position(self, x, y):
        with self.board_lock:
            position_value = self.get_in_position(x, y)
            if position_value:
                self.clear_position(x, y)
                self.__kill_token_thread(position_value)
                self.eliminated += 1
                
            if (self.eliminated == TOKENS_COUNT):
                self.finished_game = True
                self.win()
    
    def has_in_position(self, x, y):
        return bool(self.board[x][y])

    def get_in_position(self, x, y):
        return self.board[x][y]

    def clear_position(self, x, y):
        self.board[x][y] = 0

    def start_game(self, difficulty):
        self.__select_difficulty(difficulty)
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

    def exit_game(self):
        self.finished_game = True
        self.killed_all_threads_ev.set()
        self.ui.show_menu()

    def __select_difficulty(self, difficulty):
        self.difficulty_config = DIFFICULTIES_CONFIG[difficulty]

    def refresh_game(self):
        self.ui.refresh_game(
            self.board,
            self.time,
            self.eliminated,
            self.finished_game
        )

    def win(self):
        self.killed_all_threads_ev.set()
        
        self.ui.show_victory()

    def defeat(self):
        self.killed_all_threads_ev.set()

        self.ui.show_defeat()

    def __get_token_position(self, token_id):
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if (self.board[x][y] == token_id):
                    return Position(x, y)

    def __initialize_board(self):
        self.board = []

        for row in range(BOARD_SIZE):
            self.board.append([])
            for _ in range(BOARD_SIZE):
                self.board[row].append(0)

    def __initialize_tokens(self):
        token_id = 1
        while(token_id < TOKENS_COUNT + 1):
            position = self.__find_random_free_position()
            self.board[position.x][position.y] = token_id
            token_id += 1

    def __find_random_free_position(self):
        while (True):
            position = Utils.get_random_position()
            has_in_position = self.has_in_position(position.x, position.y)

            if (not has_in_position):
                return position

    def __initialize_game_threads(self):
        for index in range(TOKENS_COUNT):
            key = "token_" + str(index + 1)

            kill_event = threading.Event()
            self.kill_evs[key] = kill_event

            thread = threading.Thread(target=token_thread, args=(
                self,
                kill_event,
                index + 1
            ), daemon=True)
            self.threads[key] = thread
            thread.start()
        
        kill_event = threading.Event()
        self.kill_evs["timer"] = kill_event

        self.threads["timer"] = threading.Thread(target=timer_thread, args=(self, kill_event), daemon=True)
        self.threads["timer"].start()

    def __reset_variables(self):
        self.board = []
        self.eliminated = 0
        self.threads = {}
        self.kill_evs = {}
        self.messages_queue = Queue()
        self.killed_all_threads_ev.clear()
        self.finished_game = False
    
    def __set_timer(self):
        self.time = self.difficulty_config.get("limit_time")
    
    def __kill_token_thread(self, token_id):
        self.kill_evs["token_" + str(token_id)].set()

    def __event_loop(self):
        while True:
            if (self.ui.closed):
                break

            if (self.ui.window):
                try:
                    action = self.messages_queue.get(block=False)
                    getattr(self, action["command"])(*action["args"])
                        
                except Empty:
                    pass

                event, _ = self.ui.window.read(timeout=0)

                if event in (None, 'exit'):
                    self.ui.closed = True
                    break
                if (event == 'exit_game'):
                    self.exit_game()

                if (event == 'play_easy'):
                    # DEV use Enums
                    self.start_game('easy')
                
                if (event == 'play_medium'):
                    self.start_game('medium')

                if (event == 'play_hard'):
                    self.start_game('hard')
                
                if (event == 'back_to_menu'):
                    self.ui.show_menu()

                # when click a token button
                if (type(event) is tuple):
                    x, y = event
                    self.thread_safe_click_position(x, y)
