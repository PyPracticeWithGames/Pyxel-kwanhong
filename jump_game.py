import pyxel
from random import randint

class App:
    def __init__(self):
        # init screen
        pyxel.init(160, 120, caption="Pyxel Jump")

        # load Pyxel resource file(.pyxres)
        # we can create or edit images and sounds with attached Pyxel Editor
        # pyxeleditor assets/jump_game.pyxres
        pyxel.load('assets/jump_game.pyxres')

        # game status
        self.score = 0
        self.player_x = 72  # x coordinate of player
        self.player_y = -16  # y coordinate of player
        self.player_vy = 0
        self.player_is_alive = True

        self.far_cloud = [(-10, 75), (40, 65), (90, 60)]
        self.near_cloud = [(10, 25), (70, 35), (120, 15)]
        # coordinate of floor to jump
        # ex: [(0, 34, True), (60, 92, True), (120, 59, True), (180, 84, True)]
        self.floor = [(i * 60, randint(8, 104), True) for i in range(4)]
        self.fruit = [(i * 60, randint(0, 104), randint(0, 2), True) for i in range(4)]  # coordinate of fruit

        # Play music(0-7)
        pyxel.playm(0, loop=True)

        # Runs Pyxel app
        pyxel.run(self.update, self.draw)

    # frame 갱신을 처리하는 함수
    def update(self):
        # Press button Q
        # btnp(key, [hold], [period]); 해당 프레임에 key가 눌리면 True
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # update player
        self.update_player()

        for i, v in enumerate(self.floor):
            self.floor[i] = self.update_floor(*v)

        for i, v in enumerate(self.fruit):
            self.fruit[i] = self.update_fruit(*v)

    def update_player(self):
        # move left
        # btn(key); key가 눌리고 있으면 True
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
            self.player_x = max(self.player_x - 2, 0)  # 0 is minimum

        # move right
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
            self.player_x = min(self.player_x + 2, pyxel.width - 16)  # pyxel.width (screen width); character width (16)

        self.player_y += self.player_vy
        self.player_vy = min(self.player_vy + 1, 8)

        if self.player_y > pyxel.height:
            if self.player_is_alive:
                self.player_is_alive = False
                pyxel.play(3, 5) # play different sound for player death

            # re-start
            # update player status with initial value
            if self.player_y > 600:
                self.score = 0
                self.player_x = 72
                self.player_y = -16
                self.player_vy = 0
                self.player_is_alive = True

    def update_floor(self, x, y, is_active):
        if is_active:
            if (
                self.player_x + 16 >= x
                and self.player_x <= x + 40
                and self.player_y + 16 >= y
                and self.player_y <= y + 8
                and self.player_vy > 0
            ):
                is_active = False
                self.score += 10
                self.player_vy = -12
                pyxel.play(3, 3)
        else:
            y += 6

        x -= 4

        if x < -40:
            x += 240
            y = randint(8, 104)
            is_active = True

        return x, y, is_active

    def update_fruit(self, x, y, kind, is_active):
        if is_active and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            is_active = False
            self.score += (kind + 1) * 100
            self.player_vy = min(self.player_vy, -8)
            pyxel.play(3, 4) # play different sound for hitting fruit

        # x coordinate of fruit object is changing by -2 to go backward
        x -= 2

        # 값이 -40인 이유는?
        # re-assign x value of fruit object gone behind screen
        if x < -40:
            x += 240
            y = randint(0, 104)
            kind = randint(0, 2)
            is_active = True

        return x, y, kind, is_active

    def draw(self):
        pyxel.cls(12)

        # draw sky
        # location fixed
        pyxel.blt(0, 88, 0, 0, 88, 160, 32)

        # draw mountain
        # location fixed
        pyxel.blt(0, 88, 0, 0, 64, 160, 24, 12)

        # draw forest
        offset = pyxel.frame_count % 160
        for i in range(2):
            pyxel.blt(i * 160 - offset, 104, 0, 0, 48, 160, 16, 12)

        # draw clouds
        offset = (pyxel.frame_count // 16) % 160
        for i in range(2):
            for x, y in self.far_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 64, 32, 32, 8, 12)

        offset = (pyxel.frame_count // 8) % 160
        for i in range(2):
            for x, y in self.near_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 0, 32, 56, 8, 12)

        # draw floors
        for x, y, is_active in self.floor:
            pyxel.blt(x, y, 0, 0, 16, 40, 8, 12)

        # draw fruits
        for x, y, kind, is_active in self.fruit:
            if is_active:
                pyxel.blt(x, y, 0, 32 + kind * 16, 0, 16, 16, 12)

        # draw player
        pyxel.blt(
            self.player_x,
            self.player_y,
            0,
            16 if self.player_vy > 0 else 0,
            0,
            16,
            16,
            12,
        )

        # draw score
        s = "SCORE {:>4}".format(self.score)
        # draw two score texts having different color to make them look like shadowed text
        pyxel.text(5, 4, s, 1)
        pyxel.text(4, 4, s, 7)


App()