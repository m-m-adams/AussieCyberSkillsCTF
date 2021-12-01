import math
import gmpy


def bin2int(file):
    with open(file) as f:
        raw = f.read()

    a = raw.split()
    #string_read = ''.join(a[::-1])
    #out = int(string_read[::-1],2)
    s = ''.join([str(int(el, 2)) for el in a])
    out = int(s, 10)
    return out

# def bin2int(file):
#     #
#     with open(file) as f:
#         raw = f.read()

#     a = raw.split()
#     string_read = ''.join(a[::-1])
#     return int(string_read,2)

def getModInverse(a, m):
    assert math.gcd(a, m) == 1, "phi and e not coprime"

    r0, r1 = a, m
    s0, s1 = 1, 0
    t0, t1 = 0, 1


    while r1 != 0:
        q = r0 // r1
        r1, r0 = r0-q*r1, r1
        s1, s0 = s0-q*s1, s1
        t1, t0 = t0-q*t1, t1
    return s0 % m

def main():
    e= bin2int("./e.txt")
    ct= bin2int("./c.txt")
    p= bin2int("./p.txt")
    q= bin2int("./q.txt")
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
    #d = gmpy.invert(e,n)
    d = pow(e,-1,phi)

    print("d:  " + str(d))

    # Decrypt ciphertext
    pt = pow(ct, d, n)
    assert(pow(pt, e, n) == ct)
    print(pt.to_bytes(512, 'big'))

if __name__ == "__main__":
    main()
