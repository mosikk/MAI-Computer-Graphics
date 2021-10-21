import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox


"""
function: r = a / phi; phi in [A; B]
a, A, B are entered by user
"""
eps = 1e-8
a = 1
A = 0.05
B = 40
phi = np.linspace(A+eps, B-eps, int(B-A) * 10)
r = a / (phi+eps)


def update_function(param_name, param_val):
    """
    Updates data after changing the parameters
    """
    global phi, r, a, A, B
    if param_name == 'a':
        a = param_val
    elif param_name == 'A':
        A = param_val
    elif param_name == 'B':
        B = param_val

    phi = np.linspace(A + eps, B - eps, max(0, int(B-A) * 10))
    r = a / (phi + eps)
    p.set_xdata(phi)
    p.set_ydata(r)


fig = plt.figure()
fig.subplots_adjust(bottom=0.2)
fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)

ax = fig.add_subplot(111, projection='polar')
p, = ax.plot(phi, r)
ax.set_title(r"$r = \frac{a}{\phi}; \phi \in [A; B]$")
ax.set_rmax(a+eps)
ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
ax.grid(True)


def submit_fn_a(value):
    """
    Updates the plot after changing the parameter a in textbox
    """
    update_function('a', float(value))
    ax.set_rmax(a+eps)
    plt.draw()


axbox_a = fig.add_axes([0.1, 0.05, 0.2, 0.06])
text_box_a = TextBox(axbox_a, "a ")
text_box_a.on_submit(submit_fn_a)
text_box_a.set_val(a)  # Trigger `submit` with the initial value


def submit_fn_A(value):
    """
    Updates the plot after changing the range of phi in textbox
    """
    update_function('A', float(value))
    plt.draw()


axbox_A = fig.add_axes([0.7, 0.15, 0.2, 0.06])
text_box_A = TextBox(axbox_A, "A ")
text_box_A.on_submit(submit_fn_A)
text_box_A.set_val(A)

def submit_fn_B(value):
    """
    Updates the plot after changing the range of phi in textbox
    """
    update_function('B', float(value))
    plt.draw()


axbox_B = fig.add_axes([0.7, 0.05, 0.2, 0.06])
text_box_B = TextBox(axbox_B, "B ")
text_box_B.on_submit(submit_fn_B)
text_box_B.set_val(B)

plt.show()
