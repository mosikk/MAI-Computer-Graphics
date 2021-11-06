import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.widgets import Button

fig = plt.figure()
fig.subplots_adjust(bottom=0.3)
ax = fig.add_subplot(111, projection='3d')

vertices_num = 10  # amount of vertices in prism
v = []  # vertices of prism
for i in range(vertices_num):
    v.append([np.cos(2 * np.pi * i / vertices_num), np.sin(2 * np.pi * i / vertices_num), 0])
    v.append([np.cos(2 * np.pi * i / vertices_num), np.sin(2 * np.pi * i / vertices_num), 1])

v = np.array(v)
ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])  # adding vertices to plot

sides = [[v[i % (2 * vertices_num)],
          v[(i+1) % (2 * vertices_num)],
          v[(i+3) % (2 * vertices_num)],
          v[(i+2) % (2 * vertices_num)]] for i in range(0, 19, 2)]

sides.append([v[i] for i in range(0, 19, 2)])
sides.append([v[i] for i in range(1, 20, 2)])

ax.add_collection3d(Poly3DCollection(sides, alpha=0.5, edgecolors='black'))  # adding sides to plot


def button_callback_remove(event):
    ax.add_collection3d(Poly3DCollection(sides, alpha=1, edgecolors='black'))
    plt.draw()


button_ax_remove = fig.add_axes([0.5, 0.05, 0.31, 0.06])
button_remove = Button(button_ax_remove, "Remove invisible lines")
button_remove.on_clicked(button_callback_remove)


def button_callback_show(event):
    ax.add_collection3d(Poly3DCollection(sides, alpha=0.5, edgecolors='black'))
    plt.draw()


button_ax_show = fig.add_axes([0.5, 0.15, 0.31, 0.06])
button_show = Button(button_ax_show, "Show invisible lines")
button_show.on_clicked(button_callback_show)


def button_callback_isometric(event):
    ax.view_init(35, 45)
    plt.draw()


button_ax_isometric = fig.add_axes([0.1, 0.05, 0.31, 0.06])
button_isometric = Button(button_ax_isometric, "Isometric projection")
button_isometric.on_clicked(button_callback_isometric)


def button_callback_ortographic_top(event):
    ax.view_init(90)
    plt.draw()


button_ax_ortographic_top = fig.add_axes([0.1, 0.15, 0.31, 0.06])
button_ortographic_top = Button(button_ax_ortographic_top, "Top ortographic projection")
button_ortographic_top.on_clicked(button_callback_ortographic_top)

def button_callback_ortographic_front(event):
    ax.view_init(0)
    plt.draw()


button_ax_ortographic_front = fig.add_axes([0.1, 0.25, 0.31, 0.06])
button_ortographic_front = Button(button_ax_ortographic_front, "Front ortographic projection")
button_ortographic_front.on_clicked(button_callback_ortographic_front)

ax.grid(None)
ax.axis('off')
plt.show()
