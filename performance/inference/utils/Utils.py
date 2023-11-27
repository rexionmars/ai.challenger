class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    ORANGE = '\033[38;5;208m'


class Common:
    def writelnc(text: str, color: str) -> None:
        """
        Esta função escreve uma linha de texto com a cor especificada.

        Args:
            text (str): Texto a ser escrito.
            color (str): Cor do texto.
        Returns:
            None
        """
        print(f'{color}{text}{Colors.RESET}')
    
    def authors() -> None:
        print(f'Autores:{Colors.ORANGE}\n\tjoao_leonardi.melo@somosicev.com\n\tjoao_vinicius.carvalho@somosicev.com\n\tenzo.goncalves@somosicev.com{Colors.RESET}')

class Logger:
    def __init__(self) -> None:
        pass