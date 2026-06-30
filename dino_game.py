"""
Dinosaur Game - Chrome Dino oyununun Python/graphics.py ile OOP implementasyonu.

Kurallar:
  - Space veya yukari ok ile dino ziplayabilir
  - Kaktus engellerinden kacin
  - Her kaktus asildiginda skor artar
  - Oyun hizi zamanla artar
"""

from graphics import *
import random
import time

# ---------------------------------------------------------------------------
# Sabitler
# ---------------------------------------------------------------------------
WIN_W      = 800
WIN_H      = 300
GROUND_Y   = 240          # zemin cizgisi y koordinati
DINO_X     = 80           # dinozor sabit x konumu
DINO_W     = 44
DINO_H     = 48
JUMP_VEL   = -14          # ziplarken baslangic hizi (yukari = negatif)
GRAVITY    = 0.8
CACTUS_W   = 24
CACTUS_MIN_H = 40
CACTUS_MAX_H = 70
FPS        = 60
COLOR_BG   = "white"
COLOR_DINO = "#555555"
COLOR_CACTUS = "#333333"
COLOR_GROUND = "#555555"
COLOR_CLOUD  = "#cccccc"


# ---------------------------------------------------------------------------
# Yardimci: dikdortgen bloklari grupla (graphics.py Rectangle listesi)
# ---------------------------------------------------------------------------
def _make_rect(win, x1, y1, x2, y2, fill, outline=""):
    r = Rectangle(Point(x1, y1), Point(x2, y2))
    r.setFill(fill)
    r.setOutline(outline if outline else fill)
    r.draw(win)
    return r


# ---------------------------------------------------------------------------
class Ground:
    """Zemin cizgisi ve dogal pixelart doku."""

    def __init__(self, win):
        self.win = win
        self.parts = []
        # Ana zemin bandi
        self.parts.append(_make_rect(win, 0, GROUND_Y, WIN_W, GROUND_Y + 4, COLOR_GROUND))
        # Kucuk noktalar / doku
        for x in range(0, WIN_W, 40):
            self.parts.append(_make_rect(win, x, GROUND_Y + 6, x + 8, GROUND_Y + 8, "#aaaaaa"))

    def undraw(self):
        for p in self.parts:
            p.undraw()


# ---------------------------------------------------------------------------
class Cloud:
    """Arka planda yuzuyor gorunen bulutlar."""

    def __init__(self, win, x, y):
        self.win = win
        self.x = x
        self.y = y
        self.speed = 1.5
        self.parts = []
        self._draw()

    def _draw(self):
        x, y = self.x, self.y
        # Basit oval bulut
        for dx, dy, w, h in [
            (0, 0, 60, 20),
            (10, -12, 40, 20),
            (30, -8, 30, 18),
        ]:
            o = Oval(Point(x + dx, y + dy), Point(x + dx + w, y + dy + h))
            o.setFill(COLOR_CLOUD)
            o.setOutline(COLOR_CLOUD)
            o.draw(self.win)
            self.parts.append(o)

    def move(self):
        for p in self.parts:
            p.move(-self.speed, 0)
        self.x -= self.speed

    def is_off_screen(self):
        return self.x + 90 < 0

    def undraw(self):
        for p in self.parts:
            p.undraw()


# ---------------------------------------------------------------------------
class Dino:
    """
    Oyuncunun kontrol ettigi dinozor.
    Pixel-art gorunumu dikdortgen bloklarla cizilmistir.
    """

    def __init__(self, win):
        self.win = win
        self.y = float(GROUND_Y - DINO_H)   # sol-ust kose y
        self.vel_y = 0.0
        self.on_ground = True
        self.parts = []
        self._draw_dino()

    # -- Gorsel --------------------------------------------------------
    def _draw_dino(self):
        self._clear()
        x = DINO_X
        y = int(self.y)
        c = COLOR_DINO
        w = self.win

        # Govde bloklar (piksel-art tarzinda)
        # Kafa
        self.parts += [
            _make_rect(w, x+8,  y,    x+44, y+8,  c),   # kafa ust
            _make_rect(w, x+8,  y+8,  x+40, y+24, c),   # kafa orta (goz boslugu)
            _make_rect(w, x+32, y+8,  x+40, y+16, "white"),  # goz
            _make_rect(w, x+32, y+8,  x+36, y+12, c),   # goz bebegi
            _make_rect(w, x+40, y+16, x+44, y+20, c),   # agiz
            # Boyun + govde
            _make_rect(w, x+8,  y+24, x+36, y+44, c),
            # Kuyruk
            _make_rect(w, x,    y+28, x+12, y+36, c),
            _make_rect(w, x,    y+36, x+8,  y+40, c),
            # Bacaklar (kosu pozisyonu)
            _make_rect(w, x+16, y+44, x+24, y+DINO_H, c),
            _make_rect(w, x+28, y+40, x+36, y+DINO_H, c),
        ]

    def _clear(self):
        for p in self.parts:
            p.undraw()
        self.parts = []

    # -- Fizik ---------------------------------------------------------
    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_VEL
            self.on_ground = False

    def update(self):
        if not self.on_ground:
            self.vel_y += GRAVITY
            self.y += self.vel_y
            ground_top = float(GROUND_Y - DINO_H)
            if self.y >= ground_top:
                self.y = ground_top
                self.vel_y = 0.0
                self.on_ground = True
        self._draw_dino()

    # -- Carpisma kutusu -----------------------------------------------
    def get_box(self):
        margin = 4
        return (DINO_X + margin, self.y + margin,
                DINO_X + DINO_W - margin, self.y + DINO_H - margin)

    def undraw(self):
        self._clear()


# ---------------------------------------------------------------------------
class Cactus:
    """Rastgele yukseklikte kaktus engeli."""

    def __init__(self, win, speed):
        self.win = win
        self.speed = speed
        self.h = random.randint(CACTUS_MIN_H, CACTUS_MAX_H)
        # Kaktus bazen uc veya iki govdeli olabilir
        self.num_trunks = random.choice([1, 1, 2, 3])
        self.x = float(WIN_W + 10)
        self.parts = []
        self._draw_cactus()

    def _draw_cactus(self):
        self._clear()
        x = int(self.x)
        y1 = GROUND_Y - self.h
        c = COLOR_CACTUS
        w = self.win

        trunk_gap = CACTUS_W + 6
        for i in range(self.num_trunks):
            ox = x + i * trunk_gap
            # Ana govde
            self.parts += [
                _make_rect(w, ox + 8,  y1,            ox + 16, GROUND_Y,     c),
                # Sol kol
                _make_rect(w, ox,      y1 + self.h//3, ox + 8, y1 + self.h//2, c),
                _make_rect(w, ox,      y1 + self.h//4, ox + 4, y1 + self.h//3, c),
                # Sag kol
                _make_rect(w, ox + 16, y1 + self.h//3, ox + 24, y1 + self.h//2, c),
                _make_rect(w, ox + 20, y1 + self.h//4, ox + 24, y1 + self.h//3, c),
            ]

    def _clear(self):
        for p in self.parts:
            p.undraw()
        self.parts = []

    def move(self):
        self.x -= self.speed
        self._draw_cactus()

    def is_off_screen(self):
        return self.x + CACTUS_W * self.num_trunks + 20 < 0

    def get_box(self):
        margin = 3
        right = self.x + (self.num_trunks - 1) * (CACTUS_W + 6) + CACTUS_W
        return (self.x + margin, GROUND_Y - self.h + margin,
                right - margin, GROUND_Y)

    def undraw(self):
        self._clear()


# ---------------------------------------------------------------------------
class ScoreBoard:
    """Skor ve hiz gostergesi."""

    def __init__(self, win):
        self.win = win
        self.score = 0
        self.hi_score = 0
        self.label = Text(Point(WIN_W - 120, 30), "HI 00000  00000")
        self.label.setSize(14)
        self.label.setStyle("bold")
        self.label.setFill("#555555")
        self.label.draw(win)

    def update(self, score):
        self.score = score
        if score > self.hi_score:
            self.hi_score = score
        self.label.setText("HI {:05d}  {:05d}".format(self.hi_score, self.score))

    def undraw(self):
        self.label.undraw()


# ---------------------------------------------------------------------------
class Game:
    """Ana oyun dongusu ve durum yoneticisi."""

    def __init__(self):
        self.win = GraphWin("Dinosaur Game", WIN_W, WIN_H, autoflush=False)
        self.win.setBackground(COLOR_BG)
        self._running = True
        self._bind_keys()

    # -- Klavye --------------------------------------------------------
    def _bind_keys(self):
        self._jump_pressed = False
        self.win.bind_all("<space>",   self._on_jump)
        self.win.bind_all("<Up>",      self._on_jump)

    def _on_jump(self, event=None):
        self._jump_pressed = True

    # -- Ekran temizle -------------------------------------------------
    def _clear_screen(self):
        self.win.delete("all")

    # -- Baslik ekrani --------------------------------------------------
    def _show_start_screen(self, message="Press SPACE to Start"):
        self._clear_screen()
        Ground(self.win)
        t = Text(Point(WIN_W // 2, WIN_H // 2 - 20), message)
        t.setSize(20)
        t.setStyle("bold")
        t.setFill("#333333")
        t.draw(self.win)
        sub = Text(Point(WIN_W // 2, WIN_H // 2 + 20), "Use SPACE or UP arrow to jump")
        sub.setSize(12)
        sub.setFill("#777777")
        sub.draw(self.win)
        update()

        # Basismak icin bekle
        self._jump_pressed = False
        while not self._jump_pressed:
            update()
            if self.win.isClosed():
                return False
            time.sleep(0.05)
        return True

    # -- Bir oyun turu -------------------------------------------------
    def _play_round(self):
        self._clear_screen()

        ground     = Ground(self.win)
        dino       = Dino(self.win)
        scoreboard = ScoreBoard(self.win)
        clouds     = []
        cacti      = []

        score      = 0
        base_speed = 5.0
        speed      = base_speed
        frame      = 0
        next_cactus_frame = random.randint(60, 100)
        next_cloud_frame  = 0

        frame_time = 1.0 / FPS

        while not self.win.isClosed():
            t_start = time.time()

            # --- Girdi ---
            if self._jump_pressed:
                dino.jump()
                self._jump_pressed = False

            # --- Guncelle ---
            dino.update()

            # Bulutlar
            if frame >= next_cloud_frame:
                clouds.append(Cloud(self.win, WIN_W, random.randint(60, 140)))
                next_cloud_frame = frame + random.randint(80, 150)
            for cl in clouds[:]:
                cl.move()
                if cl.is_off_screen():
                    cl.undraw()
                    clouds.remove(cl)

            # Kaktusler
            if frame >= next_cactus_frame:
                cacti.append(Cactus(self.win, speed))
                next_cactus_frame = frame + random.randint(50, 110)
            for ca in cacti[:]:
                ca.move()
                if ca.is_off_screen():
                    ca.undraw()
                    cacti.remove(ca)

            # Skor & hiz artisi
            score += 1
            speed = base_speed + score * 0.003
            scoreboard.update(score // 6)

            # Carpisma kontrolu
            dx1, dy1, dx2, dy2 = dino.get_box()
            for ca in cacti:
                cx1, cy1, cx2, cy2 = ca.get_box()
                if dx2 > cx1 and dx1 < cx2 and dy2 > cy1 and dy1 < cy2:
                    dino.undraw()
                    ground.undraw()
                    scoreboard.undraw()
                    for cl in clouds: cl.undraw()
                    for c  in cacti:  c.undraw()
                    update()
                    return score // 6   # oyun bitti, skoru dondur

            update()
            frame += 1

            # FPS sinirla
            elapsed = time.time() - t_start
            sleep_t = frame_time - elapsed
            if sleep_t > 0:
                time.sleep(sleep_t)

        return score // 6

    # -- Ana dongu -----------------------------------------------------
    def run(self):
        if not self._show_start_screen():
            return

        while not self.win.isClosed():
            final_score = self._play_round()
            if self.win.isClosed():
                break
            msg = "Game Over!  Score: {:05d}\nPress SPACE to Play Again".format(final_score)
            if not self._show_start_screen(msg):
                break

        if not self.win.isClosed():
            self.win.close()


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    game = Game()
    game.run()
