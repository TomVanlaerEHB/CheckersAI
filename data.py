from copy import deepcopy

def print_board(board):
    for y in range(0, 8):
        for (x) in range(1, 9):
            set = False
            if y % 2 == 0:
                for piece in board.pieces:
                    if piece.captured:
                        continue
                    if piece.position == (x + (y * 8)) / 2:
                        if piece.player == 1:
                            print('x', end='')
                            set = True
                        elif piece.player == 2:
                            set = True
                            print('o', end='')
            else:
                for piece in board.pieces:
                    if piece.captured:
                        continue
                    if piece.position * 2 - 1 == (x + (y * 8)):
                        if piece.player == 1:
                            set = True
                            print('x', end='')
                        elif piece.player == 2:
                            set = True
                            print('o', end='')
            if not set:
                print('_', end='')
        print()
    print("==================================================================================")

def is_won(game):
    """
        Returns true if the game has been won
    """
    return game.is_over()
        

def minMax2(game):
    """
        Main minmax function, takes a board as input and returns the best possible move in the form
        of a board and the value of that board.
    """
    bestBoard = None
    currentDepth = game.board.maxDepth + 1
    while not bestBoard and currentDepth > 0:
        currentDepth -= 1
        # Get the best move and it's value from maxMinBoard (minmax handler)
        (bestBoard, bestVal) = maxMove2(game, currentDepth)
        # If we got a NUll board raise an exception
    if not bestBoard:
        raise Exception("Could only return null boards")
    # Otherwise return the board and it's value
    else:
        #print(bestBoard)
        #print(bestVal)
        return (bestBoard, bestVal)

def maxMove2(maxBoard, currentDepth):
    """
        Calculates the best move for BLACK player (computer) (seeks a board with INF value)
    """
    return maxMinBoard(maxBoard, currentDepth-1, float('-inf'))
    

def minMove2(minBoard, currentDepth):
    """
        Calculates the best move from the perspective of WHITE player (seeks board with -INF value)
    """
    return maxMinBoard(minBoard, currentDepth-1, float('inf'))

def maxMinBoard(board, currentDepth, bestMove):
    """
        Does the actual work of calculating the best move
    """
    # Check if we are at an end node
    if is_won(board) or currentDepth <= 0:
        return (board, staticEval2(board))
  
    # So we are not at an end node, now we need to do minmax
    # Set up values for minmax
    best_move = bestMove
    best_board = None
  
    # I could probably consolidate MaxNode and MinNode more by assigning the iterator with a 
    # function and doing some trickery with the bestmove == INF bullshit
    # MaxNode
    if bestMove == float('-inf'):
        # Create the iterator for the Moves
        moves = board.board.get_possible_moves()
        #print(moves)
        for move in moves:
            maxBoard = deepcopy(board)
            #print(move)            
            maxBoard.move(move)
            value = minMove2(maxBoard, currentDepth-1)[1]
            if value > best_move:
                best_move = value
                best_board = maxBoard         
  
    # MinNode
    elif bestMove == float('inf'):
        moves = board.board.get_possible_moves()
        #print(moves)
        for move in moves:
            minBoard = deepcopy(board)
            minBoard.move(move)
            value = maxMove2(minBoard, currentDepth-1)[1]
            # Take the smallest value we can
            if value < best_move:
                best_move = value
                best_board = minBoard
  
    # Something is wrong with bestMove so raise an Exception
    else:
        raise Exception("bestMove is set to something other than inf or -inf")
  
    # Things appear to be fine, we should have a board with a good value to move to
    return (best_board, best_move)

def staticEval2(evalBoard):
    """
        Evaluates a board for how advantageous it is
        -INF if WHITE player has won
        INF if BLACK player has won
        Otherwise use a particular strategy to evaluate the move
        See Comments above an evaluator for what it's strategy is
    """
    # Has someone won the game? If so return an INFINITE value
    if evalBoard.get_winner() is not 1 or not 2:
        #print("No winner")
        pass
    elif evalBoard.get_winner() == evalBoard.whose_turn():
        return float('inf')  
    elif evalBoard.get_winner() != evalBoard.whose_turn():
        return float('-inf')
    # Unhappy Grandfather Evaluator
#    return 0
    
    # Some setup
    if evalBoard.whose_turn() == 1:
        scoremod = -1
    elif evalBoard.whose_turn() == 2:
        scoremod = 1

    pieces = []
    for piece in evalBoard.board.pieces:
        if piece.captured:
            continue
        if piece.player == evalBoard.whose_turn():
            pieces.append(piece)
        #pieces = evalBoard.get_possible_moves()

    # Super Gigadeath Defense Evaluator
    # This AI will attempt to keep it's pieces as close together as possible until it has a chance
    # to jump the opposing player. It's super effective
    distance = 0
    for piece1 in pieces:
        #print(piece1.position)
        for piece2 in pieces:
            #print(piece2.position)
            if piece1 == piece2:
                continue
            dx = abs(piece1.position - piece2.position)
            #dy = abs(piece1[1] - piece2[1])
            distance += dx**2 #+ dy**2
    if len(pieces) != 0:
        distance /= len(pieces)
    if distance == 0 :
        return 1.0/scoremod
    return 1.0/distance * scoremod