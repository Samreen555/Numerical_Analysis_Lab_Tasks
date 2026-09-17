# Task 2: Error in the Area of a Circle
# Numerical Methods - Lab 02

import math

print("===== ERROR IN THE AREA OF A CIRCLE =====")

# Input radius and possible error
r = float(input("Enter radius r: "))
dr = float(input("Enter possible error Δr: "))

# Calculate approximate area
A = math.pi * r ** 2

# Calculate minimum and maximum radius
r_min = r - dr
r_max = r + dr

# Calculate minimum and maximum area
A_min = math.pi * r_min ** 2
A_max = math.pi * r_max ** 2

# Display results
print("\n===== RESULTS =====")

print("Radius r =", r)
print("Possible error Δr =", dr)

print("\nRadius range:")
print(r_min, "<= true radius <=", r_max)

print("\nApproximate Area:")
print("A =", A)

print("\nArea Range:")
print("A_min =", A_min)
print("A_max =", A_max)

print("\nTherefore:")
print(A_min, "<= true area <=", A_max)