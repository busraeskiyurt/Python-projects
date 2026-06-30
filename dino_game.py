"""
Dinosaur Game
=============
Google Chrome offline dinosaur game implemented using the graphics.py module.

Controls:
  SPACE or UP arrow  -> Jump
  R                  -> Restart after game over
  Q or close window  -> Quit

Object hierarchy:
  DinoGame       - main controller (game loop, score, state)
  Dinosaur       - player character (jumping logic)
  Obstacle       - cactus obstacles scrolling from right to left
  Ground         - the scrolling ground line
  ScoreBoard     - HUD displaying current score and high score
"""

import time
import random
from graphics import GraphWin, Rectangle, Line, Text, Point, Polygon, color_rgb

# ---------------------------------------------------------------------------
# Window / world constants
# ---------------------------------------------------------------------------
WIN_WIDTH  = 800
WIN_HEIGHT = 300
GROUND_Y   = 240          # y-pixel where the ground line sits
FPS        = 60
DINO_COLOR = "#555555"
SKY_COLOR  = "#f7f7f7"
GROUND_COLOR = "#535353"


# ---------------------------------------------------------------------------
# Dinosaur
# ---------------------------------------------------------------------------
class Dinosaur:
    """Pixel-art T-Rex drawn with Rectangle objects."""

    DINO_X     = 80        # fixed horizontal position
    DINO_W     = 40        # width of bounding box
    DINO_H     = 50        # height of bounding box
    JUMP_VEL   = -14       # initial upward velocity (pixels/frame)
    GRAVITY    = 0.7       # downward acceleration

    def __init__(self, win):
        self.win = win
        self.y   = GROUND_Y - self.DINO_H   # top-left y of bounding box
        self.vy  = 0
        self.on_ground = True
        self.parts = []
        self._draw()

    # --- drawing helpers ---------------------------------------------------

    def _rect(self, x1, y1, x2, y2):
        r = Rectangle(Point(x1, y1), Point(x2, y2))
        r.setFill(DINO_COLOR)
        r.setOutline(DINO_COLOR)
        r.draw(self.win)
        return r

    def _draw(self):
        """Build the T-Rex shape from rectangles relative to (DINO_X, self.y)."""
        x = self.DINO_X
        y = self.y
        # body
        self.parts.append(self._rect(x,      y+10,  x+30,  y+40))
        # head
        self.parts.append(self._rect(x+10,   y,     x+40,  y+18))
        # eye (white gap)
        eye = Rectangle(Point(x+28, y+3), Point(x+35, y+9))
        eye.setFill("white")
        eye.setOutline("white")
        eye.draw(self.win)
        self.parts.append(eye)
        # mouth bump
        self.parts.append(self._rect(x+35,   y+10,  x+40,  y+14))
        # tail
        self.parts.append(self._rect(x-10,   y+20,  x+5,   y+28))
        # upper leg
        self.parts.append(self._rect(x+5,    y+38,  x+15,  y+50))
        self.parts.append(self._rect(x+18,   y+38,  x+28,  y+50))

    def _undraw(self):
        for p in self.parts:
            p.undraw()
        self.parts = []

    def _move_parts(self, dy):
        for p in self.parts:
            p.move(0, dy)

    # --- public API --------------------------------------------------------

    def jump(self):
        if self.on_ground:
            self.vy = self.JUMP_VEL
            self.on_ground = False

    def update(self):
        if not self.on_ground:
            self.vy += self.GRAVITY
            dy = self.vy
            new_y = self.y + dy
            ground_top = GROUND_Y - self.DINO_H
            if new_y >= ground_top:
                dy = ground_top - self.y
                self.y = ground_top
                self.vy = 0
                self.on_ground = True
            else:
                self.y = new_y
            self._move_parts(dy)

    def get_bbox(self):
        """Return (x1, y1, x2, y2) bounding box for collision."""
        margin = 5
        return (self.DINO_X + margin,
                self.y + margin,
                self.DINO_X + self.DINO_W - margin,
                self.y + self.DINO_H - margin)

    def remove(self):
        self._undraw()


# ---------------------------------------------------------------------------
# Obstacle (cactus)
# ---------------------------------------------------------------------------
class Obstacle:
    """A cactus made of rectangles that scrolls left across the screen."""

    CACTUS_COLOR = "#235820"

    def __init__(self, win, speed):
        self.win   = win
        self.speed = speed
        self.x     = WIN_WIDTH + 10
        self.parts = []
        # randomise a small or large cactus
        kind = random.choice(["small", "large", "double"])
        if kind == "small":
            self.w, self.h = 18, 45
        elif kind == "large":
            self.w, self.h = 22, 65
        else:
            self.w, self.h = 36, 55
        self.y = GROUND_Y - self.h
        self._draw(kind)

    def _rect(self, x1, y1, x2, y2):
        r = Rectangle(Point(x1, y1), Point(x2, y2))
        r.setFill(self.CACTUS_COLOR)
        r.setOutline(self.CACTUS_COLOR)
        r.draw(self.win)
        return r

    def _draw(self, kind):
        x, y, w, h = self.x, self.y, self.w, self.h
        if kind == "double":
            # two trunks side by side with arms
            self.parts.append(self._rect(x,      y,      x+10,   y+h))
            self.parts.append(self._rect(x+14,   y+10,   x+24,   y+h))
            self.parts.append(self._rect(x-6,    y+15,   x+10,   y+22))
            self.parts.append(self._rect(x+14,   y+20,   x+30,   y+27))
        else:
            # single trunk with one arm
            mid = w // 2
            self.parts.append(self._rect(x+mid-5, y,      x+mid+5, y+h))
            self.parts.append(self._rect(x,        y+h//3, x+mid-5, y+h//3+8))
            self.parts.append(self._rect(x,        y+h//5, x+8,     y+h//3))

    def update(self):
        dx = -self.speed
        for p in self.parts:
            p.move(dx, 0)
        self.x += dx

    def is_off_screen(self):
        return self.x + self.w < 0

    def get_bbox(self):
        margin = 4
        return (self.x + margin,
                self.y + margin,
                self.x + self.w - margin,
                self.y + self.h - margin)

    def remove(self):
        for p in self.parts:
            p.undraw()
        self.parts = []


# ---------------------------------------------------------------------------
# Ground
# ---------------------------------------------------------------------------
class Ground:
    """A scrolling dotted ground line."""

    def __init__(self, win):
        self.win  = win
        self.line = Line(Point(0, GROUND_Y), Point(WIN_WIDTH, GROUND_Y))
        self.line.setFill(GROUND_COLOR)
        self.line.setWidth(2)
        self.line.draw(win)
        # small pebble rectangles
        self.pebbles = []
        for i in range(10):
            px = random.randint(0, WIN_WIDTH)
            self._make_pebble(px)

    def _make_pebble(self, px):
        r = Rectangle(Point(px, GROUND_Y+2), Point(px+4, GROUND_Y+4))
        r.setFill(GROUND_COLOR)
        r.setOutline(GROUND_COLOR)
        r.draw(self.win)
        self.pebbles.append([r, px])

    def update(self, speed):
        for peb in self.pebbles:
            peb[0].move(-speed, 0)
            peb[1] -= speed
            if peb[1] < -10:
                peb[0].move(WIN_WIDTH + 20, 0)
                peb[1] += WIN_WIDTH + 20

    def remove(self):
        self.line.undraw()
        for peb, _ in self.pebbles:
            peb.undraw()


# ---------------------------------------------------------------------------
# ScoreBoard
# ---------------------------------------------------------------------------
class ScoreBoard:
    """Displays score and high score in the top-right corner."""

    def __init__(self, win):
        self.win        = win
        self.score      = 0
        self.high_score = 0
        self._label = Text(Point(WIN_WIDTH - 100, 20), "HI 00000  00000")
        self._label.setSize(14)
        self._label.setFace("courier")
        self._label.setFill("#535353")
        self._label.draw(win)

    def update(self, score):
        self.score = score
        if score > self.high_score:
            self.high_score = score
        self._label.setText("HI {:05d}  {:05d}".format(self.high_score, self.score))

    def remove(self):
        self._label.undraw()


# ---------------------------------------------------------------------------
# DinoGame  (main controller)
# ---------------------------------------------------------------------------
class DinoGame:
    """
    Main game controller.
    Manages the game loop, spawning obstacles, collision detection, and
    restarting after game over.
    """

    INITIAL_SPEED   = 6.0
    SPEED_INCREMENT = 0.002   # speed increase per frame
    OBSTACLE_MIN_GAP = 60     # minimum frames between obstacles

    def __init__(self):
        self.win = GraphWin("Dinosaur Game", WIN_WIDTH, WIN_HEIGHT, autoflush=False)
        self.win.setBackground(SKY_COLOR)
        self._run()

    # --- game lifecycle ----------------------------------------------------

    def _setup(self):
        self.speed        = self.INITIAL_SPEED
        self.frame        = 0
        self.score        = 0
        self.next_obstacle = self.OBSTACLE_MIN_GAP
        self.game_over    = False

        self.ground    = Ground(self.win)
        self.dino      = Dinosaur(self.win)
        self.scoreboard = ScoreBoard(self.win)
        self.obstacles = []
        self.overlay   = None   # game-over text

    def _teardown(self):
        self.dino.remove()
        self.ground.remove()
        self.scoreboard.remove()
        for obs in self.obstacles:
            obs.remove()
        self.obstacles = []
        if self.overlay:
            for t in self.overlay:
                t.undraw()
            self.overlay = None

    def _run(self):
        """Outer loop: play -> game over -> restart."""
        while not self.win.isClosed():
            self._setup()
            self._show_start_screen()
            if self.win.isClosed():
                break
            self._game_loop()
            if self.win.isClosed():
                break
            self._show_game_over()
            if self.win.isClosed():
                break
            self._teardown()

    # --- screens -----------------------------------------------------------

    def _show_start_screen(self):
        msg = Text(Point(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 20),
                   "DINOSAUR GAME")
        msg.setSize(24)
        msg.setStyle("bold")
        msg.setFill("#535353")
        msg.draw(self.win)

        sub = Text(Point(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 20),
                   "Press SPACE or UP to start")
        sub.setSize(14)
        sub.setFill("#535353")
        sub.draw(self.win)

        update_win = self.win
        while not update_win.isClosed():
            key = update_win.checkKey()
            if key in ("space", "Up"):
                break
            update_win.update()
            time.sleep(1 / FPS)

        msg.undraw()
        sub.undraw()

    def _show_game_over(self):
        t1 = Text(Point(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 20), "GAME OVER")
        t1.setSize(22)
        t1.setStyle("bold")
        t1.setFill("#535353")
        t1.draw(self.win)

        t2 = Text(Point(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 20),
                  "Press R to restart  |  Q to quit")
        t2.setSize(13)
        t2.setFill("#535353")
        t2.draw(self.win)

        self.win.update()

        while not self.win.isClosed():
            key = self.win.checkKey()
            if key == "r":
                break
            if key == "q":
                self.win.close()
                return
            self.win.update()
            time.sleep(1 / FPS)

        t1.undraw()
        t2.undraw()

    # --- main game loop ----------------------------------------------------

    def _game_loop(self):
        last_time = time.time()

        while not self.win.isClosed() and not self.game_over:
            # --- timing ---
            now = time.time()
            elapsed = now - last_time
            last_time = now
            sleep_time = (1 / FPS) - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

            # --- input ---
            key = self.win.checkKey()
            if key in ("space", "Up"):
                self.dino.jump()
            if key == "q":
                self.win.close()
                return

            # --- update ---
            self.speed += self.SPEED_INCREMENT
            self.frame += 1
            self.score  = self.frame // 6

            self.dino.update()
            self.ground.update(self.speed)

            # spawn obstacle
            if self.frame >= self.next_obstacle:
                self.obstacles.append(Obstacle(self.win, self.speed))
                gap = random.randint(self.OBSTACLE_MIN_GAP,
                                     max(self.OBSTACLE_MIN_GAP + 1,
                                         int(120 - self.speed * 2)))
                self.next_obstacle = self.frame + gap

            # update / remove obstacles
            for obs in self.obstacles[:]:
                obs.update()
                if obs.is_off_screen():
                    obs.remove()
                    self.obstacles.remove(obs)

            # collision detection
            dx1, dy1, dx2, dy2 = self.dino.get_bbox()
            for obs in self.obstacles:
                ox1, oy1, ox2, oy2 = obs.get_bbox()
                if dx1 < ox2 and dx2 > ox1 and dy1 < oy2 and dy2 > oy1:
                    self.game_over = True
                    break

            self.scoreboard.update(self.score)
            self.win.update()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    DinoGame()
