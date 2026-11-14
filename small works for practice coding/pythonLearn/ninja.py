import tkinter as tk
import random
import math

# ============================================================
# NINJA DUEL
# Advanced Tkinter Game
# ============================================================

WIDTH = 1200
HEIGHT = 750

GROUND_Y = 610

FPS = 60
FRAME_MS = 1000 // FPS

GRAVITY = 0.8

ARENA_LEFT = 80
ARENA_RIGHT = 1120

random.seed()


# ============================================================
# WINDOW
# ============================================================

root = tk.Tk()
root.title("Ninja Duel - Python")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="#080912",
    highlightthickness=0
)

canvas.pack()


# ============================================================
# GAME STATE
# ============================================================

game_running = True

keys = set()

projectiles = []
particles = []

stars = []

ai_timer = 0
game_time = 0


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

    # Sky
    canvas.create_rectangle(
        0,
        0,
        WIDTH,
        HEIGHT,
        fill="#080912",
        outline=""
    )

    # Moon glow
    for radius in range(120, 40, -15):

        shade = max(20, 50 - radius // 4)

        canvas.create_oval(
            850 - radius,
            100 - radius,
            850 + radius,
            100 + radius,
            outline=f"#{shade:02x}{shade:02x}{min(80, shade + 30):02x}"
        )

    # Moon
    canvas.create_oval(
        800,
        50,
        900,
        150,
        fill="#e9e3c8",
        outline=""
    )

    # Moon craters
    for _ in range(12):

        x = random.randint(815, 880)
        y = random.randint(65, 135)
        r = random.randint(2, 7)

        canvas.create_oval(
            x - r,
            y - r,
            x + r,
            y + r,
            fill="#c9c3ab",
            outline=""
        )

    # Stars
    for _ in range(180):

        x = random.randint(0, WIDTH)
        y = random.randint(20, 350)

        size = random.choice([1, 1, 1, 2])

        star = canvas.create_oval(
            x - size,
            y - size,
            x + size,
            y + size,
            fill=random.choice([
                "#ffffff",
                "#aab8e8",
                "#d8d4b5"
            ]),
            outline=""
        )

        stars.append(star)

    # Mountains
    canvas.create_polygon(
        0,
        470,
        150,
        300,
        300,
        470,
        470,
        270,
        650,
        470,
        820,
        310,
        1030,
        470,
        1200,
        280,
        1200,
        610,
        0,
        610,
        fill="#111522",
        outline=""
    )

    # Mountain highlights
    canvas.create_line(
        470,
        270,
        400,
        390,
        fill="#242a3c",
        width=3
    )

    canvas.create_line(
        820,
        310,
        750,
        400,
        fill="#242a3c",
        width=3
    )

    # Far trees
    for x in range(0, WIDTH, 45):

        height = random.randint(50, 100)

        canvas.create_polygon(
            x,
            GROUND_Y,
            x + 22,
            GROUND_Y - height,
            x + 44,
            GROUND_Y,
            fill="#0c1218",
            outline=""
        )

    # Ground
    canvas.create_rectangle(
        0,
        GROUND_Y,
        WIDTH,
        HEIGHT,
        fill="#0a0c12",
        outline=""
    )

    # Ground lines
    for y in range(GROUND_Y + 20, HEIGHT, 25):

        canvas.create_line(
            0,
            y,
            WIDTH,
            y,
            fill="#10141c"
        )

    # Title
    canvas.create_text(
        WIDTH / 2,
        30,
        text="NINJA DUEL",
        fill="#eeeeee",
        font=("Arial", 26, "bold")
    )

    canvas.create_text(
        WIDTH / 2,
        58,
        text="SHADOW ARENA",
        fill="#656b7c",
        font=("Arial", 10, "bold")
    )


# ============================================================
# ARENA
# ============================================================

def create_arena():

    # Platforms
    canvas.create_rectangle(
        ARENA_LEFT,
        GROUND_Y - 8,
        ARENA_RIGHT,
        GROUND_Y,
        fill="#393d48",
        outline=""
    )

    # Torches
    create_torch(130, GROUND_Y)
    create_torch(1070, GROUND_Y)

    # Arena symbols
    canvas.create_oval(
        520,
        540,
        680,
        700,
        outline="#1d222d",
        width=3
    )

    canvas.create_line(
        600,
        540,
        600,
        700,
        fill="#171b24",
        width=2
    )


def create_torch(x, y):

    canvas.create_line(
        x,
        y,
        x,
        y - 100,
        fill="#383c45",
        width=7
    )

    canvas.create_oval(
        x - 13,
        y - 120,
        x + 13,
        y - 94,
        fill="#ff9e32",
        outline=""
    )

    canvas.create_oval(
        x - 7,
        y - 113,
        x + 7,
        y - 100,
        fill="#ffe9a3",
        outline=""
    )


# ============================================================
# PARTICLES
# ============================================================

def create_particles(x, y, amount=15):

    for _ in range(amount):

        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1, 6)

        obj = canvas.create_oval(
            x - 3,
            y - 3,
            x + 3,
            y + 3,
            fill=random.choice([
                "#ffffff",
                "#ffcf4a",
                "#ff5c5c",
                "#7ca8ff"
            ]),
            outline=""
        )

        particles.append({
            "object": obj,
            "x": x,
            "y": y,
            "dx": math.cos(angle) * speed,
            "dy": math.sin(angle) * speed,
            "life": random.randint(10, 25)
        })


def update_particles():

    for p in particles[:]:

        p["x"] += p["dx"]
        p["y"] += p["dy"]

        p["dy"] += 0.15

        p["life"] -= 1

        canvas.coords(
            p["object"],
            p["x"] - 3,
            p["y"] - 3,
            p["x"] + 3,
            p["y"] + 3
        )

        if p["life"] <= 0:

            canvas.delete(p["object"])
            particles.remove(p)


# ============================================================
# PROJECTILE
# ============================================================

class Projectile:

    def __init__(self, x, y, direction, owner):

        self.x = x
        self.y = y

        self.direction = direction

        self.owner = owner

        self.speed = 12

        self.damage = 12

        self.life = 100

        self.object = canvas.create_oval(
            x - 8,
            y - 8,
            x + 8,
            y + 8,
            fill="#9d68ff",
            outline="#e5d9ff",
            width=2
        )

        self.trail = []

    def update(self):

        self.x += self.speed * self.direction

        self.life -= 1

        canvas.coords(
            self.object,
            self.x - 8,
            self.y - 8,
            self.x + 8,
            self.y + 8
        )

        if random.random() < 0.5:

            trail = canvas.create_oval(
                self.x - 3,
                self.y - 3,
                self.x + 3,
                self.y + 3,
                fill="#6c3fb5",
                outline=""
            )

            self.trail.append({
                "object": trail,
                "life": 8
            })

        for t in self.trail[:]:

            t["life"] -= 1

            if t["life"] <= 0:

                canvas.delete(t["object"])
                self.trail.remove(t)

        if self.x < 0 or self.x > WIDTH:

            self.destroy()

        return self.life > 0

    def destroy(self):

        canvas.delete(self.object)

        for t in self.trail:

            canvas.delete(t["object"])

        if self in projectiles:

            projectiles.remove(self)


# ============================================================
# FIGHTER
# ============================================================

class Ninja:

    def __init__(
        self,
        x,
        color,
        accent,
        name,
        is_player=False
    ):

        self.x = x
        self.y = GROUND_Y

        self.vx = 0
        self.vy = 0

        self.color = color
        self.accent = accent

        self.name = name

        self.is_player = is_player

        self.health = 100
        self.stamina = 100

        self.direction = 1

        self.speed = 5

        self.jump_power = -15

        self.on_ground = True

        self.blocking = False

        self.attack = None
        self.attack_timer = 0

        self.attack_cooldown = 0

        self.dash_timer = 0

        self.invincible_timer = 0

        self.hit_flash = 0

        self.dead = False

        self.create_graphics()


    # ========================================================
    # GRAPHICS
    # ========================================================

    def create_graphics(self):

        x = self.x
        y = self.y

        # Shadow
        self.shadow = canvas.create_oval(
            x - 32,
            y - 6,
            x + 32,
            y + 6,
            fill="#050609",
            outline=""
        )

        # Legs
        self.left_leg = canvas.create_line(
            x - 10,
            y - 60,
            x - 22,
            y,
            fill=self.color,
            width=13
        )

        self.right_leg = canvas.create_line(
            x + 10,
            y - 60,
            x + 22,
            y,
            fill=self.color,
            width=13
        )

        # Body
        self.body = canvas.create_polygon(
            x - 25,
            y - 125,
            x + 25,
            y - 125,
            x + 30,
            y - 55,
            x - 30,
            y - 55,
            fill=self.color,
            outline="#050609",
            width=2
        )

        # Belt
        self.belt = canvas.create_rectangle(
            x - 28,
            y - 70,
            x + 28,
            y - 57,
            fill=self.accent,
            outline=""
        )

        # Head
        self.head = canvas.create_oval(
            x - 24,
            y - 175,
            x + 24,
            y - 127,
            fill="#b87859",
            outline="#050609",
            width=2
        )

        # Mask
        self.mask = canvas.create_rectangle(
            x - 23,
            y - 158,
            x + 23,
            y - 138,
            fill="#11131b",
            outline=""
        )

        # Eyes
        self.eye1 = canvas.create_rectangle(
            x - 14,
            y - 153,
            x - 5,
            y - 149,
            fill="#ff4545",
            outline=""
        )

        self.eye2 = canvas.create_rectangle(
            x + 5,
            y - 153,
            x + 14,
            y - 149,
            fill="#ff4545",
            outline=""
        )

        # Headband
        self.band = canvas.create_line(
            x - 26,
            y - 165,
            x + 26,
            y - 165,
            fill=self.accent,
            width=5
        )

        # Tail of headband
        self.band_tail = canvas.create_line(
            x + 25,
            y - 165,
            x + 50,
            y - 145,
            fill=self.accent,
            width=5
        )

        # Arms
        self.left_arm = canvas.create_line(
            x - 20,
            y - 115,
            x - 55,
            y - 75,
            fill=self.color,
            width=12
        )

        self.right_arm = canvas.create_line(
            x + 20,
            y - 115,
            x + 55,
            y - 75,
            fill=self.color,
            width=12
        )

        # Hands
        self.left_hand = canvas.create_oval(
            x - 64,
            y - 84,
            x - 48,
            y - 68,
            fill=self.accent,
            outline=""
        )

        self.right_hand = canvas.create_oval(
            x + 48,
            y - 84,
            x + 64,
            y - 68,
            fill=self.accent,
            outline=""
        )

        self.objects = [
            self.shadow,
            self.left_leg,
            self.right_leg,
            self.body,
            self.belt,
            self.head,
            self.mask,
            self.eye1,
            self.eye2,
            self.band,
            self.band_tail,
            self.left_arm,
            self.right_arm,
            self.left_hand,
            self.right_hand
        ]


    # ========================================================
    # UPDATE GRAPHICS
    # ========================================================

    def update_graphics(self):

        x = self.x
        y = self.y

        # Shadow
        canvas.coords(
            self.shadow,
            x - 32,
            GROUND_Y - 5,
            x + 32,
            GROUND_Y + 7
        )

        # Head
        canvas.coords(
            self.head,
            x - 24,
            y - 175,
            x + 24,
            y - 127
        )

        canvas.coords(
            self.mask,
            x - 23,
            y - 158,
            x + 23,
            y - 138
        )

        canvas.coords(
            self.eye1,
            x - 14,
            y - 153,
            x - 5,
            y - 149
        )

        canvas.coords(
            self.eye2,
            x + 5,
            y - 153,
            x + 14,
            y - 149
        )

        canvas.coords(
            self.band,
            x - 26,
            y - 165,
            x + 26,
            y - 165
        )

        canvas.coords(
            self.band_tail,
            x + 25,
            y - 165,
            x + 50,
            y - 145
        )

        # Body
        canvas.coords(
            self.body,
            x - 25,
            y - 125,
            x + 25,
            y - 125,
            x + 30,
            y - 55,
            x - 30,
            y - 55
        )

        # Belt
        canvas.coords(
            self.belt,
            x - 28,
            y - 70,
            x + 28,
            y - 57
        )

        # Legs
        canvas.coords(
            self.left_leg,
            x - 10,
            y - 60,
            x - 22,
            y
        )

        canvas.coords(
            self.right_leg,
            x + 10,
            y - 60,
            x + 22,
            y
        )

        # Attack / block positions
        if self.blocking:

            canvas.coords(
                self.left_arm,
                x - 20,
                y - 115,
                x - 35,
                y - 165
            )

            canvas.coords(
                self.right_arm,
                x + 20,
                y - 115,
                x + 35,
                y - 165
            )

            left_hand_x = x - 35
            right_hand_x = x + 35

        elif self.attack == "slash":

            if self.direction == 1:

                canvas.coords(
                    self.right_arm,
                    x + 20,
                    y - 115,
                    x + 100,
                    y - 125
                )

                canvas.coords(
                    self.left_arm,
                    x - 20,
                    y - 115,
                    x - 55,
                    y - 75
                )

                right_hand_x = x + 100
                left_hand_x = x - 55

            else:

                canvas.coords(
                    self.left_arm,
                    x - 20,
                    y - 115,
                    x - 100,
                    y - 125
                )

                canvas.coords(
                    self.right_arm,
                    x + 20,
                    y - 115,
                    x + 55,
                    y - 75
                )

                left_hand_x = x - 100
                right_hand_x = x + 55

        else:

            canvas.coords(
                self.left_arm,
                x - 20,
                y - 115,
                x - 55,
                y - 75
            )

            canvas.coords(
                self.right_arm,
                x + 20,
                y - 115,
                x + 55,
                y - 75
            )

            left_hand_x = x - 55
            right_hand_x = x + 55

        canvas.coords(
            self.left_hand,
            left_hand_x - 8,
            y - 84,
            left_hand_x + 8,
            y - 68
        )

        canvas.coords(
            self.right_hand,
            right_hand_x - 8,
            y - 84,
            right_hand_x + 8,
            y - 68
        )


    # ========================================================
    # MOVEMENT
    # ========================================================

    def move(self, direction):

        if self.dead:
            return

        if self.dash_timer > 0:
            speed = 13
        else:
            speed = self.speed

        self.vx = direction * speed

        self.direction = 1 if direction > 0 else -1


    # ========================================================
    # JUMP
    # ========================================================

    def jump(self):

        if self.dead:
            return

        if self.on_ground:

            self.vy = self.jump_power

            self.on_ground = False


    # ========================================================
    # DASH
    # ========================================================

    def dash(self):

        if self.dead:
            return

        if self.stamina < 25:
            return

        if self.dash_timer > 0:
            return

        self.stamina -= 25

        self.dash_timer = 12

        self.invincible_timer = 12

        create_particles(
            self.x,
            self.y - 80,
            8
        )


    # ========================================================
    # ATTACK
    # ========================================================

    def slash(self):

        if self.dead:
            return

        if self.attack is not None:
            return

        if self.attack_cooldown > 0:
            return

        if self.stamina < 18:
            return

        self.stamina -= 18

        self.attack = "slash"

        self.attack_timer = 14

        self.attack_cooldown = 18

        self.update_graphics()


    # ========================================================
    # PROJECTILE
    # ========================================================

    def throw_projectile(self):

        if self.dead:
            return

        if self.stamina < 30:
            return

        self.stamina -= 30

        x = self.x + self.direction * 65
        y = self.y - 115

        projectiles.append(
            Projectile(
                x,
                y,
                self.direction,
                self
            )
        )


    # ========================================================
    # BLOCK
    # ========================================================

    def block(self, state):

        if self.dead:
            self.blocking = False
            return

        self.blocking = state

        self.update_graphics()


    # ========================================================
    # DAMAGE
    # ========================================================

    def take_damage(self, damage, attacker):

        if self.dead:
            return

        if self.invincible_timer > 0:
            return

        if self.blocking:

            damage *= 0.2

            create_particles(
                self.x,
                self.y - 110,
                8
            )

        else:

            create_particles(
                self.x,
                self.y - 110,
                15
            )

        self.health -= damage

        self.health = max(
            0,
            self.health
        )

        self.hit_flash = 5

        # Knockback
        self.x += attacker.direction * 15

        self.x = max(
            ARENA_LEFT + 50,
            min(
                ARENA_RIGHT - 50,
                self.x
            )
        )

        if self.health <= 0:

            self.dead = True

            self.blocking = False

            self.vy = -10


    # ========================================================
    # PHYSICS
    # ========================================================

    def physics(self):

        if self.dead:

            self.vy += GRAVITY

            self.y += self.vy

            if self.y > GROUND_Y:

                self.y = GROUND_Y
                self.vy = 0

            self.update_graphics()

            return

        # Gravity
        self.vy += GRAVITY

        self.y += self.vy

        if self.y >= GROUND_Y:

            self.y = GROUND_Y

            self.vy = 0

            self.on_ground = True

        else:

            self.on_ground = False

        # Horizontal
        self.x += self.vx

        self.vx *= 0.75

        # Boundaries
        self.x = max(
            ARENA_LEFT + 50,
            min(
                ARENA_RIGHT - 50,
                self.x
            )
        )


    # ========================================================
    # UPDATE
    # ========================================================

    def update(self):

        if self.attack_timer > 0:

            self.attack_timer -= 1

            if self.attack_timer == 0:

                self.attack = None

        if self.attack_cooldown > 0:

            self.attack_cooldown -= 1

        if self.dash_timer > 0:

            self.dash_timer -= 1

        if self.invincible_timer > 0:

            self.invincible_timer -= 1

        # Stamina regeneration
        if not self.attack and not self.blocking:

            self.stamina += 0.35

        elif self.blocking:

            self.stamina -= 0.15

        self.stamina = max(
            0,
            min(
                100,
                self.stamina
            )
        )

        self.physics()

        self.update_graphics()


# ============================================================
# CREATE BACKGROUND
# ============================================================

create_background()
create_arena()


# ============================================================
# CREATE NINJAS
# ============================================================

player = Ninja(
    350,
    "#8f1827",
    "#ff394d",
    "PLAYER",
    True
)

enemy = Ninja(
    850,
    "#202c68",
    "#4c7dff",
    "SHADOW"
)

player.direction = 1
enemy.direction = -1


# ============================================================
# UI
# ============================================================

canvas.create_text(
    170,
    105,
    text="PLAYER",
    fill="#eeeeee",
    font=("Arial", 16, "bold")
)

canvas.create_text(
    1030,
    105,
    text="SHADOW",
    fill="#eeeeee",
    font=("Arial", 16, "bold")
)


# Health backgrounds
canvas.create_rectangle(
    70,
    125,
    470,
    150,
    fill="#171a22",
    outline="#414552"
)

canvas.create_rectangle(
    730,
    125,
    1130,
    150,
    fill="#171a22",
    outline="#414552"
)


player_health_bar = canvas.create_rectangle(
    70,
    125,
    470,
    150,
    fill="#c52f42",
    outline=""
)

enemy_health_bar = canvas.create_rectangle(
    730,
    125,
    1130,
    150,
    fill="#426ed0",
    outline=""
)


# Stamina backgrounds
canvas.create_rectangle(
    70,
    158,
    470,
    168,
    fill="#171a22",
    outline=""
)

canvas.create_rectangle(
    730,
    158,
    1130,
    168,
    fill="#171a22",
    outline=""
)


player_stamina_bar = canvas.create_rectangle(
    70,
    158,
    470,
    168,
    fill="#d5a936",
    outline=""
)

enemy_stamina_bar = canvas.create_rectangle(
    730,
    158,
    1130,
    168,
    fill="#d5a936",
    outline=""
)


# Controls
canvas.create_text(
    WIDTH / 2,
    700,
    text="A / D  Move     W  Jump     J  Slash     K  Shuriken     L  Dash     SPACE  Block",
    fill="#676d7c",
    font=("Arial", 11)
)


# ============================================================
# COMBAT DETECTION
# ============================================================

def check_melee_attack(attacker, defender):

    if attacker.attack != "slash":
        return

    # Hit only during specific animation frame
    if attacker.attack_timer != 7:
        return

    distance = abs(
        attacker.x - defender.x
    )

    if distance <= 145:

        damage = random.randint(
            10,
            18
        )

        defender.take_damage(
            damage,
            attacker
        )


# ============================================================
# PROJECTILE COLLISION
# ============================================================

def check_projectiles():

    for projectile in projectiles[:]:

        if not projectile.update():
            continue

        target = (
            enemy
            if projectile.owner == player
            else player
        )

        if target.dead:
            projectile.destroy()
            continue

        distance = math.sqrt(
            (projectile.x - target.x) ** 2 +
            (projectile.y - (target.y - 100)) ** 2
        )

        if distance < 45:

            target.take_damage(
                projectile.damage,
                projectile.owner
            )

            projectile.destroy()


# ============================================================
# PLAYER INPUT
# ============================================================

def player_control():

    if player.dead:
        return

    if "a" in keys:

        player.move(-1)

    if "d" in keys:

        player.move(1)

    if "w" in keys:

        player.jump()

    if "j" in keys:

        player.slash()

    if "k" in keys:

        player.throw_projectile()

    if "l" in keys:

        player.dash()

    if "space" in keys:

        player.block(True)

    else:

        player.block(False)


# ============================================================
# AI
# ============================================================

def enemy_ai():

    global ai_timer

    if enemy.dead:
        return

    ai_timer -= 1

    distance = abs(
        enemy.x - player.x
    )

    # Face player
    if enemy.x < player.x:

        enemy.direction = 1

    else:

        enemy.direction = -1

    if ai_timer > 0:
        return

    ai_timer = random.randint(
        8,
        20
    )

    # Far away
    if distance > 300:

        if enemy.x < player.x:

            enemy.move(1)

        else:

            enemy.move(-1)

        # Occasionally projectile
        if random.random() < 0.25:

            enemy.throw_projectile()

        return

    # Medium distance
    if distance > 140:

        decision = random.random()

        if decision < 0.55:

            if enemy.x < player.x:

                enemy.move(1)

            else:

                enemy.move(-1)

        elif decision < 0.8:

            enemy.throw_projectile()

        else:

            enemy.dash()

        return

    # Close distance
    decision = random.random()

    if decision < 0.55:

        enemy.slash()

    elif decision < 0.75:

        enemy.block(True)

        root.after(
            random.randint(250, 600),
            lambda: enemy.block(False)
        )

    elif decision < 0.9:

        enemy.dash()

    else:

        # Jump away
        enemy.jump()


# ============================================================
# SEPARATE FIGHTERS
# ============================================================

def prevent_overlap():

    if player.dead or enemy.dead:
        return

    distance = abs(
        player.x - enemy.x
    )

    minimum = 65

    if distance < minimum:

        difference = minimum - distance

        if player.x < enemy.x:

            player.x -= difference / 2
            enemy.x += difference / 2

        else:

            player.x += difference / 2
            enemy.x -= difference / 2

        player.x = max(
            ARENA_LEFT + 50,
            min(
                ARENA_RIGHT - 50,
                player.x
            )
        )

        enemy.x = max(
            ARENA_LEFT + 50,
            min(
                ARENA_RIGHT - 50,
                enemy.x
            )
        )


# ============================================================
# UPDATE UI
# ============================================================

def update_ui():

    player_width = (
        400 * player.health / 100
    )

    enemy_width = (
        400 * enemy.health / 100
    )

    player_stamina_width = (
        400 * player.stamina / 100
    )

    enemy_stamina_width = (
        400 * enemy.stamina / 100
    )

    canvas.coords(
        player_health_bar,
        70,
        125,
        70 + player_width,
        150
    )

    canvas.coords(
        enemy_health_bar,
        1130 - enemy_width,
        125,
        1130,
        150
    )

    canvas.coords(
        player_stamina_bar,
        70,
        158,
        70 + player_stamina_width,
        168
    )

    canvas.coords(
        enemy_stamina_bar,
        1130 - enemy_stamina_width,
        158,
        1130,
        168
    )


# ============================================================
# WINNER SCREEN
# ============================================================

def show_winner():

    global game_running

    game_running = False

    if player.dead and enemy.dead:

        winner = "DRAW"

    elif enemy.dead:

        winner = "PLAYER WINS!"

    else:

        winner = "SHADOW WINS!"

    canvas.create_rectangle(
        300,
        270,
        900,
        500,
        fill="#080a10",
        outline="#555b6a",
        width=3
    )

    canvas.create_text(
        WIDTH / 2,
        330,
        text="BATTLE OVER",
        fill="#eeeeee",
        font=("Arial", 28, "bold")
    )

    canvas.create_text(
        WIDTH / 2,
        395,
        text=winner,
        fill="#ffd34d",
        font=("Arial", 38, "bold")
    )

    canvas.create_text(
        WIDTH / 2,
        450,
        text="Press R to restart",
        fill="#777d8c",
        font=("Arial", 14)
    )


# ============================================================
# RESTART
# ============================================================

def restart(event=None):

    global game_running
    global ai_timer
    global projectiles
    global particles

    game_running = True

    ai_timer = 0

    for projectile in projectiles[:]:

        projectile.destroy()

    projectiles.clear()

    for particle in particles:

        canvas.delete(
            particle["object"]
        )

    particles.clear()

    canvas.delete("all")

    stars.clear()

    create_background()
    create_arena()

    player.x = 350
    player.y = GROUND_Y

    player.vx = 0
    player.vy = 0

    player.health = 100
    player.stamina = 100

    player.dead = False
    player.attack = None
    player.blocking = False

    enemy.x = 850
    enemy.y = GROUND_Y

    enemy.vx = 0
    enemy.vy = 0

    enemy.health = 100
    enemy.stamina = 100

    enemy.dead = False
    enemy.attack = None
    enemy.blocking = False

    player.direction = 1
    enemy.direction = -1

    player.create_graphics()
    enemy.create_graphics()

    create_ui()


# ============================================================
# RECREATE UI
# ============================================================

def create_ui():

    global player_health_bar
    global enemy_health_bar
    global player_stamina_bar
    global enemy_stamina_bar

    canvas.create_text(
        170,
        105,
        text="PLAYER",
        fill="#eeeeee",
        font=("Arial", 16, "bold")
    )

    canvas.create_text(
        1030,
        105,
        text="SHADOW",
        fill="#eeeeee",
        font=("Arial", 16, "bold")
    )

    canvas.create_rectangle(
        70,
        125,
        470,
        150,
        fill="#171a22",
        outline="#414552"
    )

    canvas.create_rectangle(
        730,
        125,
        1130,
        150,
        fill="#171a22",
        outline="#414552"
    )

    player_health_bar = canvas.create_rectangle(
        70,
        125,
        470,
        150,
        fill="#c52f42",
        outline=""
    )

    enemy_health_bar = canvas.create_rectangle(
        730,
        125,
        1130,
        150,
        fill="#426ed0",
        outline=""
    )

    canvas.create_rectangle(
        70,
        158,
        470,
        168,
        fill="#171a22",
        outline=""
    )

    canvas.create_rectangle(
        730,
        158,
        1130,
        168,
        fill="#171a22",
        outline=""
    )

    player_stamina_bar = canvas.create_rectangle(
        70,
        158,
        470,
        168,
        fill="#d5a936",
        outline=""
    )

    enemy_stamina_bar = canvas.create_rectangle(
        730,
        158,
        1130,
        168,
        fill="#d5a936",
        outline=""
    )

    canvas.create_text(
        WIDTH / 2,
        700,
        text="A / D  Move     W  Jump     J  Slash     K  Shuriken     L  Dash     SPACE  Block",
        fill="#676d7c",
        font=("Arial", 11)
    )


# ============================================================
# RESTART KEY
# ============================================================

root.bind(
    "<KeyPress-r>",
    restart
)

root.bind(
    "<KeyPress-R>",
    restart
)


# ============================================================
# GAME LOOP
# ============================================================

def game_loop():

    global game_time

    if game_running:

        game_time += 1

        player_control()

        enemy_ai()

        player.update()
        enemy.update()

        check_melee_attack(
            player,
            enemy
        )

        check_melee_attack(
            enemy,
            player
        )

        check_projectiles()

        prevent_overlap()

        update_ui()

        if player.dead or enemy.dead:

            show_winner()

    update_particles()

    root.after(
        FRAME_MS,
        game_loop
    )


# ============================================================
# START
# ============================================================

create_ui()

game_loop()

root.mainloop()