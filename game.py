import pygame
import sys

class SimpleGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('Simple Game')
        self.clock = pygame.time.Clock()
        self.cube_color = (255, 0, 0)
        self.cube_size = 50
        self.cube_x = 320
        self.cube_y = 240
        self.speed = 5

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.cube_y -= self.speed
            if keys[pygame.K_s]:
                self.cube_y += self.speed
            if keys[pygame.K_a]:
                self.cube_x -= self.speed
            if keys[pygame.K_d]:
                self.cube_x += self.speed


            if self.cube_x < 0:
                self.cube_x = 0
            if self.cube_x > 640 - self.cube_size:
                self.cube_x = 640 - self.cube_size
            if self.cube_y < 0:
                self.cube_y = 0
            if self.cube_y > 480 - self.cube_size:
                self.cube_y = 480 - self.cube_size

            self.screen.fill((0, 0, 0))
            pygame.draw.rect(self.screen, self.cube_color, (self.cube_x, self.cube_y, self.cube_size, self.cube_size))
            pygame.display.flip()
            self.clock.tick(60)

    def stop(self):
        pygame.quit()

