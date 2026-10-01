import matplotlib.pyplot as plt
import math


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def format_number(value):
    """Format numbers neatly."""
    if abs(value) < 1e-12:
        value = 0

    if float(value).is_integer():
        return str(int(value))

    return f"{value:.6f}".rstrip("0").rstrip(".")


def superscript(number):
    """Convert integer to superscript characters."""
    chars = {
        "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
        "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
        "-": "⁻"
    }
    return "".join(chars.get(ch, ch) for ch in str(number))


def check_equal_spacing(x_values):
    """Check whether x values are equally spaced."""
    if len(x_values) < 2:
        return False

    h = x_values[1] - x_values[0]

    for i in range(2, len(x_values)):
        current_h = x_values[i] - x_values[i - 1]

        if not math.isclose(current_h, h, rel_tol=1e-9, abs_tol=1e-9):
            return False

    return True


# ============================================================
# DIFFERENCE TABLE
# ============================================================

def build_difference_table(y_values):
    """
    Construct forward difference table.

    table[0] = y
    table[1] = Δy
    table[2] = Δ²y
    ...
    """

    table = [y_values.copy()]
    current = y_values.copy()

    while len(current) > 1:
        next_column = []

        for i in range(len(current) - 1):
            difference = current[i + 1] - current[i]
            next_column.append(difference)

        table.append(next_column)
        current = next_column

    return table


# ============================================================
# DISPLAY TABLE
# ============================================================

def print_table(x_values, table):
    print("\n" + "=" * 80)
    print("DIFFERENCE TABLE")
    print("=" * 80)

    headers = ["x", "y"]

    for order in range(1, len(table)):
        headers.append("Δ" + superscript(order) + "y")

    print(" | ".join(f"{h:^12}" for h in headers))
    print("-" * 80)

    for i in range(len(x_values)):
        row = [
            format_number(x_values[i]),
            format_number(table[0][i])
        ]

        for order in range(1, len(table)):
            if i < len(table[order]):
                row.append(format_number(table[order][i]))
            else:
                row.append("")

        print(" | ".join(f"{value:^12}" for value in row))

    print("=" * 80)


# ============================================================
# FORWARD DIFFERENCE TABLE
# ============================================================

def print_forward_table(x_values, table, origin):
    print("\n" + "=" * 80)
    print("FORWARD DIFFERENCE OPERATOR TABLE (Δ)")
    print("=" * 80)

    print(f"Origin selected: x = {format_number(x_values[origin])}")
    print()

    print(f"{'Order':<10}{'Operator':<20}{'Value':<15}")
    print("-" * 45)

    for order in range(1, len(table)):
        if origin < len(table[order]):
            value = table[order][origin]
            label = "Δ" + superscript(order) + "y₀"

            print(
                f"{order:<10}"
                f"{label:<20}"
                f"{format_number(value):<15}"
            )

    print("=" * 80)


# ============================================================
# BACKWARD DIFFERENCE TABLE
# ============================================================

def print_backward_table(x_values, table, origin):
    print("\n" + "=" * 80)
    print("BACKWARD DIFFERENCE OPERATOR TABLE (∇)")
    print("=" * 80)

    print(f"Origin selected: x = {format_number(x_values[origin])}")
    print()

    print(f"{'Order':<10}{'Operator':<20}{'Value':<15}")
    print("-" * 45)

    for order in range(1, len(table)):
        index = origin - order

        if 0 <= index < len(table[order]):
            value = table[order][index]
            label = "∇" + superscript(order) + "y₀"

            print(
                f"{order:<10}"
                f"{label:<20}"
                f"{format_number(value):<15}"
            )

    print("=" * 80)


# ============================================================
# CENTRAL DIFFERENCE
# ============================================================

def central_difference(y_values, center, order):
    """
    Calculate central difference.
    """

    if order == 0:
        return y_values[center]

    if order == 1:
        if center - 1 >= 0 and center + 1 < len(y_values):
            return (y_values[center + 1] - y_values[center - 1]) / 2
        return None

    if center - order // 2 < 0:
        return None

    if center + order // 2 >= len(y_values):
        return None

    total = 0
    k = order

    for j in range(k + 1):
        index = center + (k // 2) - j

        if index < 0 or index >= len(y_values):
            return None

        coefficient = math.comb(k, j)
        total += ((-1) ** j) * coefficient * y_values[index]

    return total


def print_central_table(x_values, y_values, origin):
    print("\n" + "=" * 80)
    print("CENTRAL DIFFERENCE OPERATOR TABLE (δ)")
    print("=" * 80)

    print(f"Origin selected: x = {format_number(x_values[origin])}")
    print()

    print(f"{'Order':<10}{'Operator':<20}{'Value':<15}")
    print("-" * 45)

    for order in range(1, len(y_values)):
        value = central_difference(y_values, origin, order)

        if value is not None:
            label = "δ" + superscript(order) + "y₀"

            print(
                f"{order:<10}"
                f"{label:<20}"
                f"{format_number(value):<15}"
            )

    print("=" * 80)


# ============================================================
# INTERPOLATION RANGE CHECK
# ============================================================

def check_interpolation_range(x_values, target_x):
    x_min = min(x_values)
    x_max = max(x_values)

    if target_x < x_min or target_x > x_max:
        print("\n" + "!" * 70)
        print("ERROR: EXTRAPOLATION REQUIRED")
        print("!" * 70)

        print(f"Given x range : [{format_number(x_min)}, "
              f"{format_number(x_max)}]")

        print(f"Entered x     : {format_number(target_x)}")

        print("\nThe entered value is outside the given data range.")
        print("Interpolation can only be performed inside the range.")
        print("Please enter an x value within the given range.")

        print("!" * 70)

        return False

    return True


# ============================================================
# LAGRANGE INTERPOLATION
# ============================================================

def lagrange_interpolation(x_values, y_values, target_x):
    n = len(x_values)
    result = 0

    for i in range(n):
        term = y_values[i]

        for j in range(n):
            if i != j:
                term *= (
                    (target_x - x_values[j])
                    /
                    (x_values[i] - x_values[j])
                )

        result += term

    return result


# ============================================================
# NEWTON FORWARD INTERPOLATION
# ============================================================

def newton_forward_interpolation(x_values, table, target_x, origin):
    """
    Newton's Forward Difference formula:
      f(x) = f0 + p*Δf0 + [p(p-1)/2!]Δ²f0 + ...
    where p = (x - x0)/h
    """
    h = x_values[1] - x_values[0]
    p = (target_x - x_values[origin]) / h

    result = table[0][origin]
    term = 1

    for order in range(1, len(table)):
        if origin >= len(table[order]):
            break

        term *= (p - (order - 1))
        term /= order

        result += term * table[order][origin]

    return result, p


# ============================================================
# NEWTON BACKWARD INTERPOLATION (Lab 05)
# ============================================================

def newton_backward_interpolation(x_values, table, target_x, origin):
    """
    Newton's Backward Difference formula:
      f(x) = f0 + p*∇f0 + [p(p+1)/2!]∇²f0 + [p(p+1)(p+2)/3!]∇³f0 + ...
    where p = (x - x0)/h and ∇^k f0 is at index (origin - k).
    """
    h = x_values[1] - x_values[0]
    p = (target_x - x_values[origin]) / h

    result = table[0][origin]
    term = 1

    for order in range(1, len(table)):
        index = origin - order

        if index < 0 or index >= len(table[order]):
            break

        term *= (p + (order - 1))
        term /= order

        result += term * table[order][index]

    return result, p


# ============================================================
# AUTOMATIC ORIGIN SELECTION (Lab 05)
# ============================================================

def choose_origin(x_values, target_x):
    """
    Decide method (FORWARD / BACKWARD) and origin automatically
    per lecture rule:
      - target in first half  -> FORWARD, origin just before target
      - target in second half -> BACKWARD, origin just after target
      - ensures 0 < p < 1
    """
    n = len(x_values)

    interval_index = None
    for i in range(n - 1):
        if x_values[i] <= target_x <= x_values[i + 1]:
            interval_index = i
            break

    if interval_index is None:
        return None, None

    midpoint = (n - 1) / 2.0

    if interval_index < midpoint:
        method = "FORWARD"
        origin = interval_index
    else:
        method = "BACKWARD"
        origin = interval_index + 1

    return method, origin


# ============================================================
# QUERY OPERATOR VALUE
# ============================================================

def get_operator_value(table, y_values, operator, order,
                       relative_index, origin):

    if order < 1:
        return None

    if order >= len(table):
        return None

    if operator == "Δ":
        if not float(relative_index).is_integer():
            return None
        relative_index = int(relative_index)
        index = origin + relative_index

        if 0 <= index < len(table[order]):
            return table[order][index]

        return None

    elif operator == "∇":
        if not float(relative_index).is_integer():
            return None
        relative_index = int(relative_index)
        index = origin + relative_index - order

        if 0 <= index < len(table[order]):
            return table[order][index]

        return None

    elif operator == "δ":
        if not float(relative_index).is_integer():
            return None
        relative_index = int(relative_index)
        center = origin + relative_index

        return central_difference(y_values, center, order)

    return None


# ============================================================
# PARSE OPERATOR QUERY
# ============================================================

def parse_query(query):
    query = query.strip()
    operators = ["Δ", "∇", "δ"]
    operator = None

    for op in operators:
        if query.startswith(op):
            operator = op
            break

    if operator is None:
        return None

    remaining = query[1:]

    if "y" not in remaining:
        return None

    order_text, index_text = remaining.split("y", 1)

    if order_text == "":
        return None

    superscript_map = {
        "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
        "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9"
    }

    for s, normal in superscript_map.items():
        order_text = order_text.replace(s, normal)

    order = int(order_text)

    subscript_map = {
        "₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4",
        "₅": "5", "₆": "6", "₇": "7", "₈": "8", "₉": "9"
    }

    for s, normal in subscript_map.items():
        index_text = index_text.replace(s, normal)

    index_text = index_text.strip()

    if index_text == "":
        relative_index = 0
    else:
        relative_index = int(index_text)

    return operator, order, relative_index


# ============================================================
# FIND LABELS FOR A GIVEN VALUE
# ============================================================

def find_labels(table, y_values, origin, target_value):
    labels = []

    for order in range(1, len(table)):
        for relative_index in range(-origin,
                                   len(table[order]) - origin):
            value = get_operator_value(table, y_values, "Δ",
                                       order, relative_index, origin)

            if value is not None and math.isclose(
                    value, target_value, rel_tol=1e-9, abs_tol=1e-9):

                label = ("Δ" + superscript(order) + "y"
                         + str(relative_index))
                labels.append(label)

    for order in range(1, len(table)):
        for relative_index in range(-origin,
                                   len(table[order]) - origin):
            value = get_operator_value(table, y_values, "∇",
                                       order, relative_index, origin)

            if value is not None and math.isclose(
                    value, target_value, rel_tol=1e-9, abs_tol=1e-9):

                label = ("∇" + superscript(order) + "y"
                         + str(relative_index))
                labels.append(label)

    return labels


# ============================================================
# IMAGE GENERATION
# ============================================================

def save_table_image(x_values, table, filename, title):
    headers = ["x", "y"]

    for order in range(1, len(table)):
        headers.append("Δ" + superscript(order) + "y")

    rows = []

    for i in range(len(x_values)):
        row = [
            format_number(x_values[i]),
            format_number(table[0][i])
        ]

        for order in range(1, len(table)):
            if i < len(table[order]):
                row.append(format_number(table[order][i]))
            else:
                row.append("")

        rows.append(row)

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.axis("off")

    table_plot = ax.table(cellText=rows, colLabels=headers,
                          loc="center", cellLoc="center")
    table_plot.auto_set_font_size(False)
    table_plot.set_fontsize(10)
    table_plot.scale(1.2, 2)

    ax.set_title(title, fontsize=16, fontweight="bold", pad=20)

    plt.savefig(filename, bbox_inches="tight", dpi=300)
    plt.close()

    print(f"Saved: {filename}")


def save_operator_image(labels, values, filename, title):
    rows = []

    for label, value in zip(labels, values):
        rows.append([label, format_number(value)])

    fig, ax = plt.subplots(figsize=(9, 7))
    ax.axis("off")

    table_plot = ax.table(cellText=rows, colLabels=["Operator", "Value"],
                          loc="center", cellLoc="center")
    table_plot.auto_set_font_size(False)
    table_plot.set_fontsize(12)
    table_plot.scale(1.5, 2)

    ax.set_title(title, fontsize=16, fontweight="bold", pad=20)

    plt.savefig(filename, bbox_inches="tight", dpi=300)
    plt.close()

    print(f"Saved: {filename}")


def save_interpolation_image(x_values, y_values, target_x, result,
                             method, origin, p, filename, title):
    """Save plot showing data points and interpolated point."""
    fig, ax = plt.subplots(figsize=(10, 7))

    ax.plot(x_values, y_values, "bo-",
            label="Data points", markersize=8)
    ax.plot(target_x, result, "r*", markersize=20,
            label=f"Interpolated f({format_number(target_x)}) "
                  f"= {format_number(result)}")
    ax.plot(x_values[origin], y_values[origin], "gs", markersize=14,
            label=f"Origin x₀ = {format_number(x_values[origin])}")

    ax.set_xlabel("x", fontsize=12)
    ax.set_ylabel("f(x)", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)

    info_text = (
        f"Method : Newton {method}\n"
        f"Origin : x₀ = {format_number(x_values[origin])}\n"
        f"p      : {format_number(p)}\n"
        f"Result : {format_number(result)}"
    )

    ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
            fontsize=11, verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.9))

    plt.savefig(filename, bbox_inches="tight", dpi=300)
    plt.close()

    print(f"Saved: {filename}")


# ============================================================
# MAXIMUM DEGREE POLYNOMIAL (Lab 05)
# ============================================================

def print_maximum_degree(table):
    """Report the maximum degree polynomial that fits the data."""
    n_points = len(table[0])
    degree = n_points - 1

    print("\n" + "=" * 80)
    print("MAXIMUM DEGREE POLYNOMIAL")
    print("=" * 80)
    print(f"Number of data points : {n_points}")
    print(f"Maximum degree        : {degree}")

    if degree >= 1 and len(table) > degree:
        top_diff = table[degree][0]
        print(f"Δ{superscript(degree)}f (constant) = "
              f"{format_number(top_diff)}")

        if all(math.isclose(v, top_diff, rel_tol=1e-9, abs_tol=1e-9)
               for v in table[degree]):
            print(f"→ The {degree}-th difference is constant.")
            print(f"→ Data fits exactly a polynomial of degree {degree}.")

    print("=" * 80)


# ============================================================
# NEWTON POLYNOMIAL IN p-FORM (Lab 05)
# ============================================================

def print_newton_polynomial_p_form(table, x_values, origin, method):
    """
    Print the Newton polynomial in terms of p, using the origin.
    p = (x - x0)/h
    """
    print("\n" + "=" * 80)
    print(f"NEWTON {method} POLYNOMIAL IN p-FORM")
    print("=" * 80)
    print(f"Origin: x₀ = {format_number(x_values[origin])}")
    print(f"h     = {format_number(x_values[1] - x_values[0])}")
    print(f"p     = (x - {format_number(x_values[origin])}) / "
          f"{format_number(x_values[1] - x_values[0])}")
    print()

    if method == "FORWARD":
        terms = [f"f₀ = {format_number(table[0][origin])}"]

        for order in range(1, len(table)):
            if origin >= len(table[order]):
                break

            value = table[order][origin]

            factors = "p"
            for k in range(1, order):
                factors += f"(p - {k})"

            terms.append(
                f"+ [ {factors} / {order}! ] * "
                f"Δ{superscript(order)}f₀ "
                f"[= {format_number(value)}]"
            )
    else:  # BACKWARD
        terms = [f"f₀ = {format_number(table[0][origin])}"]

        for order in range(1, len(table)):
            index = origin - order

            if index < 0 or index >= len(table[order]):
                break

            value = table[order][index]

            factors = "p"
            for k in range(1, order):
                factors += f"(p + {k})"

            terms.append(
                f"+ [ {factors} / {order}! ] * "
                f"∇{superscript(order)}f₀ "
                f"[= {format_number(value)}]"
            )

    print(f"P(p) = " + "\n       ".join(terms))
    print("=" * 80)


# ============================================================
# EXPANDED POLYNOMIAL IN x (NEW - Lab 05)
# ============================================================

def build_polynomial_in_x(x_values, table, origin, method):
    """
    Build the actual polynomial P(x) as a list of coefficients
    in ascending powers of x, using Newton's formula with
    p = (x - x0)/h.

    Returns coefficients [c0, c1, c2, ...] meaning
        P(x) = c0 + c1*x + c2*x² + ...
    """
    h = x_values[1] - x_values[0]
    x0 = x_values[origin]

    # Accumulate in "p" polynomial first: coeffs of p^0, p^1, ...
    # Then substitute p = (x - x0)/h
    p_coeffs = [0.0] * len(table)  # coefficients in ascending p powers

    # --- Build p-polynomial ---
    if method == "FORWARD":
        # term 0 : f0
        p_coeffs[0] += table[0][origin]

        for order in range(1, len(table)):
            if origin >= len(table[order]):
                break

            # numerator = p(p-1)(p-2)...(p-(order-1))
            numerator = [1.0]
            for k in range(order):
                # multiply by (p - k)
                new = [0.0] * (len(numerator) + 1)
                for i, c in enumerate(numerator):
                    new[i] += -k * c
                    new[i + 1] += c
                numerator = new

            denominator = math.factorial(order)
            value = table[order][origin]

            for i, c in enumerate(numerator):
                p_coeffs[i] += value * c / denominator

    else:  # BACKWARD
        p_coeffs[0] += table[0][origin]

        for order in range(1, len(table)):
            index = origin - order
            if index < 0 or index >= len(table[order]):
                break

            # numerator = p(p+1)(p+2)...(p+(order-1))
            numerator = [1.0]
            for k in range(order):
                new = [0.0] * (len(numerator) + 1)
                for i, c in enumerate(numerator):
                    new[i] += k * c
                    new[i + 1] += c
                numerator = new

            denominator = math.factorial(order)
            value = table[order][index]

            for i, c in enumerate(numerator):
                p_coeffs[i] += value * c / denominator

    # --- Substitute p = (x - x0)/h into p_coeffs to get x_coeffs ---
    # p = (x - x0)/h = (1/h) * x - (x0/h)
    # So p^k = sum_{j=0}^{k} C(k,j) * (1/h)^j * x^j * (-x0/h)^(k-j)
    x_coeffs = [0.0] * (len(p_coeffs) + 1)

    for k, ck in enumerate(p_coeffs):
        if ck == 0:
            continue

        for j in range(k + 1):
            binom = math.comb(k, j)
            coeff = (binom
                     * (1.0 / h) ** j
                     * (-x0 / h) ** (k - j))
            x_coeffs[j] += ck * coeff

    return x_coeffs


def print_polynomial_in_x(x_coeffs):
    """Print polynomial in x from coefficients."""
    print("\n" + "=" * 80)
    print("MAXIMUM DEGREE POLYNOMIAL P(x)")
    print("=" * 80)

    # Find degree (highest nonzero coefficient)
    degree = 0
    for i in range(len(x_coeffs) - 1, -1, -1):
        if abs(x_coeffs[i]) > 1e-12:
            degree = i
            break

    print(f"Degree: {degree}")
    print()

    # Build string in descending powers
    parts = []
    for i in range(degree, -1, -1):
        c = x_coeffs[i]
        if abs(c) < 1e-12:
            continue

        if i == 0:
            parts.append(f"{format_number(c)}")
        elif i == 1:
            if abs(c - 1) < 1e-12:
                parts.append("x")
            elif abs(c + 1) < 1e-12:
                parts.append("-x")
            else:
                parts.append(f"{format_number(c)}*x")
        else:
            if abs(c - 1) < 1e-12:
                parts.append(f"x^{i}")
            elif abs(c + 1) < 1e-12:
                parts.append(f"-x^{i}")
            else:
                parts.append(f"{format_number(c)}*x^{i}")

    # Join with + / - signs
    poly_str = ""
    for i, part in enumerate(parts):
        if i == 0:
            poly_str += part
        else:
            if part.startswith("-"):
                poly_str += " - " + part[1:]
            else:
                poly_str += " + " + part

    print(f"P(x) = {poly_str}")
    print("=" * 80)


# ============================================================
# MAIN PROGRAM
# ============================================================

print("\n" + "=" * 80)
print("LAB 05 - NEWTON FORWARD & BACKWARD INTERPOLATION")
print("=" * 80)

# ------------------------------------------------------------
# INPUT DATA
# ------------------------------------------------------------

n = int(input("\nEnter number of data points: "))

x_values = []
y_values = []

print("\nEnter x values:")
for i in range(n):
    x_values.append(float(input(f"x[{i}] = ")))

print("\nEnter corresponding y values:")
for i in range(n):
    y_values.append(float(input(f"y[{i}] = ")))

# ------------------------------------------------------------
# CHECK EQUAL SPACING
# ------------------------------------------------------------

if not check_equal_spacing(x_values):
    print("\nERROR!")
    print("The x values must be equally spaced.")
    print("Finite difference interpolation requires equally spaced data.")
    exit()

h = x_values[1] - x_values[0]

print("\n" + "=" * 80)
print("DATA VALIDATION")
print("=" * 80)

print(f"Given x range: [{format_number(min(x_values))}, "
      f"{format_number(max(x_values))}]")
print(f"Step size h = {format_number(h)}")
print("The x values are equally spaced.")

# ------------------------------------------------------------
# BUILD DIFFERENCE TABLE
# ------------------------------------------------------------

difference_table = build_difference_table(y_values)

print_table(x_values, difference_table)

# ------------------------------------------------------------
# SAVE DIFFERENCE TABLE IMAGE
# ------------------------------------------------------------

save_table_image(
    x_values,
    difference_table,
    "01_Difference_Table.png",
    "Finite Difference Table"
)

# ------------------------------------------------------------
# MAXIMUM DEGREE POLYNOMIAL (report)
# ------------------------------------------------------------

print_maximum_degree(difference_table)

# ------------------------------------------------------------
# SELECT ORIGIN (for operator tables)
# ------------------------------------------------------------

print("\nAvailable origin points:")
for i, x in enumerate(x_values):
    print(f"{i}: x = {format_number(x)}, "
          f"y = {format_number(y_values[i])}")

origin = int(input("\nEnter origin point index: "))

if origin < 0 or origin >= n:
    print("Invalid origin index.")
    exit()

print(f"\nSelected origin: x = {format_number(x_values[origin])}")

# ------------------------------------------------------------
# FORWARD TABLE
# ------------------------------------------------------------

print_forward_table(x_values, difference_table, origin)

forward_labels = []
forward_values = []

for order in range(1, len(difference_table)):
    if origin < len(difference_table[order]):
        forward_labels.append("Δ" + superscript(order) + "y₀")
        forward_values.append(difference_table[order][origin])

save_operator_image(
    forward_labels,
    forward_values,
    "02_Forward_Difference_Table.png",
    "Forward Difference Operator (Δ)"
)

# ------------------------------------------------------------
# BACKWARD TABLE
# ------------------------------------------------------------

print_backward_table(x_values, difference_table, origin)

backward_labels = []
backward_values = []

for order in range(1, len(difference_table)):
    index = origin - order
    if 0 <= index < len(difference_table[order]):
        backward_labels.append("∇" + superscript(order) + "y₀")
        backward_values.append(difference_table[order][index])

save_operator_image(
    backward_labels,
    backward_values,
    "03_Backward_Difference_Table.png",
    "Backward Difference Operator (∇)"
)

# ------------------------------------------------------------
# CENTRAL TABLE
# ------------------------------------------------------------

print_central_table(x_values, y_values, origin)

central_labels = []
central_values = []

for order in range(1, len(y_values)):
    value = central_difference(y_values, origin, order)
    if value is not None:
        central_labels.append("δ" + superscript(order) + "y₀")
        central_values.append(value)

save_operator_image(
    central_labels,
    central_values,
    "04_Central_Difference_Table.png",
    "Central Difference Operator (δ)"
)

# ============================================================
# LAB 05 - MULTIPLE INTERPOLATION QUERIES (NEW)
# ============================================================

print("\n" + "=" * 80)
print("INTERPOLATION QUERIES (Lab 05)")
print("=" * 80)
print("Enter x values one by one. Press ENTER on empty line to stop.")
print()

query_number = 0

while True:
    query = input("Enter x value for interpolation "
                  "(blank to stop): ").strip()

    if query == "":
        break

    try:
        target_x = float(query)
    except ValueError:
        print("  ⚠ Please enter a valid number.\n")
        continue

    query_number += 1

    # Range check — no extrapolation
    if not check_interpolation_range(x_values, target_x):
        print("  → Interpolation NOT performed.\n")
        continue

    # Automatic method & origin selection
    method, auto_origin = choose_origin(x_values, target_x)

    if method is None:
        print("  ⚠ Could not determine origin.\n")
        continue

    # Newton interpolation
    if method == "FORWARD":
        result, p = newton_forward_interpolation(
            x_values, difference_table, target_x, auto_origin
        )
    else:
        result, p = newton_backward_interpolation(
            x_values, difference_table, target_x, auto_origin
        )

    # Lagrange cross-check
    lagrange_result = lagrange_interpolation(
        x_values, y_values, target_x
    )

    # ---------------- DISPLAY ----------------
    print("\n" + "-" * 70)
    print(f"Query {query_number}: x = {format_number(target_x)}")
    print("-" * 70)

    if method == "FORWARD":
        upper = x_values[auto_origin + 1]
    else:
        upper = x_values[auto_origin]

    print(f"  Target lies in interval containing "
          f"x = {format_number(target_x)}")
    print(f"  Method used : NEWTON {method}")
    print(f"  Origin x₀   : {format_number(x_values[auto_origin])}")
    print(f"  h           : {format_number(h)}")
    print(f"  p           : {format_number(p)}")
    print(f"  Interpolated value:")
    print(f"      f({format_number(target_x)}) = "
          f"{format_number(result)}")
    print(f"  Lagrange cross-check: "
          f"{format_number(lagrange_result)}")

    # Show terms used
    if method == "FORWARD":
        print("\n  Forward formula terms:")
        term = 1.0
        print(f"    f₀ = {format_number(difference_table[0][auto_origin])}")
        for order in range(1, len(difference_table)):
            if auto_origin >= len(difference_table[order]):
                break
            term *= (p - (order - 1))
            term /= order
            contrib = term * difference_table[order][auto_origin]
            print(f"    term {order}: Δ{superscript(order)}f₀ = "
                  f"{format_number(difference_table[order][auto_origin])}, "
                  f"contribution = {format_number(contrib)}")
    else:
        print("\n  Backward formula terms:")
        term = 1.0
        print(f"    f₀ = {format_number(difference_table[0][auto_origin])}")
        for order in range(1, len(difference_table)):
            index = auto_origin - order
            if index < 0:
                break
            term *= (p + (order - 1))
            term /= order
            contrib = term * difference_table[order][index]
            print(f"    term {order}: ∇{superscript(order)}f₀ = "
                  f"{format_number(difference_table[order][index])}, "
                  f"contribution = {format_number(contrib)}")

    print()

    # Save plot for first query only
    if query_number == 1:
        save_interpolation_image(
            x_values, y_values, target_x, result,
            method, auto_origin, p,
            "05_Interpolation_Result.png",
            f"Newton {method} Interpolation at "
            f"x = {format_number(target_x)}"
        )

# ============================================================
# NEWTON POLYNOMIAL IN p-FORM (for the operator-table origin)
# ============================================================

# Decide method for this origin based on the midpoint rule
n_points = len(x_values)
midpoint = (n_points - 1) / 2.0

if origin < midpoint:
    poly_method = "FORWARD"
else:
    poly_method = "BACKWARD"

print_newton_polynomial_p_form(
    difference_table, x_values, origin, poly_method
)

# ============================================================
# EXPANDED POLYNOMIAL IN x
# ============================================================

x_coeffs = build_polynomial_in_x(
    x_values, difference_table, origin, poly_method
)
print_polynomial_in_x(x_coeffs)

# ============================================================
# OPERATOR QUERY (kept from original)
# ============================================================

print("\n" + "=" * 80)
print("OPERATOR QUERY")
print("=" * 80)

print("\nExamples:")
print("Δ²y0")
print("∇¹y0")
print("δ²y0")

query = input("\nEnter operator label: ").strip()

parsed = parse_query(query)

if parsed is not None:
    operator, order, relative_index = parsed

    value = get_operator_value(
        difference_table, y_values, operator,
        order, relative_index, origin
    )

    if value is not None:
        print(f"\n{query} = {format_number(value)}")
    else:
        print("\nThe requested operator value "
              "is not available for the selected origin.")
else:
    print("\nInvalid operator format.")

# ============================================================
# VALUE TO LABEL QUERY (kept from original)
# ============================================================

print("\n" + "=" * 80)
print("VALUE TO LABEL QUERY")
print("=" * 80)

value_query = input(
    "\nEnter a value to find its operator labels: "
)

try:
    target_value = float(value_query)

    labels = find_labels(
        difference_table, y_values, origin, target_value
    )

    if labels:
        print(f"\nValue {format_number(target_value)} "
              "is associated with:")
        for label in labels:
            print(" -", label)
    else:
        print("\nNo matching operator label was found.")

except ValueError:
    print("Please enter a valid numerical value.")

# ============================================================
# CLOSE
# ============================================================

print("\n" + "=" * 80)
print("PROGRAM COMPLETED SUCCESSFULLY")
print("=" * 80)

print("\nGenerated image files:")
print("1. 01_Difference_Table.png")
print("2. 02_Forward_Difference_Table.png")
print("3. 03_Backward_Difference_Table.png")
print("4. 04_Central_Difference_Table.png")
print("5. 05_Interpolation_Result.png  (only if at least one query ran)")

print("\nThank you!")