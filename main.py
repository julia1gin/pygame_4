import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Параметры окна
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Размеры
PLAYER_SIZE = 50
PLAYER_SPEED = 5
JUMP_FORCE = -15
GRAVITY = 1
ITEM_SIZE = 20
PORTAL_SIZE = 60
PLATFORM_WIDTH = 120
PLATFORM_HEIGHT = 20

# Инициализация окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Практическая работа №4")
clock = pygame.time.Clock()

# Переменные персонажа
player_pos = [WINDOW_WIDTH // 2, WINDOW_HEIGHT - PLAYER_SIZE]
player_velocity = [0, 0]
is_jumping = False

# Неподвижные объекты, собираемые предметы, порталы и платформы
obstacles = []
def spawn_items():
    return [
        (pygame.Rect(random.randint(0, WINDOW_WIDTH - ITEM_SIZE), random.randint(0, WINDOW_HEIGHT - ITEM_SIZE), ITEM_SIZE, ITEM_SIZE), random.randint(1, 10))
        for _ in range(5)
    ]
items = spawn_items()
portals = [
    pygame.Rect(100, 100, PORTAL_SIZE, PORTAL_SIZE),
    pygame.Rect(600, 400, PORTAL_SIZE, PORTAL_SIZE)
]
platforms = [
    pygame.Rect(200, 500, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(400, 400, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(600, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT)
]

score = 0

# Основной игровой цикл
running = True
while running:
    screen.fill(WHITE)

    # События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_velocity[0] = -PLAYER_SPEED
            elif event.key == pygame.K_RIGHT:
                player_velocity[0] = PLAYER_SPEED
            elif event.key == pygame.K_UP and not is_jumping:
                player_velocity[1] = JUMP_FORCE
                is_jumping = True
        elif event.type == pygame.KEYUP:
            if event.key in {pygame.K_LEFT, pygame.K_RIGHT}:
                player_velocity[0] = 0

    # Гравитация
    player_velocity[1] += GRAVITY

    # Обновление позиции
    player_pos[0] += player_velocity[0]
    player_pos[1] += player_velocity[1]

    # Ограничения движения
    player_pos[0] = max(0, min(player_pos[0], WINDOW_WIDTH - PLAYER_SIZE))
    if player_pos[1] + PLAYER_SIZE >= WINDOW_HEIGHT:
        player_pos[1] = WINDOW_HEIGHT - PLAYER_SIZE
        player_velocity[1] = 0
        is_jumping = False

    # Проверка столкновений с платформами
    player_rect = pygame.Rect(player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE)
    on_ground = False
    for platform in platforms:
        if player_rect.colliderect(platform) and player_velocity[1] >= 0:
            player_pos[1] = platform.top - PLAYER_SIZE
            player_velocity[1] = 0
            is_jumping = False
            on_ground = True

    # Проверка сборки предметов
    collected_items = []
    for item, value in items:
        if player_rect.colliderect(item):
            score += value
            collected_items.append((item, value))
    items = [i for i in items if i not in collected_items]

    # Респавн предметов, если все собраны
    if not items:
        items = spawn_items()

    # Проверка пересечения с порталом
    for portal in portals:
        if player_rect.colliderect(portal):
            # Переместить игрока ко второму порталу
            other_portal = portals[1] if portal == portals[0] else portals[0]
            player_pos[0] = other_portal.x + (PORTAL_SIZE - PLAYER_SIZE) // 2
            player_pos[1] = other_portal.y + (PORTAL_SIZE - PLAYER_SIZE) // 2

    # Отрисовка игрока
    pygame.draw.rect(screen, BLUE, (*player_pos, PLAYER_SIZE, PLAYER_SIZE))

    # Отрисовка препятствий
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)

    # Отрисовка предметов
    for item, value in items:
        pygame.draw.rect(screen, YELLOW, item)

    # Отрисовка порталов
    for portal in portals:
        pygame.draw.ellipse(screen, PURPLE, portal)

    # Отрисовка платформ
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)

    # Отображение очков
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
