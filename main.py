import pygame
import os
from pygame import sprite, transform, image, Surface

pygame.init()
win_width = 800
win_height = 600
ball_radius = 15
ball_x = win_width // 2
ball_y = win_height // 2

clock = pygame.time.Clock()
spawn_ball = pygame.USEREVENT + 1 

window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Game")

try:
    img = pygame.image.load("bg.png")
    background = pygame.transform.scale(img, (win_width, win_height))
except:
    background = pygame.Surface((win_width, win_height))
    background.fill((0, 0, 255)) 


pygame.time.set_timer(spawn_ball, 1000)

class Sprite(sprite.Sprite):
    def __init__(self, _img_path=None, _img_width=150, _img_height=150, _img_col=(150, 150, 150)):
        super().__init__()
        self.img_path = _img_path
        self.img_width = _img_width
        self.img_height = _img_height
        self.img_col = _img_col

        if _img_path and os.path.exists(_img_path):
            self.image = transform.scale(image.load(_img_path), (_img_width, _img_height))
        else:
            self.image = Surface((_img_width, _img_height))
            self.image.fill(_img_col)

class Object(Sprite):
    def __init__(self, _img_path=None, _img_width=150, _img_height=150, _img_col=(255, 255, 255), _x=0, _y=0):
        super().__init__(_img_path, _img_width, _img_height, _img_col)
        self.rect = self.image.get_rect()
        self.rect.x = _x
        self.rect.y = _y
        self.speed = 7
        self.limit_left = self.limit_right = self.limit_up = self.limit_down = None

    def draw(self, _win):
        _win.blit(self.image, self.rect)

    def move_controls2(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and (self.limit_up is None or self.rect.y > self.limit_up):
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and (self.limit_down is None or self.rect.bottom < self.limit_down):
            self.rect.y += self.speed

    def move_controls(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and (self.limit_up is None or self.rect.y > self.limit_up):
            self.rect.y -= self.speed
        if keys[pygame.K_s] and (self.limit_down is None or self.rect.bottom < self.limit_down):
            self.rect.y += self.speed

    def move_ball(self, ball):
        if ball.rect.y < self.rect.y + self.rect.height // 2:
            self.rect.y -= self.speed
        elif ball.rect.y > self.rect.y + self.rect.height // 2:
            self.rect.y += self.speed

class Game:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.fps = 60
        self.bg_color = (50, 50, 50) 
        self.ball_speed_x = 5
        self.ball_speed_y = 5

        self.ball_active = True
        self.respawn_delay = 2000
        

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("My Managed Game")
        self.clock = pygame.time.Clock()
        self.running = True

        try:
            bg_path = os.path.join(os.path.dirname(__file__), "table.png")
            bg_img = image.load(bg_path)
            self.background = transform.scale(bg_img, (self.screen_width, self.screen_height))
        except Exception:
            self.background = Surface((self.screen_width, self.screen_height))
            self.background.fill(self.bg_color)

        self.player = Object(_img_path="palddle.jpg", _img_width=60, _img_height=60, _x=10, _y=self.screen_height//2)
        self.player2 = Object(_img_path="palddle.jpg", _img_width=60, _img_height=60, _x=self.screen_width-70, _y=self.screen_height//2)
        self.ball = Object(_img_path="ball.png", _img_width=30, _img_height=30, _x=self.screen_width//2, _y=self.screen_height//2)
        
        self.player.limit_up = 0
        self.player.limit_down = self.screen_height

        self.player2.limit_up = 0
        self.player2.limit_down = self.screen_height

        self.ball.limit_left = 0
        self.ball.limit_right = self.screen_width
        self.ball.limit_up = 0
        self.ball.limit_down = self.screen_height

    def run(self):
        """The main execution loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == spawn_ball and not self.ball_active:
                pygame.time.set_timer(spawn_ball, 0)
                self.ball.rect.center = (self.screen_width // 2, self.screen_height // 2)
                self.ball_speed_x = 5 if pygame.time.get_ticks() % 2 == 0 else -5
                self.ball_speed_y = 5 if pygame.time.get_ticks() % 3 == 0 else -5
                self.ball_active = True

    def update(self):
        self.player.move_controls()
        self.player2.move_controls2()

        if self.ball_active:
            self.ball.rect.x += self.ball_speed_x
            self.ball.rect.y += self.ball_speed_y

            if self.ball.rect.top <= self.ball.limit_up:
                self.ball.rect.top = self.ball.limit_up
                self.ball_speed_y *= -1
            if self.ball.rect.bottom >= self.ball.limit_down:
                self.ball.rect.bottom = self.ball.limit_down
                self.ball_speed_y *= -1

            if self.ball.rect.colliderect(self.player.rect) and self.ball_speed_x < 0:
                self.ball_speed_x *= -1
            if self.ball.rect.colliderect(self.player2.rect) and self.ball_speed_x > 0:
                self.ball_speed_x *= -1
            if self.ball.rect.left <= self.ball.limit_left or self.ball.rect.right >= self.ball.limit_right:
                self.ball.rect.center = (self.screen_width // 2, self.screen_height // 2)
                self.ball_active = False
                pygame.time.set_timer(spawn_ball, self.respawn_delay)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)
        self.player2.draw(self.screen)
        if self.ball_active:
            self.ball.draw(self.screen)
        else:
            pass
        pygame.display.update()


if __name__ == "__main__":
    Game().run()
