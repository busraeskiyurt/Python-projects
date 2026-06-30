# dinosaur_game.py
"""
Dinosaur Game - Google Chrome Offline Dinosaur Game
Uses the graphics.py module (John Zelle) for the UI.
Object-Oriented implementation for ENd Mühendisliği 1. Sınıf Assignment.
"""

from graphics import *
import time
import random

# ──────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────
WIN_WIDTH  = 800
WIN_HEIGHT = 300
GROUND_Y   = 240          # y-coordinate of the ground line
FPS        = 60           # target frames per second
GRAVITY    = 0.8          # downward acceleration per frame
JUMP_VEL   = -14          # upward velocity when jumping


# ──────────────────────────────────────────────
# Dinosaur class
# ──────────────────────────────────────────────
class Dinosaur:
    """Represents the player's dinosaur character."""

    WIDTH  = 40
    HEIGHT = 50

    def __init__(self, win):
        self.win = win
        self.x   = 80
        self.y   = GROUND_Y - self.HEIGHT      # top-left y
        self.vel = 0                           # vertical velocity
        self.on_ground = True

        # Body rectangle
        self.body = Rectangle(
            Point(self.x, self.y),
            Point(self.x + self.WIDTH, self.y + self.HEIGHT)
        )
        self.body.setFill("dark green")
        self.body.setOutline("black")
        self.body.draw(win)

        # Eye
        self.eye = Circle(Point(self.x + 30, self.y + 12), 5)
        self.eye.setFill("white")
        self.eye.draw(win)

        # Pupil
        self.pupil = Circle(Point(self.x + 32, self.y + 12), 2)
        self.pupil.setFill("black")
        self.pupil.draw(win)

    def jump(self):
        """Make the dinosaur jump (only from the ground)."""
        if self.on_ground:
            self.vel = JUMP_VEL
            self.on_ground = False

    def update(self):
        """Apply gravity and move the dinosaur vertically."""
        self.vel += GRAVITY
        dy = self.vel

        # Don't go below the ground
        new_y = self.y + dy
        if new_y >= GROUND_Y - self.HEIGHT:
            new_y = GROUND_Y - self.HEIGHT
            self.vel = 0
            self.on_ground = True

        actual_dy = new_y - self.y
        self.y = new_y

        # Move all parts
        self.body.move(0, actual_dy)
        self.eye.move(0, actual_dy)
        self.pupil.move(0, actual_dy)

    def get_rect(self):
        """Return (x1, y1, x2, y2) bounding box for collision detection."""
        return (self.x, self.y,
                self.x + self.WIDTH, self.y + self.HEIGHT)

    def undraw(self):
        self.body.undraw()
        self.eye.undraw()
        self.pupil.undraw()


# ──────────────────────────────────────────────
# Cactus class
# ──────────────────────────────────────────────
class Cactus:
    """An obstacle that scrolls from right to left."""

    WIDTH  = 20
    HEIGHT = 50

    def __init__(self, win):
        self.win   = win
        self.x     = WIN_WIDTH + 10
        self.y     = GROUND_Y - self.HEIGHT

        self.body = Rectangle(
            Point(self.x, self.y),
            Point(self.x + self.WIDTH, self.y + self.HEIGHT)
        )
        self.body.setFill("forest green")
        self.body.setOutline("black")
        self.body.draw(win)

        # Small arm
        arm_y = self.y + 15
        self.arm = Rectangle(
            Point(self.x - 10, arm_y),
            Point(self.x + self.WIDTH + 10, arm_y + 10)
        )
        self.arm.setFill("forest green")
        self.arm.setOutline("black")
        self.arm.draw(win)

    def move(self, dx):
        """Scroll the cactus left by dx pixels."""
        self.x += dx
        self.body.move(dx, 0)
        self.arm.move(dx, 0)

    def is_off_screen(self):
        return self.x + self.WIDTH < 0

    def get_rect(self):
        """Return (x1, y1, x2, y2) for the cactus body (used for collision)."""
        return (self.x, self.y,
                self.x + self.WIDTH, self.y + self.HEIGHT)

    def undraw(self):
        self.body.undraw()
        self.arm.undraw()


# ──────────────────────────────────────────────
# Cloud class  (decorative background element)
# ──────────────────────────────────────────────
class Cloud:
    """A simple decorative cloud that drifts left."""

    def __init__(self, win, x=None):
        self.win = win
        self.x   = x if x is not None else WIN_WIDTH + 20
        self.y   = random.randint(60, 140)

        self.oval = Oval(
            Point(self.x, self.y),
            Point(self.x + 80, self.y + 30)
        )
        self.oval.setFill("white")
        self.oval.setOutline("light gray")
        self.oval.draw(win)

    def move(self, dx):
        self.x += dx
        self.oval.move(dx, 0)

    def is_off_screen(self):
        return self.x + 80 < 0

    def undraw(self):
        self.oval.undraw()


# ──────────────────────────────────────────────
# Game class  (main controller)
# ──────────────────────────────────────────────
class Game:
    """Controls the game loop, score, and all objects."""

    def __init__(self):
        self.win = GraphWin("Dinosaur Game", WIN_WIDTH, WIN_HEIGHT, autoflush=False)
        self.win.setBackground("white")

        # Ground line
        self.ground = Line(Point(0, GROUND_Y), Point(WIN_WIDTH, GROUND_Y))
        self.ground.setWidth(2)
        self.ground.draw(self.win)

        # Score display
        self.score     = 0
        self.score_txt = Text(Point(WIN_WIDTH - 80, 30), "Score: 0")
        self.score_txt.setSize(14)
        self.score_txt.draw(self.win)

        # High score
        self.high_score     = 0
        self.hi_txt = Text(Point(WIN_WIDTH - 220, 30), "Best: 0")
        self.hi_txt.setSize(14)
        self.hi_txt.draw(self.win)

        # Game objects
        self.dino    = Dinosaur(self.win)
        self.cacti   = []
        self.clouds  = []

        # Timing / speed
        self.speed          = 5.0    # pixels per frame the world moves left
        self.frame_count    = 0
        self.cactus_timer   = 0
        self.cloud_timer    = 0
        self.next_cactus_in = random.randint(60, 120)
        self.next_cloud_in  = random.randint(40, 100)

    # ── helpers ───────────────────────────────
    def _check_collision(self, dino_rect, cactus_rect):
        """AABB collision detection with a small margin."""
        margin = 5
        dx1, dy1, dx2, dy2 = dino_rect
        cx1, cy1, cx2, cy2 = cactus_rect
        dx1 += margin; dy1 += margin
        dx2 -= margin; dy2 -= margin
        return not (dx2 < cx1 or dx1 > cx2 or dy2 < cy1 or dy1 > cy2)

    def _spawn_cactus(self):
        self.cacti.append(Cactus(self.win))
        self.next_cactus_in = random.randint(55, 130)
        self.cactus_timer   = 0

    def _spawn_cloud(self):
        self.clouds.append(Cloud(self.win))
        self.next_cloud_in = random.randint(60, 150)
        self.cloud_timer   = 0

    def _show_message(self, text):
        msg = Text(Point(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 20), text)
        msg.setSize(20)
        msg.setStyle("bold")
        msg.draw(self.win)
        return msg

    # ── main methods ──────────────────────────
    def start_screen(self):
        """Show a simple 'press space to start' screen."""
        title = Text(Point(WIN_WIDTH // 2, 110), "DINOSAUR GAME")
        title.setSize(28)
        title.setStyle("bold")
        title.draw(self.win)

        instr = Text(Point(WIN_WIDTH // 2, 160), "Press SPACE to start")
        instr.setSize(16)
        instr.draw(self.win)

        update()
        while True:
            key = self.win.checkKey()
            if self.win.isClosed():
                return False
            if key == "space":
                title.undraw()
                instr.undraw()
                return True
            time.sleep(0.05)

    def run(self):
        """Main game loop."""
        frame_time = 1.0 / FPS

        while True:
            t_start = time.time()

            # ── Input ──
            key = self.win.checkKey()
            if self.win.isClosed():
                break
            if key in ("space", "Up"):
                self.dino.jump()

            # ── Update dino ──
            self.dino.update()

            # ── Spawn / move clouds ──
            self.cloud_timer += 1
            if self.cloud_timer >= self.next_cloud_in:
                self._spawn_cloud()
            for cloud in self.clouds:
                cloud.move(-self.speed * 0.4)   # clouds drift slower
            self.clouds = [c for c in self.clouds if not c.is_off_screen()]

            # ── Spawn / move cacti ──
            self.cactus_timer += 1
            if self.cactus_timer >= self.next_cactus_in:
                self._spawn_cactus()
            for cactus in self.cacti:
                cactus.move(-self.speed)

            # ── Remove off-screen cacti ──
            remaining = []
            for cactus in self.cacti:
                if cactus.is_off_screen():
                    cactus.undraw()
                else:
                    remaining.append(cactus)
            self.cacti = remaining

            # ── Collision detection ──
            dino_rect = self.dino.get_rect()
            for cactus in self.cacti:
                if self._check_collision(dino_rect, cactus.get_rect()):
                    self._game_over()
                    return

            # ── Score & speed ──
            self.frame_count += 1
            self.score = self.frame_count // 6        # roughly 1 point per 6 frames
            self.score_txt.setText("Score: " + str(self.score))
            if self.score > self.high_score:
                self.high_score = self.score
                self.hi_txt.setText("Best: " + str(self.high_score))

            # Gradually increase speed
            self.speed = 5.0 + self.score * 0.01

            # ── Render ──
            update()

            # ── Frame rate cap ──
            elapsed = time.time() - t_start
            sleep_t = frame_time - elapsed
            if sleep_t > 0:
                time.sleep(sleep_t)

    def _game_over(self):
        """Show game-over screen and ask to restart."""
        msg  = self._show_message("GAME OVER!")
        sc   = Text(Point(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 20),
                    "Score: " + str(self.score))
        sc.setSize(16)
        sc.draw(self.win)

        again = Text(Point(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 60),
                     "Press SPACE to play again   |   Close window to quit")
        again.setSize(12)
        again.draw(self.win)
        update()

        while True:
            key = self.win.checkKey()
            if self.win.isClosed():
                return
            if key == "space":
                # Clean up and restart
                msg.undraw(); sc.undraw(); again.undraw()
                for c in self.cacti:
                    c.undraw()
                for cl in self.clouds:
                    cl.undraw()
                self.dino.undraw()
                self._reset()
                self.run()
                return
            time.sleep(0.05)

    def _reset(self):
        """Reset game state for a new round."""
        self.dino          = Dinosaur(self.win)
        self.cacti         = []
        self.clouds        = []
        self.score         = 0
        self.frame_count   = 0
        self.cactus_timer  = 0
        self.cloud_timer   = 0
        self.speed         = 5.0
        self.next_cactus_in = random.randint(60, 120)
        self.next_cloud_in  = random.randint(40, 100)
        self.score_txt.setText("Score: 0")


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────
def main():
    game = Game()
    if game.start_screen():
        game.run()

if __name__ == "__main__":
    main()
