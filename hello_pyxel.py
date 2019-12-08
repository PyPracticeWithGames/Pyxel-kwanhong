'''
Hello Pyxel!!

Install packages

pip install -U pyxel
On Mac: brew install python3 sdl2 sdl2_image

한국어 Readme
https://github.com/kitao/pyxel/blob/master/README.ko.md

'''

import pyxel


# Wraps pyxel setting code
class App:
    def __init__(self) -> None:
        # init screen
        pyxel.init(160, 120, caption="Hello Pyxel")  # width, height, caption, scale...
        # image(img, [system])
        # Image class; load(x, y, filename) 실행 스크립트가 위치한 폴더에서 png 파일을 (x, y) 좌표에 load
        pyxel.image(0).load(0, 0, 'assets/pyxel_logo_38x16.png')
        # Runs Pyxel app
        # pyxel.run needs update and draw method as parameter
        pyxel.run(self.update, self.draw)

    def update(self):
        # btnp(key, [hold], [period])
        # 해당 프레임에 key가 눌리면 True, 눌리지 않으면 False 반환
        if pyxel.btnp(pyxel.KEY_Q): # When Q btn pressed
            pyxel.quit()  # Quit Pyxel app

    def draw(self):
        pyxel.cls(0)  # cls(col); 화면을 col색으로 지움
        # text(x, y, s, col)
        # col 색을 사용해 문자열 s를 (x, y) 좌표에 그
        pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)
        # blt(x, y, img, u, v, w, h, [colkey])
        # 이미지 뱅크 img (0-2)의 (u, v)부터 (w, h)까지의 영역을 (x, y) 좌표에 복
        pyxel.blt(61, 66, 0, 0, 0, 38, 16)


App()
