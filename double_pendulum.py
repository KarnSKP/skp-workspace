import pygame
import numpy as np
from numba import njit

pygame.init()

resolution = (720, 720)
screen = pygame.display.set_mode(resolution)
screen_color = (0, 0, 0)

clock = pygame.time.Clock()
fps = 500
dt = 1/fps
running = True
time = 0

text_size = 35
text_color = (255, 255, 255)
text_font = pygame.font.SysFont('Arial', text_size, bold=True, italic=True)
text_the1_pos = pygame.Vector2(0, 0)
text_the2_pos = pygame.Vector2(0, text_size)
text_time_pos = pygame.Vector2(0, screen.get_height() - text_size)
text_energy_pos = pygame.Vector2(0, screen.get_height() - 2*text_size)

def text_print(text, font, color, pos):
    img = font.render(text, True, color)
    screen.blit(img, pos)

length_factor = screen.get_height()/3 # screen height = 3 m
g = 9.8 * length_factor
m1, l1 = 0.25, 0.6 * length_factor
m2, l2 = 0.25, 0.3 * length_factor

y_unit = pygame.Vector2(0, 1)

the1 = np.radians(90)
the2 = np.radians(120)
a = pygame.Vector2(screen.get_width()/2, 0.4*screen.get_height())
ra1 = pygame.Vector2(l1 * np.sin(the1), l1 * np.cos(the1))
r12 = pygame.Vector2(l2 * np.sin(the2), l2 * np.cos(the2))
r1 = a + ra1
r2 = r1 + r12

the1_dot = 0
the2_dot = 0

@njit(fastmath=True)
def the_ddot(the1, the2, the1_dot, the2_dot):
    the1_ddot = (
        -g * (2*m1 + m2) * np.sin(the1)
        - m2 * g * np.sin(the1 - 2*the2)
        - 2 * np.sin(the1 - the2) * m2
            * (the2_dot**2 * l2 + the1_dot**2 * l1 * np.cos(the1 - the2))
        ) / (
        l1 * (2*m1 + m2 - m2 * np.cos(2*the1 - 2*the2))
        )

    the2_ddot = (
          2 * np.sin(the1 - the2)
            * (
              the1_dot**2 * l1 * (m1 + m2)
              + g * (m1 + m2) * np.cos(the1)
              + the2_dot**2 * l2 * m2 * np.cos(the1 - the2)
            )
        ) / (
          l2 * (2*m1 + m2 - m2 * np.cos(2*the1 - 2*the2))
        )
    return the1_ddot, the2_ddot

@njit(fastmath=True)
def rk4(the1, the2, the1_dot, the2_dot):
    k1_the = (the1_dot, the2_dot)
    k1_the_dot = the_ddot(the1, the2, k1_the[0], k1_the[1])

    k2_the = (the1_dot + 0.5*dt*k1_the_dot[0], the2_dot + 0.5*dt*k1_the_dot[1])
    k2_the_dot = the_ddot(the1 + the1_dot*dt/2, the2 + the2_dot*dt/2, k2_the[0], k2_the[1])

    k3_the = (the1_dot + 0.5*dt*k2_the_dot[0], the2_dot + 0.5*dt*k2_the_dot[1])
    k3_the_dot = the_ddot(the1 + the1_dot*dt/2, the2 + the2_dot*dt/2, k3_the[0], k3_the[1])

    k4_the = (the1_dot + dt*k3_the_dot[0], the2_dot + dt*k3_the_dot[1])
    k4_the_dot = the_ddot(the1 + the1_dot*dt, the2 + the2_dot*dt, k4_the[0], k4_the[1])

    the1 += dt/6*(k1_the[0] + 2*k2_the[0] + 2*k3_the[0] + k4_the[0])
    the2 += dt/6*(k1_the[1] + 2*k2_the[1] + 2*k3_the[1] + k4_the[1])
    the1_dot += dt/6*(k1_the_dot[0] + 2*k2_the_dot[0] + 2*k3_the_dot[0] + k4_the_dot[0])
    the2_dot += dt/6*(k1_the_dot[1] + 2*k2_the_dot[1] + 2*k3_the_dot[1] + k4_the_dot[1])
    return the1, the2, the1_dot, the2_dot

obj1_color = (255, 0, 0)
obj2_color = (255, 0, 0)
obj1_radius = 0.07 * length_factor
obj2_radius = 0.07 * length_factor
line_color = (50, 50, 50)

trail = [(r2.x, r2.y), (r2.x, r2.y)]
trail_color = (0, 0, 255)
trail_on = True
toggle = False

stop = False
choose1 = False
choose2 = False

while running:
    screen.fill(screen_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if trail_on:
        pygame.draw.lines(screen, trail_color, False, trail, width=2)
    pygame.draw.lines(screen, line_color, False, [a, r1, r2], width=10)
    pygame.draw.circle(screen, obj1_color, r1, obj1_radius)
    pygame.draw.circle(screen, obj2_color, r2, obj2_radius)

    keys_state = pygame.key.get_pressed()
    buttons_state = pygame.mouse.get_pressed()

    if keys_state[pygame.K_SPACE]:
        stop = True
    else:
        stop = False

    if keys_state[pygame.K_r] and not keys_state[pygame.K_LSHIFT]:
        the1 = 90 * np.pi/180
        the2 = 120 * np.pi/180
        ra1 = pygame.Vector2(l1 * np.sin(the1), l1 * np.cos(the1))
        r12 = pygame.Vector2(l2 * np.sin(the2), l2 * np.cos(the2))
        r1 = a + ra1
        r2 = r1 + r12

        the1_dot = 0
        the2_dot = 0
        time = 0

        trail = [(r2.x, r2.y), (r2.x, r2.y)]
    elif keys_state[pygame.K_r] and keys_state[pygame.K_LSHIFT]:
        trail = [(r2.x, r2.y), (r2.x, r2.y)]

    if keys_state[pygame.K_f]:
        toggle = True
    if toggle and not keys_state[pygame.K_f]:
        trail_on = not trail_on
        toggle = False

    if buttons_state[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse = pygame.Vector2(mouse_x, mouse_y)
        dis1 = pygame.Vector2.distance_to(mouse, r1)
        dis2 = pygame.Vector2.distance_to(mouse, r2)

        if dis1 <= obj1_radius:
            choose1 = True

        elif dis2 <= obj2_radius:
            choose2 = True

        if choose1:
            r1 = a + l1/pygame.Vector2.magnitude(mouse - a) * (mouse - a)
            the1 = np.arccos(pygame.Vector2.dot(r1 - a, y_unit)/pygame.Vector2.magnitude(r1 - a)) if r1.x >= a.x else -np.arccos(pygame.Vector2.dot(r1 - a, y_unit)/pygame.Vector2.magnitude(r1 - a))
            the1_dot, the2_dot = 0, 0          
            the1_ddot, the2_ddot = the_ddot(the1, the2, the1_dot, the2_dot)
        elif choose2:
            r2 = r1 + l2/pygame.Vector2.magnitude(mouse - r1) * (mouse - r1)
            the2 = np.arccos(pygame.Vector2.dot(r2 - r1, y_unit)/pygame.Vector2.magnitude(r2 - r1)) if r2.x >= r1.x else -np.arccos(pygame.Vector2.dot(r2 - r1, y_unit)/pygame.Vector2.magnitude(r2 - r1))
            the1_dot, the2_dot = 0, 0
            the1_ddot, the2_ddot = the_ddot(the1, the2, the1_dot, the2_dot)
        
        if choose1 or choose2:
            time = 0
            trail = [(r2.x, r2.y), (r2.x, r2.y)]
    else:
        choose1 = False
        choose2 = False

    if not stop:
        the1, the2, the1_dot, the2_dot = rk4(the1, the2, the1_dot, the2_dot)
        time += dt

    ra1 = pygame.Vector2(l1 * np.sin(the1), l1 * np.cos(the1))
    r12 = pygame.Vector2(l2 * np.sin(the2), l2 * np.cos(the2))
    r1 = a + ra1
    r2 = r1 + r12

    energy = (0.5*m1*(l1*the1_dot)**2 + 0.5*m2*(l1*the1_dot*np.cos(the1) + l2*the2_dot*np.cos(the2))**2 + 0.5*m2*(l1*the1_dot*np.sin(the1) + l2*the2_dot*np.sin(the2))**2 - m1*g*r1.y - m2*g*r2.y) / length_factor**2

    trail.append((r2.x, r2.y))

    text_print(f'θ1: {abs(np.degrees(the1)) % 360:.1f}°', text_font, text_color, text_the1_pos)
    text_print(f'θ2: {abs(np.degrees(the2)) % 360:.1f}°', text_font, text_color, text_the2_pos)
    text_print(f'time: {time:.1f}s.', text_font, text_color, text_time_pos)
    text_print(f'energy: {energy:.3f}J.', text_font, text_color, text_energy_pos)

    pygame.display.flip()
    clock.tick_busy_loop(fps)

pygame.quit()
