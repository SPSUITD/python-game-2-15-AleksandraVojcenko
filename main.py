import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размеры экрана
WIDTH, HEIGHT = 800, 600

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Инициализация экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")
background_image = pygame.image.load('resources/game_screen.png').convert()
menu_background_image = pygame.image.load('resources/menu_screen.png').convert()

# Инициализация платформ и мяча
platform_width, platform_height = 120, 15
ball_size = 20
platform1_image = pygame.image.load('resources/platform1.png').convert_alpha()
platform2_image = pygame.image.load('resources/platform2.png').convert_alpha()

platform_speed = 10
ball_speed = [0, 0]  # Изначально мяч стоит на месте
initial_ball_speed = [5, 5]  # Начальная скорость мяча
ball_acceleration = -0.2  # Незначительное ускорение при отскоках

platform1 = pygame.Rect(WIDTH // 2 - platform_width // 2, HEIGHT - platform_height - 20, platform_width,
                        platform_height)
platform2 = pygame.Rect(WIDTH // 2 - platform_width // 2, 20, platform_width, platform_height)
ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2, ball_size, ball_size)

clock = pygame.time.Clock()

# Счет
score1 = 0
score2 = 0

font = pygame.font.Font(None, 36)

# Переменная состояния для определения, находится ли игра в главном меню
in_menu = True

# Переменная состояния для отсчета времени перед стартом
countdown_timer = 180  # 3 секунды * 60 кадров/секунду

# Переменные для определения видимости мяча и платформ
ball_visible = False
platforms_visible = True


def handle_ball_platform_collision(ball, platform):
    global ball_speed
    if ball.colliderect(platform):
        if ball_speed[1] > 0:  # Мяч движется вниз
            ball.top = platform.top - ball.height
        else:  # Мяч движется вверх
            ball.bottom = platform.bottom + ball.height
        ball_speed[1] = -ball_speed[1] + (ball_speed[1] / abs(ball_speed[1])) * ball_acceleration


def reset_ball():
    global ball_speed, ball_visible
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed = [0, 0]
    ball_visible = False


def update_score(ball):
    global score1, score2
    if ball.top <= 0:
        score2 += 1
        reset_ball()
    elif ball.bottom >= HEIGHT:
        score1 += 1
        reset_ball()

    # Проверка на завершение игры
    if score1 >= 10 or score2 >= 10:
        # Заполняем экран чёрным цветом
        screen.fill(BLACK)

        # Вывод сообщения о победе
        winner = "Player 1" if score1 >= 10 else "Player 2"
        victory_text = font.render(f"{winner} wins! Press Enter to restart", True, WHITE)
        screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        # Ожидание нажатия клавиши Enter для перезапуска игры
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Обнуление счета и перезапуск игры
                        score1 = 0
                        score2 = 0
                        reset_ball()
                        return


def draw_menu():
    screen.blit(menu_background_image, (0, 0))
    pygame.display.flip()


# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and in_menu:
                in_menu = False
                reset_ball()
                countdown_timer = 180  # Сбрасываем таймер перед стартом
            elif event.key == pygame.K_ESCAPE and not in_menu:
                in_menu = True
                reset_ball()

    if in_menu:
        draw_menu()
    else:
        keys = pygame.key.get_pressed()

        # Управление платформами
        if keys[pygame.K_LEFT] and platform1.left > 0:
            platform1.move_ip(-platform_speed, 0)
        if keys[pygame.K_RIGHT] and platform1.right < WIDTH:
            platform1.move_ip(platform_speed, 0)

        if keys[pygame.K_a] and platform2.left > 0:
            platform2.move_ip(-platform_speed, 0)
        if keys[pygame.K_d] and platform2.right < WIDTH:
            platform2.move_ip(platform_speed, 0)

        # Таймер перед стартом
        if countdown_timer > 0:
            countdown_timer -= 1
            ball_visible = False  # Делаем мяч невидимым во время таймера
        else:
            # Движение мяча после завершения таймера
            ball_visible = True
            ball.move_ip(ball_speed[0], ball_speed[1])

            # Если мяч стоит на месте, устанавливаем начальную скорость
            if ball_speed == [0, 0]:
                ball_speed = initial_ball_speed

            # Обработка столкновений с верхней и нижней границами
            if ball.top <= 0 or ball.bottom >= HEIGHT:
                ball_speed[1] = -ball_speed[1]

            # Обработка столкновений с платформами
            handle_ball_platform_collision(ball, platform1)
            handle_ball_platform_collision(ball, platform2)

            # Обработка счета
            update_score(ball)

            # Проверка на выход мяча за границы по бокам
            if ball.left <= 0 or ball.right >= WIDTH:
                ball_speed[0] = -ball_speed[0]

        # Очистка экрана
        screen.blit(background_image, (0, 0))

        # Отрисовка платформ и мяча, только если мяч видим
        if ball_visible:
            screen.blit(platform1_image, platform1)
            screen.blit(platform2_image, platform2)
            pygame.draw.ellipse(screen, WHITE, ball)

        # Отрисовка счета
        score_text = font.render(f"{score1} - {score2}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

        # Отрисовка таймера перед стартом
        if countdown_timer > 0:
            countdown_text = font.render(str((countdown_timer // 60) + 1), True, WHITE)
            screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2))

        # Обновление экрана
        pygame.display.flip()

        # Задержка для контроля частоты кадров
        clock.tick(60)
