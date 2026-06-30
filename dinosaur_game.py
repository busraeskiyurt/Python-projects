from graphics import *
import time
import random

WIN_W = 800
WIN_H = 300
GROUND_Y = 255
GRAVITY = 0.9
JUMP_VEL = -16
BASE_SPEED = 5


class Dinosaur:
    def __init__(self, win):
        self.win = win
        self.x = 80
        self.y = GROUND_Y
        self.w = 40
        self.h = 50
        self.vy = 0
        self.grounded = True

        self.body = Rectangle(
            Point(self.x, self.y - self.h),
            Point(self.x + self.w, self.y)
        )
        self.body.setFill("darkgreen")
        self.body.setOutline("black")
        self.body.draw(win)

        self.eye = Circle(Point(self.x + self.w - 8, self.y - self.h + 12), 5)
        self.eye.setFill("white")
        self.eye.setOutline("black")
        self.eye.draw(win)

        self.pupil = Circle(Point(self.x + self.w - 6, self.y - self.h + 10), 2)
        self.pupil.setFill("black")
        self.pupil.draw(win)

        self.tail = Polygon(
            Point(self.x, self.y - self.h + 30),
            Point(self.x - 15, self.y - self.h + 20),
            Point(self.x, self.y - self.h + 10)
        )
        self.tail.setFill("green")
        self.tail.setOutline("black")
        self.tail.draw(win)

        self._parts = [self.body, self.eye, self.pupil, self.tail]

    def jump(self):
        if self.grounded:
            self.vy = JUMP_VEL
            self.grounded = False

    def update(self):
        if not self.grounded:
            self.vy += GRAVITY
            dy = self.vy
            new_y = self.y + dy
            if new_y >= GROUND_Y:
                dy = GROUND_Y - self.y
                self.y = GROUND_Y
                self.vy = 0
                self.grounded = True
            else:
                self.y = new_y
            for obj in self._parts:
                obj.move(0, dy)

    def bounds(self):
        margin = 5
        return (self.x + margin, self.y - self.h + margin,
                self.x + self.w - margin, self.y - margin)

    def undraw(self):
        for obj in self._parts:
            obj.undraw()


class Cactus:
    def __init__(self, win, speed):
        self.x = WIN_W + 10
        self.w = random.randint(22, 42)
        self.h = random.randint(45, 80)
        self.speed = speed
        self._parts = []

        sw = max(8, self.w // 3)
        sx = self.x + (self.w - sw) // 2

        stem = Rectangle(
            Point(sx, GROUND_Y - self.h),
            Point(sx + sw, GROUND_Y)
        )
        stem.setFill("forestgreen")
        stem.setOutline("darkgreen")
        stem.draw(win)
        self._parts.append(stem)

        arm_top = GROUND_Y - self.h + self.h // 3
        arm_bot = GROUND_Y - self.h // 2

        left_arm = Rectangle(
            Point(self.x, arm_top + 10),
            Point(sx, arm_bot)
        )
        left_arm.setFill("forestgreen")
        left_arm.setOutline("darkgreen")
        left_arm.draw(win)
        self._parts.append(left_arm)

        right_arm = Rectangle(
            Point(sx + sw, arm_top + 10),
            Point(self.x + self.w, arm_bot)
        )
        right_arm.setFill("forestgreen")
        right_arm.setOutline("darkgreen")
        right_arm.draw(win)
        self._parts.append(right_arm)

        left_tip = Rectangle(
            Point(self.x, arm_top),
            Point(self.x + sw, arm_top + 12)
        )
        left_tip.setFill("forestgreen")
        left_tip.setOutline("darkgreen")
        left_tip.draw(win)
        self._parts.append(left_tip)

        right_tip = Rectangle(
            Point(self.x + self.w - sw, arm_top),
            Point(self.x + self.w, arm_top + 12)
        )
        right_tip.setFill("forestgreen")
        right_tip.setOutline("darkgreen")
        right_tip.draw(win)
        self._parts.append(right_tip)

    def update(self):
        for p in self._parts:
            p.move(-self.speed, 0)
        self.x -= self.speed

    def off_screen(self):
        return self.x + self.w < 0

    def bounds(self):
        return (self.x + 2, GROUND_Y - self.h + 2,
                self.x + self.w - 2, GROUND_Y)

    def set_speed(self, s):
        self.speed = s

    def undraw(self):
        for p in self._parts:
            p.undraw()


class Cloud:
    def __init__(self, win):
        self.x = WIN_W + random.randint(0, 200)
        self.y = random.randint(40, 110)
        self.speed = 1.5
        self._ovals = []
        shapes = [(0, 5, 60, 30), (10, 0, 50, 20), (20, 5, 55, 28)]
        for x1, y1, x2, y2 in shapes:
            o = Oval(
                Point(self.x + x1, self.y + y1),
                Point(self.x + x2, self.y + y2)
            )
            o.setFill("lightgray")
            o.setOutline("lightgray")
            o.draw(win)
            self._ovals.append(o)

    def update(self):
        for o in self._ovals:
            o.move(-self.speed, 0)
        self.x -= self.speed

    def off_screen(self):
        return self.x + 60 < 0

    def undraw(self):
        for o in self._ovals:
            o.undraw()


class ScoreBoard:
    def __init__(self, win):
        self.hi = 0
        self._score_txt = Text(Point(680, 22), "Score: 0")
        self._score_txt.setSize(13)
        self._score_txt.draw(win)

        self._hi_txt = Text(Point(530, 22), "HI: 0")
        self._hi_txt.setSize(13)
        self._hi_txt.draw(win)

    def update(self, score):
        self._score_txt.setText("Score: {}".format(score))

    def update_hi(self, score):
        if score > self.hi:
            self.hi = score
            self._hi_txt.setText("HI: {}".format(self.hi))


class Game:
    def __init__(self):
        self.win = GraphWin("Dinosaur Game", WIN_W, WIN_H)
        self.win.setBackground("white")

        self._ground = Line(Point(0, GROUND_Y), Point(WIN_W, GROUND_Y))
        self._ground.setWidth(3)
        self._ground.draw(self.win)

        self._board = ScoreBoard(self.win)
        self._overlay = []

    def _show_overlay(self, lines):
        texts = []
        base_y = WIN_H // 2 - 30
        for i, (msg, size, bold) in enumerate(lines):
            t = Text(Point(WIN_W // 2, base_y + i * 40), msg)
            t.setSize(size)
            if bold:
                t.setStyle("bold")
            t.draw(self.win)
            texts.append(t)
        self._overlay = texts

    def _clear_overlay(self):
        for t in self._overlay:
            t.undraw()
        self._overlay = []

    def _wait_space(self):
        while True:
            if self.win.isClosed():
                return False
            if self.win.checkKey() == "space":
                return True
            time.sleep(0.05)

    def _run_round(self):
        dino = Dinosaur(self.win)
        cacti = []
        clouds = []
        score = 0
        speed = BASE_SPEED
        frame = 0
        spawn_every = 90

        while True:
            if self.win.isClosed():
                dino.undraw()
                for c in cacti:
                    c.undraw()
                for cl in clouds:
                    cl.undraw()
                return False

            key = self.win.checkKey()
            if key in ("space", "Up"):
                dino.jump()

            dino.update()

            if frame > 0 and frame % spawn_every == 0:
                cacti.append(Cactus(self.win, speed))
            if frame % 140 == 0:
                clouds.append(Cloud(self.win))

            live_cacti = []
            for c in cacti:
                c.update()
                if c.off_screen():
                    c.undraw()
                else:
                    live_cacti.append(c)
            cacti = live_cacti

            live_clouds = []
            for cl in clouds:
                cl.update()
                if cl.off_screen():
                    cl.undraw()
                else:
                    live_clouds.append(cl)
            clouds = live_clouds

            frame += 1
            score += 1

            if score % 300 == 0:
                speed = min(speed + 0.5, 15)
                spawn_every = max(45, spawn_every - 4)
                for c in cacti:
                    c.set_speed(speed)

            self._board.update(score)

            dx1, dy1, dx2, dy2 = dino.bounds()
            hit = any(
                dx2 > cx1 and dx1 < cx2 and dy2 > cy1 and dy1 < cy2
                for cx1, cy1, cx2, cy2 in (c.bounds() for c in cacti)
            )

            if hit:
                self._board.update_hi(score)
                dino.undraw()
                for c in cacti:
                    c.undraw()
                for cl in clouds:
                    cl.undraw()
                return score

            time.sleep(1 / 60)

    def run(self):
        self._show_overlay([
            ("DINOSAUR GAME", 22, True),
            ("Press SPACE to jump over cacti", 12, False),
            ("Press SPACE to start", 14, False),
        ])
        if not self._wait_space():
            self.win.close()
            return
        self._clear_overlay()

        while True:
            result = self._run_round()
            if result is False:
                break

            self._show_overlay([
                ("GAME OVER", 24, True),
                ("Score: {}".format(result), 15, False),
                ("Press SPACE to play again", 13, False),
            ])
            if not self._wait_space():
                break
            self._clear_overlay()

        if not self.win.isClosed():
            self.win.close()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
