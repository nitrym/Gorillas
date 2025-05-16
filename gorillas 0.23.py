import tkinter as tk
import math
import random

window = tk.Tk()
window.title("Gorillas mit richtiger Gebäudeschädigung")
canvas = tk.Canvas(window, width=800, height=600, bg="skyblue")
canvas.pack()

# Gebäude
buildings = []
building_width = 50
building_hits = {}

for i in range(0, 800, building_width):
    height = random.randint(100, 300)
    building = canvas.create_rectangle(i, 600 - height, i + building_width, 600, fill="gray")
    buildings.append((building, i, 600 - height, i + building_width, 600))
    building_hits[i] = []

# Gorillas
gorilla1 = canvas.create_oval(70, 350, 90, 370, fill="orange")
gorilla2 = canvas.create_oval(710, 320, 730, 340, fill="purple")

# Eingabe
tk.Label(window, text="Winkel (°):").pack()
angle_entry = tk.Entry(window)
angle_entry.pack()

tk.Label(window, text="Stärke:").pack()
speed_entry = tk.Entry(window)
speed_entry.pack()

# Explosion zeichnen (mehrere Schadenspunkte)
def create_explosion(x, y):
    radius = 10
    offsets = [(0, 0), (-15, 0), (15, 0), (0, -15), (0, 15), (-10, -10), (10, -10), (-10, 10), (10, 10)]
    for dx, dy in offsets:
        cx = x + dx
        cy = y + dy
        canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, fill="black", outline="black")

# Wurf-Funktion
def throw_banana():
    try:
        angle = float(angle_entry.get())
        speed = float(speed_entry.get())
    except ValueError:
        print("Ungültige Eingabe")
        return

    angle_rad = math.radians(angle)
    x, y = 80, 350
    vx = math.cos(angle_rad) * speed
    vy = -math.sin(angle_rad) * speed

    banana = canvas.create_oval(x, y, x + 10, y + 10, fill="yellow")

    def animate():
        nonlocal x, y, vx, vy
        vy += 0.5
        x += vx
        y += vy
        canvas.move(banana, vx, vy)

        bx1, by1, bx2, by2 = canvas.coords(banana)

        # Treffer Gorilla 2
        gx1, gy1, gx2, gy2 = canvas.coords(gorilla2)
        if gx1 < bx1 < gx2 and gy1 < by1 < gy2:
            canvas.delete(banana)
            canvas.create_text(400, 100, text="Treffer! Gorilla 2!", font=("Arial", 16), fill="red")
            return

        # Treffer Gebäude
        for building_id, x1b, y1b, x2b, y2b in buildings:
            if x1b < bx1 < x2b and y1b < by1 < y2b:
                canvas.delete(banana)
                # Explosionszentrum
                center_x = (bx1 + bx2) / 2
                center_y = (by1 + by2) / 2
                create_explosion(center_x, center_y)
                return

        if x > 800 or y > 600:
            canvas.delete(banana)
            return

        canvas.after(30, animate)

    animate()

# Button
tk.Button(window, text="Werfen (Gorilla 1)", command=throw_banana).pack()

window.mainloop()
