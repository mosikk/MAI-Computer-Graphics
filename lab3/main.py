import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.widgets import Button, TextBox


def draw_figure(new_approximation):
    global ax, approximation, r_lower, r_upper, sides, alpha
    approximation = new_approximation

    ax.clear()
    v = []  # vertices of cone
    for i in range(approximation):
        v.append([r_lower * np.cos(2 * np.pi * i / approximation), r_lower * np.sin(2 * np.pi * i / approximation), 0])
        v.append([r_upper * np.cos(2 * np.pi * i / approximation), r_upper * np.sin(2 * np.pi * i / approximation), 1])

    v = np.array(v)
    ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])  # adding vertices to plot

    sides = [[v[i % (2 * approximation)],
              v[(i + 1) % (2 * approximation)],
              v[(i + 3) % (2 * approximation)],
              v[(i + 2) % (2 * approximation)]] for i in range(0, approximation * 2 - 1, 2)]

    sides.append([v[i] for i in range(0, approximation * 2 - 1, 2)])
    sides.append([v[i] for i in range(1, approximation * 2, 2)])

    # adding sides to plot
    collection = Poly3DCollection(sides, alpha=alpha, edgecolors='black', linewidth=0.1, facecolor='red')
    ax.add_collection3d(collection)

    ax.grid(None)
    ax.axis('off')
    plt.draw()


fig = plt.figure()
fig.subplots_adjust(bottom=0.2)
fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)
ax = fig.add_subplot(111, projection='3d')

r_upper = 1  # radius for upper side of truncated cone
r_lower = 3  # radius for lower side of truncated cone

approximation = 10  # amount of sides for approximation of a truncated cone
alpha = 0.5  # 0.5 -> show invisible lines; 1 -> delete invisible lines

draw_figure(approximation)


def button_callback_remove(event):
    global alpha
    alpha = 1
    ax.add_collection3d(Poly3DCollection(sides, alpha=alpha, edgecolors='black', linewidth=0.1, facecolors='red'))
    plt.draw()


button_ax_remove = fig.add_axes([0.5, 0.05, 0.31, 0.06])
button_remove = Button(button_ax_remove, "Remove invisible lines")
button_remove.on_clicked(button_callback_remove)


def button_callback_show(event):
    global alpha
    alpha = 0.5
    ax.add_collection3d(Poly3DCollection(sides, alpha=alpha, edgecolors='black', linewidth=0.1, facecolors='red'))
    plt.draw()


button_ax_show = fig.add_axes([0.5, 0.15, 0.31, 0.06])
button_show = Button(button_ax_show, "Show invisible lines")
button_show.on_clicked(button_callback_show)


def submit_fn(value):
    draw_figure(int(value))


axbox = fig.add_axes([0.2, 0.05, 0.2, 0.06])
text_box_B = TextBox(axbox, "Approximation: ")
text_box_B.on_submit(submit_fn)
text_box_B.set_val(approximation)


plt.show()
