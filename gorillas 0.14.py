import tkinter as tk
import math
import random

window = tk.Tk()
window.title("where banana?")
canvas = tk.Canvas(window, width=800, height=600, bg="skyblue")
canvas.pack()

# Parameter
building_width = 50
building_hits = {}  # X-Spalte → Liste von zerstörten Y-Bereichen
buildings = []

# Gebäude generieren
for i in range(0, 800, building_width):
    height = random.randint(100, 300)
    building = canvas.create_rectangle(i, 600 - height, i + building_width, 600, fill="gray")
    buildings.append((i, 600 - height, i + building_width, 600))  # (x1, y1, x2, y2)
    building_hits[i] = []  # Liste der zerstörten Y-Zonen

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

# Explosion zeichnen
def create_explosion(x, y, col_x):
    r = 10
    canvas.create_oval(x - r, y - r, x + r, y + r, fill="black", outline="black")
    # In Zerstörungsliste eintragen
    destroyed_zones = building_hits[col_x]
    destroyed_zones.append((y - 10, y + 10))  # Bereich oben/unten

# Prüfen ob Trefferstelle bereits zerstört
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
        center_x = (bx1 + bx2) / 2
        center_y = (by1 + by2) / 2

        # Gorilla-Treffer
        gx1, gy1, gx2, gy2 = canvas.coords(gorilla2)
        if gx1 < center_x < gx2 and gy1 < center_y < gy2:
            canvas.delete(banana)
            canvas.create_text(400, 100, text="Treffer! Gorilla 2!", font=("Arial", 16), fill="red")
            return

        # Gebäude-Treffer mit Durchschussprüfung
        for x1b, y1b, x2b, y2b in buildings:
            if x1b < center_x < x2b and y1b < center_y < y2b:
                col_x = int(x1b)
                if is_destroyed(col_x, center_y):
                    # Loch vorhanden → durchfliegen
                    break
                else:
                    # Neuer Schaden
                    create_explosion(center_x, center_y, col_x)
                    canvas.delete(banana)
                    return

        if x > 800 or y > 600:
            canvas.delete(banana)
            return

        canvas.after(30, animate)

    animate()

# Button
tk.Button(window, text="Werfen (Gorilla 1)", command=throw_banana).pack()
window.mainloop()
