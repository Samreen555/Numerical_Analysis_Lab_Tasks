import math
import json
import matplotlib.pyplot as plt


# ============================================================
# FUNCTION EVALUATION
# ============================================================

def calculate_function(function, x):
    """Evaluate a user-supplied function at x safely."""

    function = function.replace("^", "**")

    allowed = {
        "x": x,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "log10": math.log10,
        "exp": math.exp,
        "pi": math.pi,
        "e": math.e,
        "abs": abs
    }

    return eval(function, {"__builtins__": {}}, allowed)


# ============================================================
# DIFFERENCE TABLE CONSTRUCTION
# ============================================================

def create_difference_table(values, max_order):
    """Build the difference table up to max_order."""

    table = [values.copy()]

    for order in range(1, max_order + 1):

        previous = table[-1]

        if len(previous) < 2:
            break

        next_column = []

        for i in range(len(previous) - 1):
            difference = previous[i + 1] - previous[i]
            next_column.append(difference)

        table.append(next_column)

    return table


# ============================================================
# BINOMIAL COEFFICIENTS
# ============================================================

def binomial_coefficients(order):
    """Return the binomial coefficients for a given order."""

    coefficients = [1]

    for i in range(1, order + 1):

        new_coefficients = [1]

        for j in range(1, len(coefficients)):
            new_coefficients.append(coefficients[j - 1] + coefficients[j])

        new_coefficients.append(1)

        coefficients = new_coefficients

    return coefficients


# ============================================================
# PRINT DIFFERENCE TABLE
# ============================================================

def print_difference_table(x_values, table, decimals):
    """Print the difference table neatly."""

    print("\n")
    print("=" * 90)
    print("                         DIFFERENCE TABLE")
    print("=" * 90)

    print(f"{'x':>12}", end="")
    print(f"{'f(x)':>15}", end="")

    for order in range(1, len(table)):
        print(f"{'Δ' + str(order):>15}", end="")

    print()
    print("-" * 90)

    for i in range(len(x_values)):

        print(f"{x_values[i]:>12.{decimals}f}", end="")

        for column in range(len(table)):

            if i < len(table[column]):
                print(f"{table[column][i]:>15.{decimals}f}", end="")
            else:
                print(f"{'':>15}", end="")

        print()

    print("=" * 90)


# ============================================================
# SAVE TASK 1 DATA
# ============================================================

def save_task1_data(function, x_values, values, table, decimals, max_order):
    """Save Task 1 data to a JSON file."""

    data = {
        "function": function,
        "x_values": x_values,
        "values": values,
        "table": table,
        "decimals": decimals,
        "max_order": max_order
    }

    with open("task1_data.json", "w") as file:
        json.dump(data, file)


# ============================================================
# TASK 1 IMAGE
# ============================================================

def create_task1_image(x_values, table, decimals):
    """Create the Task 1 difference table image (white values)."""

    headers = ["x", "f(x)"]

    for order in range(1, len(table)):
        headers.append("Δ" + str(order))

    rows = []

    for i in range(len(x_values)):

        row = [f"{x_values[i]:.{decimals}f}"]

        for column in range(len(table)):

            if i < len(table[column]):
                row.append(f"{table[column][i]:.{decimals}f}")
            else:
                row.append("")

        rows.append(row)

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis("off")

    table_plot = ax.table(
        cellText=rows,
        colLabels=headers,
        loc="center",
        cellLoc="center"
    )

    table_plot.auto_set_font_size(False)
    table_plot.set_fontsize(11)
    table_plot.scale(1, 1.8)

    plt.title("Task 1 - Difference Table", fontsize=16)

    plt.savefig("1_Task1_Values_Table.png", dpi=200, bbox_inches="tight")
    plt.close()


# ============================================================
# AFFECTED CELL MASK
# ============================================================

def find_affected_cells(wrong_table, correct_table):
    """Return a set of (column, row) cells affected by the error.

    These are the cells where the wrong table differs from the
    correct table. This mask is computed from the actual
    propagation of the error through the difference table.
    """

    affected = set()

    for column in range(len(wrong_table)):

        for row in range(len(wrong_table[column])):

            if row < len(correct_table[column]):

                if abs(wrong_table[column][row] - correct_table[column][row]) > 0.0000001:

                    affected.add((column, row))

    return affected


# ============================================================
# TASK 2 WRONG TABLE IMAGE WITH RED FAN
# ============================================================

def create_wrong_table_image(x_values, wrong_table, correct_table, wrong_row, decimals, affected_cells):
    """Create the wrong-value image with the red error fan.

    Only cells in the affected_cells mask are coloured red.
    The mask is computed from the actual difference propagation.
    """

    headers = ["x", "f(x)"]

    for order in range(1, len(wrong_table)):
        headers.append("Δ" + str(order))

    rows = []

    for i in range(len(x_values)):

        row = [f"{x_values[i]:.{decimals}f}"]

        for column in range(len(wrong_table)):

            if i < len(wrong_table[column]):
                row.append(f"{wrong_table[column][i]:.{decimals}f}")
            else:
                row.append("")

        rows.append(row)

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis("off")

    table_plot = ax.table(
        cellText=rows,
        colLabels=headers,
        loc="center",
        cellLoc="center"
    )

    table_plot.auto_set_font_size(False)
    table_plot.set_fontsize(11)
    table_plot.scale(1, 1.8)

    # --------------------------------------------------------
    # RED FAN: only the affected cells
    # --------------------------------------------------------

    for (column, row) in affected_cells:

        # +1 because row 0 is the header, +1 because column 0 is x
        table_plot[(row + 1, column + 1)].get_text().set_color("red")

    plt.title("Task 2 - Wrong Value and Error Fan (RED)", fontsize=16)

    plt.savefig("2_Task2_Wrong_Value_Fan.png", dpi=200, bbox_inches="tight")
    plt.close()


# ============================================================
# CORRECTED TABLE IMAGE
# ============================================================

def create_corrected_table_image(x_values, corrected_table, decimals, affected_cells):
    """Create the corrected difference table image.

    Only cells that were affected by the error (same mask used
    for the red fan) are coloured GREEN.

    All other numerical cells remain WHITE/NORMAL.
    The x-column remains WHITE/NORMAL.
    """

    headers = ["x", "f(x)"]

    for order in range(1, len(corrected_table)):
        headers.append("Δ" + str(order))

    rows = []

    for i in range(len(x_values)):

        row = [f"{x_values[i]:.{decimals}f}"]

        for column in range(len(corrected_table)):

            if i < len(corrected_table[column]):
                row.append(f"{corrected_table[column][i]:.{decimals}f}")
            else:
                row.append("")

        rows.append(row)

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis("off")

    table_plot = ax.table(
        cellText=rows,
        colLabels=headers,
        loc="center",
        cellLoc="center"
    )

    table_plot.auto_set_font_size(False)
    table_plot.set_fontsize(11)
    table_plot.scale(1, 1.8)

    # --------------------------------------------------------
    # GREEN cells: SAME POSITIONS as the red fan mask
    # --------------------------------------------------------

    for (column, row) in affected_cells:

        # Only colour if this cell still exists in the corrected table
        if row < len(corrected_table[column]):

            table_plot[(row + 1, column + 1)].get_text().set_color("green")

    plt.title("Task 2 - Corrected Difference Table (GREEN)", fontsize=16)

    plt.savefig("3_Task2_Corrected_Table.png", dpi=200, bbox_inches="tight")
    plt.close()


# ============================================================
# TASK 1
# ============================================================

print("\n")
print("=" * 60)
print("                         TASK 1")
print("=" * 60)

print("\nFunction Examples To Enter:")
print("x**2")
print("x**3")
print("x**4")
print("x**2 + 3*x + 5")
print("2*x**3 - 4*x + 7")
print("sqrt(x)")
print("sqrt(x**2 + x + 1)")
print("sin(x)")
print("cos(x)")
print("tan(x)")
print("log(x)")
print("exp(x)")

function = input(
    "\nEnter function: "
)

start = float(input("\nEnter starting value: "))
end = float(input("Enter ending value: "))
step = float(input("Enter step value: "))
decimals = int(input("Enter decimal places for rounding: "))

# ------------------------------------------------------------
# Difference order
# ------------------------------------------------------------

print("\nDifference order:")
print("Press Enter for default Δ4")
print("Enter 5 for Δ5, 6 for Δ6, etc.")

order_input = input("Enter highest difference order: ")

if order_input == "":
    max_order = 4
else:
    max_order = int(order_input)

# ------------------------------------------------------------
# Generate x values
# ------------------------------------------------------------

x_values = []

x = start

while x <= end + 0.0000001:
    x_values.append(x)
    x = x + step

# ------------------------------------------------------------
# Calculate f(x)
# ------------------------------------------------------------

values = []

for x in x_values:

    value = calculate_function(function, x)
    value = round(value, decimals)
    values.append(value)

# ------------------------------------------------------------
# Create difference table
# ------------------------------------------------------------

table = create_difference_table(values, max_order)

# ------------------------------------------------------------
# Print Task 1
# ------------------------------------------------------------

print_difference_table(x_values, table, decimals)

# ------------------------------------------------------------
# Save Task 1
# ------------------------------------------------------------

save_task1_data(function, x_values, values, table, decimals, max_order)

# ------------------------------------------------------------
# Create Task 1 image
# ------------------------------------------------------------

create_task1_image(x_values, table, decimals)

print("\nTask 1 image created: 1_Task1_Values_Table.png")


# ============================================================
# TASK 2
# ============================================================

print("\n")
print("=" * 60)
print("                         TASK 2")
print("=" * 60)

print("\nTask 2 continues from Task 1.")

# ------------------------------------------------------------
# Load Task 1 data
# ------------------------------------------------------------

with open("task1_data.json", "r") as file:
    data = json.load(file)

x_values = data["x_values"]
correct_values = data["values"]
correct_table = data["table"]
decimals = data["decimals"]
max_order = data["max_order"]

# ------------------------------------------------------------
# Display Task 1 values
# ------------------------------------------------------------

print("\nFunction values from Task 1:\n")

for i in range(len(x_values)):
    print("Row", i + 1, ": x =", x_values[i], ", f(x) =", correct_values[i])

# ------------------------------------------------------------
# User gives wrong value
# ------------------------------------------------------------

print("\nEnter the row containing the wrong value.")

wrong_row = int(input("Row number: "))
wrong_row = wrong_row - 1

wrong_value = float(input("Enter the WRONG function value: "))

# ------------------------------------------------------------
# Insert wrong value
# ------------------------------------------------------------

wrong_values = correct_values.copy()
wrong_values[wrong_row] = wrong_value

# ------------------------------------------------------------
# Create wrong difference table
# ------------------------------------------------------------

wrong_table = create_difference_table(wrong_values, max_order)

print("\nDifference Table With Error")
print_difference_table(x_values, wrong_table, decimals)

# ------------------------------------------------------------
# Compute the affected-cell mask ONCE from the actual propagation
# ------------------------------------------------------------

affected_cells = find_affected_cells(wrong_table, correct_table)

# ------------------------------------------------------------
# Create RED FAN image using the mask
# ------------------------------------------------------------

create_wrong_table_image(
    x_values,
    wrong_table,
    correct_table,
    wrong_row,
    decimals,
    affected_cells
)

print("\nWrong-value fan image created: 2_Task2_Wrong_Value_Fan.png")


# ============================================================
# ERROR DETECTION (LECTURE METHOD)
# ============================================================

print("\n")
print("=" * 60)
print("                    ERROR DETECTION")
print("=" * 60)

# ------------------------------------------------------------
# 1. Find the affected difference order (first irregular column)
# ------------------------------------------------------------

affected_order = None

for order in range(1, len(wrong_table)):

    for row in range(len(wrong_table[order])):

        difference = wrong_table[order][row] - correct_table[order][row]

        if abs(difference) > 0.0000001:
            affected_order = order
            break

    if affected_order is not None:
        break

if affected_order is None:
    print("\nNo error detected in the difference table.")
    exit()

print(f"\nFirst affected difference order: Δ{affected_order}")

# ------------------------------------------------------------
# 2. Error coefficients (binomial coefficients) for this order
# ------------------------------------------------------------

coefficients = binomial_coefficients(affected_order)

print(f"Error coefficients (binomial): {coefficients}")

largest_coefficient = max(coefficients)
print(f"Largest coefficient: {largest_coefficient}")

# ------------------------------------------------------------
# 3. Find the largest irregular value in the affected column
# ------------------------------------------------------------

largest_irregular = 0.0
largest_irregular_row = -1

for row in range(len(wrong_table[affected_order])):

    if row < len(correct_table[affected_order]):

        difference = wrong_table[affected_order][row] - correct_table[affected_order][row]

        if abs(difference) > abs(largest_irregular):
            largest_irregular = difference
            largest_irregular_row = row

print(f"Largest irregular value in Δ{affected_order}: {largest_irregular}")

# ------------------------------------------------------------
# 4. Error ε = largest irregular / largest coefficient
# ------------------------------------------------------------

error = largest_irregular / largest_coefficient

# Round to avoid floating-point noise
error = round(error, decimals)

print(f"\nError ε = {largest_irregular} / {largest_coefficient} = {error}")

# ------------------------------------------------------------
# 5. Correction = opposite sign
# ------------------------------------------------------------

correction = -error

corrected_value = round(wrong_value + correction, decimals)

print("\n")
print("=" * 60)
print("                       CORRECTION")
print("=" * 60)

print(f"Wrong value:        {wrong_value}")
print(f"Error ε:            {error}")
print(f"Correction:         {correction}")
print(f"Corrected value:    {corrected_value}")

# ------------------------------------------------------------
# Replace wrong value
# ------------------------------------------------------------

corrected_values = wrong_values.copy()
corrected_values[wrong_row] = corrected_value

# ------------------------------------------------------------
# Rebuild corrected table
# ------------------------------------------------------------

corrected_table = create_difference_table(corrected_values, max_order)

print("\nCorrected Difference Table")
print_difference_table(x_values, corrected_table, decimals)

# ------------------------------------------------------------
# Create GREEN corrected image using the SAME mask
# ------------------------------------------------------------

create_corrected_table_image(
    x_values,
    corrected_table,
    decimals,
    affected_cells
)

print("\nCorrected table image created: 3_Task2_Corrected_Table.png")


# ============================================================
# FINAL
# ============================================================

print("\n")
print("=" * 60)
print("                    FINAL OUTPUT")
print("=" * 60)

print("\nThree images have been created:")
print("\n1. 1_Task1_Values_Table.png      - Original difference table")
print("2. 2_Task2_Wrong_Value_Fan.png   - Wrong value + red error fan")
print("3. 3_Task2_Corrected_Table.png   - Corrected table (affected cells green)")

print("\nDone!")