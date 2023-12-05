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
import threading
import time
import atexit

from chess.engine import PovScore

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtSvg import QSvgWidget

from utils.Utils import Common, Colors, Logger


class ChessUI(QMainWindow):
    SVG_FILENAME = 'board.svg'
    SCORES_FILENAME = 'evaluation.txt'
    DEPTHS_FILENAME = 'depth.txt'

    def __init__(self, engine_path: str, player_color: int, config: dict) -> None:
        super().__init__()

        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)

        engine_limit_config = config.get('engine_limit', {})
        self.engine.configure(config.get('engine_config', {}))
        self.engine_limit_config = chess.engine.Limit(**engine_limit_config)

        self.engine_path = engine_path
        self.board = chess.Board()
        self.player_color = player_color
        self.scores_history = []
        self.depths_history = []

        atexit.register(self.cleanup)

        self.init_ui()

    def cleanup(self):
        """
        Limpa o conteúdo do arquivo de avaliações ao encerrar o programa.
        """
        with open(self.SCORES_FILENAME, 'w') as file:
            file.write('')

        with open(self.DEPTHS_FILENAME, 'w') as file:
            file.write('')

    def init_ui(self) -> None:
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.svg_widget = QSvgWidget(self)
        self.update_board()
        layout.addWidget(self.svg_widget)

        self.setGeometry(100, 100, 600, 600)
        self.setWindowTitle('Volts ⚡️')

        if self.player_color == 0:
            self.suggest_move()

    def update_board(self) -> None:
        svg_data = chess.svg.board(self.board)
        with open(self.SVG_FILENAME, 'w') as svg_file:
            svg_file.write(svg_data)

        self.svg_widget.load(self.SVG_FILENAME)
        self.svg_widget.show()

    def suggest_move(self) -> None:
        result = self.engine.play(self.board, self.engine_limit_config)
        print(f"{Colors.RED}[ENGINE {result.move}]{Colors.RESET}")
        self.board.push(result.move)
        self.update_board()

        info = self.engine.analyse(self.board, self.engine_limit_config)
        score_value = self.get_score_value(info)
        if score_value is not None:
            self.scores_history.append(score_value)
            with open(self.SCORES_FILENAME, 'a') as file:
                file.write(str(score_value) + '\n')

        self.print_evaluation(info)

    def check_game_result(self) -> bool:
        if self.board.is_checkmate():
            # Se for a vez das brancas jogar, e estivermos com as brancas, perdemos
            if self.board.turn and self.player_color == 0:
                print("Xeque-mate! Fomos de Americanas 💔️😭️")
                return True
            # Se for a vez das pretas jogar, e estivermos com as pretas, perdemos
            elif not self.board.turn and self.player_color == 1:
                print("Xeque-mate! FAZ O L 💔️😭️")
                return True
            else:
                print("Xeque-mate! TACA O PAU 🏆️🎉️")
                return True
        elif self.board.is_stalemate():
            print("Empate! O jogo terminou empatado 🤝️😐️")
            return True
        elif self.board.is_insufficient_material():
            print("Empate! Material insuficiente para xeque-mate 🤝️🫥️")
            return True
        elif self.board.is_seventyfive_moves():
            print("Empate! O jogo atingiu o limite de 75 movimentos sem capturas ou movimentos de peões 🤝️🫠️")
            return True
        elif self.board.is_fivefold_repetition():
            print("Empate! A posição se repetiu pela quinta vez 🤝️🤨️")
            return True
        return False

    def print_evaluation(self, info: dict) -> None:
        if 'score' in info and isinstance(info['score'], PovScore):
            score_text = str(info['score'])
            match = re.search(r'\((-?\d+)\)', score_text)

            if match:
                score_value = int(match.group(1))
                print(f"Avaliação: {score_value}")
                self.scores_history.append(score_value)
            else:
                print("Avaliação não disponível.")
        else:
            print("Avaliação não disponível.")

        if 'pv' in info:
            print(f"Variação Principal: {info['pv']}")
        else:
            print("Variação Principal não disponível.")

        if 'depth' in info:
            depth_value = info['depth']
            print(f"Profundidade: {depth_value}")
            self.depths_history.append(depth_value)

            with open('depth.txt', 'a') as depth_file:
                depth_file.write(f"{depth_value}\n")
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

    def get_score_value(self, info):
        if 'score' in info and isinstance(info['score'], PovScore):
            score_text = str(info['score'])
            match = re.search(r'\((-?\d+)\)', score_text)

            if match:
                return int(match.group(1))
        return None


def load_config(filename="config/config.yaml"):
    try:
        with open(filename, "r") as config_file:
            config = yaml.safe_load(config_file)
        return config
    except FileNotFoundError:
        print(f"Arquivo de configuração '{filename}' não encontrado.")
        return {}


def validate_input_from_re(user_input: str) -> bool:
    # Define um padrão regex para validar a entrada no formato "d7c7".
    padrao_regex = re.compile(r'^[a-h][1-8][a-h][1-8]$')

    # Verifica se a entrada corresponde ao padrão.
    if padrao_regex.match(user_input):
        return True
    else:
        print("Formato inválido. Digite no formato correto, por exemplo, 'd7c7'.")
        return False


def play_chess(chess_ui):
    while True:
        user_move = input(f"{Colors.ORANGE}👿️ PoST: {Colors.RESET}")
        if not validate_input_from_re(user_move):
            # Se a entrada for inválida, pule para a próxima iteração do loop.
            continue

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


def wait_for_opponent_move(chess_ui):
    while True:
        opponent_move = input(f"{Colors.BLUE}🤖 Oponente: {Colors.RESET}")
        if validate_input_from_re(opponent_move):
            if chess.Move.from_uci(opponent_move) in chess_ui.board.legal_moves:
                chess_ui.board.push(chess.Move.from_uci(opponent_move))
                chess_ui.update_board()
                break
            else:
                print("Jogada do oponente inválida. Tente novamente.")


def main():
    Common.authors()
    model_path = "C:\GitHub\stockfish\stockfish.exe"

    while True:
        player_color_input = input("Escolha a cor das peças 0 (Brancas) ou 1 (Pretas): ")
        if player_color_input.isdigit() and int(player_color_input) in [0, 1]:
            break
        print("Opção inválida. Por favor, escolha entre 0 (Brancas) ou 1 (Pretas).")

    player_color = int(player_color_input)

    config_filename = "config/config.yaml"
    config = load_config(config_filename)

    app = QApplication(sys.argv)
    chess_ui = ChessUI(model_path, player_color, config)
    chess_ui.show()

    if player_color == 0:
        play_chess(chess_ui)
    else:
        wait_for_opponent_move(chess_ui)
        chess_ui.suggest_move()
        play_chess(chess_ui)

    chess_ui.engine.quit()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
