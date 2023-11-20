import sys
import subprocess
import os
import threading
import re

import chess
import chess.svg
import chess.engine
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtSvg import QSvgWidget
from art import *

from utils.Utils import Colors, writelnc


def run_command_in_terminal(command: str):
    # Abre um novo terminal e executa o comando fornecido
    subprocess.Popen(["kitty", command])


os_command = "htop"  # Comando para monitorar o uso de hardware

# Inicia o monitoramento da GPU em um terminal separado
gpu_thread = threading.Thread(target=run_command_in_terminal, args=(os_command,))
gpu_thread.start()
gpu_thread.join()


class ChessUI(QMainWindow):
    def __init__(self, algorihm_path: str):
        super().__init__()

        self.board = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci(algorihm_path)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.svg_widget = QSvgWidget(self)
        self.update_board()
        layout.addWidget(self.svg_widget)

        self.setGeometry(100, 100, 600, 600)
        self.setWindowTitle("Chess UI")

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

        # Solicita uma análise para obter informações sobre a jogada sugerida
        info = self.engine.analyse(self.board, chess.engine.Limit(depth=20))

        # Imprime as informações
        print(f"Stockfish sugere: {result.move.uci()}")
        self.print_evaluation(info)
 

    def check_game_result(self):
        if self.board.is_checkmate():
            print("Xeque-mate! Você perdeu.")
            return True
        elif self.board.is_stalemate():
            print("Empate! O jogo terminou empatado.")
            return True
        elif self.board.is_insufficient_material():
            print("Empate! Material insuficiente para xeque-mate.")
            return True
        elif self.board.is_seventyfive_moves():
            print("Empate! O jogo atingiu o limite de 75 movimentos sem capturas ou movimentos de peões.")
            return True
        elif self.board.is_fivefold_repetition():
            print("Empate! A posição se repetiu pela quinta vez.")
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
    stockfish_path = "../../engines/stockfish/Stockfish/src/stockfish"

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