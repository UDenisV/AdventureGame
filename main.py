import pygame
from os import walk

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60


class Object:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.vector = [0, 0]
        objects.append(self)

    def draw(self):
        screen.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.x, self.y))

    def update(self):
        self.x += self.vector[0]
        self.y += self.vector[1]
        self.draw()


class Entity(Object):
    def __init__(self, x, y, width, height, spritesheet, speed):
        super().__init__(x, y, width, height, None)

        self.speed = speed
        self.spritesheet = load_spritesheet(spritesheet)
        self.pose = 'down'
        self.flipx = False
        self.frame = 0
        self.frame_timer = 0

    def change_pos(self):
        if self.vector[0] < 0:
            self.flipx = True
        elif self.vector[0] > 0:
            self.flipx = False
        if self.vector[0] == 0 and self.vector[1] == 1:
            self.pose = 'down'
        elif self.vector[0] != 0 and self.vector[1] == 1:
            self.pose = 'down_horizontal'
        elif self.vector[0] != 0 and self.vector[1] == 0:
            self.pose = 'horizontal'
        elif self.vector[0] != 0 and self.vector[1] == -1:
            self.pose = 'up_horizontal'
        elif self.vector[0] == 0 and self.vector[1] == -1:
            self.pose = 'up'

    def draw(self):
        image = pygame.transform.scale(self.spritesheet[self.pose][self.frame], (self.width, self.height))
        self.change_pos()
        image = pygame.transform.flip(image, self.flipx, False)
        screen.blit(image, (self.x, self.y))
        if 'attack' in self.pose:
            self.frame_timer += 1

            if self.frame_timer < 10:
                return
            if self.frame >= 2:
                self.pose.replace("_attack", "")
                return
            self.frame += 1
        else:
            if self.vector[0] == 0 and self.vector[1] == 0:
                self.frame = 0
                return

            self.frame_timer += 1

            if self.frame_timer < 5:
                return

            self.frame += 1
            if self.frame >= 6:
                self.frame = 0

            self.frame_timer = 0

    def update(self):
        self.draw()
        self.x += self.vector[0] * self.speed
        self.y += self.vector[1] * self.speed


class Player(Entity):
    def __init__(self, x, y, width, height, spritesheet, speed):
        super().__init__(x, y, width, height, spritesheet, speed)
        self.attacking = False
        self.attack_reload = 300
        self.attack_time = None

    def change_pos(self):
        if self.attacking:
            self.vector = [0, 0]
            if "attack" not in self.pose:
                self.pose = self.pose + '_attack'
        else:
            super().change_pos()
            if 'attack' in self.pose:
                self.pose = self.pose.replace("_attack", "")

    def attack(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.frame = 0
            self.attack_time = pygame.time.get_ticks()

    def reloading(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_reload:
                self.attacking = False
                self.frame = 0

    def update(self):
        super().update()
        self.attack()
        self.reloading()
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))


def load_spritesheet(filename):
    spritesheet = {"down": [], "down_horizontal": [], "horizontal": [], "up_horizontal": [], "up": [],
                   "down_attack": [], "down_horizontal_attack": [], "horizontal_attack": [], "up_horizontal_attack": [],
                   "up_attack": []}
    for pose in spritesheet.keys():
        path = filename + pose
        images = []
        for folder, nested_folder, files in walk(path):
            for file in files:
                full_path = path + "/" + file
                image = pygame.image.load(full_path).convert_alpha()
                images.append(image)
        spritesheet[pose] = images
    return spritesheet


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    objects = []
    player = Player(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 100, 200, 200, "data/player/", 2)

    running = True

    player_moving = {"left": False, "right": False, "up": False, "down": False}

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_moving["left"] = True
                elif event.key == pygame.K_RIGHT:
                    player_moving["right"] = True
                elif event.key == pygame.K_UP:
                    player_moving["up"] = True
                elif event.key == pygame.K_DOWN:
                    player_moving["down"] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player_moving["left"] = False
                elif event.key == pygame.K_RIGHT:
                    player_moving["right"] = False
                elif event.key == pygame.K_UP:
                    player_moving["up"] = False
                elif event.key == pygame.K_DOWN:
                    player_moving["down"] = False
        player.vector[0] = player_moving["right"] - player_moving["left"]
        player.vector[1] = player_moving["down"] - player_moving["up"]
        screen.fill((255, 255, 255))
        for obj in objects:
            obj.update()
        clock.tick(FPS)
        pygame.display.update()
