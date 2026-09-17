#Rounding error
import math

pi = math.pi

for n in [2, 4, 5]:
    rounded = round(pi, n)
    error = abs(pi - rounded)

    print("Decimal places:", n)
    print("Rounded Pi:", rounded)
    print("Error:", error)
    print()