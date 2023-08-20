# Importando bibliotecas necessárias
import pygame, random, sys
from pygame.locals import *

def on_grid_random():
    # Retorna uma posição aleatória na grade (múltiplos de 10 para manter alinhamento).
    x = random.randint(0, 590)
    y = random.randint(0, 590)
    return (x // 10 * 10, y // 10 * 10)

def collision(c1, c2):
    # Verifica se duas coordenadas colidem (são iguais).
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

def game_over():
    # Exibe uma mensagem de game over e aguarda entrada para recomeçar ou sair.
    global snake, apple_pos, my_direction
    fonte = pygame.font.SysFont('Arial', 30)
    mensagem = fonte.render('Aperte ESPAÇO para recomeçar', True, (255, 255, 255))
    screen.blit(mensagem, (200, 250))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    reset_game()
                    return True  # indica que o jogo deve ser reiniciado
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def reset_game():
    # Reinicia os valores do jogo para iniciar um novo.
    global snake, apple_pos, my_direction
    snake = [(200, 200), (210, 200), (220, 200)]
    apple_pos = on_grid_random()
    my_direction = LEFT

# Definições de direções e inicialização do pygame.
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Snake')

# Inicialização das variáveis do jogo.
snake = [(200, 200), (210, 200), (220, 200)]
snake_skin = pygame.Surface((10, 10))
snake_skin.fill((255, 255, 255))

apple_pos = on_grid_random()
apple = pygame.Surface((10, 10))
apple.fill((255, 0, 0))

my_direction = LEFT

clock = pygame.time.Clock()

# Loop principal do jogo.
while True:
    clock.tick(20)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            # Captura entrada do jogador para alterar a direção ou reiniciar.
            if event.key == K_UP and my_direction != DOWN:
                my_direction = UP
            if event.key == K_DOWN and my_direction != UP:
                my_direction = DOWN
            if event.key == K_LEFT and my_direction != RIGHT:
                my_direction = LEFT
            if event.key == K_RIGHT and my_direction != LEFT:
                my_direction = RIGHT
            if event.key == K_SPACE:
                reset_game()

    # Verificação de colisão com o corpo da cobra.
    for i in range(1, len(snake)):
        if snake[0] == snake[i]:
            if game_over():
                break  # reinicia o loop para reiniciar o jogo
            else:
                pygame.quit()
                sys.exit()

    # Verificação de colisão com a maçã e atualização da posição da maçã.
    if collision(snake[0], apple_pos):
        apple_pos = on_grid_random()
        snake.append((0, 0))

    # Atualização da posição da cobra.
    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i - 1][0], snake[i - 1][1])

    # Movimentação da cabeça da cobra baseada na direção.
    if my_direction == UP:
        snake[0] = (snake[0][0], snake[0][1] - 10)
    if my_direction == DOWN:
        snake[0] = (snake[0][0], snake[0][1] + 10)
    if my_direction == RIGHT:
        snake[0] = (snake[0][0] + 10, snake[0][1])
    if my_direction == LEFT:
        snake[0] = (snake[0][0] - 10, snake[0][1])

    # Looping da cobra pelas bordas da tela.
    if snake[0][0] > 590:
        snake[0] = (0, snake[0][1])
    if snake[0][0] < 0:
        snake[0] = (600, snake[0][1])
    if snake[0][1] > 590:
        snake[0] = (snake[0][0], 0)
    if snake[0][1] < 0:
        snake[0] = (snake[0][0], 600)

    # Atualização da tela com os elementos do jogo.
    screen.fill((0, 0, 0))
    screen.blit(apple, apple_pos)
    for pos in snake:
        screen.blit(snake_skin, pos)
    pygame.display.update()
