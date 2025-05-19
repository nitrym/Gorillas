import tkinter as tk
import math
import random
import winsound  # Für Soundeffekte unter Windows

# Fenstergröße für 16:8 (2:1) Verhältnis
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 500

# Fenster & Canvas
window = tk.Tk()
window.title("Gorillas mit realistischer Gebäudeschädigung und Soundeffekten")
canvas = tk.Canvas(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="skyblue")
canvas.pack()

# Gebäudeparameter
building_width = 50
building_hits = {}  # Zerstörte Bereiche pro Spalte
buildings = []

# Gebäude erzeugen
for x in range(0, CANVAS_WIDTH, building_width):
    height = random.randint(100, 250)
    top = CANVAS_HEIGHT - height
    building = canvas.create_rectangle(x, top, x + building_width, CANVAS_HEIGHT, fill="gray")
    buildings.append((x, top, x + building_width, CANVAS_HEIGHT))  # (x1, y1, x2, y2)
    building_hits[x] = []  # noch keine Schäden

# Gorillas auf Gebäude setzen
def place_gorilla(building, color):
    x1, y1, x2, _ = building
    gx = (x1 + x2) / 2 - 10
    gy = y1 - 20
    return canvas.create_oval(gx, gy, gx + 20, gy + 20, fill=color)

left_building = buildings[1]
right_building = buildings[-2]

gorilla1 = place_gorilla(left_building, "orange")
gorilla2 = place_gorilla(right_building, "purple")

# Eingabe
tk.Label(window, text="Winkel (°):").pack()
angle_entry = tk.Entry(window)
angle_entry.pack()

tk.Label(window, text="Stärke:").pack()
speed_entry = tk.Entry(window)
speed_entry.pack()

# Funktion, um die Banane zu zeichnen (ohne Rotation)
def draw_banana(x, y):
    return canvas.create_arc(x, y, x + 40, y + 15, start=0, extent=180, fill="yellow", outline="orange", width=2)

# Explosion mit Schaden speichern
def create_explosion(x, y, col_x):
    # Soundeffekt für Explosion
    winsound.PlaySound("boom.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

    r = 10
    offsets = [(0,0), (10,0), (-10,0), (0,10), (0,-10), (7,7), (-7,7), (7,-7), (-7,-7)]
    for dx, dy in offsets:
        ex, ey = x + dx, y + dy
        canvas.create_oval(ex - r, ey - r, ex + r, ey + r, fill="black", outline="black")
        building_hits[col_x].append((ey - r, ey + r))

# Prüfen, ob Stelle zerstört ist
def is_destroyed(col_x, y):
    for y1, y2 in building_hits[col_x]:
        if y1 <= y <= y2:
            return True
    return False

# Wurf
def throw_banana():
    try:
        angle = float(angle_entry.get())
        speed = float(speed_entry.get())
    except ValueError:
        print("Ungültige Eingabe")
        return

    # Soundeffekt für Wurf
    winsound.PlaySound("yeet.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

    angle_rad = math.radians(angle)
    x, y = canvas.coords(gorilla1)[0] + 10, canvas.coords(gorilla1)[1]
    vx = math.cos(angle_rad) * speed
    vy = -math.sin(angle_rad) * speed

    banana = draw_banana(x, y)

    def animate():
        nonlocal x, y, vx, vy
        vy += 0.5  # Gravitation
        x += vx
        y += vy
        canvas.move(banana, vx, vy)

        bx1, by1, bx2, by2 = canvas.coords(banana)
        cx = (bx1 + bx2) / 2
        cy = (by1 + by2) / 2

        # Gorilla 2 treffen?
        gx1, gy1, gx2, gy2 = canvas.coords(gorilla2)
        if gx1 < cx < gx2 and gy1 < cy < gy2:
            canvas.delete(banana)
            canvas.create_text(CANVAS_WIDTH // 2, 50, text="Treffer! Gorilla 2!", font=("Arial", 16), fill="red")
            return

        # Gebäude-Kollision
        for x1b, y1b, x2b, y2b in buildings:
            if x1b < cx < x2b and y1b < cy < y2b:
                col_x = int(x1b)
                if is_destroyed(col_x, cy):
                    break  # durch beschädigten Bereich durchfliegen
                else:
                    canvas.delete(banana)
                    create_explosion(cx, cy, col_x)
                    return

        if x > CANVAS_WIDTH or y > CANVAS_HEIGHT or x < 0 or y < 0:
            canvas.delete(banana)
            return

        canvas.after(30, animate)

    animate()

# Button
tk.Button(window, text="Werfen (Gorilla 1)", command=throw_banana).pack()

window.mainloop()
