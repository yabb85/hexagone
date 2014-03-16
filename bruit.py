#!/usr/bin/python
# -*-coding:Utf-8 -*


import math
#import random
from pylab import plot, linspace, show
#import pgm


points = [(-5, 3), (3, 1), (1, 3), (3, 2), (2, 1), (1, 0.5), (0.5, -1)]


def rand_noise(t):
    """docstring for rand_noise"""
    t = int(t)
    t = (t << 13) ^ t
    t = (t * (t * t * 15731 + 789221) + 1376312589)
    return 1.0 - (t & 0x7fffffff) / 1073741824.0


#def noise(t):
    #"""docstring for noise"""
    #t = int(t)
    #random.seed(t)
    #return random.random()


def noise(t):
    return rand_noise(t)


def noise_2d(x, y):
    """docstring for noise_2d"""
    tmp = rand_noise(x) * 850000
    result = rand_noise(tmp + y)
    return result


def linear_interpolate(a, b, t):
    """docstring for interpolate"""
    return (1 - t) * a + t * b


def cosine_interpolate(a, b, t):
    """docstring for cosine_interpolate"""
    c = (1.0 - math.cos(t * math.pi)) * 0.5
    return (1.0 - c) * a + c * b


def cubic_interpolate(before_p0, p0, p1, after_p1, t):
    """docstring for cubic_interpolate"""
    a3 = -0.5 * before_p0 + 1.5 * p0 - 1.5 * p1 + 0.5 * after_p1
    a2 = before_p0 - 2.5 * p0 + 2 * p1 - 0.5 * after_p1
    a1 = -0.5 * before_p0 + 0.5 * p1
    a0 = p0

    return a3 * t * t * t + a2 * t * t + a1 * t + a0


def smooth_noise_linear(x):
    """docstring for smooth_nosie"""
    if x > 0:
        int_x = int(x)
    else:
        int_x = int(x) - 1
    float_x = x - int_x

    a = noise(int_x)
    b = noise(int_x + 1)

    return linear_interpolate(a, b, float_x)


def smooth_noise_cosine(x):
    """docstring for smooth_noise_cosine"""
    if x > 0:
        int_x = int(x)
    else:
        int_x = int(x) - 1
    float_x = x - int_x

    a = noise(int_x)
    b = noise(int_x + 1)

    return cosine_interpolate(a, b, float_x)


def smooth_noise_cubic(x):
    """docstring for smooth_noise_cubic"""
    if x > 0:
        int_x = int(x)
    else:
        int_x = int(x) - 1
    float_x = x - int_x

    a = noise(int_x - 1)
    b = noise(int_x)
    c = noise(int_x + 1)
    d = noise(int_x + 2)

    return cubic_interpolate(a, b, c, d, float_x)


def perlin(octaves, frequency, persistence, x):
    """docstring for perlin"""
    r = 0
    f = frequency
    amplitude = 1

    for i in range(0, octaves):
        r += smooth_noise_cosine(x * f) * amplitude
        amplitude *= persistence
        f *= 2
    geo_lim = (1 - persistence) / (1 - amplitude)
    return r * geo_lim


def trace(fonction, opt):
    """docstring for trace"""
    global points
    x = []
    y = []
    i = 0
    for p in points:
        x1 = linspace(0, 1, 30)
        for v in x1:
            x.append(v + i)
            y.append(fonction(p[0], p[1], v))
        i += 1
    #y = sin(x)
    #print x
    plot(x, y, opt)


def trace_cubic():
    """docstring for trace"""
    global points
    x = []
    y = []
    i = 0
    prev = (0, 0)
    d_prev = (0, 0)
    for p in points:
        if i > 1:
            x1 = linspace(0, 1, 30)
            for v in x1:
                x.append(v + i)
                y.append(cubic_interpolate(d_prev[1], prev[0],
                                           prev[1], p[0], v))
        d_prev = prev
        prev = p
        i += 1
    #y = sin(x)
    #print x
    x = [i - 1 for i in x]
    plot(x, y, 'g-')


def trace_smooth_noise(fonction, opt, factor):
    """docstring for trace_smooth_noise"""
    x = linspace(-100, 100, 1000)
    y = []
    for value in x:
        y.append(fonction(value * factor))
    plot(x, y, opt)


def trace_perlin():
    """docstring for trace_perlin"""
    x = linspace(-100, 100, 1000)
    y = []
    for value in x:
        y.append(perlin(8, 0.1, 0.9, value))
    plot(x, y)


def image():
    """docstring for image"""
    y = []
    for i in range(0, 2):
        x = []
        for j in range(0, 2):
            x.append(noise_2d(j, i))
        y.append(x)
    return y


def frange(x, y, jump):
    while x < y:
        yield x
        x += jump


def interpolate_img(liste):
    """docstring for interpolate_img"""
    height = len(liste)
    width = len(liste[0])
    buff = {}
    for y in range(0, height - 1):
        for x in range(0, width - 1):
            a = liste[x][y]
            b = liste[x + 1][y]
            c = liste[x][y + 1]
            d = liste[x + 1][y + 1]
            for i in frange(x, x + 1, 0.1):
                frac_x = i - x
                f = cosine_interpolate(a, b, frac_x)
                g = cosine_interpolate(c, d, frac_x)
                for j in frange(y, y + 1, 0.1):
                    frac_y = j - y
                    result = cosine_interpolate(f, g, frac_y)
                    buff[(int(i * 10), int(j * 10))] = result
    return buff


#form = image()
#liste = interpolate_img(form)
#img = pgm.convertDictToImage(liste, 20, 20)
#img.show()

#trace(linear_interpolate, 'b-')
#trace(cosine_interpolate, 'r-')
#trace_cubic()

#trace_smooth_noise(noise, 'c-', 1)
#trace_smooth_noise(smooth_noise_linear, 'b-', 1)
#trace_smooth_noise(smooth_noise_cosine, 'r-', 1)
#trace_smooth_noise(smooth_noise_cubic, 'g-', 1)
#trace_smooth_noise(smooth_noise_cubic, 'b-', 0.1)
#trace_smooth_noise(smooth_noise_cubic, 'r-', 0.05)
#trace_smooth_noise(smooth_noise_cubic, 'c-', 0.01)
trace_perlin()

show()
