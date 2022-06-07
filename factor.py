from trial_division import trial_division
from lenstra_ecm import lenstra_ecm
from gmpy2 import is_prime

def factor(n):
    factors, N = trial_division(n)
    while True:
        if N == 1:
            break
        elif is_prime(N):
            factors[int(N)] = 1
            break
        # This isn't ensured to be
        # prime... should fix this...
        factor = lenstra_ecm(N)
        if factor == 0:
            print(f"No factor found, increasing bounds")
            factor_digits = int(len(str(N)) / 10) * 5
            factor_digits = max(factor_digits, 25)
            factor = lenstra_ecm(N, factor_digits=factor_digits)
            if factor == 0:
                print(f"No factor found, giving up...")
                print(f"Remaining composite: {N=}")
                return factors
        while N % factor == 0:
            if factor in factors:
                factors[int(factor)] += 1
            else:
                factors[int(factor)] = 1
            N //= factor
    return factors

if __name__ == '__main__':
    from gmpy2 import next_prime
    from random import seed, randint
    from factor_util import test_factors
    seed(0)

    # Factor me!
    n = randint(0, 10**15)
    for _ in range(10):
        n *= next_prime(randint(0, 10**12))

    if 0:
        """
        Check the factoring
        """
        from time import time
        print(f"Factoring N = {n}")
        t = time()
        factors = factor(n)
        print(f"{time() - t} seconds...")
        assert test_factors(n, factors)
        print(list(factors.items()))
    else:
        """
        Bench the factoring
        """
        import cProfile
        gvars = {'n' : n}
        lvars = {'factor': factor}
        cProfile.runctx('factor(n)', globals=gvars, locals=lvars)
