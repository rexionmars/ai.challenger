import chess
import chess.svg

def exibir_tabuleiro(tabuleiro):
    # Exibe o tabuleiro em formato SVG
    svg = chess.svg.board(board=tabuleiro)
    with open("tabuleiro.svg", "w") as f:
        f.write(svg)

def main():
    # Inicializa o tabuleiro
    tabuleiro = chess.Board()

    # Exibe o tabuleiro inicial
    exibir_tabuleiro(tabuleiro)

    # Realiza alguns movimentos de exemplo
    movimentos = ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "O-O", "Nxe4", "d4", "exd4", "Re1", "f5", "Nxd4"]
    for movimento in movimentos:
        tabuleiro.push_uci(movimento)
        exibir_tabuleiro(tabuleiro)

if __name__ == "__main__":
    main()
