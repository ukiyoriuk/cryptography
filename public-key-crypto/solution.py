#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import random

P_INFINITY = (None, None)

def uoc_isElliptic(curve):
    a, b, p = curve

    return (4 * pow(a, 3) + 27 * pow(b, 2)) % p != 0


def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    sqrt_n = math.isqrt(n) + 1
    for divisor in range(3, sqrt_n, 2):
        if n % divisor == 0:
            return False
    return True


def uoc_GetCurvePoints(curve):
    a, b, p = curve
    points = []

    for x in range(p):
        for y in range(p):
            if pow(y, 2) % p == (pow(x, 3, p) + a * x + b) % p:
                points.append((x, y))

    return points


# ----------------------------------------------------------------------------


def uoc_ComputePoints(curve):
    """
    Count the points on an elliptic curve
    :curve: a list with the curve values [a, b, p]
    :return: number of points on the curve
    """

    num_points = 0

    a, b, p = curve

    for x in range(p):
        for y in range(p):
            if pow(y, 2) % p == (pow(x, 3) + a * x + b) % p:
                num_points += 1

    num_points += 1

    return num_points


def uoc_VerifyNumPoints(curve, n):
    """
    Verify group order
    :curve: a list with the curve values [a, b, p]
    :n: number of points
    :return: True if it satisfies the equation or False
    """

    result = False

    if not uoc_isElliptic(curve):
        return result

    a, b, p = curve

    left_side = p + 1 - 2 * math.isqrt(p)
    right_side = p + 1 + 2 * math.isqrt(p)
    result = left_side <= n <= right_side

    return result


def uoc_AddPoints(curve, P, Q):
    """
    Add two points
    :curve: a list with the curve values [a, b, p]
    :P: a point as a pair (x, y)
    :Q: another point as a pair (x, y)
    :return: P+Q
    """

    suma = None

    a, b, p = curve

    x1, y1 = P
    x2, y2 = Q

    if P == P_INFINITY:
        return Q
    elif Q == P_INFINITY:
        return P
    elif x1 == x2 and (y1 == -y2 % p or y2 == -y1):
        return P_INFINITY
    elif P == Q and y1 != 0:
        st = ((3 * pow(x1, 2) + a) % p) * pow((2 * y1), -1, p)
        x3 = (pow(st, 2) - 2 * x1) % p
        y3 = (st * (x1 - x3) - y1) % p
        suma = (x3, y3)
    else:
        sc = ((y1 - y2) % p) * pow((x1 - x2), -1, p)
        x3 = (pow(sc, 2) - x1 - x2) % p
        y3 = (sc * (x1 - x3) - y1) % p
        suma = (x3, y3)

    # --------------------------------
    return suma


def uoc_SelfProductPoint(curve, n, P):
    """
    Multiplication of a scalar by a point
    :curve: a list with the curve values [a, b, p]
    :n: constant to multiply
    :P: a point as a pair (x, y)
    :return: nP
    """

    product = None

    if n == 0 or P == P_INFINITY:
        return P_INFINITY

    current_point = P

    product = P_INFINITY

    if isinstance(n, int):
        while n > 0:
            if n & 1:
                product = uoc_AddPoints(curve, product, current_point)

            current_point = uoc_AddPoints(curve, current_point, current_point)

            n >>= 1
    elif isinstance(n, tuple):
        for scalar in n:
            product = uoc_SelfProductPoint(curve, scalar, product)

    return product


def uoc_IsGroup(curve):
    """
    :curve: check if the curve is a group
    :n: constant to multiply
    :P: a point as a pair (x, y)
    :return: nP
    """

    return uoc_isElliptic(curve)


def uoc_OrderPoint(curve, P):
    """
    Point order
    :curve: a list with the curve values [a, b, p]
    :n: constant to multiply
    :P: a point as a pair (x, y)
    :return: nP
    """

    point_order = None

    point_order = 1
    Q = P

    while Q != P_INFINITY:
        Q = uoc_AddPoints(curve, Q, P)
        point_order += 1

    return point_order


def uoc_GenKey(curve, P):
    """
    Generate a pair of keys
    :curve: a list with the curve values [a, b, p]
    :P: a point as a pair (x, y)
    :return: a pair of keys (pub, priv)
    """

    key = (None, None)

    a, b, p = curve

    priv = random.randint(1, p)

    pub = uoc_SelfProductPoint(curve, priv, P)

    key = (pub, priv)
    return key


def uoc_SharedKey(curve, priv_user1, pub_user2):
    """
    Generate a shared secret
    :curve: a list with the curve values [a, b, p]
    :pub_user1: a public key
    :pub_user2: a private key
    :return: shared secret
    """

    shared = None
    shared = uoc_SelfProductPoint(curve, pub_user2, priv_user1)
    return shared
