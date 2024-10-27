import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as Ani
from rich.console import Console

x = 1
y = 0

Vx = -0.75
Vy = 0.5

trail_x = [x]
trail_y = [y]

time = 0
dt = 1e-2

fig, ax = plt.subplots()
ax.grid()
ax.set_aspect('equal')
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)

trail, = ax.plot([], [])
balls, = ax.plot([], [], 'o')
ax.plot([0], [0], 'o')
vector, = ax.plot([], [])

balls_t = ax.text(x, y, 'small dude')
ax.text(0, 0, 'massive guy')

start = None
end = None
hold = False

def A(x, y):
    r = (x**2 + y**2)**0.5
    return -x/r**3, -y/r**3

def press(event):
    global x, y, Vx, Vy, trail_x, trail_y, start, hold, time

    if event.button == 2 and event.inaxes == ax:
        hold = True

        start = (event.xdata, event.ydata)

        x = start[0]
        y = start[1]

        trail_x = [x]
        trail_y = [y]

        time = 0

def motion(event):
    global start, end, x, y, Vx, Vy, time

    if start is not None:
        end = (event.xdata, event.ydata)

        Vx = end[0] - start[0]
        Vy = end[1] - start[1]

        vector.set_data([start[0], end[0]], [start[1], end[1]])

        ax.set_title(f'time = {time:.1f}, speed = {(Vx**2 + Vy**2)**0.5:.2f}')

def release(event):
    global start, end, hold

    if event.button == 2 and event.inaxes == ax and start is not None and end is not None:
        hold = False
        start = None
        end = None

        vector.set_data([], [])

def RK4():
    global x, y, Vx, Vy

    k1x = Vx
    k1y = Vy
    k1Vx = A(x, y)[0]
    k1Vy = A(x, y)[1]

    k2x = Vx + 0.5*dt*k1Vx
    k2y = Vy + 0.5*dt*k1Vy
    k2Vx = A(x + 0.5*dt*k1x, y + 0.5*dt*k1y)[0]
    k2Vy = A(x + 0.5*dt*k1x, y + 0.5*dt*k1y)[1]

    k3x = Vx + 0.5*dt*k2Vx
    k3y = Vy + 0.5*dt*k2Vy
    k3Vx = A(x + 0.5*dt*k2x, y + 0.5*dt*k2y)[0]
    k3Vy = A(x + 0.5*dt*k2x, y + 0.5*dt*k2y)[1]

    k4x = Vx + dt*k3Vx
    k4y = Vy + dt*k3Vy
    k4Vx = A(x + dt*k3x, y + dt*k3y)[0]
    k4Vy = A(x + dt*k3x, y + dt*k3y)[1]

    x += dt/6*(k1x + 2*k2x + 2*k3x + k4x)
    y += dt/6*(k1y + 2*k2y + 2*k3y + k4y)
    Vx += dt/6*(k1Vx + 2*k2Vx + 2*k3Vx + k4Vx)
    Vy += dt/6*(k1Vy + 2*k2Vy + 2*k3Vy + k4Vy)

def update(i):
    global x, y, Vx, Vy, hold, time

    if not hold:
        RK4()

    trail_x.append(x)
    trail_y.append(y)

    if not hold:
        time += dt

    balls.set_data([x], [y])
    trail.set_data(trail_x, trail_y)
    balls_t.set_position((x, y))
    plt.title(f'time = {time:.1f}, speed = {(Vx**2 + Vy**2)**0.5:.2f}')

console = Console()
console.print("--------------------------")
console.print("Kepler's Orbit Simulation", style='bold red')
console.print("--------------------------")
console.print("Description", style='italic underline yellow')
console.print("You can press the middle mouse button to adjust the position and the velocity of the planet.", style='blue')

fig.canvas.mpl_connect('button_press_event', press)
fig.canvas.mpl_connect('motion_notify_event', motion)
fig.canvas.mpl_connect('button_release_event', release)
ani = Ani(fig, update, frames=int(60/dt), interval=1000*dt)
plt.show()
