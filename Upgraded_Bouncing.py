import pygame
import random

pygame.init()

resolution = (1280, 720)
screen_color = (0, 0, 0)
fps = 240
dt = 1/fps

screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
running = True

text_size = 35
error_size = 20
text_font = pygame.font.SysFont("Arial", text_size, bold=True, italic=True)
error_font = pygame.font.SysFont("Arial", error_size, bold=True, italic=True)
text_color = (255, 255, 255)
text_speed_pos = pygame.Vector2(0, 0)
text_KE_pos = pygame.Vector2(0, text_size)
text_PE_pos = pygame.Vector2(0, 2 * text_size)
text_energy_pos = pygame.Vector2(0, 3 * text_size)
text_energyERROR_pos = pygame.Vector2(0, 4 * text_size + 0.5 * error_size)

factor = screen.get_height() / 3 # screen height = 3 m.
gravity = 9.81 * factor
damp = 1

mass = 2
obj_radius = 25
obj_color = (255, 0, 0)
obj_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
obj_vel = pygame.Vector2(factor, 0)
speed_init = pygame.Vector2.magnitude(obj_vel) / factor
energy_init = 0.5*mass*speed_init**2 + (mass*gravity*(screen.get_height() - obj_pos.y) / factor**2)

bound_radius_out = 320
bound_width = 2
bound_radius_in = bound_radius_out - bound_width
bound_color = (255, 255, 255)
bound_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)

def text_print(text, font, color, pos):
    img = font.render(text, True, color)
    screen.blit(img, pos)

stop = False

while running:
    screen.fill(screen_color)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    buttons_state = pygame.mouse.get_pressed()
    keys_state = pygame.key.get_pressed()

    if keys_state[pygame.K_SPACE]:
        stop = True
    else:
        stop = False

    if buttons_state[0]:
        obj_pos.x, obj_pos.y = pygame.mouse.get_pos()
        obj_vel = pygame.Vector2(0, 0)
        energy_init = (mass*gravity*(screen.get_height() - obj_pos.y) / factor**2)

    dis = pygame.Vector2.distance_to(bound_pos, obj_pos)

    if dis >= bound_radius_in - obj_radius:
        norm = (obj_pos - bound_pos) / pygame.Vector2.magnitude(obj_pos - bound_pos)
        v_norm = pygame.Vector2.dot(obj_vel, norm) * norm
        obj_vel = obj_vel - (1 + damp) * v_norm

    if not stop:
        obj_pos += obj_vel*dt + 0.5*pygame.Vector2(0, gravity)*dt**2
        obj_vel.y += gravity*dt
        speed = pygame.Vector2.magnitude(obj_vel) / factor
        KE = 0.5*mass*speed**2
        PE = (mass*gravity*(screen.get_height() - obj_pos.y) / factor**2)
        energy = 0.5*mass*speed**2 + (mass*gravity*(screen.get_height() - obj_pos.y) / factor**2)
        energyERROR = abs(1 - energy/energy_init) * 100

    pygame.draw.circle(screen, obj_color, obj_pos, obj_radius)
    pygame.draw.circle(screen, bound_color, bound_pos, bound_radius_out, width=bound_width)
    text_print(f"speed: {speed:.2f} m/s", text_font, text_color, text_speed_pos)
    text_print(f"KE: {KE:.2f} J", text_font, text_color, text_KE_pos)
    text_print(f"PE: {PE:.2f} J", text_font, text_color, text_PE_pos)
    text_print(f"KE + PE: {energy:.2f} J", text_font, text_color, text_energy_pos)

    if damp == 1:
        text_print(f"energyERROR: {energyERROR:.2f}%", error_font, text_color, text_energyERROR_pos)

    pygame.display.flip()

    clock.tick_busy_loop(fps)

pygame.quit()
