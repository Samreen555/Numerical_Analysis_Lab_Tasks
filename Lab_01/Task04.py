# Task 4: Significant Digits
number = input("Enter a number: ")

if "." in number:
    digits = number.replace(".", "").lstrip("0")
    significant = len(digits)

else:
    digits = number.lstrip("0")
    significant = len(digits.rstrip("0"))

print("Number:", number)
print("Significant Digits:", significant)

if "." not in number and number.endswith("0"):
    value = float(number)
    print("Exponent Form:", f"{value:.{significant - 1}e}")