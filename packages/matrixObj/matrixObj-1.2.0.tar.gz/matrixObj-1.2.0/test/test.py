
from fractions import Fraction

from Matrix import Matrix, AugMatrix

a = Matrix([4, 8, 2], [0, 5, 2], [4, 8, 1])
#a = RREF.Matrix([0,1],[0,0],[5,9])
#a = RREF.Matrix([1, 1, 5], [0, 1, 2], [0, 0, 0])
#a = Matrix([1, 0, 1, -3], [0, 1, 0, -4], [1, 0, 1, 4], [0, 1, 2, 1])
#a = RREF.Matrix([0, 1, 3], [2, 1, -4], (2, 3, 2))

"""a = RREF.Matrix([1, 3, 1, 0], [2, -1, -1, 1], [1, -4, -2, 2])
#a = RREF.Matrix([1, 0, 5, 0], [0, 1, 2, 1], [0, 0, 0, 3])
print(a)
b = a.rref(infraction=True)
print(b)
print(a == b)

print(a[-1:,-1])
k = RREF.AugMatrix(a[:,:-1], a[:,-3:])
k = RREF.AugMatrix(a)
print(k)
print(k.rref(True).rref())

matA = RREF.Matrix([2, 5, -4], [4, 5, 9], [-1, -8, 0], [7, 0, 5])
print(matA)
print(matA[:, 1:])"""


# 4x + 2y + 3z = 4
# 2x - 4y - 7z = -6
# -9x + 6y + 8z = 2

# equation = Matrix([4, 2, 3], [2, -4, -7], [-9, 6, 8])
# b = (4, -6, 2)

# print(AugMatrix(equation, b).rref(infraction=True))

"""b = Matrix([4], [-6], [2])
print(equation)
print(b)

print(equation.inverse(infraction=True) * b)
# x = A' * b"""

"""print(AugMatrix(equation, b).rref(infraction=True))

print(AugMatrix(equation, b).full_matrix)

# Examples of Normal Matrix
a = Matrix([1, 1, 0], [0, 1, 1], [1, 0, 1])
print(a.transpose() * a)
print(a.isnormal())

b = Matrix([1j, 0], [0, 3 - 5j])
print(b.isnormal())

# Examples of orthogonal matrix
c = Matrix([-1, 0], [0, 1])
print(c)
print(c.inverse())
print(c.transpose())
print(c.isorthogonal())"""


#k = AugMatrix(a, a.identity())
#print(k)
"""print(a)
b = Matrix([6, 7, 0], [6, 8, 9], [0, 7, 9])
print(2 / a)"""






"""eq = AugMatrix(([1, 3, 1, 0], [2, -1, -1, 1], [1, -4, -2, 2]))
print(eq.rref(infraction=True))
print(eq.rank())
print(eq.matrix.rank())
print(eq.augcolumn.rank())"""


# Important a = Matrix([2,0,8], [4,0,10], [1, 0, 9], [3, 0, 3,])


a = Matrix([1, 0, 1, -3], [0, 1, 0, -4], [1, 0, 1, 4], [0, 1, 2, 1])
augA = AugMatrix(a)
augA = AugMatrix(([1, 3, 1, 0], [2, -1, -1, 1], [1, -4, -2, 2]))
# print(augA.rref(True))
# print(augA.rank(2))

from Matrix import augment_matrix

mat = [
    [2, 1, -1, 1],
    [0, 2, 1, 2],
    [5, 2, -3, 3]
    ]

"""mat = [
    [1, 2, 1, 2],
    [3, 1, -2, 1],
    [4, -3, -1, 3]
    ]"""

# Algebraically

A = Matrix([1, 2, 1], [3, 1, -2], [4, -1, -1])
C = Matrix([2], [1], [3])

B = (A ** -1) * C
print(B)

print(f"\n B = {[int(i) for i in B.getcolumn(1)]}")

# By Cramer's Rule
print("\nUsing Cramer's Rule")
det = A.determinant()           # Determinant of Matrix A

# Value of a
Acopy = A.copy()                # Making a copy of Matrix A
Acopy[:, 0] = C                 # Modifying Matrix, seting column 1 of A to C
a = Acopy.determinant() / det
print(f"a = {a}")

# Value of b
Acopy = A.copy()                # Making a copy of Matrix A
Acopy[:, 1] = C                 # Modifying Matrix, seting column 1 of A to C
b = Acopy.determinant() / det
print(f"b = {b}")

# Value of c
Acopy = A.copy()                # Making a copy of Matrix A
Acopy[:, 2] = C                 # Modifying Matrix, seting column 1 of A to C
c = Acopy.determinant() / det
print(f"c = {c}")



