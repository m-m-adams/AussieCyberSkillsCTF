import math
import gmpy2
from base64 import b32encode
from itertools import combinations_with_replacement

# key is noticing there are only a couple different 5 bit combos in the files.
# googling them brought up baudot encoding for telegrams...

# crypto wise we have p/q/e so just derive d as e modinverse  under phi(n)


def run():
    e = baudot2int("./e.txt")

    ct = baudot2int("./c.txt")

    p = baudot2int("./p.txt")
    assert(gmpy2.is_prime(p))
    q = baudot2int("./q.txt")
    assert(gmpy2.is_prime(q))
    # compute n
    n = p * q

    # Compute phi(n)
    phi = (p - 1) * (q - 1)

    d = gmpy2.invert(e, phi)

    # Decrypt ciphertext
    pt = pow(ct, d, n)
    assert(pow(pt, e, n) == ct)

    print(int(pt).to_bytes(512, 'big').decode('utf8'))


def baudot2int(file):
    with open(file) as f:
        raw = f.read().split()

    baudot = {
        '11011': '',
        '10111': 1,
        '10011': 2,
        '00001': 3,
        '01010': 4,
        '10000': 5,
        '10101': 6,
        '00111': 7,
        '00110': 8,
        '11000': 9,
        '10110': 0
    }
    out = ''
    for grouping in raw:
        out += str(baudot[grouping])
    out = int(out, 10)
    return out


if __name__ == "__main__":
    run()
