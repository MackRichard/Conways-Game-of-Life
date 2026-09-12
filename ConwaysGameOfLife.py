import random
import pygame

# Configuration
WIDTH, HEIGHT = 900, 850
MAX_AGE = 40
FADE_SPEED = 25  # Wie schnell verblasst die Spur (0-255 pro Schritt)

# Colors
COLOR_BG = (10, 10, 15)
COLOR_TEXT = (220, 220, 230)
COLOR_TEXT_MUTED = (160, 160, 175)
COLOR_TEXT_BG = (20, 20, 30, 200)
COLOR_MENU_BG = (15, 15, 25)
COLOR_BOX_BG = (25, 25, 40)
COLOR_ACCENT = (50, 150, 255)
COLOR_ACCENT_HOVER = (80, 180, 255)
COLOR_SLIDER_TRACK = (40, 40, 60)
COLOR_SLIDER_THUMB = (80, 180, 255)
COLOR_GRID = (30, 30, 45)

CYAN = (80, 200, 240)


def get_cell_color(age):
    """Calculates a smooth color gradient based on cell age."""
    factor = min(age / MAX_AGE, 1.0)

    if factor < 0.33:
        sub_f = factor / 0.33
        r = 255
        g = int(225 * sub_f) + 30
        b = 0
    elif factor < 0.66:
        sub_f = (factor - 0.33) / 0.33
        r = int(255 * (1 - sub_f))
        g = 255
        b = 0
    else:
        sub_f = (factor - 0.66) / 0.34
        r = 0
        g = int(255 * (1 - sub_f))
        b = int(255 * sub_f)

    return (r, g, b)


def get_rule_properties(survive_rules, birth_rules, neighborhood):
    """Generates an extensive list of known rules and detailed behavioral tags."""
    s_set = set(survive_rules)
    b_set = set(birth_rules)
    traits = []

    RED = (255, 90, 90)
    GREEN = (80, 220, 120)
    PURPLE = (180, 130, 255)
    GRAY = (180, 180, 190)
    YELLOW = (240, 210, 80)
    BLUE = (100, 180, 255)
    ORANGE = (255, 150, 50)

    # 1. Neighborhood Tag
    if neighborhood == "von_neumann":
        traits.append(("[NEUMANN]", PURPLE, "Von-Neumann-Nachbarschaft (4 Nachbarn)"))
    else:
        traits.append(("[MOORE]", CYAN, "Moore-Nachbarschaft (8 Nachbarn)"))

    # 2. Extended Famous Rule Sets Identification
    if neighborhood == "moore":
        if b_set == {3} and s_set == {2, 3}:
            traits.append(("[KLASSISCH]", GREEN, "Conways Game of Life (B3/S23)"))
        elif b_set == {3, 6} and s_set == {2, 3}:
            traits.append(("[HIGHLIFE]", BLUE, "HighLife: Enthält Replikator-Muster (B36/S23)"))
        elif b_set == {2} and s_set == set():
            traits.append(("[SEEDS]", YELLOW, "Seeds: Reine Vermehrung, kein Überleben (B2/S)"))
        elif b_set == {3, 5, 6, 7, 8} and s_set == {5, 6, 7, 8}:
            traits.append(("[DIAMOEBA]", PURPLE, "Diamoeba: Organisches Amöben-Wachstum"))
        elif b_set == {3} and s_set == {0, 1, 2, 3, 4, 5, 6, 7, 8}:
            traits.append(("[NO-DEATH]", GREEN, "Life without Death: Zellen sterben nie"))
        elif b_set == {2, 3, 4} and s_set == {3, 4}:
            traits.append(("[MAZE]", BLUE, "Labyrinth-Generator (B234/S34)"))
        elif b_set == {3, 6, 7, 8} and s_set == {3, 4, 6, 7, 8}:
            traits.append(("[DAY & NIGHT]", YELLOW, "Day & Night: Symmetrisches Universum"))
        elif b_set == {3} and s_set == {4, 6, 7, 8}:
            traits.append(("[CORAL]", ORANGE, "Coral Growth: Bildet korallenartige Strukturen"))
        elif b_set == {3, 4} and s_set == {3, 4}:
            traits.append(("[ROASTED]", RED, "34 Life: Kompakte, stabile Cluster"))
        elif b_set == {3, 5, 7} and s_set == {1, 3, 5, 8}:
            traits.append(("[AMOEBA]", PURPLE, "Amoeba-Variante für fließende Formen"))
        elif b_set == {3} and s_set == {4, 6, 7, 8}:
            traits.append(("[STAINS]", YELLOW, "Stains: Fleckenartige, expandierende Muster"))

    # 3. Comprehensive Behavioral Tags
    if len(b_set) == 0:
        traits.append(("[INAKTIV]", GRAY, "Keine Geburten möglich - Welt stirbt rasch aus"))
    elif 0 in b_set:
        traits.append(("[CHAOS]", RED, "Spontane Entstehung im leeren Raum (B0)"))

    if len(s_set) == 0 and not (b_set == {2} and neighborhood == "moore"):
        traits.append(("[STERBLICH]", RED, "Absolute Sterblichkeit: Jede Zelle stirbt sofort"))
    else:
        # Isolation & Loneliness checks
        if 1 not in s_set and 0 not in s_set:
            traits.append(("[ISOLATION]", YELLOW, "Hohes Einsamkeitsrisiko (sterben bei < 2 Nachbarn)"))
        
        # Overcrowding checks
        if any(x >= 6 for x in s_set):
            traits.append(("[ROBUST]", GREEN, "Robust gegen Übervölkerung (vertragen viele Nachbarn)"))
        elif max(s_set) <= 3 if s_set else True:
            traits.append(("[EMPFINDLICH]", ORANGE, "Empfindlich bei zu viel Gesellschaft"))

        # Growth / Expansion checks
        if len(b_set) >= 4:
            traits.append(("[EXPANSIV]", RED, "Sehr hohes Wachstumstempo durch viele Geburtsregeln"))
        elif len(b_set) <= 1:
            traits.append(("[SELEKTIV]", BLUE, "Selektives Wachstum (brauchen exakte Bedingungen)"))

        # Stability checks
        if len(s_set) >= 5:
            traits.append(("[STABIL]", GREEN, "Hohe Beständigkeit und dichte Strukturen"))

    # Fallback if no specific tags except neighborhood were triggered
    if len(traits) == 1:
        traits.append(("[CUSTOM]", GRAY, "Benutzerdefinierte Regelkombination"))

    return traits


def get_neighbor_offsets(neighborhood):
    """Returns offsets based on neighborhood type."""
    if neighborhood == "von_neumann":
        return ((-1, 0), (1, 0), (0, -1), (0, 1))
    else:  # Moore
        return (
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        )


def update_grid(cells, dead_cells, survive_rules, birth_rules, neighborhood):
    """Calculates next gen and records dying cells for the fade-out effect."""
    offsets = get_neighbor_offsets(neighborhood)
    neighbor_counts = {}

    for r, c in cells.keys():
        for dr, dc in offsets:
            pos = (r + dr, c + dc)
            neighbor_counts[pos] = neighbor_counts.get(pos, 0) + 1

    new_cells = {}

    for pos, count in neighbor_counts.items():
        is_alive = pos in cells
        if is_alive and count in survive_rules:
            new_cells[pos] = cells[pos] + 1
        elif not is_alive and count in birth_rules:
            new_cells[pos] = 1

    for pos in cells:
        if pos not in new_cells:
            dead_cells[pos] = 200

    return new_cells


def generate_random_in_viewport(screen_w, screen_h, offset_x, offset_y, cell_size, density=0.15):
    """Generates random cells in viewport."""
    min_col = int((0 - offset_x) // cell_size)
    max_col = int((screen_w - offset_x) // cell_size) + 1
    min_row = int((0 - offset_y) // cell_size)
    max_row = int((screen_h - offset_y) // cell_size) + 1

    new_generated = {}
    for r in range(min_row, max_row):
        for c in range(min_col, max_col):
            if random.random() < density:
                new_generated[(r, c)] = 1
    return new_generated


def draw_checkbox(screen, font, rect, text, is_checked, is_hovered):
    """Draws a custom checkbox with text."""
    box_size = 18
    box_rect = pygame.Rect(rect.x, rect.centery - box_size // 2, box_size, box_size)

    bg_color = (40, 50, 70) if is_hovered else COLOR_BOX_BG
    pygame.draw.rect(screen, bg_color, box_rect, border_radius=4)
    pygame.draw.rect(screen, COLOR_ACCENT if is_checked else (80, 80, 100), box_rect, width=1, border_radius=4)

    if is_checked:
        p1 = (box_rect.x + 4, box_rect.y + 9)
        p2 = (box_rect.x + 7, box_rect.y + 13)
        p3 = (box_rect.x + 14, box_rect.y + 5)
        pygame.draw.lines(screen, COLOR_ACCENT, False, [p1, p2, p3], 2)

    txt_surf = font.render(text, True, COLOR_TEXT if is_checked else COLOR_TEXT_MUTED)
    screen.blit(txt_surf, (box_rect.right + 10, rect.centery - txt_surf.get_height() // 2))


def show_config_screen(screen, font, title_font, desc_font):
    """Configuration screen with checkboxes and dynamic tags."""
    survive_selected = {2, 3}
    birth_selected = {3}
    sim_speed = 15
    neighborhood = "moore"

    running_config = True
    clock = pygame.time.Clock()
    dragging_slider = False

    btn_size = 36
    btn_gap = 6
    row_width = 9 * btn_size + 8 * btn_gap

    while running_config:
        win_w, win_h = screen.get_size()
        center_x = win_w // 2

        curr_y = max(15, win_h // 2 - 380)

        title_y = curr_y
        curr_y += 45

        slider_lbl_y = curr_y
        slider_y = slider_lbl_y + 22
        slider_w = 320
        slider_h = 8
        slider_rect = pygame.Rect(center_x - slider_w // 2, slider_y, slider_w, slider_h)
        curr_y = slider_y + 32

        neigh_lbl_y = curr_y
        curr_y += 22

        cb_width = 240
        cb_height = 24

        cb_moore_rect = pygame.Rect(center_x - cb_width // 2, curr_y, cb_width, cb_height)
        curr_y += cb_height + 5

        cb_neumann_rect = pygame.Rect(center_x - cb_width // 2, curr_y, cb_width, cb_height)
        curr_y += cb_height + 15

        survive_lbl_y = curr_y
        survive_btn_y = survive_lbl_y + 22
        curr_y = survive_btn_y + btn_size + 12

        birth_lbl_y = curr_y
        birth_btn_y = birth_lbl_y + 22
        curr_y = birth_btn_y + btn_size + 15

        desc_box_y = curr_y
        desc_box_w = min(640, win_w - 40)

        traits = get_rule_properties(survive_selected, birth_selected, neighborhood)
        line_height = 19
        padding_y = 8
        desc_box_h = max(50, len(traits) * line_height + padding_y * 2)

        desc_box_rect = pygame.Rect(center_x - desc_box_w // 2, desc_box_y, desc_box_w, desc_box_h)
        curr_y = desc_box_y + desc_box_h + 12

        start_button = pygame.Rect(center_x - 110, curr_y, 220, 40)

        row_start_x = center_x - (row_width // 2)

        buttons = []
        for i in range(9):
            bx = row_start_x + i * (btn_size + btn_gap)
            buttons.append({"type": "survive", "val": i, "rect": pygame.Rect(bx, survive_btn_y, btn_size, btn_size)})
            buttons.append({"type": "birth", "val": i, "rect": pygame.Rect(bx, birth_btn_y, btn_size, btn_size)})

        mouse_pos = pygame.mouse.get_pos()
        screen.fill(COLOR_MENU_BG)

        title_surf = title_font.render("Game of Life - Settings", True, COLOR_TEXT)
        screen.blit(title_surf, (center_x - title_surf.get_width() // 2, title_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                thumb_x = slider_rect.x + int(((sim_speed - 1) / 59) * slider_w)
                thumb_rect = pygame.Rect(thumb_x - 10, slider_y - 6, 20, 20)

                if thumb_rect.collidepoint(mouse_pos) or slider_rect.inflate(0, 10).collidepoint(mouse_pos):
                    dragging_slider = True

                if cb_moore_rect.collidepoint(mouse_pos):
                    neighborhood = "moore"
                elif cb_neumann_rect.collidepoint(mouse_pos):
                    neighborhood = "von_neumann"

                for btn in buttons:
                    if btn["rect"].collidepoint(mouse_pos):
                        val = btn["val"]
                        if btn["type"] == "survive":
                            if val in survive_selected:
                                survive_selected.remove(val)
                            else:
                                survive_selected.add(val)
                        else:
                            if val in birth_selected:
                                birth_selected.remove(val)
                            else:
                                birth_selected.add(val)

                if start_button.collidepoint(mouse_pos):
                    running_config = False

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging_slider = False

            elif event.type == pygame.MOUSEMOTION and dragging_slider:
                rel_x = max(0, min(slider_w, mouse_pos[0] - slider_rect.x))
                sim_speed = int(1 + (rel_x / slider_w) * 59)

        speed_lbl = font.render(f"Geschwindigkeit: {sim_speed} Generationen/Sekunde", True, COLOR_TEXT)
        screen.blit(speed_lbl, (center_x - speed_lbl.get_width() // 2, slider_lbl_y))

        pygame.draw.rect(screen, COLOR_SLIDER_TRACK, slider_rect, border_radius=4)
        fill_w = int(((sim_speed - 1) / 59) * slider_w)
        pygame.draw.rect(screen, COLOR_ACCENT, (slider_rect.x, slider_rect.y, fill_w, slider_h), border_radius=4)
        thumb_x = slider_rect.x + fill_w
        pygame.draw.circle(screen, COLOR_SLIDER_THUMB, (thumb_x, slider_y + slider_h // 2), 8)

        n_title = font.render("Nachbarschafts-Typ wählen:", True, COLOR_TEXT)
        screen.blit(n_title, (center_x - n_title.get_width() // 2, neigh_lbl_y))

        draw_checkbox(
            screen, font, cb_moore_rect,
            "Moore-Nachbarschaft (8 Nachbarn - Standard)",
            neighborhood == "moore",
            cb_moore_rect.collidepoint(mouse_pos)
        )
        draw_checkbox(
            screen, font, cb_neumann_rect,
            "Von-Neumann-Nachbarschaft (4 Nachbarn)",
            neighborhood == "von_neumann",
            cb_neumann_rect.collidepoint(mouse_pos)
        )

        s_lbl = font.render("Cell SURVIVES with neighbor count:", True, COLOR_TEXT)
        screen.blit(s_lbl, (center_x - s_lbl.get_width() // 2, survive_lbl_y))

        b_lbl = font.render("New cell IS BORN with neighbor count:", True, COLOR_TEXT)
        screen.blit(b_lbl, (center_x - b_lbl.get_width() // 2, birth_lbl_y))

        for btn in buttons:
            is_active = (btn["val"] in survive_selected) if btn["type"] == "survive" else (btn["val"] in birth_selected)
            bg_col = COLOR_ACCENT if is_active else (40, 40, 60)

            pygame.draw.rect(screen, bg_col, btn["rect"], border_radius=5)
            pygame.draw.rect(screen, (80, 80, 100), btn["rect"], width=1, border_radius=5)

            txt = font.render(str(btn["val"]), True, (255, 255, 255) if is_active else (150, 150, 150))
            screen.blit(txt, (btn["rect"].centerx - txt.get_width() // 2, btn["rect"].centery - txt.get_height() // 2))

        pygame.draw.rect(screen, COLOR_BOX_BG, desc_box_rect, border_radius=8)
        pygame.draw.rect(screen, (60, 60, 90), desc_box_rect, width=1, border_radius=8)

        start_x = desc_box_rect.x + 12
        start_y = desc_box_rect.y + padding_y

        for i, (tag, color, desc) in enumerate(traits):
            current_y = start_y + i * line_height
            tag_surf = desc_font.render(tag, True, color)
            screen.blit(tag_surf, (start_x, current_y))
            desc_surf = desc_font.render(" " + desc, True, COLOR_TEXT_MUTED)
            screen.blit(desc_surf, (start_x + tag_surf.get_width(), current_y))

        btn_col = COLOR_ACCENT_HOVER if start_button.collidepoint(mouse_pos) else COLOR_ACCENT
        pygame.draw.rect(screen, btn_col, start_button, border_radius=8)
        start_txt = font.render("START GAME", True, (255, 255, 255))
        screen.blit(start_txt, (start_button.centerx - start_txt.get_width() // 2, start_button.centery - start_txt.get_height() // 2))

        pygame.display.flip()
        clock.tick(60)

    return survive_selected, birth_selected, sim_speed, neighborhood


def draw_grid_lines(screen, win_w, win_h, offset_x, offset_y, cell_size):
    """Draws grid overlay only when zoomed in close enough."""
    if cell_size < 8.0:
        return

    start_x = offset_x % cell_size
    start_y = offset_y % cell_size

    x = start_x
    while x < win_w:
        pygame.draw.line(screen, COLOR_GRID, (int(x), 0), (int(x), win_h))
        x += cell_size

    y = start_y
    while y < win_h:
        pygame.draw.line(screen, COLOR_GRID, (0, int(y)), (win_w, int(y)))
        y += cell_size


def render_chart_panel(screen, font, history, title_text, y_pos, max_samples=None):
    """Generic helper to render a population chart panel."""
    panel_w = 320
    panel_h = 105
    x_pos = 10

    panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    panel.fill(COLOR_TEXT_BG)
    screen.blit(panel, (x_pos, y_pos))
    pygame.draw.rect(screen, (50, 50, 70), (x_pos, y_pos, panel_w, panel_h), 1, border_radius=6)

    title = font.render(title_text, True, COLOR_TEXT)
    screen.blit(title, (x_pos + 10, y_pos + 6))

    if len(history) < 2:
        return

    max_pop = max(history) if max(history) > 0 else 1
    current_pop = history[-1]

    left_margin = 85
    graph_x = x_pos + left_margin
    graph_y = y_pos + 28
    graph_w = panel_w - left_margin - 12
    graph_h = panel_h - 36

    pygame.draw.rect(screen, (18, 18, 28), (graph_x, graph_y, graph_w, graph_h))
    pygame.draw.line(screen, (35, 35, 50), (graph_x, graph_y + graph_h // 2), (graph_x + graph_w, graph_y + graph_h // 2), 1)

    lbl_max = font.render(f"Max: {max_pop}", True, COLOR_TEXT_MUTED)
    lbl_now = font.render(f"Now: {current_pop}", True, COLOR_ACCENT)
    lbl_zero = font.render("Min: 0", True, COLOR_TEXT_MUTED)

    screen.blit(lbl_max, (x_pos + 10, graph_y - 2))
    screen.blit(lbl_now, (x_pos + 10, graph_y + (graph_h // 2) - 6))
    screen.blit(lbl_zero, (x_pos + 10, graph_y + graph_h - 12))

    points = []
    fill_points = [(graph_x, graph_y + graph_h)]

    data_points = history if max_samples is None else history[-max_samples:]
    total_points = len(data_points)

    for i, pop in enumerate(data_points):
        x_factor = i / (max_samples - 1) if max_samples else i / max(1, total_points - 1)
        px = graph_x + int(x_factor * graph_w)
        py = graph_y + graph_h - int((pop / max_pop) * graph_h)
        py = max(graph_y, min(graph_y + graph_h, py))
        points.append((px, py))
        fill_points.append((px, py))

    fill_points.append((points[-1][0], graph_y + graph_h))

    fill_surface = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    if len(fill_points) > 2:
        pygame.draw.polygon(fill_surface, (50, 150, 255, 45), fill_points)
    screen.blit(fill_surface, (0, 0))

    if len(points) >= 2:
        pygame.draw.lines(screen, COLOR_ACCENT, False, points, 2)


def draw_population_charts(screen, font, history_100, full_history, win_h):
    """Draws both the total history chart and the recent 100 gen chart stacked vertically."""
    panel_h = 105
    gap = 10

    y_pos_recent = win_h - panel_h - 10
    render_chart_panel(screen, font, history_100, "Population (Last 100 Gen)", y_pos_recent, max_samples=100)

    y_pos_total = y_pos_recent - panel_h - gap
    gen_count = len(full_history)
    render_chart_panel(screen, font, full_history, f"Total History ({gen_count} Gen)", y_pos_total)


def draw_hud(screen, font, paused, cell_count, survive_rules, birth_rules, sim_speed, neighborhood):
    """Draws controls, active rules, and status overlay."""
    s_str = ",".join(map(str, sorted(survive_rules))) if survive_rules else "None"
    b_str = ",".join(map(str, sorted(birth_rules))) if birth_rules else "None"
    n_str = "Moore (8)" if neighborhood == "moore" else "Von Neumann (4)"

    lines = [
        "--- CONTROLS ---",
        "[SPACE]     : Pause / Resume",
        "[UP / DOWN] : Speed +/- (Hold)",
        "[R]         : Randomize Viewport",
        "[C]         : Clear Grid",
        "[Left M]    : Draw Cell",
        "[Right M]   : Pan Viewport",
        "[Wheel]     : Zoom In / Out",
        "",
        "--- ACTIVE RULES ---",
        f"• Mode     : {n_str}",
        f"• Survival : {s_str}",
        f"• Birth    : {b_str}",
        f"• Speed    : {sim_speed} Gen/s",
        "",
        f"Status: {'PAUSED' if paused else 'RUNNING'} | Cells: {cell_count}",
    ]

    padding = 10
    line_height = 18
    hud_width = 240
    hud_height = len(lines) * line_height + padding * 2

    hud_surface = pygame.Surface((hud_width, hud_height), pygame.SRCALPHA)
    hud_surface.fill(COLOR_TEXT_BG)
    screen.blit(hud_surface, (10, 10))

    for i, line in enumerate(lines):
        color = (255, 100, 100) if "PAUSED" in line else COLOR_TEXT
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (10 + padding, 10 + padding + i * line_height))


def main():
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Consolas", 13)
    desc_font = pygame.font.SysFont("Consolas", 12)
    title_font = pygame.font.SysFont("Consolas", 22, bold=True)

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Infinite Game of Life")

    survive_rules, birth_rules, sim_speed, neighborhood = show_config_screen(screen, font, title_font, desc_font)

    cell_size = 16.0
    win_w, win_h = screen.get_size()
    offset_x = win_w // 2
    offset_y = win_h // 2

    cells = generate_random_in_viewport(win_w, win_h, offset_x, offset_y, cell_size)
    dead_cells = {}

    dragging = False
    last_mouse_pos = (0, 0)

    running = True
    paused = False
    clock = pygame.time.Clock()

    history_100 = []
    full_history = []
    max_history_len = 100

    last_step_time = pygame.time.get_ticks()

    while running:
        win_w, win_h = screen.get_size()
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEWHEEL:
                mx, my = pygame.mouse.get_pos()

                world_x = (mx - offset_x) / cell_size
                world_y = (my - offset_y) / cell_size

                if event.y > 0:
                    cell_size = min(100.0, cell_size * 1.15)
                elif event.y < 0:
                    cell_size = max(2.0, cell_size / 1.15)

                offset_x = mx - (world_x * cell_size)
                offset_y = my - (world_y * cell_size)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_c:
                    cells = {}
                    dead_cells = {}
                    history_100.clear()
                    full_history.clear()
                elif event.key == pygame.K_r:
                    cells = generate_random_in_viewport(
                        win_w, win_h, offset_x, offset_y, cell_size, density=0.15
                    )
                    dead_cells = {}
                    history_100.clear()
                    full_history.clear()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    dragging = True
                    last_mouse_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    dx = event.pos[0] - last_mouse_pos[0]
                    dy = event.pos[1] - last_mouse_pos[1]
                    offset_x += dx
                    offset_y += dy
                    last_mouse_pos = event.pos

            if pygame.mouse.get_pressed()[0]:
                mx, my = pygame.mouse.get_pos()
                col = int((mx - offset_x) // cell_size)
                row = int((my - offset_y) // cell_size)
                cells[(row, col)] = 1
                if (row, col) in dead_cells:
                    del dead_cells[(row, col)]

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_PLUS] or keys[pygame.K_KP_PLUS]:
            sim_speed = min(60, sim_speed + 1)
        if keys[pygame.K_DOWN] or keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
            sim_speed = max(1, sim_speed - 1)

        screen.fill(COLOR_BG)

        draw_grid_lines(screen, win_w, win_h, offset_x, offset_y, cell_size)

        size = max(1, int(cell_size) - 1) if cell_size > 4 else int(cell_size)

        # 1. Dead Cells (Fade-Out Trail)
        to_remove = []
        ghost_surface = pygame.Surface((size, size), pygame.SRCALPHA)

        for (r, c), alpha in dead_cells.items():
            x = c * cell_size + offset_x
            y = r * cell_size + offset_y

            if -cell_size <= x <= win_w and -cell_size <= y <= win_h:
                ghost_surface.fill((100, 100, 150, int(alpha)))
                screen.blit(ghost_surface, (int(x), int(y)))

            dead_cells[(r, c)] -= FADE_SPEED * (60 / 1000.0)
            if dead_cells[(r, c)] <= 0:
                to_remove.append((r, c))

        for pos in to_remove:
            del dead_cells[pos]

        # 2. Living Cells
        for (r, c), age in cells.items():
            x = c * cell_size + offset_x
            y = r * cell_size + offset_y

            if -cell_size <= x <= win_w and -cell_size <= y <= win_h:
                color = get_cell_color(age)
                pygame.draw.rect(screen, color, (int(x), int(y), size, size))

        # Simulation Step
        step_interval = 1000 / sim_speed

        if not paused and (current_time - last_step_time >= step_interval):
            cells = update_grid(cells, dead_cells, survive_rules, birth_rules, neighborhood)

            count = len(cells)
            history_100.append(count)
            full_history.append(count)

            if len(history_100) > max_history_len:
                history_100.pop(0)

            last_step_time = current_time

        # Draw Overlay
        draw_hud(screen, font, paused, len(cells), survive_rules, birth_rules, sim_speed, neighborhood)
        draw_population_charts(screen, font, history_100, full_history, win_h)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
