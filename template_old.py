import utils
import time
import copy

class PlayerAI:
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
        
        # Naive Evaluation Function for Breakthrough 
        # Calculates total distance moved by all black pawns - total distance moved by all white pawns
        # with maximum of distance moved by all black pawns
        def evaluate(state):
            res = 0
            max_MD = 1
            for r in range(len(state)):
                for c in range(len(state[r])):
                    if state[r][c] == 'B':
                        res += 5 - r
                        max_MD = max(max_MD, r)
                    if state[r][c] == 'W':
                        res -= r
            
            res += max_MD
            return res
        
        # Iterative Deepening MiniMax Algorithm limited by time
        # Returns [eval, [state, src, dst]]
        def mini_max(position, timeout, max_player):
            if time.time() > timeout or utils.is_game_over(position):
                return evaluate(position), position
            
            if max_player:
                max_eval = float('-inf')
                best_move = None
                for move in generate_moves(position, True):
                    evaluation = mini_max(move[0], timeout, False)[0]
                    max_eval = max(max_eval, evaluation)
                    if max_eval == evaluation:
                        best_move = move
                
                return max_eval, best_move
            else:
                min_eval = float('inf')
                best_move = None
                for move in generate_moves(position, False):
                    evaluation = mini_max(move[0], timeout, True)[0]
                    min_eval = min(min_eval, evaluation)
                    if min_eval == evaluation:
                        best_move = move
                
                return min_eval, best_move
        
        # Iterative Deepening Alpha Beta Pruning MiniMax Algorithm limited by time
        # Returns [eval, [state, src, dst]]
        def alpha_beta_mini_max(position, depth):
            max_eval, best_move = maximize(position, depth, float('-inf'), float('inf'))
            
            if not best_move:
                return utils.generate_rand_move(position)
            
            return best_move[1], best_move[2]
        
        def maximize(position, depth, alpha, beta):
            if depth == 0 or utils.is_game_over(position):
                return evaluate(position), position
            
            max_eval, best_move = float('-inf'), None
            
            for move in generate_moves(position, True):
                evaluation, _ = minimize(move[0], depth-1, alpha, beta)
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
                if max_eval == evaluation:
                    best_move = move
            return max_eval, best_move
        
        def minimize(position, depth, alpha, beta):
            if depth == 0 or utils.is_game_over(position):
                return evaluate(position), position
            
            min_eval, best_move = float('inf'), None
            
            for move in generate_moves(position, False):
                evaluation, _ = maximize(move[0], depth-1, alpha, beta)
                min_eval = min(min_eval, evaluation)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
                if min_eval == evaluation:
                    best_move = move
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
        
        return alpha_beta_mini_max(board, 4)
        

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