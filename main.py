import math
import random
import numpy as np
import timeit


def num_check(n:int) -> bool:
    if (((n % 2) >= 1) and ((n % 3) >= 1)):
        return True
    else:
        return False


def hasse_weil_bound(n: int) -> [int,int]:
    # Estimate the number of points on the elliptic curve
    right_bound = (n + 1) + math.floor(2 * (math.sqrt(n)))
    left_bound = (n + 1) - math.floor(2 * (math.sqrt(n)))
    return [left_bound, right_bound]


def weierstrass_B(a:int, x:tuple, y:tuple, n:int) -> int:
    b = ((y * y) - (x * x * x) - (a * x))
    b = (b % n)
    return b


def EC_singulaity_check(A:int, B:int, n:int) -> bool:
    # check condition whether the curve is singular or not if singular then it is discarded
    singular = (4 * (A * A * A) + 27 * (B * B))
    calc_mod = (singular% n)
    if calc_mod != 0:
        print('curve is non-singular')
    if calc_mod >= 1 and calc_mod <= n:
        return True
    elif calc_mod == n:
        print("Choose new B for the curve")
        return False


def point_on_EC(a:int, b:int, x:tuple, y:tuple, n:int) -> bool:
    # confirmation of points on EC
    weierstrass_eq = ((x * x * x) + (a * x) + b)
    Ec_result = (weierstrass_eq % n)
    if (y * y) == Ec_result:
        return True
    return False


def Ec_Point_generator(a:int, n:int, l_bound:int, r_bound:int) -> list:
    range = np.arange(2, r_bound)
    x_range = range
    y_range = range
    points_on_EC = []
    x = random.randint(l_bound, r_bound)
    y = random.randint(l_bound, r_bound)
    b = weierstrass_B(a, x, y, n)
    print("y=", y, "x=", x, "a=", a, "b=", b)
    if EC_singulaity_check(a, b, n):
        for x_1 in x_range:
            for y_1 in y_range:
                if point_on_EC(a, b, x_1, y_1, n):
                    points_on_EC.append([x_1, y_1])
    return points_on_EC


def k_generator() -> int:
    k = random.randint(500, 10000)
    return k


def lambda_calculate_for_Xpoints(P:tuple, Q:tuple) -> int:
    x_p, y_p = P
    x_q, y_q = Q
    lambdaa = ((y_p - y_q) // (x_p - x_q))
    return lambdaa


def lambda_calculate_for_Ypoints(a:int, P:tuple, Q:tuple) -> int:
    x_p, y_p = P
    x_q, y_q = Q
    lambdaa = (3 * (x_p * x_p + a) // (y_p + y_q))
    return lambdaa


def divisor_using_addition(a:int, n:int, P:tuple, Q:tuple):
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
            print(d)
            return d
        elif d == 1:
            print("Euclidean Algorithm give Multiplicative inverse hence we found the third point")
            lambdaa = lambda_calculate_for_Xpoints(P, Q)
            x_R = (((lambdaa * lambdaa) - x_p - x_q)%n)
            y_R = ((lambdaa * (x_p - x_R) - y_p)%n)
            R = (x_R, y_R)
            print(R)
            return R
        elif d == n:
            print ('X_p == X_q')
        d = math.gcd((y_p + y_q), n)
        if(1 < d < n):
            print("We find the divisor")
            return d
        elif d == n:
            print("Y_P == -Y_Q Then R= Point at infinity")
        elif d == 1:
            print("Found third point on the Curve")
            lambdaa = lambda_calculate_for_Ypoints(a, P, Q)
            x_R = (((lambdaa * lambdaa) - x_p - x_q)%n)
            y_R = ((lambdaa * (x_p - x_R) - y_p)%n)
            R = (x_R, y_R)
            print(R)
            return R


def divisor_using_multiplication(a,k:int, n:int, point:list):
    k = bin(k)
    k = (k[2:])
    k = k[::-1]
    binary_points = []
    kp = point
    for num, ones in enumerate(k):
        if int(ones) == 1:
            binary_points.append(num)
    for binary in binary_points:
       if(binary == 0):
           pass
       else:
            R = divisor_using_addition(a, n, kp, kp)
            kp = R
# def lenstras_factorization(k, n, points) -> int:
#     factors_list=[]
#     for point in points:
#         X_p, Y_p = point
#         F_1 = math.gcd(k*X_p,n)
#         F_2 = math.gcd(k*Y_p,n)
#         factors_list.append([F_1,F_2])
#     return factors_list


if __name__ == '__main__':

    prime_num = 91
    condition_check = num_check(prime_num)
    if (condition_check):
        A = random.randint(10, 100)
        # print(A)
        start = timeit.default_timer()
        bound = hasse_weil_bound(prime_num)
        l_bound, r_bound = bound
        points_list = Ec_Point_generator(A, prime_num, l_bound, r_bound)
        point=points_list[0]
        k = k_generator()
        if(divisor_using_multiplication(A,k, prime_num, point)):
            pass
        else:
            print("Cannot found any non-trivial divisor for the given prime integer")
        stop = timeit.default_timer()
        (print(l_bound, '<= E(F_P)<=', r_bound))
        print('time elapsed', stop - start)
    else:
        print("composite integer is fully divided by the 2 or 3")
