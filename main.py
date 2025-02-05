import tkinter as Snake
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.resizable(False, False)

        self.canvas = Snake.Canvas(root, width=600, height=400, bg="black")
        self.canvas.pack()

        self.snake = [(20, 20), (20, 30), (20, 40)]
        self.snake_direction = "Down"
        self.food = self.create_food()

        self.root.bind("<KeyPress>", self.change_direction)
        self.update_snake()

    def create_food(self):
        x = random.randint(0, 29) * 20
        y = random.randint(0, 19) * 20
        return (x, y)

    def change_direction(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            self.snake_direction = event.keysym

    def update_snake(self):
        head_x, head_y = self.snake[-1]

        if self.snake_direction == "Up":
            new_head = (head_x, head_y - 20)
        elif self.snake_direction == "Down":
            new_head = (head_x, head_y + 20)
        elif self.snake_direction == "Left":
            new_head = (head_x - 20, head_y)
        elif self.snake_direction == "Right":
            new_head = (head_x + 20, head_y)

        self.snake.append(new_head)

        if new_head == self.food:
            self.food = self.create_food()
        else:
            self.snake.pop(0)

        if self.check_collision():
            self.game_over()
        else:
            self.draw_elements()
            self.root.after(100, self.update_snake)

    def check_collision(self):
        head_x, head_y = self.snake[-1]
        if head_x < 0 or head_x >= 600 or head_y < 0 or head_y >= 400:
            return True
        if len(self.snake) != len(set(self.snake)):
            return True
        return False

    def draw_elements(self):
        self.canvas.delete(Snake.ALL)
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="green")
        food_x, food_y = self.food
        self.canvas.create_rectangle(food_x, food_y, food_x + 20, food_y + 20, fill="red")

    def game_over(self):
        self.canvas.create_text(300, 200, text="Game Over", fill="white", font=("Helvetica", 24))
        self.root.bind("<Return>", self.restart_game)
        self.root.bind("<Escape>", self.terminate_game)

    def restart_game(self, event):
        self.canvas.delete(Snake.ALL)
        self.snake = [(20, 20), (20, 30), (20, 40)]
        self.snake_direction = "Down"
        self.food = self.create_food()
        self.root.bind("<KeyPress>", self.change_direction)
        self.update_snake()

    def terminate_game(self, event):
        self.root.quit()

def center_window(root, width=400, height=300):
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate coordinates to center the window
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set window geometry
    root.geometry(f"{width}x{height}+{x}+{y}")

def animate_label(label, colors, index=0):
    # Change the text color periodically
    label.config(fg=colors[index])
    next_index = (index + 1) % len(colors)
    label.after(200, animate_label, label, colors, next_index)

def show_intro():
    frame = Snake.Frame(window, bd=5)
    frame.pack(expand=True, fill=Snake.BOTH, padx=10, pady=10)

    bg_image = Snake.PhotoImage(file="gioco.gif")
    bg_label = Snake.Label(frame, image=bg_image)
    bg_label.image = bg_image  # Keep a reference to avoid garbage collection
    bg_label.pack(expand=True, fill=Snake.BOTH)

    label = Snake.Label(frame, text="Snake", font=("Helvetica", 96), bg="black", fg="white")  # Doubled font size
    label.place(relx=0.5, rely=0.5, anchor=Snake.CENTER)  # Center the text label

    colors = ["white", "red", "green", "blue", "yellow"]
    animate_label(label, colors)

    window.after(3000, frame.destroy)  # Close the intro frame after 10 seconds

def clear_window():
    for widget in window.winfo_children():
        widget.destroy()

def on_key_press(event):
    clear_window()
    window.geometry("600x400")
    game = SnakeGame(window)

window = Snake.Tk()
window.title("Snake")
window.geometry("600x200")
center_window(window, 600, 600)
show_intro()

message_label = Snake.Label(window, text="Premi un tasto...", font=("Helvetica", 16))
message_label.pack(pady=20)

window.bind("<Key>", on_key_press)

if __name__ == "__main__":
    window.mainloop()