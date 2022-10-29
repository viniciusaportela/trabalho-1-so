import threading
from constants import BOARD_SIZE, TOKENS_COUNT
from core.ui import Ui
from core.utils import Utils
from threads.change_position_thread import change_position


class Game:
    def __init__(self) -> None:
        self.board = None
        self.eliminated = 0
        self.threads = {}

        self.ui = Ui()
        self.lock = threading.Lock()

    def initialize(self):
        self.initialize_board()
        self.initialize_tokens()
        self.initialize_ui()
        self.initialize_threads()

    def initialize_board(self):
        self.board = []

        for row in range(BOARD_SIZE):
            self.board.append([])
            for _ in range(BOARD_SIZE):
                self.board[row].append(0)

    def initialize_tokens(self):
        fulfilled_positions_count = 0
        while(fulfilled_positions_count < TOKENS_COUNT):
            position = Utils.get_random_position()
            has_in_position = self.has_in_position(position.x, position.y)

            if (not has_in_position):
                self.board[position.x][position.y] = 1
                fulfilled_positions_count += 1

    def initialize_ui(self):
        self.ui.initialize(self.board)

    def initialize_threads(self):
        for index in range(TOKENS_COUNT):
            thread = threading.Thread(target=change_position, args=(self))
            self.threads[index] = thread

            thread.start()

    def has_in_position(self, x, y):
        return bool(self.board[x][y])

    def thread_safe_has_in_position(self, x, y):
        with self.lock:
            return bool(self.board[x][y])

    def thread_safe_change_position(self, token_id, from_position, to_position):
        with self.lock:
            self.thread_safe_clear_position(from_position.x, from_position.y)
            self.board[to_position.x][to_position] = token_id

    def thread_safe_click_position(self, x, y):
        with self.lock:
            has_in_position = self.thread_safe_has_in_position()
            if (has_in_position):
                self.thread_safe_clear_position(x, y)

    def thread_safe_clear_position(self, x, y):
        self.board[x][y] = 0
