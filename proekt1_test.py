import pytest
import pygame
from proekt1 import reset_game, Bird, change_bird, Pipe, Button, sc


def test_reset_game():
    assert reset_game() == 0

def test_bird_initialization():
    bird = Bird(100, 200)
    assert bird.rect.center == (100, 200)
    assert bird.vel == 0
    assert bird.clicked is False

def test_change_bird():
    global current_skin
    initial_skin = current_skin
    bird_skins = [1,2,3,4]
    change_bird()
    assert current_skin == (initial_skin + 1) % len(bird_skins)

def test_pipe_initialization():
    pipe = Pipe(300, 400, 1)
    assert pipe.rect.topleft == (300, 400)
    assert pipe.image is not None

def test_button_initialization():
    button = Button(200, 300, pygame.Surface((50, 50)))
    assert button.rect.topleft == (200, 300)
    assert button.image is not None


def test_sc():
    pygame.init()

    screen = pygame.Surface((800, 600))
    scores = 42
    x, y = 100, 200
    sc(scores, x, y)
    rect_four = pygame.Rect(x, y, 20, 20)
    image_four = pygame.Surface((20, 20))

    rect_two = pygame.Rect(x + 20, y, 20, 20)
    image_two = pygame.Surface((20, 20))

    assert screen.get_rect().contains(rect_four)
    assert screen.get_rect().contains(rect_two)

    assert screen.get_rect().contains(image_four)
    assert screen.get_rect().contains(image_two)

