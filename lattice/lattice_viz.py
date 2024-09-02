import tkinter as tk


class GridApp:
    def __init__(self, grid=None):
        self.root = tk.Tk()
        self.root.title("8x8 Grid Visualization")
        self.root.geometry("400x400")

        self.bg_grid = initial_grid = [
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0]
        ]

        # Create a canvas widget
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        # Define the size of each cell in the grid
        self.cell_size = 50

        # Initialize the grid if not provided
        self.grid = grid if grid else [[0 for _ in range(8)] for _ in range(8)]

        # Draw the initial grid
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")  # Clear the canvas before redrawing
        for i in range(8):
            for j in range(8):
                if self.grid[i][j] == 1:
                    color = "black"  
                elif self.bg_grid[i][j] == 1:
                    color = "gray" 
                else:
                    color = "white"
                self.canvas.create_rectangle(j * self.cell_size, i * self.cell_size,
                                             (j + 1) * self.cell_size, (i + 1) * self.cell_size,
                                             fill=color)

    def update_grid(self, new_grid):
        self.grid = new_grid
        self.draw_grid()
        self.root.update()


# Example of how to use the class in another function or module
if __name__ == "__main__":

    # Initialize the app with an initial grid
    initial_grid = [
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0]
    ]

    # Create an instance of the GridApp class
    app = GridApp(initial_grid)

