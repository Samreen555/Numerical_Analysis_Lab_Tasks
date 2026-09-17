# Task 1: Basic Arithmetic
# Absolute Error, Relative Error and Percentage Error
# Numerical Methods - Lab 02

print("===== BASIC ARITHMETIC ERROR ANALYSIS =====")

# Input approximate values as strings
x1_input = input("Enter first value: ")
x2_input = input("Enter second value: ")

# Convert to floating-point
x1 = float(x1_input)
x2 = float(x2_input)


# Function to calculate possible error
# Formula: e = 1/2 × 10^(-n)
def calculate_error(value):
    if "." in value:
        # Number of digits after decimal point
        n = len(value.split(".")[1])
    else:
        # Integer has no decimal places
        n = 0

    e = 0.5 * (10 ** (-n))
    return e


# Calculate individual errors
e1 = calculate_error(x1_input)
e2 = calculate_error(x2_input)

# Select operation
operation = input("Enter operation (+, -, *, /): ")


# =========================
# ADDITION
# =========================
if operation == "+":
    result = x1 + x2

    # Absolute errors add
    AE = abs(e1) + abs(e2)

    # Relative error
    RE = AE / abs(result)


# =========================
# SUBTRACTION
# =========================
elif operation == "-":
    result = x1 - x2

    # Absolute errors add
    AE = abs(e1) + abs(e2)

    # Relative error
    RE = AE / abs(result)


# =========================
# MULTIPLICATION
# =========================
elif operation == "*":
    result = x1 * x2

    # Relative errors add
    RE = (abs(e1) / abs(x1)) + (abs(e2) / abs(x2))

    # Absolute error
    AE = RE * abs(result)


# =========================
# DIVISION
# =========================
elif operation == "/":
    if x2 == 0:
        print("Error: Division by zero is not allowed.")
        exit()

    result = x1 / x2

    # Relative errors add
    RE = (abs(e1) / abs(x1)) + (abs(e2) / abs(x2))

    # Absolute error
    AE = RE * abs(result)


# =========================
# INVALID OPERATION
# =========================
else:
    print("Invalid operation.")
    exit()


# Percentage Error
PE = RE * 100

# Error Bound / Range
lower = result - AE
upper = result + AE


# =========================
# OUTPUT
# =========================
print("\n===== RESULTS =====")

print("First value =", x1)
print("Second value =", x2)

print("\nIndividual Errors:")
print("e1 =", e1)
print("e2 =", e2)

print("\nOperation:", operation)
print("Calculated result =", result)

print("\nAbsolute Error (AE) =", AE)
print("Relative Error (RE) =", RE)
print("Percentage Error (PE) =", PE, "%")

print("\nError Bound:")
print("Lower limit =", lower)
print("Upper limit =", upper)

print("\nRange:")
print(lower, "<= true value <=", upper)