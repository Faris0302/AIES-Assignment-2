import math
import time

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0,4,8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2,4,6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False

def minimax(state, player, ai_letter, human_letter, counter):
    counter['nodes'] += 1
    max_player = ai_letter
    other_player = human_letter if player == ai_letter else ai_letter

    if state.current_winner == other_player:
        return {'position': None,
                'score': 1 * (state.num_empty_squares() + 1) if other_player == ai_letter else -1 * (state.num_empty_squares() + 1)}
    elif not state.empty_squares():
        return {'position': None, 'score': 0}

    if player == max_player:
        best = {'position': None, 'score': -math.inf}
    else:
        best = {'position': None, 'score': math.inf}

    for possible_move in state.available_moves():
        state.make_move(possible_move, player)
        sim_score = minimax(state, other_player, ai_letter, human_letter, counter)

        state.board[possible_move] = ' '
        state.current_winner = None
        sim_score['position'] = possible_move

        if player == max_player:
            if sim_score['score'] > best['score']:
                best = sim_score
        else:
            if sim_score['score'] < best['score']:
                best = sim_score

    return best

def minimax_alpha_beta(state, player, ai_letter, human_letter, alpha, beta, counter):
    counter['nodes'] += 1
    max_player = ai_letter
    other_player = human_letter if player == ai_letter else ai_letter

    if state.current_winner == other_player:
        return {'position': None,
                'score': 1 * (state.num_empty_squares() + 1) if other_player == ai_letter else -1 * (state.num_empty_squares() + 1)}
    elif not state.empty_squares():
        return {'position': None, 'score': 0}

    if player == max_player:
        best = {'position': None, 'score': -math.inf}
        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = minimax_alpha_beta(state, other_player, ai_letter, human_letter, alpha, beta, counter)

            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            if sim_score['score'] > best['score']:
                best = sim_score
            alpha = max(alpha, sim_score['score'])
            if beta <= alpha:
                break
    else:
        best = {'position': None, 'score': math.inf}
        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = minimax_alpha_beta(state, other_player, ai_letter, human_letter, alpha, beta, counter)

            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            if sim_score['score'] < best['score']:
                best = sim_score
            beta = min(beta, sim_score['score'])
            if beta <= alpha:
                break

    return best

def play(game, ai_letter, human_letter, use_alpha_beta=True):
    game.print_board()
    letter = 'X'  # Starting letter
    while game.empty_squares():
        if letter == human_letter:
            valid_square = False
            val = None
            while not valid_square:
                try:
                    val = int(input('Your move (0-8): '))
                    if val not in game.available_moves():
                        raise ValueError
                    valid_square = True
                except ValueError:
                    print('Invalid move. Try again.')
            game.make_move(val, human_letter)
        else:
            print('AI is thinking...')
            counter = {'nodes': 0}
            if use_alpha_beta:
                start = time.perf_counter()
                move = minimax_alpha_beta(game, ai_letter, ai_letter, human_letter, -math.inf, math.inf, counter)
                end = time.perf_counter()
                print(f'AI chose move {move["position"]} with Alpha-Beta Pruning in {end-start:.4f} seconds, nodes explored: {counter["nodes"]}')
            else:
                start = time.perf_counter()
                move = minimax(game, ai_letter, ai_letter, human_letter, counter)
                end = time.perf_counter()
                print(f'AI chose move {move["position"]} with Minimax in {end-start:.4f} seconds, nodes explored: {counter["nodes"]}')
            game.make_move(move['position'], ai_letter)

        game.print_board()
        if game.current_winner:
            if letter == human_letter:
                print('You win!')
            else:
                print('AI wins!')
            return
        letter = human_letter if letter == ai_letter else ai_letter

    print('It\'s a tie!')

if __name__ == '__main__':
    game = TicTacToe()
    ai_letter = 'O'
    human_letter = 'X'
    mode = input("Use Alpha-Beta Pruning? (y/n): ").lower()
    use_alpha_beta = True if mode == 'y' else False
    play(game, ai_letter, human_letter, use_alpha_beta)
