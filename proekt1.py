import pygame
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 790

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(pygame.image.load('img/птичка1.png').convert_alpha())

sndDie = pygame.mixer.Sound('sounds/die.mp3')
sndScore = pygame.mixer.Sound('sounds/point.mp3')
sndFlap = pygame.mixer.Sound('sounds/flap.mp3')
sounds_playing = False

best_score = 0
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 200
pipe_frequency = 1200 * 4
last_pipe = pygame.time.get_ticks() - pipe_frequency
score_table = pygame.image.load('img/Mobile---Flappy-Bird---Version-1.png').convert_alpha()
score_1 = pygame.image.load('img/medals_1.png').convert_alpha()
score_2 = pygame.image.load('img/medals_2.png').convert_alpha()
score_3 = pygame.image.load('img/medals_3.png').convert_alpha()
score_4 = pygame.image.load('img/medals_4.png').convert_alpha()
scores = 0
score = [
    pygame.image.load('img/m_0.png').convert_alpha(),
    pygame.image.load('img/m_1.png').convert_alpha(),
    pygame.image.load('img/m_2.png').convert_alpha(),
    pygame.image.load('img/m_3.png').convert_alpha(),
    pygame.image.load('img/m_4.png').convert_alpha(),
    pygame.image.load('img/m_5.png').convert_alpha(),
    pygame.image.load('img/m_6.png').convert_alpha(),
    pygame.image.load('img/m_7.png').convert_alpha(),
    pygame.image.load('img/m_8.png').convert_alpha(),
    pygame.image.load('img/m_9.png').convert_alpha()
]
pass_pipe = False

bg = pygame.image.load('img/bg.png').convert_alpha()
ground_img = pygame.image.load('img/ground.png').convert_alpha()
button_img = pygame.image.load('img/restart.png').convert_alpha()


def reset_game():
    """
    Resets the game state.
    Clears the pipe group, resets the bird's position, and sets the score to zero.

    :return: The updated score.
    :rtype: int
    """
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    scores = 0
    return scores


bird_skins = [
    [pygame.image.load(f'img/bird{num}.png').convert_alpha() for num in range(1, 4)],
    [pygame.image.load(f'img/птичка{num}_03.png').convert_alpha() for num in range(1, 4)],
    [pygame.image.load(f'img/птичка{num}син_03.png').convert_alpha() for num in range(1, 4)],
]
current_skin = 0


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        Initializes the Bird class.

        :param int x: The initial x-coordinate of the bird.
        :param int y: The initial y-coordinate of the bird.
        """
        pygame.sprite.Sprite.__init__(self)
        self.images = bird_skins[current_skin]
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        """
        Updates the bird's position and animation.

        Handles bird movement, animation, and rotation based on game state.

        :return: None
        """
        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                if flying:
                    sndFlap.play()
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2.5)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


def change_bird():
    """
    Changes the current bird skin.

    Changes the current bird skin to the next available skin in a cyclic manner.

    :return: None
    """
    global current_skin
    current_skin = (current_skin + 1) % len(bird_skins)
    flappy.images = bird_skins[current_skin]
    flappy.index = 0
    flappy.image = flappy.images[flappy.index]


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        """
        Initializes the Pipe class.

        :param int x: The x-coordinate of the pipe.
        :param int y: The y-coordinate of the pipe.
        :param int position: The position of the pipe (1 for top, -1 for bottom).
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png').convert_alpha()
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        """
        Updates the pipe's position based on the scroll speed and removes it if it's off the screen.
        """
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x, y, image):
        """
        Initializes the Button class.

        :param int x: The x-coordinate of the button.
        :param int y: The y-coordinate of the button.
        :param pygame.Surface image: The image to be displayed on the button.
        """
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        """
        Draws the button on the screen and returns whether it was clicked.

        :return: True if the button was clicked, False otherwise.
        :rtype: bool
        """
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


def sc(scr, x, y):
    """
    Displays the score on the screen.

    Displays the score on the screen at the specified coordinates.

    :param int scr: The score to be displayed.
    :param int x: The x-coordinate of the score display.
    :param int y: The y-coordinate of the score display.
    :return: None
    """
    if scr > 9:
        return screen.blit(score[scr // 10], (x, y)), screen.blit(score[scr % 10], (x + 20, y))
    return screen.blit(score[scr], (x + 12, y))


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)

button = Button(screen_width // 2 - 55, screen_height // 2 - 50, button_img)
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
        if flying == False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    change_bird()

    clock.tick(fps)
    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    screen.blit(ground_img, (ground_scroll, 768))

    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                scores += 1
                sndScore.play()
                scroll_speed = 4 + scores // 20
                pass_pipe = False

    sc(scores, 400, 20)

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False
        scroll_speed = 4

    if game_over == False and flying == True:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency // scroll_speed:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
        pipe_group.update()

    if game_over == True:
        if not sounds_playing:
            sndDie.play()
            sounds_playing = True
        screen.blit(score_table, (290, 400))
        if scores > best_score:
            best_score = scores
        if 20 > scores:
            screen.blit(score_1, (325, 455))
        elif 40 > scores > 20:
            screen.blit(score_2, (325, 455))
        elif 70 > scores > 40:
            screen.blit(score_3, (325, 455))
        else:
            screen.blit(score_4, (325, 455))
        sc(scores, 515, 443)
        sc(best_score, 515, 500)
        if button.draw() == True:
            game_over = False
            sounds_playing = False
            scores = reset_game()

    pygame.display.update()

pygame.quit()