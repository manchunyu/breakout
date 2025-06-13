from settings import *

class Player:
    def __init__(self, texture, pos):
        self.texture = texture
        self.pos = pos
        self.rect = Rectangle(self.pos.x, self.pos.y, self.texture.width, self.texture.height)
        self.speed = PLAYER_SPEED
        self.score = 0
        self.life = 5
        
    def input(self):
        # is_key_down & is_key_up are func from raylib
        # int version of true is 1 / false is 0
        # use direct import
        self.dir = int(is_key_down(KEY_RIGHT)) - int(is_key_down(KEY_LEFT))

    def update(self, dt):
        self.pos.x += self.dir * dt * self.speed
        self.restrict_movement()

    def restrict_movement(self):
        self.pos.x = max(32, min(self.pos.x, WINDOW_WIDTH - self.texture.width - 32))
    
    def draw(self):
        draw_texture_v(self.texture, self.pos, WHITE)

    def draw_health(self):
        draw_text(str(f"Life: {self.life}/5"), WINDOW_WIDTH - 150, 35, 20, RAYWHITE)

    def draw_score(self):
        draw_text(str(f"Score: {self.score}"), WINDOW_WIDTH - 150, 60, 20, RAYWHITE)
    
    def get_rect(self):
        return Rectangle(self.pos.x, self.pos.y, self.texture.width, self.texture.height)



class Brick:
    def __init__(self, texture, pos):
        self.texture = texture
        self.pos = pos
        self.rect = Rectangle(self.pos.x, self.pos.y, self.texture.width, self.texture.height)


    def draw(self):
        draw_texture_v(self.texture, self.pos, RAYWHITE)

class Ball:
    def __init__(self, texture, pos):
        self.texture = texture
        self.pos = pos
        self.rect = Rectangle(self.pos.x, self.pos.y, self.texture.width, self.texture.height)
        self.radius = self.texture.width / 2
        self.speed = BALL_SPEED
        self.direction = Vector2(uniform(-0.5, 0.5),-1)
        self.chance_consumed = False

    def draw(self):
        draw_texture_v(self.texture, self.pos, RAYWHITE)

    def update(self, dt):
        self.pos.x += self.direction.x * self.speed * dt
        self.pos.y += self.direction.y * self.speed * dt
        
    def get_rect(self):
        return Rectangle(self.pos.x, self.pos.y, self.texture.width, self.texture.height)