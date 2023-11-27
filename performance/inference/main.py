"""
Autores: João Leonardi, Enzo e João Vinícius

Arquivo principal para execução do jogo de xadrez.
Para executar o jogo, basta executar o comando:
    python main.py
"""

import re
import os
import sys
import chess
import chess.svg
import chess.engine
import yaml
from chess.engine import PovScore

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtSvg import QSvgWidget

from utils.Utils import Common, Colors, Logger


class ChessUI(QMainWindow):
    """
    Classe que implementa a interface gráfica do jogo de xadrez.
    """
    SVG_FILENAME = 'board.svg'

    def __init__(self, engine_path: str, player_color: int, config: dict) -> None:
        """
        Construtor da classe.
        """
        super().__init__()

        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)

        engine_limit_config = config.get('engine_limit', {})
        self.engine.configure(config.get('engine_config', {}))
        self.engine_limit_config = chess.engine.Limit(**engine_limit_config)
        
        self.engine_path = engine_path
        self.board = chess.Board()
        self.player_color = player_color

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
        self.setWindowTitle('Volts ⚡')

        if self.player_color == 0:
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
        result = self.engine.play(self.board, self.engine_limit_config)
        self.board.push(result.move)
        self.update_board()

        info = self.engine.analyse(self.board, self.engine_limit_config)
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


        if 'pv' in info:
            principal_variation = info['pv']
            print(type(principal_variation))
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
    

def load_config(filename="config/config.yaml"):
    try:
        with open(filename, "r") as config_file:
            config = yaml.safe_load(config_file)
        return config
    except FileNotFoundError:
        print(f"Arquivo de configuração '{filename}' não encontrado.")
        return {}


if __name__ == "__main__":
    Common.authors()
    model_path = "/home/remix/wrkdir/my/ai.challenger/engines/Stockfish/src/stockfish"

    while True:
        player_number = input("Escolha a cor das peças 1(⚪) ou 0(⚫)   : ")
        
        if player_number.isdigit() and int(player_number) in [0, 1]:
            break

        print("Opção inválida. Por favor, escolha entre 0 (⚫) e 1 (⚪).")

    config_filename = "config/config.yaml"
    config = load_config(config_filename)
    print(f"Carregando configurações do arquivo '{config}'...")


    app = QApplication(sys.argv)
    chess_ui = ChessUI(model_path, player_number, config)
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
