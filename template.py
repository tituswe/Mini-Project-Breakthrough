import utils
import time
import copy
import random

class PlayerAI:
    # Initialize Zobrist Hash table and Transposition table for memoization
    # Zobrist Hash table stores a hashed value for each B or W piece on the board,
    # and the Zobrist Hash value of the board is calculated by XOR-ing each
    # present piece on the board together
    def __init__(self):
        self.z_table = [[[0 for i in range(2)] for j in range(6)] for k in range(6)]
        self.t_table = dict()
        
        # Generate a random bitstring for Zobrist Hashing
        def random_bitstring():
            bitstring = ""
            for i in range(36):
                temp = str(random.randint(0, 1))
                bitstring += temp
            return int(bitstring, base=2)
        
        for r in range(6):
            for c in range(6):
                for i in range(2):
                    self.z_table[r][c][i] = random_bitstring()
        
    def make_move(self, board):
        '''
        This is the function that will be called from main.py
        Your function should implement a minimax algorithm with 
        alpha beta pruning to select the appropriate move based 
        on the input board state. Play for black.

        Parameters
        ----------
        self: object instance itself, passed in automatically by Python
        board: 2D list-of-lists
        Contains characters 'B', 'W', and '_' representing
        Black pawns, White pawns and empty cells respectively
        
        Returns
        -------
        Two lists of coordinates [row_index, col_index]
        The first list contains the source position of the Black pawn 
        to be moved, the second list contains the destination position
        '''
        ###################
        # Amazing AI Code #
        ###################
        
        # Calculates the Zobrist Hash Value of each Board State
        def zobrist(state, black):
            h = 0
            x = 1010101010101010
            for r in range(len(state)):
                for c in range(len(state[r])):
                    if state[r][c] == 'B':
                        h = h ^ self.z_table[r][c][0]
                    elif state[r][c] == 'W':
                        h = h ^ self.z_table[r][c][1]
            if black:
                h = h ^ x
                
            return h            
        
        # Evaluation Function for Breakthrough 
        # Calculates total distance moved by all black pawns - total distance moved by all white pawns
        # with maximum of distance moved by all black pawns        
        def evaluate(state):
            score_b = 0
            score_w = 0
            for r in range(len(board)):
                for c in range(len(board[r])):
                    if state[0][c] == 'W':
                        return float('-inf')
                    
                    if state[5][c] == 'B':
                        return float('inf')
                    
                    if state[r][c] == 'B':
                        if r == 4:
                            score_b += 10
                        else:
                            score_b += r
                    
                    if state[r][c] == 'W':
                        if r == 1:
                            score_w += 10
                        else:
                            score_w += 5-r
            
            return score_b - score_w
            
        # Iterative Deepening Alpha Beta Pruning MiniMax Algorithm limited by depth
        # Transposition table used for memoization, storing the best_move and evaluation
        # of each already evaluated state. Key of the Transposition table is the Zobrist
        # Hash value of the board's state, with the value best_move, evaluation
        # Returns best_move: src, dst
        def alpha_beta_mini_max(position, depth):
            max_eval, best_move = maximize(position, depth, float('-inf'), float('inf'))
            
            return best_move[1], best_move[2]
        
        def maximize(position, depth, alpha, beta):
            if depth == 0 or utils.is_game_over(position):
                return evaluate(position), position
            
            max_eval, best_move = float('-inf'), None
            
            t_key = zobrist(position, True)
            
            if t_key in self.t_table:
                return self.t_table[t_key]
            
            for move in generate_moves(position, True):
                evaluation, _ = minimize(move[0], depth-1, alpha, beta)
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, max_eval)
                if beta <= alpha and best_move is not None:
                    break
                if max_eval == evaluation:
                    best_move = move
            
            self.t_table[t_key] = max_eval, best_move
            
            return max_eval, best_move
        
        def minimize(position, depth, alpha, beta):
            if depth == 0 or utils.is_game_over(position):
                return evaluate(position), position
            
            min_eval, best_move = float('inf'), None
            
            t_key = zobrist(position, False)
            
            if t_key in self.t_table:
                return self.t_table[t_key]
            
            for move in generate_moves(position, False):
                evaluation, _ = maximize(move[0], depth-1, alpha, beta)
                min_eval = min(min_eval, evaluation)
                beta = min(beta, min_eval)
                if beta <= alpha and best_move is not None:
                    break
                if min_eval == evaluation:
                    best_move = move
                    
            self.t_table[t_key] = min_eval, best_move
            
            return min_eval, best_move

                
        # Generate the next possible moves from given board state
        def generate_moves(state, black):
            moves = [] # Each element is a tuple [state, src, dst]
            if not black:
                state = utils.invert_board(state)
            
            for r in range(len(state)):
                for c in range(len(state[r])):
                    if board[r][c] == 'B':
                        for i in range(-1, 2):
                            src = [r, c]
                            dst = [r+1, c+i]
                            if utils.is_valid_move(state, src, dst):
                                temp_state = copy.deepcopy(state)
                                temp_state = utils.state_change(temp_state, src, dst)
                                if not black:
                                    temp_state = utils.invert_board(temp_state)
                                moves.append([temp_state, src, dst])
            
            return moves
        
        # Searches the current board to see if there are pawns that have an autowin condition;
        # if the pawn moves forward and cannot be stopped, it is an auto win, and execute that move.
        # If no autowin conditions, agent will search for the best move.
        def smart_move(state):
            l = len(state) - 1
            for c in range(len(state[l])):
                if state[l-1][c] == 'B':
                    for i in range(-1, 2):
                        src = [l-1, c]
                        dst = [l, c+i]
                        if utils.is_valid_move(state, src, dst):
                            return src, dst
                            
            return alpha_beta_mini_max(state, 5)
        
        return smart_move(board)

class PlayerNaive:
    ''' A naive agent that will always return the first available valid move '''
    def make_move(self, board):
        return utils.generate_rand_move(board)
        

# You may replace PLAYERS with any two players of your choice
PLAYERS = [PlayerAI(), PlayerNaive()]
COLOURS = [BLACK, WHITE] = 'Black', 'White'
TIMEOUT = 3.0

##########################
# Game playing framework #
##########################
if __name__ == "__main__":

    print("Initial State")
    board = utils.generate_init_state()
    utils.print_state(board)
    move = 0

    # game starts
    while not utils.is_game_over(board):
        player = PLAYERS[move % 2]
        colour = COLOURS[move % 2]
        if colour == WHITE: # invert if white
            utils.invert_board(board)
        start = time.time()
        src, dst = player.make_move(board) # returns [i1, j1], [i2, j2] -> pawn moves from position [i1, j1] to [i2, j2]
        end = time.time()
        within_time = end - start <= TIMEOUT
        valid = utils.is_valid_move(board, src, dst) # checks if move is valid
        if not valid or not within_time: # if move is invalid or time is exceeded, then we give a random move
            print('executing random move')
            src, dst = utils.generate_rand_move(board)
        utils.state_change(board, src, dst) # makes the move effective on the board
        if colour == WHITE: # invert back if white
            utils.invert_board(board)

        print(f'Move No: {move} by {colour}')
        utils.print_state(board) # printing the current configuration of the board after making move
        move += 1
    print(f'{colour} Won')
