import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from scipy.interpolate import CubicSpline
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

plt.style.use('dark_background')

class MyHandler(FileSystemEventHandler):
    def __init__(self, score_file_path, depth_file_path, ax):
        super().__init__()
        self.score_file_path = score_file_path
        self.depth_file_path = depth_file_path
        self.ax = ax
        self.scores_data = []
        self.depths_data = []

    def on_modified(self, event):
        if event.src_path == self.score_file_path or event.src_path == self.depth_file_path:
            self.load_data()
            self.update_plot()

    def load_data(self):
        with open(self.score_file_path, 'r') as score_file:
            score_lines = score_file.read().splitlines()
            self.scores_data.clear()
            self.scores_data.extend([int(line) for line in score_lines])

        with open(self.depth_file_path, 'r') as depth_file:
            depth_lines = depth_file.read().splitlines()
            self.depths_data.clear()
            self.depths_data.extend([int(line) for line in depth_lines])

    def update_plot(self, frame):
        self.load_data()

        min_samples = min(len(self.scores_data), len(self.depths_data))
        x = np.arange(min_samples)
        y_scores = np.array(self.scores_data[:min_samples])
        y_depths = np.array(self.depths_data[:min_samples])

        spline_scores = CubicSpline(x, y_scores)
        spline_depths = np.poly1d(np.polyfit(x, y_depths, 1))  # Usando interpolação linear

        x_interp = np.linspace(0, min_samples - 1, 100)
        y_scores_interp = spline_scores(x_interp)
        y_depths_interp = spline_depths(x_interp)

        self.ax.clear()
        self.ax.plot(x_interp, y_scores_interp, linestyle='-', color='r', label='Scores')
        self.ax.set_xlabel('Amostra')
        self.ax.set_ylabel('Score')
        self.ax.legend()

        ax2 = self.ax.twinx()
        ax2.plot(x_interp, y_depths_interp, linestyle='-', color='b', label='Depth')
        ax2.set_ylabel('Profundidade')
        ax2.legend()

        self.ax.set_title('Curvas Suavizadas de Score e Profundidade')

def main(score_file_path, depth_file_path):
    fig, ax = plt.subplots(figsize=(12, 6))
    handler = MyHandler(score_file_path, depth_file_path, ax)
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
    score_file_path = '../evaluation.txt'
    depth_file_path = '../depth.txt'
    main(score_file_path, depth_file_path)
