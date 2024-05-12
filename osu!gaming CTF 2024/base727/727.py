from sympy import mod_inverse

n = 5912718291679762008847883587848216166109
e = 876603837240112836821145245971528442417

from sympy import factorint
factors = factorint(n)
p, q = factors.keys()

phi_n = (p-1) * (q-1)

d = mod_inverse(e, phi_n)

print(f"The private exponent (d) is: {d}")
