import math
import gmpy2
from base64 import b32encode
from itertools import combinations_with_replacement


def run():
    e = bin2int("./e.txt")

    ct = bin2int("./c.txt")

    p = bin2int("./p.txt")
    assert(gmpy2.is_prime(p))
    q = bin2int("./q.txt")
    assert(gmpy2.is_prime(q))
    # p = 0xa6055ec186de51800ddd6fcbf0192384ff42d707a55f57af4fcfb0d1dc7bd97055e8275cd4b78ec63c5d592f567c66393a061324aa2e6a8d8fc2a910cbee1ed9
    # q = 0xfa0f9463ea0a93b929c099320d31c277e0b0dbc65b189ed76124f5a1218f5d91fd0102a4c8de11f28be5e4d0ae91ab319f4537e97ed74bc663e972a4a9119307
    # e = 0x6d1fdab4ce3217b3fc32c9ed480a31d067fd57d93a9ab52b472dc393ab7852fbcb11abbebfd6aaae8032db1316dc22d3f7c3d631e24df13ef23d3b381a1c3e04abcc745d402ee3a031ac2718fae63b240837b4f657f29ca4702da9af22a3a019d68904a969ddb01bcf941df70af042f4fae5cbeb9c2151b324f387e525094c41
    # ct = 0x7fe1a4f743675d1987d25d38111fae0f78bbea6852cba5beda47db76d119a3efe24cb04b9449f53becd43b0b46e269826a983f832abb53b7a7e24a43ad15378344ed5c20f51e268186d24c76050c1e73647523bd5f91d9b6ad3e86bbf9126588b1dee21e6997372e36c3e74284734748891829665086e0dc523ed23c386bb520

    # compute n
    n = p * q

    # Compute phi(n)
    phi = (p - 1) * (q - 1)

    # Compute modular inverse of e
    #d = getModInverse(e, phi)
    d = gmpy2.invert(e, phi)
    #d = pow(e, -1, phi)

    #print("d:  " + str(d))

    # Decrypt ciphertext
    pt = pow(ct, d, n)
    #assert(pow(pt, e, n) == ct)

    print(int(pt).to_bytes(512, 'big').decode('utf8'))


def bin2int(file):
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
