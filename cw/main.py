import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def find_bezier_curve(p0, p1, p2, steps):
    """
    Finds the coordinates of 3D quadratic Bézier curve
    p0, p1, p2 - points
    steps - number of steps
    returns an array of curve's coordinates
    """
    bezier = []
    for i in range(steps):
        t = i / steps

        # B(t) = (1-t)^2 * p0 + 2(1-t)t * p1 + t^2 * p2, 0 <= t <= 1
        coef0 = (1-t) ** 2
        coef1 = 2 * (1-t) * t
        coef2 = t ** 2
        bezier.append(coef0 * p0 + coef1 * p1 + coef2 * p2)

    return np.array(bezier)


# main points
# p0 = np.array([-1, 4, 8])
# p1 = np.array([-5, 1, -5])
# p2 = np.array([0, -1, -2])
print('Необходимо ввести координаты трех точек для построения направляющей - кривой Безье')
p0 = np.array([int(i) for i in input('Введите координаты первой точки: ').split()])
p1 = np.array([int(i) for i in input('Введите координаты второй точки: ').split()])
p2 = np.array([int(i) for i in input('Введите координаты третьей точки: ').split()])

bezier = find_bezier_curve(p0, p1, p2, 20)  # (bezier_steps, 3)

# counting astroid coordinates along the Bézier curve
astroid_approximation = 30
astroid_radius = 5
astroid = []
for bezier_point in bezier:
    cur_astroid_points = []
    for i in range(astroid_approximation):
        t = i / astroid_approximation
        cur_astroid_points.append([
            astroid_radius * np.cos(5 * t)**3 + bezier_point[0],
            2 * bezier_point[1],
            astroid_radius * np.sin(5 * t)**3 + bezier_point[2]
        ])

    astroid.append(np.array(cur_astroid_points))
astroid = np.array(astroid)  # (bezier_steps, astroid_approximation, 3)

sides = []  # sides of figure
for i in range(astroid.shape[0] - 1):
    for j in range(astroid.shape[1]):
        sides.append([
            astroid[i][j],
            astroid[(i + 1) % len(astroid)][j],
            astroid[(i + 1) % len(astroid)][(j + 1) % len(astroid[i])],
            astroid[i][(j + 1) % len(astroid[i])]
        ])

# plotting figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.axis('off')
plt.title('Кинематическая поверхность.\n Образующая - астроида, направляющая - кривая Безье 2 степени')

ax.set_xlim([-10, 10])
ax.set_ylim([-10, 10])
ax.set_zlim([-10, 10])

ax.add_collection3d(Poly3DCollection(sides, edgecolors='black', facecolor='lightgreen', linewidths=0.5))
plt.show()
