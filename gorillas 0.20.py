import tkinter as tk
import math
import random

# Fenster und Canvas
window = tk.Tk()
window.title("Gorillas mit Gebäuden und Zerstörung")
canvas = tk.Canvas(window, width=800, height=600, bg="skyblue")
canvas.pack()

# Liste für Gebäude
buildings = []

# Gebäude generieren
building_width = 50
for i in range(0, 800, building_width):
    height = random.randint(100, 300)
    building = canvas.create_rectangle(i, 600 - height, i + building_width, 600, fill="gray", tags="building")
    buildings.append((building, i, 600 - height, i + building_width, 600))  # (id, x1, y1, x2, y2)

# Gorillas auf festen Gebäuden platzieren
gorilla1 = canvas.create_oval(70, 350, 90, 370, fill="orange")
gorilla2 = canvas.create_oval(710, 320, 730, 340, fill="purple")

# Eingabefelder
angle_label = tk.Label(window, text="Winkel (°):")
angle_label.pack()
angle_entry = tk.Entry(window)
angle_entry.pack()

speed_label = tk.Label(window, text="Stärke:")
speed_label.pack()
speed_entry = tk.Entry(window)
speed_entry.pack()

# Bananenwurf mit Zerstörung
def throw_banana():
    try:
        angle_deg = float(angle_entry.get())
        speed = float(speed_entry.get())
    except ValueError:
        print("Ungültige Eingabe")
        return

    angle_rad = math.radians(angle_deg)
    x = 80  # Startposition (Mitte Gorilla 1)
    y = 350
    vx = math.cos(angle_rad) * speed
    vy = -math.sin(angle_rad) * speed

    banana = canvas.create_oval(x, y, x + 10, y + 10, fill="yellow")

    def animate():
        nonlocal x, y, vx, vy
        vy += 0.5  # Schwerkraft
        x += vx
        y += vy

        canvas.move(banana, vx, vy)

        # Koordinaten aktualisieren
        bx1, by1, bx2, by2 = canvas.coords(banana)

        # Kollision mit Gorilla 2
        gx1, gy1, gx2, gy2 = canvas.coords(gorilla2)
        if gx1 < bx1 < gx2 and gy1 < by1 < gy2:
            canvas.delete(banana)
            canvas.create_text(400, 100, text="Treffer! Gorilla 2 wurde getroffen!", font=("Arial", 16), fill="red")
            return

        # Kollision mit Gebäuden
        for building_id, x1b, y1b, x2b, y2b in buildings:
            if x1b < bx1 < x2b and y1b < by1 < y2b:
                canvas.delete(banana)
                # Zerstörungseffekt: Loch machen
                explosion = canvas.create_oval(bx1 - 10, by1 - 10, bx1 + 10, by1 + 10, fill="black", outline="black")
                canvas.tag_raise(explosion)  # über das Gebäude legen
                return

        # Außerhalb des Fensters
        if x > 800 or y > 600:
            canvas.delete(banana)
            return

        canvas.after(30, animate)

    animate()

# Button zum Werfen
throw_button = tk.Button(window, text="Werfen (Gorilla 1)", command=throw_banana)
throw_button.pack()

window.mainloop()
