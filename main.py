import math
import random
import numpy as np
import timeit


def num_check(n) -> bool:
    if (((n % 2) >= 1) and ((n % 3) >= 1)):
        return True
    else:
        return False


def hasse_weil_bound(n: int) -> int:
    # Estimate the number of points on the elliptic curve
    right_bound = (n + 1) + math.floor(2 * (math.sqrt(n)))
    left_bound = (n + 1) - math.floor(2 * (math.sqrt(n)))
    return [left_bound, right_bound]
    # return "Give prime number"


def weierstrass_B(a, x, y, n) -> int:
    b = ((y * y) - (x * x * x) - (a * x))
    b = (b % n)
    return b


def EC_singulaity_check(A, B, n) -> bool:
    # check condition whether the curve is singular or not if singular then it is discarded
    singular = (4 * (A * A * A) + 27 * (B * B))
    calc_gcd = math.gcd(singular, n)
    if (calc_gcd != 0):
        print('curve is non-singular')
    if (calc_gcd >= 1 and calc_gcd <= n):
        return True
    elif (calc_gcd == n):
        print("Choose new B for the curve")
        return False


def point_on_EC(a, b, x, y, n) -> bool:
    # confirmation of
    weierstrass_eq = ((x * x * x) + (a * x) + b)
    Ec_result = (weierstrass_eq % n)
    if (y * y) == Ec_result:
        return True
    return False


def Ec_Point_generator(a, n, l_bound, r_bound) -> list:
    range = np.arange(2, r_bound)
    x_range = range
    y_range = range
    points_on_EC = []
    x = random.randint(l_bound, r_bound)
    y = random.randint(l_bound, r_bound)
    b = weierstrass_B(a, x, y, n)
    print("y=", y, "x=", x, "a=", a, "b=", b)
    if (EC_singulaity_check(a, b, n)):
        for x_1 in x_range:
            for y_1 in y_range:
                if point_on_EC(a, b, x_1, y_1, n):
                    points_on_EC.append([x_1, y_1])
    return points_on_EC


def k_generator() -> int:
    k = random.randint(45321, 893483274)
    k_lcm = math.lcm(2, k)
    return k_lcm


def lambda_calculate_for_Xpoints(P, Q) -> int:
    x_p, y_p = P
    x_q, y_q = Q
    lambdaa = ((y_p - y_q) / (x_p - x_q))
    return lambdaa


def lambda_calculate_for_Ypoints(a, P, Q) -> int:
    x_p, y_p = P
    x_q, y_q = Q
    lambdaa = (3 * (x_p * x_p + a) / (y_p + y_q))
    return lambdaa


def divisor_using_addition(a, n, points):
    P = points[0]
    Q = points[1]
    x_p, y_p = P
    x_q, y_q = Q
    if P is True and Q is not True:
        print("Q is point at infinity So P points are returned")
        return P
    elif P is not True and Q is True:
        print("P is point at infinity So Q point are returned")
        return Q
    elif P is not True and Q is not True:
        print("P and Q are not at infinity")
        d = math.gcd((x_p - x_q), n)
        if 1 < d < n:
            print("We find the divisor")
            return d
        elif d == 1:
            print("Euclidean Algorithm give Multiplicative inverse hence we found the third point")
            lambdaa = lambda_calculate_for_Xpoints(P, Q)
            x_R = ((lambdaa * lambdaa) - x_p - x_q)
            y_R = (lambdaa * (x_p - x_R) - y_p)
            R = (x_R, y_R)
            return R
        elif d == n:
            return 'X_p == X_q'
    else:
        d = math.gcd((y_p + y_q), n)
        if 1 < d < n:
            print("We find the divisor")
            return d
        elif d == n:
            print("Y_P == -Y_Q Then R= Point at infinity")
        elif d == 1:
            print("foundd")
            lambdaa = lambda_calculate_for_Ypoints(a, P, Q)
            x_R = ((lambdaa * lambdaa) - x_p - x_q)
            y_R = (lambdaa * (x_p - x_R) - y_p)
            R = (x_R, y_R)
            return R


def divisor_using_multiplication(k, n, points):
    k = bin(k)
    k = (k[2:])
    k = k[::-1]
    binary_points = []
    P = []
    for num, ones in enumerate(k):
        if int(ones) == 1:
            binary_points.append(num)
    # print("binary", binary_points)
    point = points[0]
    # print(point)
    x, y = point
    for binary in binary_points:
        X_p = ((2 ** binary) * x)
        Y_p = ((2 ** binary) * y)
        Kp = (X_p, Y_p)

    # divisor_using_addition(n, Kp)
    Factor_1 = math.gcd(Kp[0], n)
    Factor_2 = math.gcd(Kp[1], n)
    div_mult = [Factor_1, Factor_2]
    # print(div_mult)


# def lenstras_factorization(k, n, points) -> int:
#     factors_list=[]
#     for point in points:
#         X_p, Y_p = point
#         F_1 = math.gcd(k*X_p,n)
#         F_2 = math.gcd(k*Y_p,n)
#         factors_list.append([F_1,F_2])
#     return factors_list


if __name__ == '__main__':

    prime_num = 98231
    condition_check = num_check(prime_num)
    if (condition_check):
        A = random.randint(1000, 10000)
        # print(A)
        start = timeit.default_timer()
        bound = hasse_weil_bound(prime_num)
        l_bound, r_bound = bound
        points_list = Ec_Point_generator(A, prime_num, l_bound, r_bound)
        k = k_generator()
        if(divisor_using_multiplication(k, prime_num, points_list)):
            pass
        else:
            print("Cannot found any non-trivial divisor for the given prime integer")
        stop = timeit.default_timer()
        (print(l_bound, '<= E(F_P)<=', r_bound))
        print('time elapsed', stop - start)
    else:
        print("composite integer is fully divided by the 2 or 3")
