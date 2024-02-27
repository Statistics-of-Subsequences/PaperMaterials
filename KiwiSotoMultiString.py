import itertools
import time

import numpy as np
# IMPORTANT: This code only works for up to sigma = 10.

# Conceptually, for strings x1x2...xl and y1y2...yl, the ordering used is the lexicographical ordering of
# x1y1x2y2...xlyl
# Note: binary operations below rely on 32-bit constants. This also means that program can only currently calculate up
# to length 16 without overflow. Easy to change, but be careful of overflow
def FeasibleTriplet(length, sigma, d, iters):
    v = [np.zeros(sigma ** (d * length)) for _ in range(d)]
    (u, r, e) = (np.zeros(sigma ** (d * length)), 0, 0)

    for i in range(d, iters + 1):
        v.append(F(v[::-1], sigma, d, length))
        R = np.max(v[-1] - v[-2])
        W = v[-1] + d * R - F([v[-1] + (d - i - 1) * R for i in range(d)], sigma, d, length)
        E = max(0, np.max(W))

        if R - E >= r - e:
            (u, r, e) = (v[-1], R, E)
        print(f"Iteration {i - d + 1}: R = {R}, E = {E}, r = {r}, e = {e}, constant = {d * (r - e)}")
        del v[0]

    return u, r, e


# b is 1 where all v start with the same character and 0 otherwise
def F(v, sigma, d, length):
    b = np.zeros(sigma ** (d * length))
    # see README, same concept as used for F_b_step and F_b_equals_1
    for i in range(0, sigma ** d, int((1 - sigma ** d) / (1 - sigma))):
        b[i * sigma ** (d * (length - 1)):(i + 1) * sigma ** (d * (length - 1))] = 1

    # Obtain each Fz's result and take the elementwise maximum
    Fz = [F_z(z, v, sigma, d, length) for z in range(sigma)]
    return b + np.maximum.reduce(Fz)


def F_z(z, v, sigma, d, length):
    output = np.zeros(sigma ** (d * length))

    for i in range(sigma ** (d * length)):
        strings = intToStrings(i, sigma, d, length)
        # obtains the indices of only the strings not starting with z
        Nz = [i for i in range(d) if strings[i][0] != str(z)]

        # output is initialized to 0, so if Nz == 0 we don't need to do anything
        if len(Nz) != 0:
            output[i] = 1 / (sigma ** len(Nz)) * variate(Nz, strings, v[len(Nz) - 1], sigma, length)

    return output


# Exact same idea as the ordering discussed in the README
def intToStrings(value, sigma, d, length):
    baseValue = np.base_repr(value, sigma).zfill(d * length)
    outputs = ["" for _ in range(d)]
    for i in range(len(baseValue)):
        outputs[i % d] += baseValue[i]

    return [st.zfill(length) for st in outputs]


def stringsToInt(values, sigma, length):
    outputStr = "".join([st[i] for i in range(length) for st in values])
    return int(outputStr, sigma)


# Takes the cartesian product of the first sigma characters in the string "0123456789" Nz times,
# creating sigma^(Nz) permutations to append to the strings that should be variated
def variate(Nz, strings, v, sigma, length):
    output = 0

    for c in itertools.product("0123456789"[:sigma], repeat=len(Nz)):
        # Variate the strings that should be changed by removing the first character and adding the new character
        variation = strings.copy()
        for j in range(len(Nz)):
            variation[Nz[j]] = variation[Nz[j]][1:] + c[j]
        output += v[stringsToInt(variation, sigma, length)]

    return output


# Parameters are defined at the top of this function
def main():
    sigma = 2
    d = 2
    l = 4
    iters = 100

    # Parameters
    print(f"σ={sigma}, d={d}, l={l}, iterations={iters}")
    start = time.time_ns()
    (v, r, e) = FeasibleTriplet(l, sigma, d, iters)
    end = time.time_ns()
    # Result
    print(d * (r - e))
    # Runtime in seconds
    print(f"Runtime: {(end - start) / 1000000}")


# Python
if __name__ == '__main__':
    main()
