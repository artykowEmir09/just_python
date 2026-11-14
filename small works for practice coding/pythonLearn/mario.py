import pygame
import sys

pygame.init()

# =====================================================
# WINDOW
# =====================================================

WIDTH = 1000
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Platform Adventure")

clock = pygame.time.Clock()
FPS = 60


# =====================================================
# COLORS
# =====================================================

SKY = (135, 206, 235)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)

GREEN = (50, 180, 70)
DARK_GREEN = (30, 120, 50)

BROWN = (150, 90, 45)

RED = (220, 50, 50)
BLUE = (50, 100, 220)

YELLOW = (255, 210, 40)
ORANGE = (240, 130, 30)

PURPLE = (150, 70, 200)


# =====================================================
# FONTS
# =====================================================

font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 25)
big_font = pygame.font.Font(None, 70)


# =====================================================
# PLAYER
# =====================================================

class Player:

    def __init__(self):

        self.width = 40
        self.height = 55

        self.x = 80
        self.y = 400

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

        self.speed = 5

        self.velocity_y = 0

        self.jump_power = -13

        self.gravity = 0.6

        self.on_ground = False

        self.lives = 3

        self.score = 0

    def reset_position(self):

        self.rect.x = 80
        self.rect.y = 400

        self.velocity_y = 0

    def move(self, platforms):

        keys = pygame.key.get_pressed()

        # -----------------------------
        # Horizontal movement
        # -----------------------------

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:

            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:

            self.rect.x += self.speed

        # Keep player inside screen

        if self.rect.left < 0:

            self.rect.left = 0

        if self.rect.right > WIDTH:

            self.rect.right = WIDTH

        # -----------------------------
        # Gravity
        # -----------------------------

        self.velocity_y += self.gravity

        if self.velocity_y > 12:

            self.velocity_y = 12

        self.rect.y += self.velocity_y

        # -----------------------------
        # Platform collision
        # -----------------------------

        self.on_ground = False

        for platform in platforms:

            if self.rect.colliderect(platform):

                # Falling

                if self.velocity_y > 0:

                    self.rect.bottom = platform.top

                    self.velocity_y = 0

                    self.on_ground = True

                # Jumping upward

                elif self.velocity_y < 0:

                    self.rect.top = platform.bottom

                    self.velocity_y = 0

    def jump(self):

        if self.on_ground:

            self.velocity_y = self.jump_power

    def draw(self):

        # Body

        pygame.draw.rect(
            screen,
            RED,
            self.rect
        )

        # Head

        pygame.draw.circle(
            screen,
            (255, 200, 150),
            (
                self.rect.centerx,
                self.rect.y + 15
            ),
            13
        )

        # Hat

        pygame.draw.rect(
            screen,
            RED,
            (
                self.rect.x + 5,
                self.rect.y,
                30,
                8
            )
        )

        # Eyes

        pygame.draw.circle(
            screen,
            BLACK,
            (
                self.rect.centerx - 5,
                self.rect.y + 14
            ),
            2
        )

        pygame.draw.circle(
            screen,
            BLACK,
            (
                self.rect.centerx + 5,
                self.rect.y + 14
            ),
            2
        )


# =====================================================
# ENEMY
# =====================================================

class Enemy:

    def __init__(self, x, y, speed=2):

        self.rect = pygame.Rect(
            x,
            y,
            40,
            40
        )

        self.speed = speed

        self.direction = 1

    def update(self):

        self.rect.x += self.speed * self.direction

        if self.rect.left <= 0:

            self.direction = 1

        if self.rect.right >= WIDTH:

            self.direction = -1

    def draw(self):

        # Body

        pygame.draw.rect(
            screen,
            ORANGE,
            self.rect
        )

        # Eyes

        pygame.draw.circle(
            screen,
            WHITE,
            (
                self.rect.x + 12,
                self.rect.y + 12
            ),
            6
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (
                self.rect.x + 28,
                self.rect.y + 12
            ),
            6
        )

        pygame.draw.circle(
            screen,
            BLACK,
            (
                self.rect.x + 12,
                self.rect.y + 12
            ),
            2
        )

        pygame.draw.circle(
            screen,
            BLACK,
            (
                self.rect.x + 28,
                self.rect.y + 12
            ),
            2
        )


# =====================================================
# COIN
# =====================================================

class Coin:

    def __init__(self, x, y):

        self.rect = pygame.Rect(
            x,
            y,
            25,
            25
        )

    def draw(self):

        pygame.draw.circle(
            screen,
            YELLOW,
            self.rect.center,
            12
        )

        pygame.draw.circle(
            screen,
            ORANGE,
            self.rect.center,
            12,
            3
        )


# =====================================================
# LEVEL DATA
# =====================================================

levels = [

    # =================================================
    # LEVEL 1
    # =================================================

    {
        "name": "LEVEL 1 - EASY",

        "platforms": [

            pygame.Rect(0, 550, 1000, 50),

            pygame.Rect(100, 450, 200, 30),

            pygame.Rect(400, 380, 180, 30),

            pygame.Rect(700, 450, 200, 30),

            pygame.Rect(300, 280, 160, 30),

        ],

        "coins": [

            (150, 410),

            (220, 410),

            (450, 340),

            (750, 410),

            (350, 240),

        ],

        "enemies": [

            (500, 340, 2)

        ]
    },


    # =================================================
    # LEVEL 2
    # =================================================

    {
        "name": "LEVEL 2 - MEDIUM",

        "platforms": [

            pygame.Rect(0, 550, 1000, 50),

            pygame.Rect(50, 450, 150, 30),

            pygame.Rect(300, 400, 130, 30),

            pygame.Rect(550, 330, 130, 30),

            pygame.Rect(800, 420, 150, 30),

            pygame.Rect(400, 220, 150, 30),

            pygame.Rect(700, 150, 150, 30),

        ],

        "coins": [

            (100, 410),

            (350, 360),

            (600, 290),

            (850, 380),

            (450, 180),

            (750, 110),

            (820, 110),

        ],

        "enemies": [

            (350, 360, 3),

            (820, 380, 3)

        ]
    },


    # =================================================
    # LEVEL 3
    # =================================================

    {
        "name": "LEVEL 3 - HARD",

        "platforms": [

            pygame.Rect(0, 550, 1000, 50),

            pygame.Rect(50, 460, 120, 30),

            pygame.Rect(230, 390, 100, 30),

            pygame.Rect(400, 320, 100, 30),

            pygame.Rect(580, 250, 100, 30),

            pygame.Rect(760, 180, 100, 30),

            pygame.Rect(400, 150, 120, 30),

            pygame.Rect(150, 250, 100, 30),

        ],

        "coins": [

            (90, 420),

            (260, 350),

            (430, 280),

            (610, 210),

            (790, 140),

            (450, 110),

            (190, 210),

            (470, 110),

        ],

        "enemies": [

            (260, 350, 3),

            (610, 210, 3),

            (790, 140, 4)

        ]
    }

]


# =====================================================
# LOAD LEVEL
# =====================================================

def load_level(level_number):

    data = levels[level_number]

    platforms = data["platforms"]

    coins = []

    for x, y in data["coins"]:

        coins.append(
            Coin(x, y)
        )

    enemies = []

    for x, y, speed in data["enemies"]:

        enemies.append(
            Enemy(x, y, speed)
        )

    return platforms, coins, enemies


# =====================================================
# GAME VARIABLES
# =====================================================

current_level = 0

platforms, coins, enemies = load_level(current_level)

player = Player()

game_over = False
game_won = False

level_message_timer = 120


# =====================================================
# RESTART GAME
# =====================================================

def restart_game():

    global current_level
    global platforms
    global coins
    global enemies
    global player
    global game_over
    global game_won
    global level_message_timer

    current_level = 0

    player = Player()

    platforms, coins, enemies = load_level(
        current_level
    )

    game_over = False
    game_won = False

    level_message_timer = 120


# =====================================================
# NEXT LEVEL
# =====================================================

def next_level():

    global current_level
    global platforms
    global coins
    global enemies
    global level_message_timer

    current_level += 1

    if current_level >= len(levels):

        return False

    platforms, coins, enemies = load_level(
        current_level
    )

    player.reset_position()

    level_message_timer = 120

    return True


# =====================================================
# GAME LOOP
# =====================================================

while True:

    # =================================================
    # EVENTS
    # =================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # Jump

            if event.key == pygame.K_SPACE:

                if not game_over and not game_won:

                    player.jump()

            # Restart

            if event.key == pygame.K_r:

                if game_over or game_won:

                    restart_game()


    # =================================================
    # UPDATE
    # =================================================

    if not game_over and not game_won:

        player.move(platforms)

        # -----------------------------
        # Update enemies
        # -----------------------------

        for enemy in enemies:

            enemy.update()

        # -----------------------------
        # Enemy collision
        # -----------------------------

        for enemy in enemies:

            if player.rect.colliderect(
                enemy.rect
            ):

                # Jump on enemy

                if player.velocity_y > 0:

                    enemies.remove(enemy)

                    player.velocity_y = -9

                    player.score += 100

                    break

                else:

                    player.lives -= 1

                    player.reset_position()

                    if player.lives <= 0:

                        game_over = True

        # -----------------------------
        # Coin collision
        # -----------------------------

        for coin in coins[:]:

            if player.rect.colliderect(
                coin.rect
            ):

                coins.remove(coin)

                player.score += 50

        # -----------------------------
        # Fall from map
        # -----------------------------

        if player.rect.top > HEIGHT:

            player.lives -= 1

            player.reset_position()

            if player.lives <= 0:

                game_over = True

        # -----------------------------
        # Level complete
        # -----------------------------

        if len(coins) == 0:

            if not next_level():

                game_won = True


    # =================================================
    # DRAW BACKGROUND
    # =================================================

    screen.fill(SKY)

    # =================================================
    # CLOUDS
    # =================================================

    pygame.draw.circle(
        screen,
        WHITE,
        (150, 100),
        30
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (185, 100),
        40
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (225, 100),
        30
    )


    pygame.draw.circle(
        screen,
        WHITE,
        (700, 80),
        25
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (730, 80),
        35
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (765, 80),
        25
    )


    # =================================================
    # PLATFORMS
    # =================================================

    for platform in platforms:

        pygame.draw.rect(
            screen,
            BROWN,
            platform
        )

        pygame.draw.rect(
            screen,
            GREEN,
            (
                platform.x,
                platform.y,
                platform.width,
                8
            )
        )


    # =================================================
    # COINS
    # =================================================

    for coin in coins:

        coin.draw()


    # =================================================
    # ENEMIES
    # =================================================

    for enemy in enemies:

        enemy.draw()


    # =================================================
    # PLAYER
    # =================================================

    player.draw()


    # =================================================
    # UI
    # =================================================

    level_text = font.render(
        levels[current_level]["name"],
        True,
        BLACK
    )

    score_text = font.render(
        f"Score: {player.score}",
        True,
        BLACK
    )

    lives_text = font.render(
        f"Lives: {player.lives}",
        True,
        BLACK
    )

    coins_text = font.render(
        f"Coins: {len(coins)}",
        True,
        BLACK
    )

    screen.blit(
        level_text,
        (20, 20)
    )

    screen.blit(
        score_text,
        (20, 55)
    )

    screen.blit(
        lives_text,
        (20, 90)
    )

    screen.blit(
        coins_text,
        (20, 125)
    )


    # =================================================
    # CONTROLS
    # =================================================

    controls = small_font.render(
        "A/D or Arrow Keys = Move     SPACE = Jump",
        True,
        BLACK
    )

    screen.blit(
        controls,
        (600, 20)
    )


    # =================================================
    # LEVEL MESSAGE
    # =================================================

    if level_message_timer > 0:

        message = big_font.render(
            levels[current_level]["name"],
            True,
            BLUE
        )

        screen.blit(
            message,
            (
                WIDTH // 2 - message.get_width() // 2,
                170
            )
        )

        level_message_timer -= 1


    # =================================================
    # GAME OVER
    # =================================================

    if game_over:

        overlay = pygame.Surface(
            (WIDTH, HEIGHT)
        )

        overlay.set_alpha(170)

        overlay.fill(BLACK)

        screen.blit(
            overlay,
            (0, 0)
        )

        text = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        restart = font.render(
            "Press R to restart",
            True,
            WHITE
        )

        screen.blit(
            text,
            (
                WIDTH // 2 -
                text.get_width() // 2,
                230
            )
        )

        screen.blit(
            restart,
            (
                WIDTH // 2 -
                restart.get_width() // 2,
                320
            )
        )


    # =================================================
    # WIN
    # =================================================

    if game_won:

        overlay = pygame.Surface(
            (WIDTH, HEIGHT)
        )

        overlay.set_alpha(170)

        overlay.fill(BLACK)

        screen.blit(
            overlay,
            (0, 0)
        )

        text = big_font.render(
            "YOU COMPLETED THE GAME!",
            True,
            YELLOW
        )

        score = font.render(
            f"Final Score: {player.score}",
            True,
            WHITE
        )

        restart = font.render(
            "Press R to play again",
            True,
            WHITE
        )

        screen.blit(
            text,
            (
                WIDTH // 2 -
                text.get_width() // 2,
                200
            )
        )

        screen.blit(
            score,
            (
                WIDTH // 2 -
                score.get_width() // 2,
                300
            )
        )

        screen.blit(
            restart,
            (
                WIDTH // 2 -
                restart.get_width() // 2,
                350
            )
        )


    # =================================================
    # DISPLAY
    # =================================================

    pygame.display.flip()

    clock.tick(FPS)