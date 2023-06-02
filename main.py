import math
import random
import numpy as np
import sympy as sm
from gmpy2 import f_mod
import timeit


def hasse_weil_bound(n: int) -> int:
    # Estimate the number of points on the elliptic curve
    right_bound = n + 1 + math.floor(2*(math.sqrt(n)))
    left_bound = n + 1 - math.floor(2*(math.sqrt(n)))
    return [left_bound, right_bound]
    # return "Give prime number"


def weierstrass_B(a,x,y,n) -> int:
    b = ((y*y)-(x*x*x)-(a*x))
    b = (b % n)
    return b

def EC_singulaity_check(A, B, n) -> bool:
    # check condition whether the curve is singular or not if singular then it is discarded
    singular = (4*(A * A * A) + 27*(B * B))
    calc_gcd = math.gcd(singular, n)
    if(calc_gcd != 0):
          return True
    else:
      return False


def point_on_EC(a, b, x, y, n) -> bool:
    # confirmation of
    weierstrass_eq = ((x * x * x) + (a * x) + b)
    Ec_result = math.gcd(weierstrass_eq, n)
    if (y * y) == Ec_result:
        return True
    return False


def Ec_Point_generator(a, n, r_bound) -> list:
    range = np.arange(1, r_bound)
    x_range = range
    y_range = range
    points_on_EC = []
    for i in x_range:
        for j in y_range:
            b = weierstrass_B(a, i, j, n)
            if point_on_EC(a, b, i, j, n):
                if (EC_singulaity_check(a, b, n)):
                    points_on_EC.append([i, j])
                continue
    return points_on_EC


def k_generator() -> int:
    k = random.randint(45321, 893483274)
    k_lcm = math.lcm(2, k)
    return k_lcm


def lenstras_factorization(k, n, points) -> int:
    factors_list=[]
    for point in points:
        X_p, Y_p = point
        F_1 = math.gcd(k*X_p,n)
        F_2 = math.gcd(k*Y_p,n)
        factors_list.append([F_1,F_2])
    return factors_list


if __name__ == '__main__':

    composite_integer =9000
    A =random.randint(100,composite_integer)
    print(A)
    start = timeit.default_timer()
    bound = hasse_weil_bound(composite_integer)
    l_bound, r_bound = bound
    points_list = Ec_Point_generator(A,composite_integer,r_bound)
    k = k_generator()
    factors= lenstras_factorization(k, composite_integer, points_list)
    stop = timeit.default_timer()
    (print(l_bound, '<= E(F_P)<=', r_bound))
    print((points_list))
    print(factors)
    print('time elapsed', stop-start)

