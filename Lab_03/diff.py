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
# TASK 2 WRONG TABLE IMAGE WITH RED FAN AND SPAN LINES
# ============================================================

def create_wrong_table_image(x_values, wrong_table, correct_table, wrong_row, decimals):
    """Create the wrong-value image with the red error fan and diagonal span lines.

    The red fan is computed from the ACTUAL difference-table propagation.
    Diagonal span lines are drawn connecting the affected cells, matching the
    lecture's Example 1 diagram.
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
    # RED FAN: cells affected by the error propagation
    # --------------------------------------------------------

    affected_cells = []  # store (col, row) of affected cells

    for column in range(len(wrong_table)):

        for row in range(len(wrong_table[column])):

            if row < len(correct_table[column]):

                if abs(wrong_table[column][row] - correct_table[column][row]) > 0.0000001:

                    table_plot[(row + 1, column + 1)].get_text().set_color("red")

                    affected_cells.append((column, row))

    # --------------------------------------------------------
    # DIAGONAL SPAN LINES (lecture style)
    # --------------------------------------------------------
    # The error starts at the wrong f(x) cell and fans out diagonally:
    # column 0 (f(x)) -> column 1 (Δ1) -> column 2 (Δ2) -> ...
    #
    # For each difference column j, the affected rows form a block.
    # We draw a red diagonal line from the top-most affected cell
    # of column j to the bottom-most affected cell of column j+1.

    if affected_cells:

        # Group affected rows by column
        affected_by_column = {}

        for col, row in affected_cells:

            if col not in affected_by_column:
                affected_by_column[col] = []

            affected_by_column[col].append(row)

        # Sort columns
        sorted_columns = sorted(affected_by_column.keys())

        # Draw diagonal span lines between consecutive columns
        for idx in range(len(sorted_columns) - 1):

            col_a = sorted_columns[idx]
            col_b = sorted_columns[idx + 1]

            rows_a = sorted(affected_by_column[col_a])
            rows_b = sorted(affected_by_column[col_b])

            # For each adjacent pair, draw a red diagonal line
            # from the bottom of column a to the top of column b
            # (the fan spreads downward)
            for r_a in rows_a:

                for r_b in rows_b:

                    # Only connect cells that are adjacent in the fan
                    # (r_b is between r_a and r_a + something)
                    if abs(r_b - r_a) <= 1 or (col_b - col_a) == 1:

                        # Convert table cell coords to figure coords
                        # table_plot cells: row 0 is header, column 0 is x
                        cell_a = table_plot[(r_a + 1, col_a + 1)]
                        cell_b = table_plot[(r_b + 1, col_b + 1)]

                        # Get cell centers in axes coordinates
                        x_a, y_a = cell_a.get_xy()
                        w_a, h_a = cell_a.get_width(), cell_a.get_height()

                        x_b, y_b = cell_b.get_xy()
                        w_b, h_b = cell_b.get_width(), cell_b.get_height()

                        # Cell center for a: (x_a + w_a, y_a + h_a/2)
                        # Cell center for b: (x_b, y_b + h_b/2)
                        start = (x_a + w_a, y_a + h_a / 2)
                        end = (x_b, y_b + h_b / 2)

                        ax.plot(
                            [start[0], end[0]],
                            [start[1], end[1]],
                            color="red",
                            linewidth=1.5,
                            alpha=0.7,
                            zorder=1
                        )

    plt.title("Task 2 - Wrong Value and Error Fan (RED)", fontsize=16)

    plt.savefig("2_Task2_Wrong_Value_Fan.png", dpi=200, bbox_inches="tight")
    plt.close()


# ============================================================
# CORRECTED TABLE IMAGE
# ============================================================

def create_corrected_table_image(x_values, corrected_table, decimals):
    """Create the corrected difference table image.

    ALL numerical values (f(x) and all differences) are coloured GREEN.
    The x-column remains normal/white.
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

    # ALL NUMERICAL VALUES = GREEN (columns 1..len(corrected_table))
    for row in range(len(x_values)):

        for column in range(1, len(corrected_table) + 1):

            if row < len(corrected_table[column - 1]):

                table_plot[(row + 1, column)].get_text().set_color("green")

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

function = input("\nEnter function: ")

start = float(input("\nEnter starting value: "))
end = float(input("Enter ending value: "))
step = float(input("Enter step value: "))
decimals = int(input("Enter decimal places for rounding: "))

print("\nDifference order:")
print("Press Enter for default Δ4")
print("Enter 5 for Δ5, 6 for Δ6, etc.")

order_input = input("Enter highest difference order: ")

if order_input == "":
    max_order = 4
else:
    max_order = int(order_input)

# Generate x values
x_values = []
x = start
while x <= end + 0.0000001:
    x_values.append(x)
    x = x + step

# Calculate f(x)
values = []
for x in x_values:
    value = calculate_function(function, x)
    value = round(value, decimals)
    values.append(value)

# Create difference table
table = create_difference_table(values, max_order)

print_difference_table(x_values, table, decimals)

save_task1_data(function, x_values, values, table, decimals, max_order)

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

with open("task1_data.json", "r") as file:
    data = json.load(file)

x_values = data["x_values"]
correct_values = data["values"]
correct_table = data["table"]
decimals = data["decimals"]
max_order = data["max_order"]

print("\nFunction values from Task 1:\n")

for i in range(len(x_values)):
    print("Row", i + 1, ": x =", x_values[i], ", f(x) =", correct_values[i])

print("\nEnter the row containing the wrong value.")

wrong_row = int(input("Row number: "))
wrong_row = wrong_row - 1

wrong_value = float(input("Enter the WRONG function value: "))

wrong_values = correct_values.copy()
wrong_values[wrong_row] = wrong_value

wrong_table = create_difference_table(wrong_values, max_order)

print("\nDifference Table With Error")
print_difference_table(x_values, wrong_table, decimals)

create_wrong_table_image(x_values, wrong_table, correct_table, wrong_row, decimals)

print("\nWrong-value fan image created: 2_Task2_Wrong_Value_Fan.png")


# ============================================================
# ERROR DETECTION
# ============================================================

print("\n")
print("=" * 60)
print("                    ERROR DETECTION")
print("=" * 60)

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

coefficients = binomial_coefficients(affected_order)
print(f"Error coefficients (binomial): {coefficients}")

largest_coefficient = max(coefficients)
print(f"Largest coefficient: {largest_coefficient}")

largest_irregular = 0.0
for row in range(len(wrong_table[affected_order])):
    if row < len(correct_table[affected_order]):
        difference = wrong_table[affected_order][row] - correct_table[affected_order][row]
        if abs(difference) > abs(largest_irregular):
            largest_irregular = difference

print(f"Largest irregular value in Δ{affected_order}: {largest_irregular}")

error = largest_irregular / largest_coefficient
error = round(error, decimals)

print(f"\nError ε = {largest_irregular} / {largest_coefficient} = {error}")

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

corrected_values = wrong_values.copy()
corrected_values[wrong_row] = corrected_value

corrected_table = create_difference_table(corrected_values, max_order)

print("\nCorrected Difference Table")
print_difference_table(x_values, corrected_table, decimals)

create_corrected_table_image(x_values, corrected_table, decimals)

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
print("2. 2_Task2_Wrong_Value_Fan.png   - Wrong value + red fan + span lines")
print("3. 3_Task2_Corrected_Table.png   - Corrected table (all values green)")

print("\nDone!")