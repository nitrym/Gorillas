import tkinter as tk
import math

# Fenster & Canvas
window = tk.Tk()
window.title("Gorillas in Python")
canvas = tk.Canvas(window, width=800, height=600, bg="skyblue")
canvas.pack()

# Gebäude und Gorillas
canvas.create_rectangle(50, 500, 150, 600, fill="gray")   # Gebäude links
canvas.create_rectangle(650, 500, 750, 600, fill="gray")  # Gebäude rechts

gorilla1 = canvas.create_oval(90, 470, 110, 490, fill="orange")  # Gorilla links
gorilla2 = canvas.create_oval(690, 470, 710, 490, fill="purple")  # Gorilla rechts

# Spieler-Eingabefelder
angle_label = tk.Label(window, text="Winkel (°):")
angle_label.pack()
angle_entry = tk.Entry(window)
angle_entry.pack()

speed_label = tk.Label(window, text="Stärke:")
speed_label.pack()
speed_entry = tk.Entry(window)
speed_entry.pack()

# Bananenwurf (Gorilla 1)
def throw_banana():
    try:
        angle_deg = float(angle_entry.get())
        speed = float(speed_entry.get())
    except ValueError:
        print("Ungültige Eingabe")
        return

    angle_rad = math.radians(angle_deg)
    x = 100
    y = 470
    vx = math.cos(angle_rad) * speed
    vy = -math.sin(angle_rad) * speed

    banana = canvas.create_oval(x, y, x + 10, y + 10, fill="yellow")

    def animate():
        nonlocal x, y, vx, vy
        # Schwerkraft
        vy += 0.5
        x += vx
        y += vy

        canvas.move(banana, vx, vy)

        # Treffer auf Gorilla 2?
        g2_coords = canvas.coords(gorilla2)
        b_coords = canvas.coords(banana)
        if (g2_coords[0] < b_coords[0] < g2_coords[2] and
            g2_coords[1] < b_coords[1] < g2_coords[3]):
            canvas.delete(banana)
            canvas.create_text(400, 100, text="Treffer! Gorilla 2 wurde getroffen!", font=("Arial", 16), fill="red")
            return

        # Boden oder außerhalb
        if y > 600 or x > 800:
            canvas.delete(banana)
            return

        canvas.after(30, animate)

    animate()

# Button zum Werfen
throw_button = tk.Button(window, text="Werfen (Gorilla 1)", command=throw_banana)
throw_button.pack()

window.mainloop()
