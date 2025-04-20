from tkinter import *
import random
import psycopg2  # Import psycopg2 for PostgreSQL connection

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="snake_db",  # Change this to your database name
    user="postgres",
    password="lolpopqwerty",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Game configuration
GAME_WIDTH = 800
GAME_HEIGHT = 700
SPACE_SIZE = 30
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLORS = {"small": "#FF0000", "medium": "#FFFF00", "large": "#00FFFF"}
BACKGROUND_COLOR = "#000000"

# Initialize level and score
LEVEL = 1
SCORE = 0
SPEED = 200

# Prompt user for username
USERNAME = input("Enter your username: ")

# Check if user exists or create a new user
def get_or_create_user(username):
    global LEVEL, SCORE
    cur.execute("""
        SELECT "user".id AS user_id, user_score.level, user_score.score
        FROM user_score
        JOIN "user" ON user_score.user_id = "user".id
        WHERE "user".username = %s
    """, (username,))
    result = cur.fetchone()
    if result:
        user_id, LEVEL, SCORE = result
        print(f"Welcome back, {username}! Level: {LEVEL}, Score: {SCORE}")
        return user_id
    else:
        cur.execute("INSERT INTO \"user\" (username) VALUES (%s) RETURNING id", (username,))
        user_id = cur.fetchone()[0]
        cur.execute("INSERT INTO user_score (user_id, level, score) VALUES (%s, %s, %s)", (user_id, LEVEL, SCORE))
        conn.commit()
        print(f"New user created: {username}")
        return user_id

# Save game state to the database
def save_game(user_id, score, level):
    cur.execute("UPDATE user_score SET score = %s, level = %s WHERE user_id = %s", (score, level, user_id))
    conn.commit()
    print("Game state saved!")

# Initialize user
user_id = get_or_create_user(USERNAME)

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        self.spawn_food()

    def spawn_food(self):
        while True:
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
            if [x, y] not in snake.coordinates:
                break
        
        self.coordinates = [x, y]
        self.type = random.choices(["small", "medium", "large"], weights=[70, 20, 10])[0]
        self.value = {"small": 1, "medium": 3, "large": 5}[self.type]
        canvas.delete("food")
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLORS[self.type], tag="food")
        self.food_timer = window.after(random.randint(5000, 8000), self.despawn_food)

    def despawn_food(self):
        canvas.delete("food")
        self.spawn_food()

def next_turn(snake, food):
    global SCORE, SPEED, LEVEL

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
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        SCORE += food.value
        label_score.config(text=f"Score: {SCORE}")
        if SCORE % 5 == 0:
            LEVEL += 1
            SPEED -= 20  # Increase speed
            label_level.config(text=f"Level: {LEVEL}")
        window.after_cancel(food.food_timer)
        food.spawn_food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        font=('consolas', 70),
        text="Ti proigral :(",
        fill="red",
        tag="gameover"
    )
    save_game(user_id, SCORE, LEVEL)  # Save the game state when the game is over

def pause_game():
    save_game(user_id, SCORE, LEVEL)
    print("Game paused and state saved!")

window = Tk()
window.title("Igra Zmeya")
window.resizable(False, False)
label_score = Label(window, text=f"Score: {SCORE}", font=('consolas', 20))
label_score.pack()
label_level = Label(window, text=f"Level: {LEVEL}", font=('consolas', 20))
label_level.pack()
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<p>', lambda event: pause_game())  # Press 'P' to pause and save the game
snake = Snake()
food = Food()
direction = 'down'
next_turn(snake, food)
window.mainloop()

# Close the database connection when the game ends
cur.close()
conn.close()