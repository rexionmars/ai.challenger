import sys
import chess
import chess.svg
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtSvg import QSvgWidget
import chess.engine

class ChessUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.board = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci("/home/remix/wrkdir/my/ai.challenger/performance/stockfish/Stockfish/src/stockfish")  # Substitua pelo caminho real

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.svg_widget = QSvgWidget(self)
        self.update_board()
        layout.addWidget(self.svg_widget)

        self.setGeometry(100, 100, 600, 600)
        self.setWindowTitle('Chess UI')

    def update_board(self):
        svg_data = chess.svg.board(self.board)
        svg_filename = "board.svg"

        with open(svg_filename, "w") as svg_file:
            svg_file.write(svg_data)

        self.svg_widget.load(svg_filename)
        self.svg_widget.show()

    def suggest_move(self):
        result = self.engine.play(self.board, chess.engine.Limit(time=1.0))
        self.board.push(result.move)
        self.update_board()
        print(f'Stockfish sugere: {result.move.uci()}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chess_ui = ChessUI()
    chess_ui.show()

    while True:
        user_move = input("Sua jogada (ou 'quit' para encerrar): ")
        if user_move.lower() == 'quit':
            break

        if chess.Move.from_uci(user_move) in chess_ui.board.legal_moves:
            chess_ui.board.push(chess.Move.from_uci(user_move))
            chess_ui.update_board()
            chess_ui.suggest_move()
        else:
            print('Jogada inválida. Tente novamente.')

    sys.exit(app.exec_())
