"""
Autores: João Leonardi, Enzo e João Vinícius

Arquivo principal para execução do jogo de xadrez.
Para executar o jogo, basta executar o comando:
    python main.py
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtSvg import QSvgWidget
import chess
import chess.svg
import chess.engine

from utils.Utils import Common, Colors, Logger


class ChessUI(QMainWindow):
    """
    Classe que implementa a interface gráfica do jogo de xadrez.
    """
    SVG_FILENAME = 'board.svg'
    ENGINE_CONFIG = {"Threads": 12, "Hash": 512}
    ENGINE_LIMIT = chess.engine.Limit(nodes=1000000, depth=50, time=5.0)

    def __init__(self, engine_path: str, player_color: str) -> None:
        """
        Construtor da classe.
        """
        super().__init__()

        self.engine_path = engine_path
        self.board = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.engine.configure(self.ENGINE_CONFIG)
        self.player_color = player_color.lower()

        self.init_ui()

    def init_ui(self) -> None:
        """
        Inicializa a interface gráfica.
        """
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.svg_widget = QSvgWidget(self)
        self.update_board()
        layout.addWidget(self.svg_widget)

        self.setGeometry(100, 100, 600, 600)
        self.setWindowTitle('Chess UI')

        if self.player_color == "pretas":
            self.suggest_move()

    def update_board(self) -> None:
        """
        Atualiza o tabuleiro de xadrez.
        """
        svg_data = chess.svg.board(self.board)
        with open(self.SVG_FILENAME, 'w') as svg_file:
            svg_file.write(svg_data)

        self.svg_widget.load(self.SVG_FILENAME)
        self.svg_widget.show()

    def suggest_move(self) -> None:
        """
        Sugere uma jogada para o jogador.
        """
        result = self.engine.play(self.board, self.ENGINE_LIMIT)
        self.board.push(result.move)
        self.update_board()

        info = self.engine.analyse(self.board, self.ENGINE_LIMIT)
        self.print_evaluation(info)

    def check_game_result(self) -> bool:
        """
        Verifica se o jogo terminou.
        """
        if self.board.is_checkmate():
            print("Xeque-mate! Você perdeu 💔😢")
            return True
        elif self.board.is_stalemate():
            print("Empate! O jogo terminou empatado 🤝😐")
            return True
        elif self.board.is_insufficient_material():
            print("Empate! Material insuficiente para xeque-mate 🤝😐")
            return True
        elif self.board.is_seventyfive_moves():
            print("Empate! O jogo atingiu o limite de 75 movimentos sem capturas ou movimentos de peões 🤝😐")
            return True
        elif self.board.is_fivefold_repetition():
            print("Empate! A posição se repetiu pela quinta vez 🤝😐")
            return True
        return False

    def print_evaluation(self, info: dict) -> None:
        """
        Imprime a avaliação da jogada sugerida pelo motor de xadrez.
        
        """
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
    Common.authors()
    model_path = ""

    while True:
        player_color = input("Escolha a cor das peças (brancas/pretas): ").lower()
        if player_color in ["brancas", "pretas"]:
            break
        else:
            print("Opção inválida Por favor, escolha entre 'brancas' e 'pretas'.")

    app = QApplication(sys.argv)
    chess_ui = ChessUI(model_path, player_color)
    chess_ui.show()

    while True:
        user_move = input(f"{Colors.ORANGE}😈 PoST: {Colors.RESET}")
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

    chess_ui.engine.quit()
    sys.exit(app.exec_())
