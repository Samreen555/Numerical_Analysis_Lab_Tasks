# Task 3: Taylor Series Approximation of sin(x)
import math

x = 0.5

true_value = math.sin(x)

approx_3 = x - x**3/6 + x**5/120
approx_5 = x - x**3/6 + x**5/120 - x**7/5040 + x**9/362880

error_3 = abs(true_value - approx_3)
error_5 = abs(true_value - approx_5)

print("True Value:", true_value)
print("3-Term Approximation:", approx_3)
print("3-Term Error:", error_3)
print("5-Term Approximation:", approx_5)
print("5-Term Error:", error_5)