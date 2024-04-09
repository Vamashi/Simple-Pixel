# Simple Pixel code by github.com/vamashi

import os;
try:
    import pyxel
except:
    os.system("pip install %s".format("pyxel"))

class Config:
    def __init__(self):
        self.TEOIC = False # TEOIC - Throw Error On Incorrect Config. Etc: Will the error been throwed, when 
        # you make a mistake in this config. Default is False. 
        self.PlayerMoveSpeed = 2 # Basic player move speed. Default is 2.
        self.PlayerGravity = 1 # Player gravity. Default is 1.
        self.PlayerUndead = False # Toggle "god" mode.

class CheckConfiguration:
    def getExceptions(self):
        return {
            1:"IncorrectGravityException"
        }
    def __init__(self) -> None:
        ConfigInit = Config()
        if ConfigInit.TEOIC==False: return;
        if ConfigInit.PlayerGravity <= 0:
            raise(BaseException(self.getExceptions()[1]))
CheckConfiguration()

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Simple Pixel game.")
        pyxel.load("assets/jump_game.pyxres")
        self.score = 0
        self.player_x = 72
        self.player_y = -16
        self.player_dy = 0
        self.is_alive = True
        self.far_cloud = [(-10, 75), (40, 65), (90, 60)]
        self.near_cloud = [(10, 25), (70, 35), (120, 15)]
        self.floor = [(i *50, pyxel.rndi(8, 104), True) for i in range(4)]
        self.fruit = [
            (i * 60, pyxel.rndi(0, 104), pyxel.rndi(0, 2), True) for i in range(4)
        ]
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        self.update_player()
        for i, v in enumerate(self.floor):
            self.floor[i] = self.update_floor(*v)
        for i, v in enumerate(self.fruit):
            self.fruit[i] = self.update_fruit(*v)

    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.player_x = max(self.player_x - Config().PlayerMoveSpeed, 0)
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.player_x = min(self.player_x + Config().PlayerMoveSpeed, pyxel.width - 16)
        self.player_y += self.player_dy
        self.player_dy = min(self.player_dy + Config().PlayerGravity, 8)

        if self.player_y > pyxel.height:
            if self.is_alive and Config().PlayerUndead==False:
                self.is_alive = False
                pyxel.play(3, 5)
            elif self.is_alive and Config().PlayerUndead==True:
                self.player_x = 72
                self.player_y = -16
                self.is_alive = True
            if self.player_y > 600:
                self.score = 0
                self.player_x = 72
                self.player_y = -16
                self.player_dy = 0
                self.is_alive = True

    def update_floor(self, x, y, is_alive):
        if is_alive:
            if (
                self.player_x + 16 >= x
                and self.player_x <= x + 40
                and self.player_y + 16 >= y
                and self.player_y <= y + 8
                and self.player_dy > 0
            ):
                is_alive = False
                self.score += 10
                self.player_dy = -12
                pyxel.play(3, 3)
        else:
            y += 6
        x -= 2
        if x < -40:
            x += 240
            y = pyxel.rndi(8, 104)
            is_alive = True
        return x, y, is_alive

    def update_fruit(self, x, y, kind, is_alive):
        if is_alive and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            is_alive = False # destroy fruit
            self.score += (kind + 1) * 100 # score update
            # self.player_dy = min(self.player_dy, -8) # jump
            pyxel.play(3, 4) 
        x -= 2 # moving
        if x < -40:
            x += 240
            y = pyxel.rndi(0, 104)
            kind = pyxel.rndi(0, 2)
            is_alive = True
        return (x, y, kind, is_alive)

    def draw(self):
        pyxel.cls(12)

        # Draw sky
        pyxel.blt(0, 88, 0, 0, 88, 160, 32)

        # Draw mountain
        pyxel.blt(0, 88, 0, 0, 64, 160, 24, 12)

        # Draw trees
        offset = pyxel.frame_count % 160
        for i in range(2):
            pyxel.blt(i * 160 - offset, 104, 0, 0, 48, 160, 16, 12)

        # Draw clouds
        offset = (pyxel.frame_count // 16) % 160
        for i in range(2):
            for x, y in self.far_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 64, 32, 32, 8, 12)
        offset = (pyxel.frame_count // 8) % 160
        for i in range(2):
            for x, y in self.near_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 0, 32, 56, 8, 12)

        # Draw floors
        for x, y, is_alive in self.floor:
            pyxel.blt(x, y, 0, 0, 16, 40, 8, 12)

        # Draw fruits
        for x, y, kind, is_alive in self.fruit:
            if is_alive:
                pyxel.blt(x, y, 0, 32 + kind * 16, 0, 16, 16, 12)

        # Draw player
        pyxel.blt(
            self.player_x,
            self.player_y,
            0,
            16 if self.player_dy > 0 else 0,
            0,
            16,
            16,
            12,
        )

        # Draw score
        s = f"SCORE: {self.score:>4}"
        pyxel.text(5, 4, s, 1)
        pyxel.text(4, 4, s, 7)


App()
