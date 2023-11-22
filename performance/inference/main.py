import sys
import subprocess
import os
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import QTimer
import chess
import chess.svg
import chess.engine
from art import *
import matplotlib.pyplot as plt

from utils.Utils import Colors, writelnc


class ChessUI(QMainWindow):
    def __init__(self, algorithm_path: str):
        super().__init__()

        self.board = chess.Board()

        stockfish_path = algorithm_path

        # Inicializa o Stockfish com as opções configuradas
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

        # Configuração das opções (Threads, Hash, etc.)
        self.engine.configure({"Threads": 12, "Hash": 1024})

        # Dados para os gráficos
        self.depth_values = []
        self.time_values = []
        self.nodes_values = []
        self.evaluation_values = []

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
        svg_filename = 'board.svg'

        with open(svg_filename, 'w') as svg_file:
            svg_file.write(svg_data)

        self.svg_widget.load(svg_filename)
        self.svg_widget.show()

    def suggest_move(self):
        result = self.engine.play(self.board, chess.engine.Limit(nodes=1000000, depth=20, time=5.0))
        self.board.push(result.move)
        self.update_board()

        # Solicita uma análise para obter informações sobre a jogada sugerida
        info = self.engine.analyse(self.board, chess.engine.Limit(nodes=1000000, depth=20, time=5.0))

        # Salva os dados para os gráficos
        self.depth_values.append(info.get('depth', 0))
        self.time_values.append(info.get('time', 0))
        self.nodes_values.append(info.get('nodes', 0))
        self.evaluation_values.append(info.get('score', {}).relative.score())

        # Imprime as informações
        print(f"ELO: {info}, Stockfish sugere: {result.move.uci()}")
        self.print_evaluation(info)


    def check_game_result(self):
        if self.board.is_checkmate():
            print("Xeque-mate! Você perdeu. 💔😢")
            return True
        elif self.board.is_stalemate():
            print("Empate! O jogo terminou empatado. 🤝😐")
            return True
        elif self.board.is_insufficient_material():
            print("Empate! Material insuficiente para xeque-mate. 🤝😐")
            return True
        elif self.board.is_seventyfive_moves():
            print("Empate! O jogo atingiu o limite de 75 movimentos sem capturas ou movimentos de peões. 🤝😐")
            return True
        elif self.board.is_fivefold_repetition():
            print("Empate! A posição se repetiu pela quinta vez. 🤝😐")
            return True
        return False

    def print_evaluation(self, info):
        if 'score' in info:
            print(f"Avaliação: {info['score']}")
        else:
            print("Avaliação não disponível.")

        if 'pv' in info:
            principal_variation = info['pv']
            print(f"Variação Principal: {principal_variation}")
        else:
            print("Variação Principal não disponível.")

        if 'depth' in info:
            print(f"Profundidade: {info['depth']}")
        else:
            print("Profundidade não disponível.")

        if 'nodes' in info:
            print(f"Nós analisados: {info['nodes']}")
        else:
            print("Nós analisados não disponíveis.")

        if 'time' in info:
            print(f"Tempo de análise: {info['time']} segundos")
        else:
            print("Tempo de análise não disponível.")

        print("\n")


if __name__ == "__main__":
    tprint("VOLTS", font="cybermedum")
    print("{joao_leonardi.melo, enzo.goncalves, joao_vinicius.carvalho}@somosicev.com")
    stockfish_path = "../../engines/stockfish/Stockfish/src/stockfish"  # Substitua pelo caminho correto do seu Stockfish

    app = QApplication(sys.argv)
    chess_ui = ChessUI(stockfish_path)
    chess_ui.show()

    while True:
        user_move = input(f"{Colors.ORANGE}V O L T S ENGINE{Colors.RESET} 🔥: ")
        if user_move.lower() == 'quit':
            break

        if chess.Move.from_uci(user_move) in chess_ui.board.legal_moves:
            chess_ui.board.push(chess.Move.from_uci(user_move))
            chess_ui.update_board()
            if chess_ui.check_game_result():
                break
            chess_ui.suggest_move()
            if chess_ui.check_game_result():
                break
        else:
            print("Jogada inválida. Tente novamente.")

    sys.exit(app.exec_())
