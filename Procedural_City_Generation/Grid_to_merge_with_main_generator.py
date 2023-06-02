import pygame

# Wymiary okna
WIDTH = 800
HEIGHT = 600

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)


def generate_grid(polygon_vertices):
    # Utworzenie siatki ulic
    grid = []
    min_x = min(polygon_vertices, key=lambda v: v[0])[0]
    max_x = max(polygon_vertices, key=lambda v: v[0])[0]
    min_y = min(polygon_vertices, key=lambda v: v[1])[1]
    max_y = max(polygon_vertices, key=lambda v: v[1])[1]
    # Rozmiar komórki siatki -- Jak chcesz zmienić rozmiary siatki (mniejsze/większe)
    step = 25

    # Obliczenie odległości od wielokąta ograniczającego na początku o 24
    distance = 24

    # Obliczenie nowych granic na podstawie odległości
    min_x -= distance
    max_x += distance
    min_y -= distance
    max_y += distance

    for x in range(min_x, max_x + step, step):
        for y in range(min_y, max_y + step, step):
            point = (x, y)
            if is_inside_polygon(point, polygon_vertices):
                grid.append(point)

    return grid


def is_inside_polygon(point, polygon_vertices):
    # Sprawdzenie, czy punkt znajduje się wewnątrz wielokąta (czy PUNKT jest w ograniczonym polu)
    vertices = len(polygon_vertices)
    x, y = point
    inside = False

    p1x, p1y = polygon_vertices[0]
    for i in range(vertices + 1):
        p2x, p2y = polygon_vertices[i % vertices]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


def draw_polygon(screen, polygon_vertices):
    # Rysowanie obwodu wielokąta (Pomocniczo)
    pygame.draw.polygon(screen, GRAY, polygon_vertices, 1)


def draw_grid(screen, grid, polygon_vertices):
    # Rysowanie połączeń w pionie i poziomie wewnątrz wielokąta (tak jak początkowo rysowałem)
    for i in range(len(grid)):
        x1, y1 = grid[i]
        #pygame.draw.circle(screen, BLACK, (x1, y1), 3)
        for j in range(i+1, len(grid)):
            x2, y2 = grid[j]
            if (x1 == x2 or y1 == y2) and is_inside_polygon((x2, y2), polygon_vertices) and not on_polygon_boundary((x1, y1), polygon_vertices):
                if not intersects_polygon((x1, y1), (x2, y2), polygon_vertices):
                    pygame.draw.line(screen, BLACK, (x1, y1), (x2, y2))


def intersects_polygon(point1, point2, polygon_vertices):
    # Sprawdzenie, czy linia między dwoma punktami przecina wielokąt (Ważne - sprawdza, czy połączenie nie wychodzi za wielokąt)
    for i in range(len(polygon_vertices)):
        p1 = polygon_vertices[i]
        p2 = polygon_vertices[(i + 1) % len(polygon_vertices)]
        if line_intersects_segment(point1, point2, p1, p2):
            return True
    return False


def line_intersects_segment(point1, point2, segment1, segment2):
    # Sprawdzenie, czy linia między dwoma punktami przecina odcinek (pomocnicza funkcja do sprawdzania przecięcia wielokąta)
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = segment1
    x4, y4 = segment2

    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if den == 0:
        return False

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

    if t >= 0 and t <= 1 and u >= 0 and u <= 1:
        return True

    return False


def on_polygon_boundary(point, polygon_vertices):
    # Sprawdzenie, czy punkt leży na granicy wielokąta
    for i in range(len(polygon_vertices)):
        p1 = polygon_vertices[i]
        p2 = polygon_vertices[(i + 1) % len(polygon_vertices)]
        if point_on_segment(point, p1, p2):
            return True
    return False


def point_on_segment(point, segment1, segment2):
    # Sprawdzenie, czy punkt leży na odcinku
    x, y = point
    x1, y1 = segment1
    x2, y2 = segment2
    return min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2) and (x - x1) * (y2 - y1) == (x2 - x1) * (y - y1)

# Tutaj już tylko wywołanie pygame, żadnej implementacji generowania


# Komentarz dla osoby mergującej tą siatkę z City Generation
# Trzeba wywalić na pewno wywoływanie okna pygame, pozatym przekazać wierzchołki/proste do polygon_vertices i zmienić nazwę main


def main():
    # Inicjalizacja Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Generator siatki ulic")

    # Wierzchołki wielokąta (Podajesz punkty przez jakie przechodzą proste, on tym ogranicza siatke)
    polygon_vertices = [
        (200, 100),
        (730, 150),
        (730, 500),
        (400, 375),
        (100, 500)
    ]

    # Generowanie siatki ulic
    grid = generate_grid(polygon_vertices)

    # Główna pętla programu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Czyszczenie ekranu
        screen.fill(WHITE)

        # Rysowanie wielokąta
        draw_polygon(screen, polygon_vertices)

        # Rysowanie siatki ulic
        draw_grid(screen, grid, polygon_vertices)

        # Aktualizacja ekranu
        pygame.display.flip()

    # Zamknięcie Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
