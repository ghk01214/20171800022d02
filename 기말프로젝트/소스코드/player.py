import random
from pico2d import *
import gfw_image
from gobj import *
from bomb import Bomb
import helper

class Player:
    KEY_MAP = {
        (SDL_KEYDOWN, SDLK_LEFT):  (-1,  0),
        (SDL_KEYDOWN, SDLK_RIGHT): ( 1,  0),
        (SDL_KEYDOWN, SDLK_DOWN):  ( 0, -1),
        (SDL_KEYDOWN, SDLK_UP):    ( 0,  1),
        (SDL_KEYUP, SDLK_LEFT):    ( 1,  0),
        (SDL_KEYUP, SDLK_RIGHT):   (-1,  0),
        (SDL_KEYUP, SDLK_DOWN):    ( 0,  1),
        (SDL_KEYUP, SDLK_UP):      ( 0, -1),
    }
    KEYDOWN_SPACE = (SDL_KEYDOWN, SDLK_SPACE)
    image = None

    def __init__(self):        
        self.pos = get_canvas_width() // 2, get_canvas_height() // 2
        self.action = 3
        self.delta = 0, 0
        self.target = None
        self.targets = []
        self.speed = 0
        if Player.image == None:
            Player.image = gfw_image.load(RES_DIR + '/player.png')

    def draw(self):
        if(self.action == 3 or self.action==2):
            self.image.clip_draw(363,195,85,110,*self.pos)
        elif(self.action ==1):
            self.image.clip_draw(535,195,85,110,*self.pos)
        elif(self.action==0):
            self.image.clip_draw(11,195,85,110,*self.pos)
        

    def update(self):
        x,y = self.pos
        dx,dy = self.delta
        self.pos = x+dx, y+dy
        
        if(x >741):
            self.pos=741,y+dy
        if(x <63):
            self.pos=63,y+dy
        if(y>507):
            self.pos=x+dx,507
        if(y<81):
            self.pos=x+dx,81
        if self.target is not None:
            ddx = -self.delta[0]
            helper.move_toward_obj(self)
            if self.target == None:
                del self.targets[0]
                if len(self.targets) > 0:
                    helper.set_target(self, self.targets[0])
                    self.updateAction(self.delta[0],0)
                else:
                    self.speed = 0
                    self.updateAction(0, ddx)

    def updateDelta(self, ddx, ddy):
        dx,dy = self.delta
        dx += ddx
        dy += ddy
        if ddx != 0:
            self.updateAction(dx, ddx)
        self.delta = dx, dy

    def updateAction(self, dx, ddx):
        self.action = \
            0 if dx < 0 else \
            1 if dx > 0 else \
            2 if ddx > 0 else 3

    def appendTarget(self, target):
        if target == self.pos: return
        for t in self.targets:
            if t == target: return

        self.targets.append(target)
        self.speed += 1
        helper.set_target(self, self.targets[0])
        self.updateAction(self.delta[0],0)

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Player.KEY_MAP:
            if self.target is not None:
                if e.type == SDL_KEYUP: return
                self.updateAction(0, -self.delta[0])
                self.target = None
                self.delta = 0,0
                self.targets = []
                self.speed = 0
            self.updateDelta(*Player.KEY_MAP[pair])
        elif pair == Player.KEYDOWN_SPACE:
            self.fire()

    def fire(self):
        bomb = Bomb(self.pos)
        if(len(Bomb.bombs) < 3):
            Bomb.bombs.append(bomb)
        print('Bomb count = %d' % len(Bomb.bombs))