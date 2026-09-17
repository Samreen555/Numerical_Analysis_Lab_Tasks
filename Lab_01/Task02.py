#Accumulated error
Sum_value = 0.0
for i in range(100):
    Sum_value += 0.1
print("Sum =", Sum_value)
print("Expected =", 10.0)   
print("Error =", 10.0 - Sum_value )

sum_value = 0.0

for i in range(50):
    sum_value += 0.2

print("Sum =", sum_value)
print("Expected =", 10.0)
print("Error =", 10.0 - sum_value)