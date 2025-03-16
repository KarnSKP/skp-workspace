
class RK4:
    def RK4(t, dt, x, dxdt):
        k1 = dxdt(t, x)
        k2 = dxdt(t + dt/2, x + k1*dt/2)
        k3 = dxdt(t + dt/2, x + k2*dt/2)
        k4 = dxdt(t + dt, x + k3*dt)
        return dt/6*(k1 + 2*k2 + 2*k3 + k4)
    
class markersize:
    def radius(fig, ax, r):
        fig_width, fig_height = fig.get_size_inches()
        ax_width = fig_width * ax.get_position().width
        ax_height = fig_height * ax.get_position().height

        x_scale = ax_width/(ax.get_xlim()[1] - ax.get_xlim()[0])
        y_scale = ax_height/(ax.get_ylim()[1] - ax.get_ylim()[0])

        scale = (x_scale + y_scale)/2
        return 72*scale*2*r