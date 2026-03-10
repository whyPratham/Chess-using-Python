import pytest
import chess
from game import ChessGame

def test_initial_board():
    game = ChessGame()
    assert game.board.fen().startswith("rnbqkbnr")

def test_reset_function():
    game = ChessGame()
    game.board.push_san("e4")
    game.reset()
    assert game.board.fen().startswith("rnbqkbnr")

def test_valid_move():
    game = ChessGame()
    move = chess.Move.from_uci("e2e4")
    assert move in game.board.legal_moves
