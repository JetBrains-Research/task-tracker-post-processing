# Helper Function Inlining does not work :( (used to collapse helper functions into the main function)
import math


def double(x):
    return 2 * x


def quadratic(a, b, c):
    (-b + math.sqrt(b * b - double(a) * double(c))) / double(a)

