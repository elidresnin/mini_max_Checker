from copy import deepcopy

RED = (255, 0, 0)
WHITE = (255, 255, 255)

class DecisionNode:
    def __init__(self, maximizing, score=None):
        self.maximizing = maximizing
        self.score = score
        self.children = []

def minimax(current_board, depth, max_player):
    root = DecisionNode(max_player)
    result = minimax_with_tree(current_board, depth, max_player, root)
    return result[0], result[1], root

def minimax_with_tree(current_board, depth, max_player, node):
    if depth == 0 or current_board == None or current_board.winner() != None:
        score = current_board.evaluate()
        node.score = score
        return score, current_board

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(current_board, WHITE):
            child_node = DecisionNode(False)
            node.children.append(child_node)
            evaluation = minimax_with_tree(move, depth-1, False, child_node)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(current_board, RED):
            child_node = DecisionNode(True)
            node.children.append(child_node)
            evaluation = minimax_with_tree(move, depth-1, True, child_node)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        return minEval, best_move

def simulate_move(piece, move, board, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board

def get_all_moves(board, color):
    moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, skip)
            moves.append(new_board)
    return moves