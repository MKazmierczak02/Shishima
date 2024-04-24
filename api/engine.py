# @formatter:on
ALLOWED_MOVES = {
    0: [1, 3, 4],
    1: [0, 2, 4],
    2: [1, 4, 5],
    3: [0, 4, 6],
    4: [0, 1, 2, 3, 5, 6, 7, 8],
    5: [2, 4, 8],
    6: [7, 4, 3],
    7: [6, 4, 8],
    8: [5, 4, 7]
}

WIN_POSITIONS = [
    [0, 4, 8],
    [1, 4, 7],
    [2, 4, 6],
    [3, 4, 5],
]


class GameEngine:
    def __init__(self):
        self.players = ["X", "O"]
        self.current_player = "X"
        self.size = 3
        self.game_over = False
        self.winner = None
        self.max_coin = 3
        self.board = [' ' for _ in range(self.size * self.size)]
        self.init_board()

    def init_board(self):
        self.board[0] = "X"
        self.board[3] = "X"
        self.board[6] = "X"
        self.board[1] = "O"
        self.board[2] = "O"
        self.board[5] = "O"

    def make_move(self, move_from: int, move_to: int):
        if self.current_player != self.board[move_from]:
            return f"Invalid MOVE_FROM NOT A PLAYER {move_from} -  {move_to}"
        if move_to in ALLOWED_MOVES.get(move_from) and self.board[move_to] == ' ':
            self.board[move_to] = self.current_player
            self.board[move_from] = ' '
            if self.check_winner():
                self.game_over = True
                self.winner = self.current_player
                return f"{self.current_player} WON"
            prev = self.current_player
            self.switch_players()
            return f"OK - {prev}: {move_from} -  {move_to}"
        return f"Invalid {move_from} to {move_to}"

    def switch_players(self):
        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"

    def check_winner(self):
        for positions in WIN_POSITIONS:
            if (self.board[positions[0]] == self.board[positions[1]] == self.board[positions[2]]
                    and self.board[positions[0]] != ' '):
                return True
        return False

    def reset_game(self):
        self.board = [' ' for _ in range(self.size * self.size)]
        self.game_over = False
        self.winner = None

    def get_board(self):
        return self.board
