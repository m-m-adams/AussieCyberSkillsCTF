from itertools import cycle

with open("./credit.pdf.rans", "rb") as f:
    data = f.read()


def bxor(ba1, ba2):
    """ XOR two byte strings """
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

print(bxor(data[0:4], b'%PDF'))

with open("./decryptedpdf", "wb") as f:
    f.write(bxor(data, cycle(b'fl4g_')))

#flag_{xOr_and_m4g1c_nUmb3rs}