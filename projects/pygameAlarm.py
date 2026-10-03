import pygame
import datetime
import os

# -----------------------------
# Initialize Pygame
# -----------------------------
pygame.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alarm Clock")

clock = pygame.time.Clock()

# -----------------------------
# Fonts
# -----------------------------
title_font = pygame.font.Font(None, 60)
time_font = pygame.font.Font(None, 90)
normal_font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 30)

# -----------------------------
# Input variables
# -----------------------------
alarm_input = ""
alarm_time = None
input_active = False
alarm_playing = False

# -----------------------------
# Buttons / input box
# -----------------------------
input_box = pygame.Rect(250, 260, 300, 60)
set_button = pygame.Rect(280, 340, 240, 60)
stop_button = pygame.Rect(280, 410, 240, 50)

# -----------------------------
# MP3 file
# -----------------------------
sound_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Baby_Cry_Long.mp3"
)

# -----------------------------
# Main loop
# -----------------------------
running = True

while running:

    # -------------------------
    # Events
    # -------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:

            # Input box clicked
            if input_box.collidepoint(event.pos):
                input_active = True

            else:
                input_active = False

            # Set alarm button
            if set_button.collidepoint(event.pos):

                try:
                    datetime.datetime.strptime(alarm_input, "%H:%M:%S")

                    alarm_time = alarm_input

                    print(f"Alarm set for {alarm_time}")

                except ValueError:
                    alarm_time = None
                    print("Please enter time in HH:MM:SS format.")

            # Stop alarm button
            if stop_button.collidepoint(event.pos):

                if alarm_playing:
                    pygame.mixer.music.stop()
                    alarm_playing = False
                    print("Alarm stopped.")

        # Keyboard input
        if event.type == pygame.KEYDOWN and input_active:

            # Backspace
            if event.key == pygame.K_BACKSPACE:
                alarm_input = alarm_input[:-1]

            # Enter
            elif event.key == pygame.K_RETURN:

                try:
                    datetime.datetime.strptime(alarm_input, "%H:%M:%S")

                    alarm_time = alarm_input

                    print(f"Alarm set for {alarm_time}")

                except ValueError:
                    alarm_time = None
                    print("Please enter time in HH:MM:SS format.")

            # Normal typing
            else:

                # Only allow numbers and :
                if event.unicode.isdigit() or event.unicode == ":":
                    alarm_input += event.unicode

    # -------------------------
    # Get current time
    # -------------------------
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    # -------------------------
    # Check alarm
    # -------------------------
    if alarm_time == current_time and not alarm_playing:

        print("WAKE UP!")

        if os.path.exists(sound_file):

            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()

            alarm_playing = True

        else:
            print("ERROR: MP3 file not found.")
            print(sound_file)

    # -------------------------
    # Background
    # -------------------------
    screen.fill((30, 30, 30))

    # -------------------------
    # Title
    # -------------------------
    title_text = title_font.render(
        "ALARM CLOCK",
        True,
        (255, 255, 255)
    )

    title_rect = title_text.get_rect(
        center=(WIDTH // 2, 50)
    )

    screen.blit(title_text, title_rect)

    # -------------------------
    # Current time
    # -------------------------
    current_text = time_font.render(
        current_time,
        True,
        (255, 255, 255)
    )

    current_rect = current_text.get_rect(
        center=(WIDTH // 2, 140)
    )

    screen.blit(current_text, current_rect)

    # -------------------------
    # Input box
    # -------------------------
    pygame.draw.rect(
        screen,
        (70, 70, 70),
        input_box
    )

    pygame.draw.rect(
        screen,
        (255, 255, 255),
        input_box,
        2
    )

    if alarm_input == "":
        input_display = "HH:MM:SS"
    else:
        input_display = alarm_input

    input_text = normal_font.render(
        input_display,
        True,
        (255, 255, 255)
    )

    screen.blit(
        input_text,
        (input_box.x + 15, input_box.y + 12)
    )

    # -------------------------
    # Set Alarm button
    # -------------------------
    pygame.draw.rect(
        screen,
        (50, 120, 200),
        set_button
    )

    set_text = normal_font.render(
        "SET ALARM",
        True,
        (255, 255, 255)
    )

    set_rect = set_text.get_rect(
        center=set_button.center
    )

    screen.blit(set_text, set_rect)

    # -------------------------
    # Stop Alarm button
    # -------------------------
    pygame.draw.rect(
        screen,
        (180, 60, 60),
        stop_button
    )

    stop_text = small_font.render(
        "STOP ALARM",
        True,
        (255, 255, 255)
    )

    stop_rect = stop_text.get_rect(
        center=stop_button.center
    )

    screen.blit(stop_text, stop_rect)

    # -------------------------
    # Alarm status
    # -------------------------
    if alarm_time:

        status = f"Alarm set for {alarm_time}"

    else:

        status = "No alarm set"

    status_text = small_font.render(
        status,
        True,
        (255, 255, 255)
    )

    status_rect = status_text.get_rect(
        center=(WIDTH // 2, 485)
    )

    screen.blit(status_text, status_rect)

    # -------------------------
    # Update display
    # -------------------------
    pygame.display.update()

    # Limit FPS
    clock.tick(60)

# -----------------------------
# Quit
# -----------------------------
pygame.mixer.music.stop()
pygame.quit()