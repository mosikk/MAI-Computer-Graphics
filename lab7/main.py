import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate
from matplotlib.widgets import Slider


n = 5
x = np.arange(n)
y = np.random.randint(low=0, high=10, size=n)


def interpolate(x, y):
    """
    Creates interpolated function
    """
    x_interpolated = np.linspace(0, n-1, 100)
    # Finds the B-spline representation of a 1-D curve
    spline_representation = scipy.interpolate.splrep(x, y, k=3)
    # Evaluates a B-spline or its derivatives
    y_interpolated = scipy.interpolate.splev(x_interpolated, spline_representation)
    return x_interpolated, y_interpolated


fig = plt.figure()
ax = fig.add_subplot(211)
initial, = plt.plot(x, y, '-o')

x_interpolated, y_interpolated = interpolate(x, y)
interpolated, = plt.plot(x_interpolated, y_interpolated)

plt.title("B-spline interpolation")
plt.ylim((-5, 15))

# Initialising sliders
sliders = []
for i in range(n):
    slider_ax = plt.axes([0.15, 0.3 - 0.05 * i, 0.75, 0.03])
    slider = Slider(slider_ax, r'$y_{0}$'.format(i), 0, 10, y[i])
    sliders.append(slider)


def update(val):
    """
    Updates the plot after changing a slider
    """
    for i in range(n):
        y[i] = sliders[i].val
    _, y_interpolated = interpolate(x, y)
    initial.set_ydata(y)
    interpolated.set_ydata(y_interpolated)


for i in range(n):
    sliders[i].on_changed(update)

plt.show()
