from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np
import sys
import threading
import time

# параметры освещения
light_pos = (20, 30, 30)  # положение источника света
light_intensity = 5  # интенсивность света
reflection = 115  # параметр отражения
# фоновое освещение - окружающее освещеие, которое всегда будет придавать объекту некоторый оттенок
ambient = [0.8, 0.0, 0.0, 0.5]
# диффузное освещение - имитирует воздействие на объект направленного источника света
diffuse = [1.0, 0.0, 0.0, light_intensity]
# зеркальный свет - устанавливает цвет блика на объекте
specular = [1.0, 0.0, 0.0, light_intensity]

# вращение
x_rot = 0
y_rot = 0
z_rot = 0

# параметры усеченного конуса
r_lower = 3  # радиус нижнего основания усеченного конуса
r_upper = 1  # радиус верхнего основания усеченного конуса
height = 4
approximation = 50  # количество боковых граней
size = 1


def init():
    glClearColor(255, 255, 255, 1.0)  # белый цвет для первоначальной закраски
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glEnable(GL_NORMALIZE)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient)  # определяем текущую модель освещения
    glEnable(GL_LIGHTING)  # включаем освещение
    glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)


def draw():
    global r_lower, r_upper, height, approximation
    v = []  # массив вершин
    for i in range(approximation):
        v.append([r_lower * np.cos(2 * np.pi * i / approximation),
                  r_lower * np.sin(2 * np.pi * i / approximation), 0])
        v.append([r_upper * np.cos(2 * np.pi * i / approximation),
                  r_upper * np.sin(2 * np.pi * i / approximation), height])

    # боковые стороны конуса
    sides = [[v[i % (2 * approximation)],
              v[(i + 1) % (2 * approximation)],
              v[(i + 3) % (2 * approximation)],
              v[(i + 2) % (2 * approximation)]] for i in range(0, approximation * 2 - 1, 2)]

    # верхнее и нижнее основания усеченного конуса
    top_side = [v[i] for i in range(1, approximation * 2, 2)]
    bottom_side = [v[i] for i in range(0, approximation * 2 - 1, 2)]

    # рисуем боковые стороны
    glBegin(GL_QUADS)
    for side in sides:
        n = np.cross(np.array(side[3]) - np.array(side[1]),
                     np.array(side[0]) - np.array(side[1]))  # вектор нормали
        glNormal3fv(n)
        for vert in side:
            glVertex3fv(vert)
    glEnd()

    # рисуем стороны-основания
    glBegin(GL_POLYGON)
    n = np.cross(np.array(top_side[2]) - np.array(top_side[1]),
                 np.array(top_side[0]) - np.array(top_side[1]))  # вектор нормали
    glNormal3fv(n)
    for vert in top_side:
        glVertex3fv(vert)
    glEnd()

    glBegin(GL_POLYGON)
    n = np.cross(np.array(bottom_side[2]) - np.array(bottom_side[1]),
                 np.array(bottom_side[0]) - np.array(bottom_side[1]))  # вектор нормали
    glNormal3fv(n)
    for vert in bottom_side:
        glVertex3fv(vert)
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(10, 10, 10, 0, 0, 0, 0, 0, 1)
    glTranslatef(size, size, size)
    init_lighting()
    glRotatef(x_rot, 1, 0, 0)
    glRotatef(y_rot, 0, 0, 1)
    glRotatef(z_rot, 0, 1, 0)

    glPushMatrix()  # сохраняем текущее положение "камеры"
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specular)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 128 - reflection)
    draw()
    glPopMatrix()  # возвращаем сохраненное положение "камеры"
    glutSwapBuffers()  # выводим все нарисованное в памяти на экран


def init_lighting():
    glEnable(GL_LIGHT0)  # включаем один источник света
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)  # определяем положение источника света

    l_dif = (2.0, 2.0, 3.0, light_intensity)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, l_dif)
    l_dir = (light_pos[0], light_pos[1], light_pos[2], 1.0)
    glLightfv(GL_LIGHT0, GL_POSITION, l_dir)

    # делаем затухание света
    attenuation = float(101 - light_intensity) / 25.0
    distance = np.sqrt(pow(light_pos[0], 2) + pow(light_pos[1], 2) + pow(light_pos[2], 2))
    constant_attenuation = attenuation / 3.0
    linear_attenuation = attenuation / (3.0 * distance)
    quadratic_attenuation = attenuation / (3.0 * distance * distance)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, constant_attenuation)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, linear_attenuation)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, quadratic_attenuation)


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(width) / float(height), 1.0, 60.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1, 0.0)


def specialkeys(key, x, y):
    global x_rot, y_rot, z_rot, size, approximation, light_intensity
    if key == b'w':
        x_rot += 5  # вращаем на 5 градусов по оси X
    if key == b's':
        x_rot -= 5  # вращаем на -5 градусов по оси X
    if key == b'a':
        y_rot += 5  # вращаем на 5 градусов по оси Y
    if key == b'd':
        y_rot -= 5  # вращаем на -5 градусов по оси Y
    if key == b'q':
        z_rot += 5  # вращаем на 5 градусов по оси Z
    if key == b'e':
        z_rot -= 5  # вращаем на -5 градусов по оси Z
    if key == b'=':
        size += 1  # увеличиваем размер на 1
    if key == b'-':
        size -= 1  # уменьшаем размер на 1
    if key == b'p':
        approximation += 1  # увеличиваем число ребер на 1
    if key == b'o':
        approximation -= 1  # уменьшаем число ребер на 1
        approximation = max(3, approximation)

    glutPostRedisplay()  # вызываем процедуру перерисовки


def change_light_intensity():
    global light_intensity
    while True:
        t = np.linspace(0, 2 * np.pi, 1000)
        for val in t:
            light_intensity = np.sin(val) * 80
            glutPostRedisplay()
            time.sleep(0.01)


def main():
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # используем двойную буферизацию и формат RGB
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(0, 0)
    glutInit(sys.argv)  # инициализируем opengl
    glutCreateWindow("cg lab 6")
    glutDisplayFunc(display)  # определяем функцию для отрисовки
    glutReshapeFunc(reshape)  # определяем функцию для масштабирования
    glutKeyboardFunc(specialkeys)  # определяем функцию для обработки нажатия клавиш
    init()

    t = threading.Thread(target=change_light_intensity)
    t.daemon = True
    t.start()

    glutMainLoop()


if __name__ == "__main__":
    print("Rotation:")
    print("OX: W S")
    print("OY: A D")
    print("OZ: Q E")
    print()
    print("Change figure size: - +")
    print("Change approximation: o p")
    main()
