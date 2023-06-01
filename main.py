import math
import random
import numpy as np


def hasse_weil_bound(n: int) -> int:
    # Estimate the number of points on the elliptic curve
    left_bound = n + 1 + math.floor(math.sqrt(n))
    right_bound = n + 1 - math.floor(math.sqrt(n))
    return left_bound, right_bound


def EC_singulaity_check(A: int, B: int, n: int) -> bool:
    # check condition whether the curve is singular or not if singular then it is discarded
    if (math.gcd((4(A * A * A) + 27(B * B)), n)) != 0:
        return True
    else:
        False


def point_on_EC(a, b, x, y, n) -> bool:
    # confirmation of
    weierstrass_eq = ((x * x * x) + (a * x) + b)
    Ec_result = math.gcd(weierstrass_eq, n)
    if (y * y) == Ec_result:
        return True
    return False


def Ec_Point_generator(a, b, n, l_bound, r_bound) -> list:
    range = np.arange(2, r_bound)
    x_range = range
    y_range = range
    valid_points_on_EC = []
    for i in x_range:
        for j in y_range:
            if point_on_EC(a, b, i, j, n):
                valid_points_on_EC.append([i, j])
    return valid_points_on_EC


def k_generator() -> int:
    k = random.randint(45321, 893483274)
    k_lcm = math.lcm(2, k)
    return k_lcm


def lenstras_factorization(k, prime_num, point) -> int:
    k*point
    return 0


if __name__ == '__main__':
    print(np.arange(2, 9))
    print(math.lcm(5, 2912312083))
