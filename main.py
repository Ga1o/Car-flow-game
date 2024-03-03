import pygame
import random


pygame.init()

SCREEN_WIDTH = 350
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Flow | CF")

player_img = pygame.image.load("car.png")
obstacle_img = pygame.image.load("car2.png")
background_img = pygame.image.load("road.png")

# Размеры игрока и препятствия
player_width, player_height = player_img.get_width(), player_img.get_height()
obstacle_width, obstacle_height = obstacle_img.get_width(), obstacle_img.get_height()

# Позиция игрока
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10

player_speed = 5
obstacles = []
min_obstacle_distance = 70
score = 0

# Счетчик пройденных препятствий для увеличения скорости, уровня сложности и состояния игры
score_for_speed_increase = 0
difficulty_level = 1
game_running = False

# Увеличение скорости препятствий и уровня сложности каждые 5 пройденных препятствий
speed_increase_interval = 5
speed_increase_amount = 1
difficulty_increase_interval = 5
difficulty_increase_amount = 1

# Шрифт для отображения текста
font = pygame.font.Font(None, 25)

# Создание кнопки "Старт"
start_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 25, 100, 50)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if start_button.collidepoint(mouse_pos) and not game_running:
                obstacles.clear()
                player_x = SCREEN_WIDTH // 2 - player_width // 2
                score = 0
                difficulty_level = 1
                obstacle_speed = 3
                difficulty_increase_interval = 5
                game_running = True

    # Логика игры
    if game_running:

        # Управление игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_speed

        # Добавление нового препятствия
        if random.randint(0, 50) < 5:
            obstacle_x = random.randint(0, SCREEN_WIDTH - obstacle_width)
            if not any(
                    obstacle_x - min_obstacle_distance < obs[0] < obstacle_x + min_obstacle_distance
                    for obs in obstacles
            ):
                obstacles.append([obstacle_x, 0])

        # Обновление позиции препятствий, увеличение скорости и уровня сложности
        for obstacle in obstacles:
            obstacle[1] += obstacle_speed

            if (
                player_x < obstacle[0] + obstacle_width
                and player_x + player_width > obstacle[0]
                and player_y < obstacle[1] + obstacle_height
                and player_y + player_height > obstacle[1]
            ):
                game_running = False

            if obstacle[1] > SCREEN_HEIGHT:
                score += 1
                score_for_speed_increase += 1
                obstacles.remove(obstacle)

            if score_for_speed_increase >= speed_increase_interval:
                obstacle_speed += speed_increase_amount
                score_for_speed_increase = 0

            if score >= difficulty_increase_interval:
                difficulty_level += difficulty_increase_amount
                difficulty_increase_interval += 5

    # Отображение фонового изображения
    screen.blit(background_img, (0, 0))

    # Отображение игрока
    screen.blit(player_img, (player_x, player_y))

    # Отображение препятствий
    for obstacle in obstacles:
        screen.blit(obstacle_img, (obstacle[0], obstacle[1]))

    # Отображение кнопки "Старт" при не запущенной игре
    if not game_running:
        pygame.draw.rect(screen, (200, 120, 20), start_button)
        text = font.render("СТАРТ", True, (0, 0, 0))
        text_rect = text.get_rect(center=start_button.center)
        screen.blit(text, text_rect)

    # Отображение уровня сложности
    difficulty_text = font.render("SPD: " + str(difficulty_level), True, (0, 0, 0))
    screen.blit(difficulty_text, (10, 10))

    # Отображение счета
    score_text = font.render("SCR: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (10, 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
