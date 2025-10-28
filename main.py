# ************************************
# 🐍 Jeu Snake en Python - par Fouad
# ************************************

from tkinter import *
import random

# ====== Paramètres du jeu ======
GAME_WIDTH = 500
GAME_HEIGHT = 500
SPEED = 120          # vitesse du jeu (plus grand = plus lent)
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


# ====== Classe Snake ======
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)


# ====== Classe Food ======
class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food"
        )


# ====== Fonction principale (tour suivant) ======
def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
    )
    snake.squares.insert(0, square)

    # Si le serpent mange la nourriture
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food()
    else:
        # Supprimer la dernière partie de la queue
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


# ====== Changer la direction ======
def change_direction(new_direction):
    global direction

    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction


# ====== Vérifier les collisions ======
def check_collisions(snake):
    x, y = snake.coordinates[0]

    # Collision avec les murs
    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    # Collision avec soi-même
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


# ====== Redémarrer le jeu ======
def restart_game():
    global snake, food, score, direction

    canvas.delete(ALL)
    score = 0
    direction = "down"
    label.config(text=f"Score: {score}")

    snake = Snake()
    food = Food()
    next_turn(snake, food)


# ====== Fin du jeu ======
def game_over():
    canvas.delete(ALL)

    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2 - 50,
        font=("consolas", 60),
        text="GAME OVER",
        fill="red",
        tag="gameover",
    )

    # Créer un bouton "Restart"
    restart_button = Button(
        window,
        text="🔁 Restart",
        font=("consolas", 24),
        bg="#333333",
        fg="white",
        command=restart_game,
    )
    restart_button_window = canvas.create_window(
        GAME_WIDTH / 2, GAME_HEIGHT / 2 + 50, window=restart_button
    )


# ====== Configuration de la fenêtre ======
window = Tk()
window.title("🐍 Snake Game by Fouad")
window.resizable(False, False)

score = 0
direction = "down"

label = Label(window, text=f"Score: {score}", font=("consolas", 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

# Centrer la fenêtre sur l'écran
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Lier les flèches du clavier
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

# ====== Lancer le jeu ======
snake = Snake()
food = Food()
next_turn(snake, food)

window.mainloop()
