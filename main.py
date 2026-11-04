
import tkinter as tk
import random
import math

# ============================================================
# REALISTIC PROCEDURAL CITY
# NO EXTERNAL LIBRARIES
# ============================================================

WIDTH = 1200
HEIGHT = 750

random.seed(42)

root = tk.Tk()
root.title("Python - Procedural City")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="#050814",
    highlightthickness=0
)

canvas.pack()

# ============================================================
# COLOR UTILITIES
# ============================================================

def rgb(r, g, b):
    return f"#{max(0,min(255,int(r))):02x}{max(0,min(255,int(g))):02x}{max(0,min(255,int(b))):02x}"


# ============================================================
# SKY GRADIENT
# ============================================================

sky_top = (4, 7, 22)
sky_bottom = (44, 30, 55)

for y in range(470):

    t = y / 470

    r = sky_top[0] * (1 - t) + sky_bottom[0] * t
    g = sky_top[1] * (1 - t) + sky_bottom[1] * t
    b = sky_top[2] * (1 - t) + sky_bottom[2] * t

    canvas.create_line(
        0,
        y,
        WIDTH,
        y,
        fill=rgb(r, g, b)
    )


# ============================================================
# STARS
# ============================================================

for _ in range(220):

    x = random.randint(0, WIDTH)
    y = random.randint(20, 310)

    size = random.choice([1, 1, 1, 1, 2])

    color = random.choice([
        "#ffffff",
        "#dce7ff",
        "#fff2c4",
        "#aebce0"
    ])

    canvas.create_oval(
        x-size,
        y-size,
        x+size,
        y+size,
        fill=color,
        outline=""
    )


# ============================================================
# MOON + HALO
# ============================================================

canvas.create_oval(
    850,
    65,
    1030,
    245,
    outline="#262a4c",
    width=3
)

canvas.create_oval(
    875,
    90,
    1005,
    220,
    fill="#fff5c7",
    outline=""
)

# moon craters

for _ in range(15):

    x = random.randint(900, 975)
    y = random.randint(120, 195)
    r = random.randint(2, 7)

    canvas.create_oval(
        x-r,
        y-r,
        x+r,
        y+r,
        fill="#e4dba9",
        outline=""
    )


# ============================================================
# DISTANT ATMOSPHERIC CITY
# ============================================================

horizon = 455

x = -30

while x < WIDTH:

    w = random.randint(35, 75)
    h = random.randint(80, 190)

    y = horizon - h

    color = random.choice([
        "#11162b",
        "#14182d",
        "#171b31",
        "#191d34"
    ])

    canvas.create_rectangle(
        x,
        y,
        x+w,
        horizon,
        fill=color,
        outline=""
    )

    # distant windows

    for wx in range(x+8, x+w-5, 14):

        for wy in range(y+15, horizon-10, 22):

            if random.random() > 0.6:

                canvas.create_rectangle(
                    wx,
                    wy,
                    wx+4,
                    wy+6,
                    fill=random.choice([
                        "#6b6042",
                        "#766844",
                        "#4f5260"
                    ]),
                    outline=""
                )

    x += w - 2


# ============================================================
# MAIN BUILDINGS
# ============================================================

building_data = []

x = -60

while x < WIDTH + 50:

    width = random.randint(75, 145)
    height = random.randint(180, 380)

    y = horizon - height

    building_type = random.randint(1, 5)

    # --------------------------------------------------------
    # BUILDING COLOR
    # --------------------------------------------------------

    color = random.choice([
        "#171b29",
        "#1d202e",
        "#222533",
        "#292b38",
        "#20242f",
        "#30313b",
        "#191d2a"
    ])

    # Main structure

    canvas.create_rectangle(
        x,
        y,
        x + width,
        horizon,
        fill=color,
        outline="#363947"
    )

    # --------------------------------------------------------
    # SIDE SHADOW
    # --------------------------------------------------------

    shadow_width = int(width * 0.12)

    canvas.create_rectangle(
        x,
        y,
        x + shadow_width,
        horizon,
        fill="#10131e",
        outline=""
    )

    # --------------------------------------------------------
    # ROOF
    # --------------------------------------------------------

    if building_type == 1:

        canvas.create_rectangle(
            x + width*.15,
            y-12,
            x + width*.85,
            y,
            fill="#12151f",
            outline=""
        )

    elif building_type == 2:

        canvas.create_rectangle(
            x + width*.30,
            y-25,
            x + width*.70,
            y,
            fill="#151823",
            outline=""
        )

        canvas.create_line(
            x + width*.5,
            y-25,
            x + width*.5,
            y-60,
            fill="#515668",
            width=2
        )

    elif building_type == 3:

        canvas.create_polygon(
            x,
            y,
            x + width*.5,
            y-28,
            x + width,
            y,
            fill="#171a26",
            outline=""
        )

    # --------------------------------------------------------
    # WINDOWS
    # --------------------------------------------------------

    window_columns = max(3, int(width / 22))
    window_rows = max(6, int(height / 28))

    for col in range(window_columns):

        wx = x + 12 + col * ((width-24) / max(1, window_columns-1))

        for row in range(window_rows):

            wy = y + 18 + row * 27

            if wy > horizon - 20:
                continue

            # realistic random lights
            probability = 0.58

            if random.random() < probability:

                window_color = random.choice([
                    "#ffd36a",
                    "#ffe19a",
                    "#ffbd55",
                    "#f4d27d",
                    "#a6d8ff",
                    "#d5e7ff"
                ])

                ww = random.choice([5, 6, 7])
                wh = random.choice([8, 9, 10])

                canvas.create_rectangle(
                    wx,
                    wy,
                    wx+ww,
                    wy+wh,
                    fill=window_color,
                    outline=""
                )

                # dark frame

                canvas.create_rectangle(
                    wx-2,
                    wy-2,
                    wx+ww+2,
                    wy+wh+2,
                    outline="#12151e"
                )

    # --------------------------------------------------------
    # HORIZONTAL FACADE LINES
    # --------------------------------------------------------

    if building_type in [2, 4, 5]:

        for yy in range(int(y+35), horizon, 55):

            canvas.create_line(
                x+5,
                yy,
                x+width-5,
                yy,
                fill="#343744",
                width=1
            )

    # --------------------------------------------------------
    # VERTICAL GLASS STRIPS
    # --------------------------------------------------------

    if building_type == 4:

        for xx in range(
            int(x+width*.25),
            int(x+width*.9),
            25
        ):

            canvas.create_rectangle(
                xx,
                y+5,
                xx+10,
                horizon,
                fill="#182331",
                outline=""
            )

            # reflected blue lights

            for yy in range(int(y+20), horizon, 35):

                if random.random() > .4:

                    canvas.create_rectangle(
                        xx+2,
                        yy,
                        xx+7,
                        yy+12,
                        fill="#537c91",
                        outline=""
                    )

    building_data.append(
        (x, y, width, height)
    )

    x += width - 5


# ============================================================
# BUILDING EDGE LIGHTS
# ============================================================

for x, y, width, height in building_data:

    if random.random() > 0.65:

        canvas.create_line(
            x + width,
            y,
            x + width,
            horizon,
            fill="#414455",
            width=1
        )


# ============================================================
# GROUND
# ============================================================

canvas.create_rectangle(
    0,
    horizon,
    WIDTH,
    HEIGHT,
    fill="#090b10",
    outline=""
)


# ============================================================
# SIDEWALK
# ============================================================

canvas.create_rectangle(
    0,
    horizon,
    WIDTH,
    horizon + 28,
    fill="#36373d",
    outline=""
)

canvas.create_line(
    0,
    horizon + 28,
    WIDTH,
    horizon + 28,
    fill="#5a5b61",
    width=2
)


# ============================================================
# ROAD
# ============================================================

road_top = horizon + 28
road_bottom = HEIGHT

canvas.create_polygon(
    180,
    road_top,
    WIDTH - 180,
    road_top,
    WIDTH,
    road_bottom,
    0,
    road_bottom,
    fill="#0b0d12",
    outline=""
)


# ============================================================
# ROAD EDGE LINES
# ============================================================

canvas.create_line(
    180,
    road_top,
    0,
    road_bottom,
    fill="#303238",
    width=3
)

canvas.create_line(
    WIDTH-180,
    road_top,
    WIDTH,
    road_bottom,
    fill="#303238",
    width=3
)


# ============================================================
# PERSPECTIVE ROAD LINES
# ============================================================

vanishing_x = WIDTH // 2
vanishing_y = road_top

# lane boundaries

for bottom_x in [280, 600, 920]:

    canvas.create_line(
        vanishing_x,
        vanishing_y,
        bottom_x,
        HEIGHT,
        fill="#1b1d22",
        width=2
    )


# ============================================================
# CENTER DASHED LINES
# ============================================================

road_markings = []

for i in range(8):

    t = i / 8

    y = road_top + 50 + t*t * 250

    width = 8 + t * 35

    x = WIDTH / 2

    line = canvas.create_rectangle(
        x-width/2,
        y,
        x+width/2,
        y + 5 + t*10,
        fill="#d8bc62",
        outline=""
    )

    road_markings.append(line)


# ============================================================
# STREET LIGHT FUNCTION
# ============================================================

street_lights = []

def create_street_light(x, y, scale):

    pole_height = 105 * scale

    pole = canvas.create_line(
        x,
        y,
        x,
        y-pole_height,
        fill="#4e515b",
        width=max(1, int(4*scale))
    )

    arm = canvas.create_line(
        x,
        y-pole_height,
        x+35*scale,
        y-pole_height,
        fill="#4e515b",
        width=max(1, int(3*scale))
    )

    lamp = canvas.create_oval(
        x+29*scale,
        y-pole_height-4,
        x+41*scale,
        y-pole_height+8,
        fill="#ffe39a",
        outline=""
    )

    glow = canvas.create_oval(
        x+10*scale,
        y-pole_height-20*scale,
        x+60*scale,
        y-pole_height+30*scale,
        outline="#4e4736"
    )

    street_lights.append(
        (pole, arm, lamp, glow)
    )


create_street_light(105, 470, 1)
create_street_light(1090, 470, 1)

create_street_light(240, 530, .7)
create_street_light(960, 530, .7)


# ============================================================
# TREES
# ============================================================

def create_tree(x, y, scale):

    trunk_w = 7 * scale

    canvas.create_rectangle(
        x-trunk_w/2,
        y-55*scale,
        x+trunk_w/2,
        y,
        fill="#30231d",
        outline=""
    )

    # multiple foliage layers

    for i in range(4):

        offset_x = random.randint(-12, 12) * scale
        offset_y = i * 10 * scale

        radius = (25 - i*3) * scale

        canvas.create_oval(
            x-radius+offset_x,
            y-80*scale-offset_y,
            x+radius+offset_x,
            y-35*scale-offset_y,
            fill=random.choice([
                "#17291f",
                "#1b3224",
                "#203a29",
                "#14271e"
            ]),
            outline=""
        )


create_tree(70, 465, .8)
create_tree(1130, 465, .8)
create_tree(155, 480, .6)
create_tree(1040, 480, .6)


# ============================================================
# CARS
# ============================================================

cars = []


def create_car(x, y, scale, color, speed):

    w = 82 * scale
    h = 27 * scale

    body = canvas.create_polygon(
        x,
        y,
        x+w,
        y,
        x+w-5*scale,
        y+h,
        x+5*scale,
        y+h,
        fill=color,
        outline="#111318"
    )

    roof = canvas.create_polygon(
        x+w*.18,
        y,
        x+w*.34,
        y-h*.65,
        x+w*.70,
        y-h*.65,
        x+w*.87,
        y,
        fill=color,
        outline="#111318"
    )

    front_window = canvas.create_polygon(
        x+w*.39,
        y-2,
        x+w*.47,
        y-h*.52,
        x+w*.62,
        y-h*.52,
        x+w*.62,
        y-2,
        fill="#1c2b3a",
        outline=""
    )

    rear_window = canvas.create_polygon(
        x+w*.24,
        y-2,
        x+w*.35,
        y-h*.52,
        x+w*.43,
        y-h*.52,
        x+w*.37,
        y-2,
        fill="#182737",
        outline=""
    )

    # wheels

    wheel1 = canvas.create_oval(
        x+w*.12,
        y+h-4,
        x+w*.29,
        y+h+13,
        fill="#030304",
        outline=""
    )

    wheel2 = canvas.create_oval(
        x+w*.71,
        y+h-4,
        x+w*.88,
        y+h+13,
        fill="#030304",
        outline=""
    )

    # headlights

    light1 = canvas.create_rectangle(
        x+w-4,
        y+5,
        x+w+2,
        y+10,
        fill="#fff4b0",
        outline=""
    )

    light2 = canvas.create_rectangle(
        x+w-4,
        y+h-11,
        x+w+2,
        y+h-6,
        fill="#fff4b0",
        outline=""
    )

    # rear red lights

    tail1 = canvas.create_rectangle(
        x-2,
        y+5,
        x+3,
        y+10,
        fill="#d52f35",
        outline=""
    )

    tail2 = canvas.create_rectangle(
        x-2,
        y+h-11,
        x+3,
        y+h-6,
        fill="#d52f35",
        outline=""
    )

    objects = [
        body,
        roof,
        front_window,
        rear_window,
        wheel1,
        wheel2,
        light1,
        light2,
        tail1,
        tail2
    ]

    cars.append({
        "objects": objects,
        "x": x,
        "speed": speed,
        "width": w
    })


# distant traffic

create_car(-200, 525, .55, "#b63c42", 2.2)
create_car(350, 545, .48, "#3e76ad", 1.8)
create_car(750, 515, .55, "#c68c35", 2.1)

# foreground traffic

create_car(-150, 620, 1.25, "#b8393f", 4.2)
create_car(650, 590, .95, "#3d83bd", 3.4)
create_car(1050, 650, 1.4, "#4a9c69", 4.7)


# ============================================================
# REFLECTIONS ON ROAD
# ============================================================

reflections = []

for _ in range(30):

    x = random.randint(50, WIDTH-50)
    y = random.randint(500, 690)

    length = random.randint(10, 50)

    reflection = canvas.create_line(
        x,
        y,
        x+length,
        y,
        fill=random.choice([
            "#2a2420",
            "#302a22",
            "#242832",
            "#27251f"
        ]),
        width=random.randint(1, 3)
    )

    reflections.append(reflection)


# ============================================================
# CITY LABEL
# ============================================================

canvas.create_text(
    WIDTH/2,
    32,
    text="PYTHON GENERATED CITY",
    fill="#e8eaf0",
    font=("Arial", 21, "bold")
)

canvas.create_text(
    WIDTH/2,
    60,
    text="100% PROCEDURAL",
    fill="#85899b",
    font=("Arial", 10)
)


# ============================================================
# ANIMATION
# ============================================================

def animate():

    # --------------------------------------------------------
    # MOVE CARS
    # --------------------------------------------------------

    for car in cars:

        car["x"] += car["speed"]

        if car["x"] > WIDTH + 150:

            car["x"] = -180

        for obj in car["objects"]:

            canvas.move(
                obj,
                car["speed"],
                0
            )

    # --------------------------------------------------------
    # RANDOM WINDOW FLICKER
    # --------------------------------------------------------

    if random.random() < 0.04:

        x, y, width, height = random.choice(
            building_data
        )

    # --------------------------------------------------------
    # STREET LIGHT SUBTLE ANIMATION
    # --------------------------------------------------------

    for pole, arm, lamp, glow in street_lights:

        if random.random() < 0.02:

            canvas.itemconfig(
                lamp,
                fill=random.choice([
                    "#ffe39a",
                    "#fff0b0",
                    "#ffd778"
                ])
            )

    root.after(
        30,
        animate
    )


# ============================================================
# START
# ============================================================

animate()

root.mainloop()

