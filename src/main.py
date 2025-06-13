from settings import *
from sprites import *

class Game():
    def __init__(self):
        init_window(*WINDOW_SIZE, "Breakout")
        init_audio_device()
        self.import_assets()
        set_target_fps(144)
        self.state = "paused"

        self.player = Player(self.textures["paddle"], PLAYER_INIT_POS)
        self.ball = Ball(self.textures["ball"], 
                         Vector2(self.player.pos.x + self.player.texture.width / 2, 
                                 self.player.pos.y - 10))
        self.bricks = self.setup_bricks()
    
    def import_assets(self):
        self.textures = {
            "paddle" : load_texture(join(*PATH_TO_IMAGES, "paddleBlu.png")),
            "brick" : load_texture(join(*PATH_TO_IMAGES, "element_purple_rectangle.png")),
            "wall": load_texture(join(*PATH_TO_IMAGES, "element_grey_square.png")),
            "ball": load_texture(join(*PATH_TO_IMAGES, "ballGrey.png"))
        }

    def setup_bricks(self):
        bricks = []
        BRICK_HEIGHT = self.textures["brick"].height
        BRICK_WIDTH = self.textures["brick"].width

        curr_y_pos = 110
        for row in range(8):
            curr_x_pos = 96
            for column in range(17):
                bricks.append(Brick(self.textures["brick"], Vector2(curr_x_pos, curr_y_pos)))
                curr_x_pos += BRICK_WIDTH
            curr_y_pos += BRICK_HEIGHT

        return bricks
    
    def draw_wall(self):
        WALL_WIDTH , WALL_HEIGHT = self.textures["wall"].width, self.textures["wall"].height
        x_current = 0
        y_current = WALL_WIDTH
        while not x_current == WINDOW_WIDTH:
            draw_texture_v(self.textures["wall"], Vector2(x_current, 0), RAYWHITE)
            if not self.ball.chance_consumed:
                draw_texture_v(self.textures["wall"], Vector2(x_current, WINDOW_HEIGHT - WALL_HEIGHT), RAYWHITE)
            x_current += WALL_WIDTH

        while not y_current == WINDOW_HEIGHT:
            draw_texture_v(self.textures["wall"],Vector2(0, y_current), RAYWHITE)
            draw_texture_v(self.textures["wall"],Vector2(WINDOW_WIDTH - WALL_WIDTH, y_current), RAYWHITE)
            y_current += WALL_WIDTH

    def draw_bricks(self):
        for brick in self.bricks:
            brick.draw()

    def draw(self):
        begin_drawing()
        clear_background(BLACK)
        self.draw_wall()
        draw_fps(30,30)

        if not self.state == "gameover":
            self.draw_bricks()
            self.ball.draw()
            self.player.draw()
            self.player.draw_score()
            self.player.draw_health()
        else:
            draw_text(f"Gameover! Your score is {self.player.score}", WINDOW_WIDTH // 2 - 320, WINDOW_HEIGHT // 2, 50, RAYWHITE)
            draw_text("Press Spacebar to try again.", WINDOW_WIDTH // 2 - 320, WINDOW_HEIGHT // 2 + 55, 50, RAYWHITE)


        end_drawing()

    def update(self):
        dt = get_frame_time()
        self.check_ball_out_of_screen()
        
        if self.state == "play":
            self.player.input()
            self.player.update(dt)

            self.check_ball_collision()
            self.ball.update(dt)

        elif self.state == "paused":
            self.player.pos = Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 100)
            self.ball.pos = Vector2(self.player.pos.x + self.player.texture.width / 2, 
                                 self.player.pos.y - 10)
            self.ball.chance_consumed = False
            
            if is_key_pressed(KEY_SPACE):
                self.state = "play"

        elif self.state == "gameover":
            self.player.pos = Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 100)
            self.ball.pos = Vector2(self.player.pos.x + self.player.texture.width / 2, 
                                 self.player.pos.y - 10)
            
            if is_key_pressed(KEY_SPACE):
                self.player.score = 0
                self.player.life = 5
                self.bricks = self.setup_bricks()
                self.state = "play"



    def check_ball_collision(self):
        WALL_WIDTH = self.textures["wall"].width
        WALL_HEIGHT = self.textures["wall"].height

        # ball vs wall
        if not WALL_WIDTH < self.ball.pos.x < WINDOW_WIDTH - WALL_WIDTH - self.ball.texture.width:
            self.ball.direction.x *= -1

        if self.ball.pos.y < WALL_HEIGHT:
            self.ball.direction.y *= -1

        if self.ball.pos.y > WINDOW_HEIGHT - WALL_HEIGHT - self.ball.texture.height:
            if not self.ball.chance_consumed:
                self.ball.chance_consumed = True
                self.ball.direction.y *= -1



        # ball vs player
        if check_collision_recs(self.ball.get_rect(), self.player.get_rect()):
            
            self.ball.direction.y *= -1
            self.ball.pos.y = self.player.pos.y - self.ball.texture.height

        # ball vs brick
        for brick in self.bricks:
            if check_collision_recs(self.ball.get_rect(), brick.rect):

                # 99% accurate algorithm
                if self.ball.pos.x + 5.5 < brick.pos.x and \
                self.ball.direction.x > 0:
                    print("LEFT")
                    self.ball.direction.x *= -1
                    self.ball.pos.x = brick.pos.x - self.ball.texture.width

                elif self.ball.pos.x + 16.5 > brick.pos.x + brick.texture.width and \
                self.ball.direction.x < 0:
                    print("RIGHT")
                    self.ball.direction.x *= -1
                    self.ball.pos.x = brick.pos.x + brick.texture.width

                elif self.ball.pos.y < brick.pos.y:
                    print("TOP")
                    self.ball.direction.y *= -1
                    self.ball.pos.y = brick.pos.y - self.ball.texture.height
                else:
                    print("BOT")
                    self.ball.direction.y *= -1
                    self.ball.pos.y = brick.pos.y + brick.texture.height


                self.bricks.remove(brick)
                self.player.score += 1

                

    def run(self):
        while not window_should_close():
            self.update()
            self.draw()
        close_audio_device()
        close_window()
            
    def check_ball_out_of_screen(self):
        if self.ball.pos.y >= WINDOW_HEIGHT:
            if self.player.life > 1:
                self.player.life -= 1
                self.state = "paused"
            else: 
                self.state = "gameover"
            
            

if __name__ == "__main__":
    game = Game()
    game.run()