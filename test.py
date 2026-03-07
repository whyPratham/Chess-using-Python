import chess

# create board
board = chess.Board()

print("Welcome to Python Chess!")
print("Moves must be entered in UCI format (example: e2e4)\n")

while not board.is_game_over():

    # show board
    print(board)
    print()

    # show whose turn
    if board.turn:
        print("White to move")
    else:
        print("Black to move")

    # show legal moves
    print("Legal moves:", list(board.legal_moves))
    print()

    # take input
    user_move = input("Enter your move: ")

    try:
        move = chess.Move.from_uci(user_move)

        if move in board.legal_moves:
            board.push(move)
        else:
            print("Illegal move!\n")

    except:
        print("Invalid move format!\n")


print("\nFinal Board:")
print(board)

print("\nGame Over")

# show result
if board.is_checkmate():
    print("Checkmate!")

elif board.is_stalemate():
    print("Stalemate!")

elif board.is_insufficient_material():
    print("Draw by insufficient material!")

elif board.is_seventyfive_moves():
    print("Draw by 75-move rule!")

elif board.is_fivefold_repetition():
    print("Draw by repetition!")