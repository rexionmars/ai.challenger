import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def __init__(self, file_path, ax):
        super().__init__()
        self.file_path = file_path
        self.ax = ax
        self.data = []

    def on_modified(self, event):
        if event.src_path == self.file_path:
            self.load_data()
            self.update_plot()

    def load_data(self):
        with open(self.file_path, 'r') as file:
            lines = file.read().splitlines()
            self.data = [int(line) for line in lines]

    def update_plot(self, frame):
        self.load_data()
        self.ax.clear()
        self.ax.plot(self.data[::-1], marker='o', linestyle='-', color='b')  # Invertendo os valores
        self.ax.set_xlabel('Amostra')
        self.ax.set_ylabel('Valor')
        self.ax.set_title('Relação Inversa: Menos Valor, Mais Chances de Perder')

def main(file_path):
    fig, ax = plt.subplots()
    handler = MyHandler(file_path, ax)
    observer = Observer()
    observer.schedule(handler, path='.', recursive=False)
    observer.start()

    ani = FuncAnimation(fig, handler.update_plot, blit=False, interval=1000)

    plt.show()

    try:
        while True:
            plt.pause(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    file_path = '../evaluation.txt'
    main(file_path)
