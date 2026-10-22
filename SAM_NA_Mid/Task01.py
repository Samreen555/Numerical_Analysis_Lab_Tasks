
import math
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

OUTPUT_DIR = Path(__file__).resolve().parent

# Highlight colors
ORIGIN_COLOR = "#FFE699"   # Yellow: origin
USED_COLOR = "#B7E1CD"     # Green: values used in formula
NORMAL_COLOR = "#FFFFFF"


# =====================================================
# INPUT DATA
# =====================================================

print("=" * 65)
print(" NUMERICAL INTERPOLATION PROGRAM")
print(" Newton Forward and Stirling Central Difference")
print("=" * 65)

try:
    n = int(input("Enter number of data points (minimum 2): "))
    if n < 2:
        raise SystemExit("Error: At least 2 data points are required.")

    x = []
    y = []

    print("\nEnter equally spaced x and y values:")
    for i in range(n):
        x.append(float(input(f"x[{i}] = ")))
        y.append(float(input(f"y[{i}] = ")))

except ValueError:
    raise SystemExit("Error: Enter valid numerical values.")


h = x[1] - x[0]

if h <= 0:
    raise SystemExit("Error: x values must be strictly increasing.")

for i in range(1, n):
    if not math.isclose(
        x[i] - x[i - 1], h, rel_tol=1e-9, abs_tol=1e-9
    ):
        raise SystemExit("Error: x values must be equally spaced.")


# =====================================================
# BUILD FORWARD DIFFERENCE TABLE
# table[order][row]
# =====================================================

table = [y.copy()]

for order in range(1, n):
    previous = table[order - 1]
    differences = [
        previous[i + 1] - previous[i]
        for i in range(len(previous) - 1)
    ]
    table.append(differences)


# =====================================================
# PRINT DIFFERENCE TABLE
# =====================================================

def print_difference_table():
    headers = ["x", "y"] + [
        f"Delta^{k}y" for k in range(1, n)
    ]

    print("\nFORWARD DIFFERENCE TABLE")
    print("-" * (15 * len(headers)))
    print(" | ".join(f"{item:>12}" for item in headers))
    print("-" * (15 * len(headers)))

    for i in range(n):
        row = [f"{x[i]:.4f}", f"{y[i]:.4f}"]

        for order in range(1, n):
            if i < len(table[order]):
                row.append(f"{table[order][i]:.4f}")
            else:
                row.append("")

        print(" | ".join(f"{item:>12}" for item in row))


# =====================================================
# SAVE A HIGHLIGHTED DIFFERENCE TABLE IMAGE
# =====================================================

def save_difference_image(method, origin, used_cells, filename):
    """
    used_cells contains (row_index, column_index) pairs.
    Image column 0 = x, column 1 = y,
    image column k+1 = Delta^k y.
    """

    headers = ["x", "y"] + [
        f"Delta^{k} y" for k in range(1, n)
    ]

    rows = []

    for i in range(n):
        row = [f"{x[i]:.4f}", f"{y[i]:.4f}"]

        for order in range(1, n):
            if i < len(table[order]):
                row.append(f"{table[order][i]:.4f}")
            else:
                row.append("")

        rows.append(row)

    fig, ax = plt.subplots(
        figsize=(max(11, n * 1.55), max(3.5, n * 0.65))
    )
    ax.axis("off")

    ax.set_title(
        f"{method}\nYellow = Origin | Green = Values Used",
        fontsize=14,
        fontweight="bold",
        pad=20
    )

    tbl = ax.table(
        cellText=rows,
        colLabels=headers,
        loc="center",
        cellLoc="center"
    )

    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1, 1.6)

    # Style header
    for col in range(len(headers)):
        tbl[(0, col)].set_facecolor("#D9EAF7")
        tbl[(0, col)].set_text_props(weight="bold")

    # Highlight the origin row's x and y cells
    for col in (0, 1):
        if 0 <= origin < n:
            tbl[(origin + 1, col)].set_facecolor(ORIGIN_COLOR)

    # Highlight all difference cells used by the formula
    for row_index, col_index in used_cells:
        if (
            0 <= row_index < n
            and 0 <= col_index < len(headers)
        ):
            tbl[(row_index + 1, col_index)].set_facecolor(
                USED_COLOR
            )

    # Keep the origin x and y cells yellow
    for col in (0, 1):
        if 0 <= origin < n:
            tbl[(origin + 1, col)].set_facecolor(ORIGIN_COLOR)

    fig.tight_layout()

    image_path = OUTPUT_DIR / filename
    fig.savefig(image_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved table image: {image_path}")


# =====================================================
# NEWTON FORWARD INTERPOLATION
# =====================================================

def newton_forward(target):
    p = (target - x[0]) / h
    result = y[0]

    print("\n" + "=" * 65)
    print("NEWTON FORWARD: STEP-BY-STEP CALCULATION")
    print("=" * 65)

    print("Formula:")
    print("y = y0 + p*Delta y0")
    print("  + p(p-1)/2! * Delta^2 y0 + ...")
    print(f"\nh = {h:.6f}")
    print(f"p = ({target:.6f} - {x[0]:.6f})/{h:.6f}")
    print(f"p = {p:.6f}")
    print(f"\nInitial value: y0 = {y[0]:.6f}")

    # Mark the exact difference cells used by Newton Forward
    used_cells = set()

    for order in range(1, n):
        product = 1.0
        for j in range(order):
            product *= p - j

        difference = table[order][0]
        term = product * difference / math.factorial(order)
        result += term

        # Difference column order k is image column k+1
        used_cells.add((0, order + 1))

        print(f"\nTerm of order {order}:")
        print(f"  Used difference: Delta^{order} y0")
        print(f"  Difference value = {difference:.6f}")
        print(f"  Polynomial factor = {product:.6f}")
        print(f"  Factorial = {math.factorial(order)}")
        print(f"  Term value = {term:.6f}")
        print(f"  Running sum = {result:.6f}")

    save_difference_image(
        "NEWTON FORWARD DIFFERENCE TABLE",
        0,
        used_cells,
        "Newton_Forward_Difference_Table.png"
    )

    print(f"\nFinal interpolated value = {result:.3f}")
    return result


# =====================================================
# STIRLING CENTRAL INTERPOLATION
# =====================================================

def stirling_central(target):
    if n % 2 == 0:
        print(
            "\nStirling's method requires an odd number "
            "of equally spaced data points."
        )
        return None

    origin = n // 2
    p = (target - x[origin]) / h
    result = y[origin]
    used_cells = set()

    print("\n" + "=" * 65)
    print("STIRLING CENTRAL: STEP-BY-STEP CALCULATION")
    print("=" * 65)

    print("Formula:")
    print("y = y0")
    print("  + p/2 * (Delta y0 + Delta y-1)")
    print("  + p^2/2! * Delta^2 y-1")
    print("  + p(p^2-1)/3! * average third differences")
    print("  + higher-order terms as available")

    print(f"\nCentral point: x0 = {x[origin]:.6f}")
    print(f"Central value: y0 = {y[origin]:.6f}")
    print(f"h = {h:.6f}")
    print(f"p = ({target:.6f} - {x[origin]:.6f})/{h:.6f}")
    print(f"p = {p:.6f}")

    for order in range(1, n):
        if order % 2 == 1:
            # Odd order: average two central differences
            left_index = origin - (order + 1) // 2
            right_index = origin - (order - 1) // 2

            if (
                left_index < 0
                or right_index >= len(table[order])
            ):
                break

            difference_left = table[order][left_index]
            difference_right = table[order][right_index]
            difference = (difference_left + difference_right) / 2

            product = p
            for j in range(1, (order + 1) // 2):
                product *= p**2 - j**2

            used_cells.add((left_index, order + 1))
            used_cells.add((right_index, order + 1))

            print(f"\nOrder {order}:")
            print(
                f"  Average = ({difference_left:.6f} + "
                f"{difference_right:.6f}) / 2"
            )

        else:
            # Even order: central even difference
            index = origin - order // 2

            if index < 0 or index >= len(table[order]):
                break

            difference = table[order][index]
            product = p**2

            for j in range(1, order // 2):
                product *= p**2 - j**2

            used_cells.add((index, order + 1))

            print(f"\nOrder {order}:")
            print(f"  Central difference = {difference:.6f}")

        term = product * difference / math.factorial(order)
        result += term

        print(f"  Polynomial factor = {product:.6f}")
        print(f"  Factorial = {math.factorial(order)}")
        print(f"  Term value = {term:.6f}")
        print(f"  Running sum = {result:.6f}")

    save_difference_image(
        "STIRLING CENTRAL DIFFERENCE TABLE",
        origin,
        used_cells,
        "Stirling_Central_Difference_Table.png"
    )

    print(f"\nFinal interpolated value = {result:.3f}")
    return result


# =====================================================
# MAIN PROGRAM
# =====================================================

print_difference_table()

# Save the forward table immediately.
forward_cells = {
    (0, col)
    for col in range(2, n + 1)
}
save_difference_image(
    "NEWTON FORWARD DIFFERENCE TABLE",
    0,
    forward_cells,
    "Newton_Forward_Difference_Table.png"
)

target = float(input("\nEnter target x value: "))

while True:
    print("\n" + "=" * 50)
    print("SELECT AN OPTION")
    print("=" * 50)
    print("1. Newton Forward Interpolation")
    print("2. Stirling Central Interpolation")
    print("3. Calculate using both methods")
    print("4. Enter a new target x value")
    print("0. Exit")

    choice = input("Your choice: ").strip()

    if choice == "0":
        print("\nProgram ended. Goodbye!")
        break

    if choice == "4":
        try:
            target = float(input("Enter new target x value: "))
        except ValueError:
            print("Error: Enter a valid number.")
        continue

    if choice not in ("1", "2", "3"):
        print("Invalid choice. Please select 0, 1, 2, 3, or 4.")
        continue

    if target < x[0] or target > x[-1]:
        print(
            f"\nError: x = {target} is outside "
            f"[{x[0]}, {x[-1]}]."
        )
        print("Extrapolation is required, not interpolation.")
        continue

    if choice == "1":
        newton_forward(target)

    elif choice == "2":
        stirling_central(target)

    else:
        forward_result = newton_forward(target)
        central_result = stirling_central(target)

        if central_result is not None:
            print("\n" + "=" * 50)
            print("FINAL COMPARISON")
            print("=" * 50)
            print(f"Newton Forward : {forward_result:.3f}")
            print(f"Stirling       : {central_result:.3f}")
            print(
                "Absolute difference: "
                f"{abs(forward_result - central_result):.6f}"
            )

    print("\nYou can select another method or exit.")
