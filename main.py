import pygame


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
        self.spritesheet = load_spritesheet(spritesheet, 32, 32)
        self.pose = 0
        self.flipx = False
        self.lastflipx = False
        self.frame = 0
        self.frame_timer = 0

    def change_pos(self):
        self.lastflipx = self.flipx
        if self.vector[0] < 0:
            self.flipx = True
        elif self.vector[0] > 0:
            self.flipx = False
        if self.vector[0] == 0 and self.vector[1] == 1:
            self.pose = 0
        elif self.vector[0] != 0 and self.vector[1] == 1:
            self.pose = 1
        elif self.vector[0] != 0 and self.vector[1] == 0:
            self.pose = 2
        elif self.vector[0] != 0 and self.vector[1] == -1:
            self.pose = 3
        elif self.vector[0] == 0 and self.vector[1] == -1:
            self.pose = 4

    def draw(self):
        image = pygame.transform.scale(self.spritesheet[self.frame][self.pose], (self.width, self.height))
        self.change_pos()
        image = pygame.transform.flip(image, self.flipx, False)
        screen.blit(image, (self.x, self.y))

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
        self.x += self.vector[0] * self.speed
        self.y += self.vector[1] * self.speed
        self.draw()


class Player(Entity):
    def __init__(self, x, y, width, height, spritesheet, speed):
        super().__init__(x, y, width, height, spritesheet, speed)

    def update(self):
        super().update()

        self.x = max(0, min(self.x, 500 - self.width))
        self.y = max(0, min(self.y, 500 - self.height))


def load_spritesheet(filename, width, height):
    image = pygame.image.load(filename).convert_alpha()
    image_width, image_height = image.get_size()
    spritesheet = []
    for x in range(0, image_width // width):
        line = []
        spritesheet.append(line)
        for y in range(0, image_height // height):
            rect = (x * width, y * height, width, height)
            line.append(image.subsurface(rect))
    return spritesheet


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()

    objects = []
    player = Player(500 / 2, 500 / 2, 100, 100, "data/spritesheet_rus01.png", 2)

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
        clock.tick(60)
        pygame.display.update()
