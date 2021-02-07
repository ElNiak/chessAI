from move.MoveUtils import move_to_uci_move
import time

max_utility = 999999
max_depth = 4


def get_best_move(board, opponents_uci_move, is_engine_white):
    best_move = 42
    start = time.time()
    for depth in range(0, max_depth):
        best_move = alpha_beta_at_root(board, opponents_uci_move, is_engine_white)
    print('time: ' + str(time.time() - start))
    return best_move


def alpha_beta_at_root(board, opponents_uci_move, is_engine_white):
    best_move_uci = 'no move'
    best_move_val = -max_utility if is_engine_white else max_utility
    moves = board.get_color_moves(is_engine_white, opponents_uci_move)
    for move in moves:
        uci_move = move_to_uci_move(move)
        move.do_move(board)
        val = alpha_beta(board, uci_move, not is_engine_white, -max_utility, max_utility, 1)
        move.undo_move(board)
        if is_engine_white:
            if val > best_move_val:
                best_move_val, best_move_uci = val, uci_move
        else:
            if val < best_move_val:
                best_move_val, best_move_uci = val, uci_move
    return best_move_uci, best_move_val


def alpha_beta(board, opponents_uci_move, is_engine_white, alpha, beta, depth):
    if depth == max_depth:
        return evaluate(board)
    if is_engine_white:
        best_val = -max_utility
        moves = board.get_color_moves(is_engine_white, opponents_uci_move)
        for move in moves:
            uci_move = move_to_uci_move(move)
            move.do_move(board)
            best_val = max(best_val, alpha_beta(board, uci_move, not is_engine_white, alpha, beta, depth + 1))
            move.undo_move(board)
            alpha = max(alpha, best_val)
            if alpha >= beta:
                break
        return best_val
    else:
        best_val = +max_utility
        moves = board.get_color_moves(is_engine_white, opponents_uci_move)
        for move in moves:
            uci_move = move_to_uci_move(move)
            move.do_move(board)
            best_val = min(best_val, alpha_beta(board, uci_move, not is_engine_white, alpha, beta, depth + 1))
            move.undo_move(board)
            beta = min(beta, best_val)
            if beta <= alpha:
                break
        return best_val


def evaluate(_board):
    return 0
