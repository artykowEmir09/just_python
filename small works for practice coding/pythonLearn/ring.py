import tkinter as tk
import random
import math
import time

# ============================================================
# PYTHON BOXING SIMULATOR
# Advanced Tkinter Version
# ============================================================

WIDTH = 1200
HEIGHT = 750

RING_LEFT = 180
RING_RIGHT = 1020
RING_TOP = 220
RING_BOTTOM = 590

FPS = 30
FRAME_MS = 1000 // FPS

ROUND_TIME = 60

random.seed()


# ============================================================
# WINDOW
# ============================================================

root = tk.Tk()
root.title("Python Boxing Simulator")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="#090b12",
    highlightthickness=0
)

canvas.pack()


# ============================================================
# GAME STATE
# ============================================================

game_running = True
round_number = 1
round_time = ROUND_TIME

last_time = time.time()

keys = set()

particles = []


# ============================================================
# KEYBOARD
# ============================================================

def key_down(event):
    keys.add(event.keysym.lower())


def key_up(event):
    keys.discard(event.keysym.lower())


root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)


# ============================================================
# BACKGROUND
# ============================================================

def create_background():

    # Background
    canvas.create_rectangle(
        0,
        0,
        WIDTH,
        HEIGHT,
        fill="#080a10",
        outline=""
    )

    # Ceiling lights
    for x in range(100, WIDTH, 120):

        canvas.create_oval(
            x,
            60,
            x + 15,
            75,
            fill="#d8d8c0",
            outline=""
        )

        canvas.create_line(
            x + 7,
            75,
            x + 7,
            160,
            fill="#333641",
            width=2
        )

    # Crowd
    for _ in range(180):

        x = random.randint(20, WIDTH - 20)
        y = random.randint(100, 205)

        radius = random.randint(3, 8)

        color = random.choice([
            "#252833",
            "#30333e",
            "#3a3d48",
            "#20232c"
        ])

        canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill=color,
            outline=""
        )

    # Arena wall
    canvas.create_rectangle(
        0,
        180,
        WIDTH,
        220,
        fill="#11141c",
        outline=""
    )

    canvas.create_text(
        WIDTH / 2,
        110,
        text="PYTHON BOXING CHAMPIONSHIP",
        fill="#eeeeee",
        font=("Arial", 26, "bold")
    )

    canvas.create_text(
        WIDTH / 2,
        145,
        text="PLAYER  vs  CPU",
        fill="#777d8e",
        font=("Arial", 12)
    )


# ============================================================
# RING
# ============================================================

def create_ring():

    # Ring floor
    canvas.create_rectangle(
        RING_LEFT,
        RING_TOP,
        RING_RIGHT,
        RING_BOTTOM,
        fill="#20232c",
        outline="#777b88",
        width=4
    )

    # Mat lines
    for y in range(RING_TOP + 40, RING_BOTTOM, 45):

        canvas.create_line(
            RING_LEFT,
            y,
            RING_RIGHT,
            y,
            fill="#2d3039"
        )

    # Corner posts
    corners = [
        (RING_LEFT, RING_TOP),
        (RING_RIGHT, RING_TOP),
        (RING_LEFT, RING_BOTTOM),
        (RING_RIGHT, RING_BOTTOM)
    ]

    for x, y in corners:

        canvas.create_rectangle(
            x - 10,
            y - 10,
            x + 10,
            y + 10,
            fill="#555963",
            outline=""
        )

    # Ropes
    rope_colors = [
        "#d7d7d7",
        "#a9abb3",
        "#777a84"
    ]

    for i, y in enumerate([290, 335, 380]):

        canvas.create_line(
            RING_LEFT,
            y,
            RING_RIGHT,
            y,
            fill=rope_colors[i],
            width=5
        )

    # Ring apron
    canvas.create_rectangle(
        RING_LEFT - 20,
        RING_BOTTOM,
        RING_RIGHT + 20,
        RING_BOTTOM + 25,
        fill="#12151c",
        outline=""
    )

    canvas.create_text(
        WIDTH / 2,
        RING_BOTTOM + 13,
        text="BOXING ARENA",
        fill="#555966",
        font=("Arial", 9, "bold")
    )


# ============================================================
# FIGHTER CLASS
# ============================================================

class Fighter:

    def __init__(self, x, y, name, body_color, glove_color):

        self.x = x
        self.y = y

        self.name = name

        self.body_color = body_color
        self.glove_color = glove_color

        self.health = 100
        self.stamina = 100

        self.width = 55
        self.height = 125

        self.direction = 1

        self.speed = 6

        self.blocking = False

        self.attack = None
        self.attack_timer = 0

        self.hit_flash = 0

        self.knocked_down = False
        self.knockdown_timer = 0

        self.score = 0

        self.objects = []

        self.create_graphics()


    # ========================================================
    # GRAPHICS
    # ========================================================

    def create_graphics(self):

        # Shadow
        self.shadow = canvas.create_oval(
            self.x - 35,
            self.y + 105,
            self.x + 35,
            self.y + 118,
            fill="#101117",
            outline=""
        )

        # Head
        self.head = canvas.create_oval(
            self.x - 18,
            self.y - 55,
            self.x + 18,
            self.y - 19,
            fill="#d89d78",
            outline="#0b0d12",
            width=2
        )

        # Hair
        self.hair = canvas.create_arc(
            self.x - 18,
            self.y - 60,
            self.x + 18,
            self.y - 25,
            start=0,
            extent=180,
            fill="#17130f",
            outline=""
        )

        # Body
        self.body = canvas.create_polygon(
            self.x - 24,
            self.y - 20,
            self.x + 24,
            self.y - 20,
            self.x + 28,
            self.y + 45,
            self.x - 28,
            self.y + 45,
            fill=self.body_color,
            outline="#090a0e",
            width=2
        )

        # Left arm
        self.left_arm = canvas.create_line(
            self.x - 20,
            self.y - 10,
            self.x - 48,
            self.y + 28,
            fill=self.body_color,
            width=12
        )

        # Right arm
        self.right_arm = canvas.create_line(
            self.x + 20,
            self.y - 10,
            self.x + 48,
            self.y + 28,
            fill=self.body_color,
            width=12
        )

        # Gloves
        self.left_glove = canvas.create_oval(
            self.x - 58,
            self.y + 22,
            self.x - 40,
            self.y + 40,
            fill=self.glove_color,
            outline="#08090d"
        )

        self.right_glove = canvas.create_oval(
            self.x + 40,
            self.y + 22,
            self.x + 58,
            self.y + 40,
            fill=self.glove_color,
            outline="#08090d"
        )

        # Shorts
        self.shorts = canvas.create_rectangle(
            self.x - 27,
            self.y + 42,
            self.x + 27,
            self.y + 67,
            fill="#11141c",
            outline="#08090d"
        )

        # Legs
        self.left_leg = canvas.create_line(
            self.x - 13,
            self.y + 65,
            self.x - 22,
            self.y + 110,
            fill="#d89d78",
            width=13
        )

        self.right_leg = canvas.create_line(
            self.x + 13,
            self.y + 65,
            self.x + 22,
            self.y + 110,
            fill="#d89d78",
            width=13
        )

        self.objects = [
            self.head,
            self.hair,
            self.body,
            self.left_arm,
            self.right_arm,
            self.left_glove,
            self.right_glove,
            self.shorts,
            self.left_leg,
            self.right_leg
        ]


    # ========================================================
    # POSITION
    # ========================================================

    def move(self, dx):

        if self.knocked_down:
            return

        self.x += dx

        min_x = RING_LEFT + 60
        max_x = RING_RIGHT - 60

        self.x = max(min_x, min(max_x, self.x))

        self.update_position()


    # ========================================================
    # UPDATE GRAPHICS
    # ========================================================

    def update_position(self):

        x = self.x
        y = self.y

        # Head
        canvas.coords(
            self.head,
            x - 18,
            y - 55,
            x + 18,
            y - 19
        )

        canvas.coords(
            self.hair,
            x - 18,
            y - 60,
            x + 18,
            y - 25
        )

        # Body
        canvas.coords(
            self.body,
            x - 24,
            y - 20,
            x + 24,
            y - 20,
            x + 28,
            y + 45,
            x - 28,
            y + 45
        )

        # Normal arms
        left_x = x - 48
        right_x = x + 48

        if self.attack == "jab":

            if self.direction == 1:
                right_x = x + 95
            else:
                left_x = x - 95

        elif self.attack == "cross":

            if self.direction == 1:
                left_x = x + 80
            else:
                right_x = x - 80

        if self.blocking:

            canvas.coords(
                self.left_arm,
                x - 20,
                y - 5,
                x - 25,
                y - 45
            )

            canvas.coords(
                self.right_arm,
                x + 20,
                y - 5,
                x + 25,
                y - 45
            )

        else:

            canvas.coords(
                self.left_arm,
                x - 20,
                y - 10,
                left_x,
                y + 28
            )

            canvas.coords(
                self.right_arm,
                x + 20,
                y - 10,
                right_x,
                y + 28
            )

        # Gloves
        canvas.coords(
            self.left_glove,
            left_x - 10,
            y + 20,
            left_x + 8,
            y + 38
        )

        canvas.coords(
            self.right_glove,
            right_x - 8,
            y + 20,
            right_x + 10,
            y + 38
        )

        # Shorts
        canvas.coords(
            self.shorts,
            x - 27,
            y + 42,
            x + 27,
            y + 67
        )

        # Legs
        canvas.coords(
            self.left_leg,
            x - 13,
            y + 65,
            x - 22,
            y + 110
        )

        canvas.coords(
            self.right_leg,
            x + 13,
            y + 65,
            x + 22,
            y + 110
        )

        canvas.coords(
            self.shadow,
            x - 35,
            y + 105,
            x + 35,
            y + 118
        )


    # ========================================================
    # ATTACK
    # ========================================================

    def punch(self, punch_type):

        if self.knocked_down:
            return

        if self.attack is not None:
            return

        if self.stamina < 15:
            return

        self.attack = punch_type

        self.attack_timer = 8

        if punch_type == "jab":
            self.stamina -= 12
        else:
            self.stamina -= 20

        self.update_position()


    # ========================================================
    # BLOCK
    # ========================================================

    def set_block(self, state):

        if self.knocked_down:
            self.blocking = False
        else:
            self.blocking = state

        self.update_position()


    # ========================================================
    # DAMAGE
    # ========================================================

    def take_damage(self, amount):

        if self.knocked_down:
            return

        if self.blocking:

            amount *= 0.25
            self.stamina -= 5

        self.health -= amount

        self.health = max(0, self.health)

        self.hit_flash = 4

        if self.health <= 0:

            self.knocked_down = True
            self.knockdown_timer = 100

            self.set_block(False)


    # ========================================================
    # UPDATE
    # ========================================================

    def update(self):

        if self.attack_timer > 0:

            self.attack_timer -= 1

            if self.attack_timer == 0:

                self.attack = None
                self.update_position()

        if self.hit_flash > 0:

            self.hit_flash -= 1

        if not self.knocked_down:

            self.stamina += 0.35
            self.stamina = min(100, self.stamina)


# ============================================================
# CREATE WORLD
# ============================================================

create_background()
create_ring()


# ============================================================
# FIGHTERS
# ============================================================

player = Fighter(
    430,
    475,
    "PLAYER",
    "#b52b35",
    "#e9e9e9"
)

cpu = Fighter(
    770,
    475,
    "CPU",
    "#285a9e",
    "#e9e9e9"
)

player.direction = 1
cpu.direction = -1


# ============================================================
# UI
# ============================================================

player_name = canvas.create_text(
    250,
    30,
    text="PLAYER",
    fill="#eeeeee",
    font=("Arial", 18, "bold")
)

cpu_name = canvas.create_text(
    950,
    30,
    text="CPU",
    fill="#eeeeee",
    font=("Arial", 18, "bold")
)


# Health bars

canvas.create_rectangle(
    100,
    55,
    500,
    80,
    fill="#171a22",
    outline="#555965"
)

player_health_bar = canvas.create_rectangle(
    100,
    55,
    500,
    80,
    fill="#c72f3a",
    outline=""
)


canvas.create_rectangle(
    700,
    55,
    1100,
    80,
    fill="#171a22",
    outline="#555965"
)

cpu_health_bar = canvas.create_rectangle(
    700,
    55,
    1100,
    80,
    fill="#3478c5",
    outline=""
)


# Stamina

canvas.create_rectangle(
    100,
    88,
    500,
    98,
    fill="#171a22",
    outline=""
)

player_stamina_bar = canvas.create_rectangle(
    100,
    88,
    500,
    98,
    fill="#d5a832",
    outline=""
)


canvas.create_rectangle(
    700,
    88,
    1100,
    98,
    fill="#171a22",
    outline=""
)

cpu_stamina_bar = canvas.create_rectangle(
    700,
    88,
    1100,
    98,
    fill="#d5a832",
    outline=""
)


# Timer

timer_text = canvas.create_text(
    WIDTH / 2,
    65,
    text="1:00",
    fill="#ffffff",
    font=("Arial", 25, "bold")
)

round_text = canvas.create_text(
    WIDTH / 2,
    95,
    text="ROUND 1",
    fill="#777d8b",
    font=("Arial", 10, "bold")
)


# ============================================================
# PARTICLES
# ============================================================

def create_hit_particles(x, y):

    for _ in range(12):

        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 7)

        particle = canvas.create_oval(
            x - 3,
            y - 3,
            x + 3,
            y + 3,
            fill=random.choice([
                "#ffffff",
                "#ffd34d",
                "#ff6b6b"
            ]),
            outline=""
        )

        particles.append({
            "object": particle,
            "x": x,
            "y": y,
            "dx": math.cos(angle) * speed,
            "dy": math.sin(angle) * speed,
            "life": random.randint(10, 20)
        })


def update_particles():

    for particle in particles[:]:

        particle["x"] += particle["dx"]
        particle["y"] += particle["dy"]

        particle["dy"] += 0.25

        particle["life"] -= 1

        canvas.coords(
            particle["object"],
            particle["x"] - 3,
            particle["y"] - 3,
            particle["x"] + 3,
            particle["y"] + 3
        )

        if particle["life"] <= 0:

            canvas.delete(particle["object"])
            particles.remove(particle)


# ============================================================
# DISTANCE
# ============================================================

def distance_between(a, b):

    return abs(a.x - b.x)


# ============================================================
# ATTACK DETECTION
# ============================================================

def check_attack(attacker, defender):

    if attacker.attack is None:
        return

    if attacker.attack_timer != 4:
        return

    distance = distance_between(
        attacker,
        defender
    )

    if distance > 125:
        return

    if attacker.attack == "jab":

        damage = random.randint(5, 9)

    else:

        damage = random.randint(9, 15)

    old_health = defender.health

    defender.take_damage(damage)

    actual_damage = old_health - defender.health

    create_hit_particles(
        defender.x,
        defender.y - 10
    )

    defender.x += attacker.direction * 8

    defender.update_position()


# ============================================================
# PLAYER CONTROL
# ============================================================

def player_control():

    if player.knocked_down:
        return

    if "a" in keys:

        player.move(-player.speed)

    if "d" in keys:

        player.move(player.speed)

    if "w" in keys:

        player.punch("jab")

    if "s" in keys:

        player.punch("cross")

    if "space" in keys:

        player.set_block(True)

    else:

        player.set_block(False)


# ============================================================
# CPU AI
# ============================================================

ai_timer = 0
ai_action = None


def cpu_ai():

    global ai_timer, ai_action

    if cpu.knocked_down:
        return

    distance = distance_between(cpu, player)

    ai_timer -= 1

    if ai_timer > 0:
        return

    ai_timer = random.randint(8, 25)

    # Very far
    if distance > 220:

        if cpu.x > player.x:

            cpu.move(-cpu.speed)

        else:

            cpu.move(cpu.speed)

        return

    # Too close
    if distance < 80:

        if random.random() < 0.4:

            cpu.move(
                random.choice([-1, 1]) * cpu.speed
            )

        else:

            cpu.punch(
                random.choice([
                    "jab",
                    "cross"
                ])
            )

        return

    # Attack
    if distance < 150:

        decision = random.random()

        if decision < 0.55:

            cpu.punch("jab")

        elif decision < 0.8:

            cpu.punch("cross")

        else:

            cpu.set_block(True)

            root.after(
                random.randint(200, 500),
                lambda: cpu.set_block(False)
            )

        return

    # Approach
    if cpu.x > player.x:

        cpu.move(-cpu.speed)

    else:

        cpu.move(cpu.speed)


# ============================================================
# KEEP FIGHTERS APART
# ============================================================

def prevent_overlap():

    distance = distance_between(
        player,
        cpu
    )

    minimum_distance = 65

    if distance < minimum_distance:

        overlap = minimum_distance - distance

        if player.x < cpu.x:

            player.x -= overlap / 2
            cpu.x += overlap / 2

        else:

            player.x += overlap / 2
            cpu.x -= overlap / 2

        player.update_position()
        cpu.update_position()


# ============================================================
# UI UPDATE
# ============================================================

def update_ui():

    player_health_width = (
        400 * player.health / 100
    )

    cpu_health_width = (
        400 * cpu.health / 100
    )

    player_stamina_width = (
        400 * player.stamina / 100
    )

    cpu_stamina_width = (
        400 * cpu.stamina / 100
    )

    canvas.coords(
        player_health_bar,
        100,
        55,
        100 + player_health_width,
        80
    )

    canvas.coords(
        cpu_health_bar,
        1100 - cpu_health_width,
        55,
        1100,
        80
    )

    canvas.coords(
        player_stamina_bar,
        100,
        88,
        100 + player_stamina_width,
        98
    )

    canvas.coords(
        cpu_stamina_bar,
        1100 - cpu_stamina_width,
        88,
        1100,
        98
    )


# ============================================================
# TIMER
# ============================================================

def update_timer():

    global round_time

    if not game_running:
        return

    round_time -= 1 / FPS

    if round_time < 0:

        round_time = 0

    minutes = int(round_time) // 60
    seconds = int(round_time) % 60

    canvas.itemconfig(
        timer_text,
        text=f"{minutes}:{seconds:02d}"
    )

    if round_time <= 0:

        end_round()


# ============================================================
# ROUND END
# ============================================================

def end_round():

    global game_running

    game_running = False

    if player.health > cpu.health:

        winner = "PLAYER WINS!"

    elif cpu.health > player.health:

        winner = "CPU WINS!"

    else:

        winner = "DRAW!"

    canvas.create_rectangle(
        300,
        270,
        900,
        480,
        fill="#080a10",
        outline="#666a76",
        width=3
    )

    canvas.create_text(
        WIDTH / 2,
        330,
        text="FIGHT OVER",
        fill="#eeeeee",
        font=("Arial", 28, "bold")
    )

    canvas.create_text(
        WIDTH / 2,
        390,
        text=winner,
        fill="#ffd34d",
        font=("Arial", 36, "bold")
    )

    canvas.create_text(
        WIDTH / 2,
        435,
        text="Press R to restart",
        fill="#888d9b",
        font=("Arial", 14)
    )


# ============================================================
# KNOCKDOWN CHECK
# ============================================================

def check_knockdown():

    global game_running

    if player.knocked_down or cpu.knocked_down:

        game_running = False

        if player.knocked_down and cpu.knocked_down:

            winner = "DOUBLE KNOCKDOWN"

        elif player.knocked_down:

            winner = "CPU WINS!"

        else:

            winner = "PLAYER WINS!"

        canvas.create_rectangle(
            300,
            270,
            900,
            480,
            fill="#080a10",
            outline="#666a76",
            width=3
        )

        canvas.create_text(
            WIDTH / 2,
            330,
            text="KNOCKDOWN!",
            fill="#ff5b5b",
            font=("Arial", 32, "bold")
        )

        canvas.create_text(
            WIDTH / 2,
            390,
            text=winner,
            fill="#ffd34d",
            font=("Arial", 36, "bold")
        )

        canvas.create_text(
            WIDTH / 2,
            435,
            text="Press R to restart",
            fill="#888d9b",
            font=("Arial", 14)
        )


# ============================================================
# RESTART
# ============================================================

def restart_game():

    global game_running
    global round_time
    global round_number
    global ai_timer

    canvas.delete("all")

    particles.clear()

    game_running = True

    round_time = ROUND_TIME

    round_number = 1

    ai_timer = 0

    create_background()
    create_ring()

    player.x = 430
    player.y = 475
    player.health = 100
    player.stamina = 100
    player.attack = None
    player.knocked_down = False
    player.blocking = False

    cpu.x = 770
    cpu.y = 475
    cpu.health = 100
    cpu.stamina = 100
    cpu.attack = None
    cpu.knocked_down = False
    cpu.blocking = False

    player.create_graphics()
    cpu.create_graphics()

    create_ui_again()


# ============================================================
# RECREATE UI
# ============================================================

def create_ui_again():

    global player_health_bar
    global cpu_health_bar
    global player_stamina_bar
    global cpu_stamina_bar
    global timer_text
    global round_text

    canvas.create_text(
        250,
        30,
        text="PLAYER",
        fill="#eeeeee",
        font=("Arial", 18, "bold")
    )

    canvas.create_text(
        950,
        30,
        text="CPU",
        fill="#eeeeee",
        font=("Arial", 18, "bold")
    )

    canvas.create_rectangle(
        100,
        55,
        500,
        80,
        fill="#171a22",
        outline="#555965"
    )

    player_health_bar = canvas.create_rectangle(
        100,
        55,
        500,
        80,
        fill="#c72f3a",
        outline=""
    )

    canvas.create_rectangle(
        700,
        55,
        1100,
        80,
        fill="#171a22",
        outline="#555965"
    )

    cpu_health_bar = canvas.create_rectangle(
        700,
        55,
        1100,
        80,
        fill="#3478c5",
        outline=""
    )

    canvas.create_rectangle(
        100,
        88,
        500,
        98,
        fill="#171a22",
        outline=""
    )

    player_stamina_bar = canvas.create_rectangle(
        100,
        88,
        500,
        98,
        fill="#d5a832",
        outline=""
    )

    canvas.create_rectangle(
        700,
        88,
        1100,
        98,
        fill="#171a22",
        outline=""
    )

    cpu_stamina_bar = canvas.create_rectangle(
        700,
        88,
        1100,
        98,
        fill="#d5a832",
        outline=""
    )

    timer_text = canvas.create_text(
        WIDTH / 2,
        65,
        text="1:00",
        fill="#ffffff",
        font=("Arial", 25, "bold")
    )

    round_text = canvas.create_text(
        WIDTH / 2,
        95,
        text="ROUND 1",
        fill="#777d8b",
        font=("Arial", 10, "bold")
    )


# ============================================================
# RESTART KEY
# ============================================================

def restart_key(event):

    if event.keysym.lower() == "r":

        restart_game()


root.bind("<KeyPress-r>", restart_key)
root.bind("<KeyPress-R>", restart_key)


# ============================================================
# GAME LOOP
# ============================================================

def game_loop():

    if game_running:

        player_control()

        cpu_ai()

        player.update()
        cpu.update()

        check_attack(
            player,
            cpu
        )

        check_attack(
            cpu,
            player
        )

        prevent_overlap()

        check_knockdown()

        update_ui()

        update_timer()

    update_particles()

    root.after(
        FRAME_MS,
        game_loop
    )


# ============================================================
# START
# ============================================================

game_loop()

root.mainloop()