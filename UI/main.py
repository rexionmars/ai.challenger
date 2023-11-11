import chess
import chess.svg
import subprocess
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget

class ChessGUI(QMainWindow):
    def __init__(self, stockfish_path):
        super(ChessGUI, self).__init__()

        self.board = chess.Board()
        self.stockfish_path = stockfish_path

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.svg_widget = QSvgWidget(self)
        self.update_board_display()

        self.layout.addWidget(self.svg_widget)

        self.move_button = QPushButton("Next Move", self)
        self.move_button.clicked.connect(self.make_next_move)
        self.layout.addWidget(self.move_button)

        self.setWindowTitle("Chess GUI")
        self.setGeometry(100, 100, 600, 600)

        self.stockfish_process = subprocess.Popen(
            [self.stockfish_path], universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )

    def update_board_display(self):
        svg = chess.svg.board(board=self.board)
        self.svg_widget.load(svg.encode("utf-8"))

    def make_next_move(self):
        if not self.board.is_game_over():
            move_uci = self.get_stockfish_move()
            self.board.push_uci(move_uci)
            self.update_board_display()

    def get_stockfish_move(self):
        self.stockfish_process.stdin.write(f"position fen {self.board.fen()}\n")
        self.stockfish_process.stdin.write("go movetime 1000\n")
        self.stockfish_process.stdin.flush()

        stockfish_output = self.stockfish_process.stdout.readline()
        while "bestmove" not in stockfish_output:
            stockfish_output = self.stockfish_process.stdout.readline()

        move_uci = stockfish_output.split()[1]
        return move_uci

if __name__ == "__main__":
    app = QApplication(sys.argv)

    stockfish_path = "../performance/core/chess_program"  # Substitua pelo caminho real
    gui = ChessGUI(stockfish_path)
    gui.show()

    sys.exit(app.exec_())
