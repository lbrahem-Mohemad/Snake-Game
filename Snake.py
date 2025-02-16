import tkinter as tk 
from collections import deque
import random

grid_size = 20
cell_size = 20
grid_width = 20
grid_height = 20

directions = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1)
}

class SnakeGame:

    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game with Bfs %%%")
       self.frame = tk.Frame(self.master, bg="blue")

        self.frame.pack(padx=10, pady=10)
        # Add a score label
        self.score = 0
        self.score_label = tk.Label(
            self.frame, text=f"Score: {self.score}", font=("Arial", 16), bg="darkgray", fg="white"
    )
       
        self.score_label.pack(pady=5)
        self.canvas = tk.Canvas(
            self.frame, width=grid_width * cell_size, height=grid_height * cell_size, bg="black"
        )
        self.canvas.pack()
        self.snake = [(5, 5)] 
        self.food = self.generate_food()
        self.direction = "RIGHT"
        self.running = True
        self.update_game()
    def generate_food(self):
        while True:
            food = (random.randint(0, grid_height - 1), random.randint(0, grid_width - 1))
        
            if food not in self.snake:
                return food

    def bfs(self, start, target): 
        queue = deque([(start, [])]) 
        visited = set() 
        while queue:  
            current, path = queue.popleft()  

             if current in visited:
                continue
                     visited.add(current)
            if current == target:  
                return path

            for dir_name, (dx, dy) in directions.items():
                new_pos = (current[0] + dx, current[1] + dy)
                if (
                    0 <= new_pos[0] < grid_height  
                    and 0 <= new_pos[1] < grid_width
                    and new_pos not in visited
                    and new_pos not in self.snake 
                ):
                    queue.append((new_pos, path + [dir_name]))  

        return []  # No path found

    def update_game(self):
        if not self.running: 
            return
        path = self.bfs(self.snake[0], self.food)
        if path:
            self.direction = path[0]
        dx, dy = directions[self.direction]
        new_head = (self.snake[0][0] + dx, self.snake[0][1] + dy)

        if (
            new_head in self.snake
            
      
            or new_head[0] < 0
           
            or new_head[1] < 0
            
            or new_head[0] >= grid_height
           
            or new_head[1] >= grid_width
        ):
            self.running = False
            self.canvas.create_text(
                grid_width * cell_size // 2,
                grid_height * cell_size // 2,
                text="loss!",
                fill="purple",
                font=("Arial", 24)
            )
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.food = self.generate_food()
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
        else:
            self.snake.pop()
        self.render()
        self.master.after(100, self.update_game)

    def render(self):

        self.canvas.delete("all")
        food_x, food_y = self.food
    
        self.canvas.create_rectangle(
            food_y * cell_size,
            food_x * cell_size,
            (food_y + 1) * cell_size,
            (food_x + 1) * cell_size,
            fill="red"
        )
        for x, y in self.snake:
            
            self.canvas.create_rectangle(
                y * cell_size,
                x * cell_size,
                (y + 1) * cell_size,
                (x + 1) * cell_size,
                fill="green"
            )
if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()