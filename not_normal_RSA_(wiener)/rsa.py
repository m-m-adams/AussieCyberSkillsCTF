import math


def DevContinuedFraction(num, denum):
    partialQuotients = []
    divisionRests = []
    for i in range(int(math.log(denum, 2)/1)):
        divisionRests = num % denum
        partialQuotients.append(num / denum)
        num = denum
        denum = divisionRests
        if denum == 0:
            break
    return partialQuotients


def DivergentsComputation(partialQuotients):
    (p1, p2, q1, q2) = (1, 0, 0, 1)
    convergentsList = []
    for q in partialQuotients:
        pn = q * p1 + p2
        qn = q * q1 + q2
        convergentsList.append([pn, qn])
        p2 = p1
        q2 = q1
        p1 = pn
        q1 = qn
    return convergentsList


def SquareAndMultiply(base, exponent, modulus):
    binaryExponent = []
    while exponent != 0:
        binaryExponent.append(exponent % 2)
        exponent = exponent/2
    result = 1
    binaryExponent.reverse()
    for i in binaryExponent:
        if i == 0:
            result = (result*result) % modulus
        else:
            result = (result*result*base) % modulus
    return result


def WienerAttack(e, N, C):
    testStr = 42
    C = SquareAndMultiply(testStr, e, N)
    for c in DivergentsComputation(DevContinuedFraction(e, N)):
        if SquareAndMultiply(C, c[1], N) == testStr:
            FullReverse(N, e, c)
            return c[1]
    return -1


def GetTheFlag(C, N, d):
    p = pow(C, d, N)

    size = len("{:02x}".format(p)) // 2
    print("Flag = "+"".join([chr((p >> j) & 0xff)
          for j in reversed(range(0, size << 3, 8))]))


def find_invpow(x, n):
    high = 1
    while high ** n < x:
        high *= 2
    low = high/2
    while low < high:
        mid = (low + high) // 2
        if low < mid and mid**n < x:
            low = mid
        elif high > mid and mid**n > x:
            high = mid
        else:
            return mid
    return mid + 1


def FullReverse(N, e, c):
    phi = (e*c[1]-1)//c[0]
    a = 1
    b = -(N-phi+1)
    c = N
    delta = b*b - 4*a*c
    if delta > 0:
        x1 = (-b + find_invpow((b*b - 4*a*c), 2))/(2*a)
        x2 = (-b - find_invpow((b*b - 4*a*c), 2))/(2*a)
        if x1*x2 == N:
            print("p = "+str(x1))
            print("q = "+str(x2))
        else:
            print("** Error **")
    else:
        print("** ERROR : (p, q)**")


if __name__ == "__main__":
    e = 488024372276774720122184925007196100459732691691159443100011921950668934358751498255363857443814989036690115342263792415002047701253100847644181806093276777904584217737136269807290263519892281711337913060025263201120077231575739183814193845319375392256712234675600841186178103094491622595354643255777936033735

    n = 615075006651875349377027316784714733731521116769606045024168304987838499894662264328389990618939179160044590205959078483861048656903017542465793786847246244372277486521469798910393312768448815073430514849386624896331527844555751457521146964566101556701694396697551334250008358127154291270810167578491213275391

    ciphertext = 73576216875763367573063464695559498603401179678049584309658023934330824470417264378034725361214823209020590979232549396079285635906982709810062826948013094559219260256030714526670481987658891568572854142097927163279207634691811109115999050633998662501601550022718551431063198809203018424215745695420162430116

    d = WienerAttack(e, n, ciphertext)
    if d != -1:
        print("d = "+str(d))
        GetTheFlag(ciphertext, n, d)
    else:
        print("** ERROR : Wiener's attack Impossible**")
