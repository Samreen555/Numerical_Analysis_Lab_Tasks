import math
import json
from collections import Counter
import matplotlib.pyplot as plt


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
    """Return the binomial coefficients for a given order.

    These are the error coefficients from the lecture:
        order 1 -> [1, 1]
        order 2 -> [1, 2, 1]
        order 3 -> [1, 3, 3, 1]
        order 4 -> [1, 4, 6, 4, 1]
        order 5 -> [1, 5, 10, 10, 5, 1]
    """

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
    print(f"{'y':>15}", end="")

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

def save_task1_data(x_values, values, table, decimals, max_order):
    """Save Task 1 data to a JSON file."""

    data = {
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

    headers = ["x", "y"]

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

def find_affected_cells(wrong_table, corrected_table):
    """Return a set of (column, row) cells that differ between
    the wrong table and the corrected table.

    These are exactly the cells affected by the error fan.
    """

    affected = set()

    for column in range(len(wrong_table)):

        for row in range(len(wrong_table[column])):

            if row < len(corrected_table[column]):

                if abs(wrong_table[column][row] - corrected_table[column][row]) > 0.0000001:

                    affected.add((column, row))

    return affected


# ============================================================
# TASK 2 WRONG TABLE IMAGE WITH RED FAN
# ============================================================

def create_wrong_table_image(x_values, wrong_table, decimals, affected_cells):
    """Create the wrong-value image with the red error fan."""

    headers = ["x", "y"]

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

    # RED FAN: only the affected cells
    for (column, row) in affected_cells:

        table_plot[(row + 1, column + 1)].get_text().set_color("red")

    plt.title("Task 2 - Wrong Value and Error Fan (RED)", fontsize=16)

    plt.savefig("2_Task2_Wrong_Value_Fan.png", dpi=200, bbox_inches="tight")
    plt.close()


# ============================================================
# CORRECTED TABLE IMAGE
# ============================================================

def create_corrected_table_image(x_values, corrected_table, decimals, affected_cells):
    """Create the corrected difference table image.

    Only the cells that were affected by the error are coloured GREEN.
    All other numerical cells remain WHITE/NORMAL.
    The x-column remains WHITE/NORMAL.
    """

    headers = ["x", "y"]

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

    # GREEN cells: SAME POSITIONS as the red fan mask
    for (column, row) in affected_cells:

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

# ------------------------------------------------------------
# Range parameters (used to generate x-values)
# ------------------------------------------------------------

start = float(input("\nEnter starting x value: "))
end = float(input("Enter ending x value: "))
step = float(input("Enter step value: "))

# Ask for decimals FIRST so x-values can be rounded while being generated
decimals = int(input("\nEnter decimal places for rounding: "))

# Generate x-values with rounding to avoid floating-point noise
x_values = []
x = start
count = 0
while x <= end + 1e-9:
    x_values.append(round(start + count * step, decimals))
    count += 1
    x = start + count * step

n = len(x_values)

print(f"\nGenerated {n} x-values:")
for i in range(n):
    print(f"  x[{i+1}] = {x_values[i]}")

# ------------------------------------------------------------
# User enters y-values only
# ------------------------------------------------------------

print("\nEnter the y-value for each x:")

values = []
for i in range(n):
    y = float(input(f"  y[{i+1}] (x = {x_values[i]}): "))
    values.append(round(y, decimals))

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
# Create difference table
# ------------------------------------------------------------

table = create_difference_table(values, max_order)

print_difference_table(x_values, table, decimals)

save_task1_data(x_values, values, table, decimals, max_order)

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
values = data["values"]
table = data["table"]
decimals = data["decimals"]
max_order = data["max_order"]

# ------------------------------------------------------------
# Display Task 1 values
# ------------------------------------------------------------

print("\nData values from Task 1:\n")

for i in range(len(x_values)):
    print("Row", i + 1, ": x =", x_values[i], ", y =", values[i])

# ------------------------------------------------------------
# User gives ONLY the row containing the wrong value
# ------------------------------------------------------------

print("\nEnter the row containing the wrong value.")

wrong_row = int(input("Row number: ")) - 1

wrong_value = values[wrong_row]

print(f"\nWrong value at Row {wrong_row + 1}: {wrong_value}")


# ============================================================
# ERROR DETECTION (LECTURE METHOD)
# ============================================================

print("\n")
print("=" * 60)
print("                    ERROR DETECTION")
print("=" * 60)

# ------------------------------------------------------------
# STEP 1 — Find the affected difference column
# ------------------------------------------------------------
# The lecture says: for an exact polynomial of degree d, the
# d-th differences are constant and higher differences are zero.
# A wrong value breaks this. The affected column is the highest
# order whose values are *almost constant* (or *almost zero*),
# with a few outliers.
#
# Detection: for each order from highest down to lowest, check
# if the column's spread (max - min) is small relative to the
# column's average magnitude. The first column that qualifies
# is treated as the affected order.

def column_spread(column):
    """Return (max - min) of a column."""
    if len(column) == 0:
        return 0.0
    return max(column) - min(column)

def column_average_magnitude(column):
    """Return average of absolute values."""
    if len(column) == 0:
        return 0.0
    return sum(abs(v) for v in column) / len(column)

affected_order = None

# Walk from highest order down to lowest
for order in range(len(table) - 1, 0, -1):

    column = table[order]

    if len(column) < 2:
        continue

    spread = column_spread(column)
    avg_mag = column_average_magnitude(column)

    # Treat as "nearly constant" if the spread is small
    # compared to the average magnitude (or if all values are tiny)
    if avg_mag < 1e-9:
        # Column is all-zero → not affected; skip
        continue

    if spread / avg_mag < 0.5:
        affected_order = order
        break

# Fallback: if no nearly-constant column found, use the highest
# non-trivial column
if affected_order is None:
    for order in range(len(table) - 1, 0, -1):
        if len(table[order]) >= 2:
            affected_order = order
            break

if affected_order is None:
    print("\nNo error detected in the difference table.")
    exit()

print(f"\nAffected difference order: Δ{affected_order}")


# ------------------------------------------------------------
# STEP 2 — Binomial (error) coefficients for that order
# ------------------------------------------------------------

coefficients = binomial_coefficients(affected_order)

print(f"Error coefficients (binomial): {coefficients}")

largest_coefficient = max(coefficients)
print(f"Largest coefficient: {largest_coefficient}")


# ------------------------------------------------------------
# STEP 3 — Largest irregular value in the affected column
# ------------------------------------------------------------
# The dominant value (most frequent) is what the column "should"
# be if it were constant. The largest deviation from that
# dominant value is the largest irregular value.

column = table[affected_order]

counts = Counter(round(v, decimals) for v in column)
expected = counts.most_common(1)[0][0]

largest_irregular = 0.0

for v in column:

    deviation = v - expected

    if abs(deviation) > abs(largest_irregular):
        largest_irregular = deviation

largest_irregular = round(largest_irregular, decimals)

print(f"Dominant value in Δ{affected_order}: {expected}")
print(f"Largest irregular value in Δ{affected_order}: {largest_irregular}")


# ------------------------------------------------------------
# STEP 4 — Error ε = largest irregular / largest coefficient
# ------------------------------------------------------------

error = largest_irregular / largest_coefficient
error = round(error, decimals)

print(f"\nError ε = {largest_irregular} / {largest_coefficient} = {error}")


# ------------------------------------------------------------
# STEP 5 — Correction = opposite sign
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
# Replace the wrong value and rebuild the corrected table
# ------------------------------------------------------------

corrected_values = values.copy()
corrected_values[wrong_row] = corrected_value

corrected_table = create_difference_table(corrected_values, max_order)

print("\nCorrected Difference Table")
print_difference_table(x_values, corrected_table, decimals)


# ------------------------------------------------------------
# Affected cells = cells where wrong table differs from corrected
# ------------------------------------------------------------

affected_cells = find_affected_cells(table, corrected_table)


# ------------------------------------------------------------
# Create RED FAN image (wrong table)
# ------------------------------------------------------------

create_wrong_table_image(
    x_values,
    table,
    decimals,
    affected_cells
)

print("\nWrong-value fan image created: 2_Task2_Wrong_Value_Fan.png")


# ------------------------------------------------------------
# Create GREEN corrected image (same mask)
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
print("\n2. 2_Task2_Wrong_Value_Fan.png   - Wrong value + red error fan")
print("\n3. 3_Task2_Corrected_Table.png   - Corrected table (affected cells green)")

print("\nDone!")