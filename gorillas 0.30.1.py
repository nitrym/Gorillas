import tkinter as tk
import math
import random
import winsound  # Für Soundeffekte unter Windows

# Fenstergröße für 16:8 (2:1) Verhältnis
CANVAS_WIDTH = 1000  # Breite des Zeichenfensters
CANVAS_HEIGHT = 500  # Höhe des Zeichenfensters

# Fenster & Canvas
window = tk.Tk()
window.title("Banana Joe _gamesound_comments")
canvas = tk.Canvas(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="skyblue")  # Zeichenfläche mit Hintergrundfarbe
canvas.pack()

# Gebäudeparameter
building_width = 50        # Breite eines einzelnen Gebäudes
building_hits = {}         # Dictionary: x-Position → Liste zerstörter Höhenbereiche
buildings = []             # Liste aller Gebäude mit ihren Koordinaten (x1, y1, x2, y2)

# Gebäude erzeugen
for x in range(0, CANVAS_WIDTH, building_width):
    height = random.randint(100, 250)                   # Zufällige Höhe zwischen 100 und 250 Pixel
    top = CANVAS_HEIGHT - height                        # Oberkante des Gebäudes
    building = canvas.create_rectangle(x, top, x + building_width, CANVAS_HEIGHT, fill="gray")
    buildings.append((x, top, x + building_width, CANVAS_HEIGHT))  # Koordinaten speichern
    building_hits[x] = []  # Noch keine Schäden an dieser Spalte

# Gorillas auf Gebäude setzen
def place_gorilla(building, color):
    x1, y1, x2, _ = building         # Gebäude-Koordinaten entpacken
    gx = (x1 + x2) / 2 - 10          # Gorilla-X: Mittelpunkt des Gebäudes, um 10 Pixel versetzt
    gy = y1 - 20                     # Gorilla-Y: über der Oberkante des Gebäudes
    return canvas.create_oval(gx, gy, gx + 20, gy + 20, fill=color)  # Kreisförmiger Gorilla

left_building = buildings[1]         # Linker Gorilla auf dem zweiten Gebäude von links
right_building = buildings[-2]      # Rechter Gorilla auf dem zweitletzten Gebäude

gorilla1 = place_gorilla(left_building, "orange")
gorilla2 = place_gorilla(right_building, "purple")

# Eingabe für Wurfwinkel
tk.Label(window, text="Winkel (°):").pack()
angle_entry = tk.Entry(window)
angle_entry.pack()

# Eingabe für Wurfstärke
tk.Label(window, text="Stärke:").pack()
speed_entry = tk.Entry(window)
speed_entry.pack()

# Funktion zum Zeichnen der Banane (als Halbkreis)
def draw_banana(x, y):
    return canvas.create_arc(x, y, x + 40, y + 15, start=0, extent=180, fill="yellow", outline="orange", width=2)

# Explosion erzeugen & zerstörte Bereiche merken
def create_explosion(x, y, col_x):
    winsound.PlaySound("boom.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)  # Explosion-Sound abspielen

    r = 10  # Radius der Explosionskreise
    offsets = [  # Versetzte Kreise rund um den Einschlagspunkt
        (0,0), (10,0), (-10,0), (0,10), (0,-10),
        (7,7), (-7,7), (7,-7), (-7,-7)
    ]
    for dx, dy in offsets:
        ex, ey = x + dx, y + dy                       # Zentrum des einzelnen Explosionskreises
        canvas.create_oval(ex - r, ey - r, ex + r, ey + r, fill="black", outline="black")
        building_hits[col_x].append((ey - r, ey + r)) # Explosionsbereich als zerstört merken

# Prüfen, ob ein bestimmter Höhenbereich bereits zerstört wurde
def is_destroyed(col_x, y):
    for y1, y2 in building_hits[col_x]:  # Alle bekannten Schadensbereiche in der Spalte
        if y1 <= y <= y2:                # Y liegt innerhalb eines zerstörten Bereichs
            return True
    return False

# Banane werfen
def throw_banana():
    try:
        angle = float(angle_entry.get())  # Winkel aus Eingabefeld (in Grad)
        speed = float(speed_entry.get())  # Stärke aus Eingabefeld
    except ValueError:
        print("Ungültige Eingabe")
        return

    # Wurf-Soundeffekt
    winsound.PlaySound("yeet.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

    angle_rad = math.radians(angle)       # Umrechnung Grad → Bogenmaß
    x, y = canvas.coords(gorilla1)[0] + 10, canvas.coords(gorilla1)[1]  # Startposition: Mitte von Gorilla 1
    vx = math.cos(angle_rad) * speed      # X-Geschwindigkeit der Banane
    vy = -math.sin(angle_rad) * speed     # Y-Geschwindigkeit (negativ = nach oben)

    banana = draw_banana(x, y)            # Banane auf Canvas zeichnen

    # Animationsfunktion
    def animate():
        nonlocal x, y, vx, vy
        vy += 0.5               # Schwerkraft: Y-Geschwindigkeit nimmt zu
        x += vx                 # Neue X-Position
        y += vy                 # Neue Y-Position
        canvas.move(banana, vx, vy)  # Banane bewegen

        # Koordinaten der Banane holen (bounding box des Halbkreises)
        bx1, by1, bx2, by2 = canvas.coords(banana)
        cx = (bx1 + bx2) / 2    # Mittelpunkt X der Banane (für Kollisionsprüfung)
        cy = (by1 + by2) / 2    # Mittelpunkt Y der Banane

        # Trefferprüfung für Gorilla 2
        gx1, gy1, gx2, gy2 = canvas.coords(gorilla2)  # Bounding Box von Gorilla 2
        if gx1 < cx < gx2 and gy1 < cy < gy2:
            canvas.delete(banana)
            canvas.create_text(CANVAS_WIDTH // 2, 50, text="Treffer! Gorilla 2!", font=("Arial", 16), fill="red")
            return

        # Gebäude-Kollision prüfen
        for x1b, y1b, x2b, y2b in buildings:  # Jede Gebäude-Bounding-Box
            if x1b < cx < x2b and y1b < cy < y2b:  # Kollision innerhalb der Gebäudefläche
                col_x = int(x1b)             # Spalte identifizieren (linker Rand des Gebäudes)
                if is_destroyed(col_x, cy):  # Ist dieser Höhenbereich bereits zerstört?
                    break                    # Banane fliegt durch
                else:
                    canvas.delete(banana)
                    create_explosion(cx, cy, col_x)
                    return

        # Wenn die Banane das Spielfeld verlässt
        if x > CANVAS_WIDTH or y > CANVAS_HEIGHT or x < 0 or y < 0:
            canvas.delete(banana)
            return

        canvas.after(30, animate)  # Nächster Animationsschritt in 30 ms

    animate()  # Animation starten

# Button zum Auslösen des Wurfs
tk.Button(window, text="Werfen (Gorilla 1)", command=throw_banana).pack()

window.mainloop()
