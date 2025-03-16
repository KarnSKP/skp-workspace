import pygame
import numpy as np

pygame.init()

resolution = (720, 540)
screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
running = True

fps = 180
dt = 1 / fps

screen_color = (0, 0, 0)
factor = resolution[0] / 3

obj_color = (255, 0, 0)
obj_radius = 0.05 * factor
obj_radius_sq = obj_radius ** 2
choose = {}

N = 5
l, k, mass = 0.8 * factor / (N - 1), 5000, 1

gravity = pygame.Vector2(0, 9.81) * factor

mid = (resolution[0] / 2, resolution[1] / 2)
pos = [[pygame.Vector2(mid[0] + j * l - (N - 1) * l / 2, mid[1] + i * l - (N - 1) * l / 2) for j in range(N)] for i in range(N)]
vel = [[pygame.Vector2(0, 0) for _ in range(N)] for _ in range(N)]
choose = [[False for _ in range(N)] for _ in range(N)]
stop = False

def get_acc(pos):
    acc = [[pygame.Vector2(0, 0) for _ in range(N)] for _ in range(N)]
    
    for i in range(N):
        for j in range(N):
            Fs = pygame.Vector2(0, 0)

            for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < N and 0 <= nj < N:
                    dist_vec = pos[ni][nj] - pos[i][j]
                    rest_length = l * (np.sqrt(2) if abs(di) + abs(dj) == 2 else 1)
                    try:
                        Fs += k * (dist_vec - rest_length * dist_vec.normalize())
                    except ValueError:
                        pass
            
            acc[i][j] = (Fs + gravity) / mass
    return acc

def if_collisions():
    for i1 in range(N):
        for j1 in range(N):
            for i2 in range(N):
                for j2 in range(N):
                    if (i1, j1) >= (i2, j2):
                        continue
                    
                    ball1, ball2 = pos[i1][j1], pos[i2][j2]
                    vel1, vel2 = vel[i1][j1], vel[i2][j2]
                    
                    diff = ball2 - ball1
                    dist_sq = diff.length_squared()
                    min_dist = 2 * obj_radius

                    if dist_sq < min_dist ** 2 and dist_sq != 0:
                        dist = np.sqrt(dist_sq)
                        norm = diff / dist
                        
                        overlap = min_dist - dist
                        ball1 -= norm * (overlap / 2)
                        ball2 += norm * (overlap / 2)

                        rel_vel = vel2 - vel1
                        speed_n = rel_vel.dot(norm)

                        if speed_n > 0:
                            continue

                        impulse = -2 * speed_n / (2 * mass)
                        vel1 -= impulse * norm
                        vel2 += impulse * norm

acc = get_acc(pos)

while running:
    screen.fill(screen_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pressed = pygame.mouse.get_pressed()[0]
    mouse_pos = pygame.mouse.get_pos()

    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_SPACE]:
        stop = True
    else:
        stop = False
    if key_pressed[pygame.K_r]:
        mid = (resolution[0] / 2, resolution[1] / 2)
        pos = [[pygame.Vector2(mid[0] + j * l - (N - 1) * l / 2, mid[1] + i * l - (N - 1) * l / 2) for j in range(N)] for i in range(N)]
        vel = [[pygame.Vector2(0, 0) for _ in range(N)] for _ in range(N)]

    if_collisions()
    acc = get_acc(pos)
    for i in range(N):
        for j in range(N):
            if mouse_pressed:
                if (mouse_pos[0] - pos[i][j].x) ** 2 + (mouse_pos[1] - pos[i][j].y) ** 2 <= obj_radius_sq:
                    choose[i][j] = True

            if choose[i][j]:
                vel[i][j].update(0, 0)
                acc[i][j].update(0, 0)
                pos[i][j].x, pos[i][j].y = mouse_pos

            if choose[i][j] and not mouse_pressed:
                choose[i][j] = False

            if pos[i][j].x >= resolution[0] - obj_radius:
                pos[i][j].x = resolution[0] - obj_radius
                vel[i][j].update(0, 0)
            elif pos[i][j].x <= obj_radius:
                pos[i][j].x = obj_radius
                vel[i][j].update(0, 0)

            if pos[i][j].y >= resolution[1] - obj_radius:
                pos[i][j].y = resolution[1] - obj_radius
                vel[i][j].update(0, 0)
            elif pos[i][j].y <= obj_radius:
                pos[i][j].y = obj_radius
                vel[i][j].update(0, 0)

            if not stop:
                vel[i][j] += acc[i][j] * dt
                pos[i][j] += vel[i][j] * dt + 0.5 * acc[i][j] * dt**2

    for i in range(N):
        for j in range(N):
            pygame.draw.circle(screen, obj_color, pos[i][j], obj_radius)
            if i < N - 1:
                pygame.draw.line(screen, obj_color, pos[i][j], pos[i + 1][j], int(0.5 * obj_radius))
            if j < N - 1:
                pygame.draw.line(screen, obj_color, pos[i][j], pos[i][j + 1], int(0.5 * obj_radius))
            if i < N - 1 and j < N - 1:
                pygame.draw.line(screen, obj_color, pos[i][j], pos[i + 1][j + 1], int(0.4 * obj_radius))
                pygame.draw.line(screen, obj_color, pos[i][j + 1], pos[i + 1][j], int(0.4 * obj_radius))

    pygame.display.flip()
    clock.tick_busy_loop(fps)

pygame.quit()
