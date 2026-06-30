"""
Dinosaur Game - Google Chrome offline dino game clone.
Controls: SPACE or UP to jump, R to restart, Q to quit.
"""

import time, random
from graphics import GraphWin, Rectangle, Line, Text, Point

WIN_W, WIN_H = 800, 300
GROUND_Y     = 240
FPS          = 60
COL_DINO     = "#555555"
COL_CACTUS   = "#2d6a27"
COL_GROUND   = "#535353"
COL_SKY      = "#f7f7f7"


# ── helpers ──────────────────────────────────────────────────────────────────

def rect(win, x1, y1, x2, y2, color):
    r = Rectangle(Point(x1, y1), Point(x2, y2))
    r.setFill(color); r.setOutline(color); r.draw(win)
    return r

def overlaps(a, b):
    return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]


# ── Dinosaur ─────────────────────────────────────────────────────────────────

class Dinosaur:
    X, W, H   = 80, 40, 50
    JUMP_V    = -14
    GRAVITY   = 0.7

    def __init__(self, win):
        self.win = win
        self.y   = GROUND_Y - self.H
        self.vy  = 0
        self.grounded = True
        self.parts = self._build()

    def _build(self):
        x, y = self.X, self.y
        c = COL_DINO
        parts = [
            rect(self.win, x,    y+10, x+30, y+40, c),   # body
            rect(self.win, x+10, y,    x+40, y+18, c),   # head
            rect(self.win, x+28, y+3,  x+35, y+9,  "white"),  # eye
            rect(self.win, x+35, y+10, x+40, y+14, c),   # snout
            rect(self.win, x-10, y+20, x+5,  y+28, c),   # tail
            rect(self.win, x+5,  y+38, x+15, y+50, c),   # leg L
            rect(self.win, x+18, y+38, x+28, y+50, c),   # leg R
        ]
        return parts

    def _shift(self, dy):
        for p in self.parts: p.move(0, dy)

    def jump(self):
        if self.grounded:
            self.vy = self.JUMP_V
            self.grounded = False

    def update(self):
        if not self.grounded:
            self.vy += self.GRAVITY
            floor = GROUND_Y - self.H
            new_y = self.y + self.vy
            if new_y >= floor:
                dy = floor - self.y
                self.y = floor
                self.vy = 0
                self.grounded = True
            else:
                dy = self.vy
                self.y = new_y
            self._shift(dy)

    def bbox(self):
        m = 6
        return (self.X+m, self.y+m, self.X+self.W-m, self.y+self.H-m)

    def remove(self):
        for p in self.parts: p.undraw()


# ── Obstacle (cactus) ────────────────────────────────────────────────────────

class Obstacle:
    def __init__(self, win, speed):
        self.win   = win
        self.speed = speed
        self.x     = WIN_W + 10
        kind = random.choice(["s", "l", "d"])
        self.w = 36 if kind == "d" else (18 if kind == "s" else 22)
        self.h = 55 if kind == "d" else (45 if kind == "s" else 65)
        self.y = GROUND_Y - self.h
        self.parts = self._build(kind)

    def _build(self, kind):
        x, y, w, h = self.x, self.y, self.w, self.h
        c = COL_CACTUS
        if kind == "d":
            return [
                rect(self.win, x,    y,    x+10, y+h,    c),
                rect(self.win, x+14, y+10, x+24, y+h,    c),
                rect(self.win, x-5,  y+15, x+10, y+22,   c),
                rect(self.win, x+14, y+20, x+29, y+27,   c),
            ]
        m = w // 2
        return [
            rect(self.win, x+m-5, y,       x+m+5, y+h,      c),
            rect(self.win, x,     y+h//3,  x+m-5, y+h//3+8, c),
            rect(self.win, x,     y+h//5,  x+8,   y+h//3,   c),
        ]

    def update(self):
        dx = -self.speed
        for p in self.parts: p.move(dx, 0)
        self.x += dx

    def off_screen(self): return self.x + self.w < 0

    def bbox(self):
        m = 4
        return (self.x+m, self.y+m, self.x+self.w-m, self.y+self.h-m)

    def remove(self):
        for p in self.parts: p.undraw()


# ── Ground ───────────────────────────────────────────────────────────────────

class Ground:
    def __init__(self, win):
        self.win = win
        ln = Line(Point(0, GROUND_Y), Point(WIN_W, GROUND_Y))
        ln.setFill(COL_GROUND); ln.setWidth(2); ln.draw(win)
        self.ln = ln
        self.pebbles = []
        for _ in range(12):
            px = random.randint(0, WIN_W)
            self.pebbles.append([rect(win, px, GROUND_Y+2, px+4, GROUND_Y+5, COL_GROUND), px])

    def update(self, speed):
        for peb in self.pebbles:
            peb[0].move(-speed, 0); peb[1] -= speed
            if peb[1] < -10:
                peb[0].move(WIN_W + 20, 0); peb[1] += WIN_W + 20

    def remove(self):
        self.ln.undraw()
        for p, _ in self.pebbles: p.undraw()


# ── ScoreBoard ───────────────────────────────────────────────────────────────

class ScoreBoard:
    def __init__(self, win):
        self.hi = 0
        self.lbl = Text(Point(WIN_W - 110, 22), "HI 00000  00000")
        self.lbl.setSize(14); self.lbl.setFace("courier")
        self.lbl.setFill(COL_GROUND); self.lbl.draw(win)

    def update(self, score):
        self.hi = max(self.hi, score)
        self.lbl.setText("HI {:05d}  {:05d}".format(self.hi, score))

    def remove(self): self.lbl.undraw()


# ── DinoGame (main controller) ───────────────────────────────────────────────

class DinoGame:
    INIT_SPEED = 6.0
    ACCEL      = 0.002
    MIN_GAP    = 55

    def __init__(self):
        self.win = GraphWin("Dinosaur Game", WIN_W, WIN_H, autoflush=False)
        self.win.setBackground(COL_SKY)
        self.hi = 0
        while not self.win.isClosed():
            self._play()

    def _msg(self, line1, line2):
        t1 = Text(Point(WIN_W//2, WIN_H//2 - 22), line1)
        t1.setSize(22); t1.setStyle("bold"); t1.setFill(COL_GROUND); t1.draw(self.win)
        t2 = Text(Point(WIN_W//2, WIN_H//2 + 18), line2)
        t2.setSize(13); t2.setFill(COL_GROUND); t2.draw(self.win)
        self.win.update()
        while not self.win.isClosed():
            k = self.win.checkKey()
            if k in ("space", "Up", "r"): break
            if k == "q": self.win.close(); return
            self.win.update(); time.sleep(1/FPS)
        t1.undraw(); t2.undraw()

    def _play(self):
        ground = Ground(self.win)
        dino   = Dinosaur(self.win)
        board  = ScoreBoard(self.win)
        board.hi = self.hi

        self._msg("DINOSAUR GAME", "Press SPACE or UP to start")
        if self.win.isClosed(): return

        speed, frame, score = self.INIT_SPEED, 0, 0
        obstacles, next_obs = [], self.MIN_GAP

        while not self.win.isClosed():
            t0 = time.time()

            k = self.win.checkKey()
            if k in ("space", "Up"): dino.jump()
            if k == "q": self.win.close(); break

            speed += self.ACCEL; frame += 1; score = frame // 6
            dino.update()
            ground.update(speed)

            if frame >= next_obs:
                obstacles.append(Obstacle(self.win, speed))
                next_obs = frame + random.randint(self.MIN_GAP, max(self.MIN_GAP+1, int(110 - speed*2)))

            for obs in obstacles[:]:
                obs.update()
                if obs.off_screen(): obs.remove(); obstacles.remove(obs)

            if any(overlaps(dino.bbox(), o.bbox()) for o in obstacles):
                break

            board.update(score)
            self.win.update()
            sleep = 1/FPS - (time.time() - t0)
            if sleep > 0: time.sleep(sleep)

        self.hi = board.hi
        for obs in obstacles: obs.remove()
        dino.remove(); ground.remove(); board.remove()

        if not self.win.isClosed():
            self._msg("GAME OVER", "Press R to restart  |  Q to quit")


if __name__ == "__main__":
    DinoGame()
