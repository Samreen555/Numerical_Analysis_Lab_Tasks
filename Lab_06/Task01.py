# ================================================================================================================
# NUMERICAL METHODS - LAB 6
# INTERPOLATION WITH CENTRAL DIFFERENCES
# Complete version with Newton Forward and Newton Backward Difference Error Analysis
# ================================================================================================================

import math
import os
import matplotlib.pyplot as plt


# ------------------------------------------------------------------------------------------------
# General utilities
# ------------------------------------------------------------------------------------------------

def line(char="=", n=112):
    print(char * n)


def difference_table(y):
    """Return forward-difference table as a list of columns."""
    table = [list(map(float, y))]
    while len(table[-1]) > 1:
        previous = table[-1]
        table.append([previous[i + 1] - previous[i] for i in range(len(previous) - 1)])
    return table


def print_difference_table(x, table):
    line()
    print("FORWARD DIFFERENCE TABLE")
    line()
    headers = ["x", "f(x)"] + [f"Δ^{i}" for i in range(1, len(table))]
    print(" ".join(f"{h:>16}" for h in headers))
    print("-" * 112)

    for i in range(len(x)):
        row = [f"{x[i]:16.6f}", f"{table[0][i]:16.10f}"]
        for order in range(1, len(table)):
            if i < len(table[order]):
                row.append(f"{table[order][i]:16.10f}")
            else:
                row.append(f"{'':16}")
        print(" ".join(row))
    line()


def print_difference_calculations(table):
    print()
    line("-")
    print("HOW THE DIFFERENCE TABLE IS CALCULATED")
    line("-")
    for order in range(1, len(table)):
        print(f"\nDelta^{order} calculations:")
        for i in range(len(table[order])):
            print(
                f"Δ^{order}f[{i}] = Δ^{order-1}f[{i+1}] - "
                f"Δ^{order-1}f[{i}] = "
                f"{table[order-1][i+1]:.10f} - "
                f"{table[order-1][i]:.10f} = "
                f"{table[order][i]:.10f}"
            )
    print("-" * 112)


def save_difference_table_image(x, table, folder):
    path = os.path.join(folder, "difference_table.png")

    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.axis("off")

    headers = ["x", "f(x)"] + [f"Δ^{i}" for i in range(1, len(table))]
    rows = []

    for i in range(len(x)):
        row = [f"{x[i]:.6f}", f"{table[0][i]:.10f}"]
        for order in range(1, len(table)):
            row.append(
                f"{table[order][i]:.10f}" if i < len(table[order]) else ""
            )
        rows.append(row)

    tbl = ax.table(cellText=rows, colLabels=headers, loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1, 1.7)
    ax.set_title("Forward Difference Table", fontsize=14, pad=15)

    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path


def save_comparison_image(results, xp, folder):
    path = os.path.join(folder, "comparison.png")

    names = list(results.keys())
    values = list(results.values())

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(names, values)
    ax.set_title(f"Interpolation Formula Comparison at x = {xp}")
    ax.set_ylabel("Interpolated Value")
    ax.tick_params(axis="x", rotation=35)

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.8f}",
            ha="center",
            va="bottom",
            fontsize=8,
        )

    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path


def save_formula_working_image(name, result, xp, folder):
    """Save a concise visual summary of the selected/first formula working."""
    path = os.path.join(folder, "formula_working.png")

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.axis("off")

    text = (
        "INTERPOLATION FORMULA WORKING\n\n"
        f"Formula: {name}\n"
        f"Interpolation point: x = {xp:.8f}\n\n"
        "The detailed step-by-step calculation is displayed in the "
        "terminal output.\n\n"
        f"Final interpolated value = {result:.10f}"
    )

    ax.text(
        0.5, 0.5, text,
        ha="center", va="center",
        fontsize=13, wrap=True
    )
    ax.set_title("Detailed Formula Working", fontsize=15, pad=18)

    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path


def save_error_analysis_image(forward_rows, backward_rows, folder):
    """Save a comparison plot for Newton Forward and Newton Backward error estimates."""
    path = os.path.join(folder, "error_analysis.png")

    forward_labels = [f"n={row['order']}" for row in forward_rows]
    backward_labels = [f"n={row['order']}" for row in backward_rows]

    max_rows = max(len(forward_rows), len(backward_rows), 1)
    positions = list(range(max_rows))
    width = 0.36

    forward_values = [abs(row["error"]) for row in forward_rows]
    backward_values = [abs(row["error"]) for row in backward_rows]

    fig, ax = plt.subplots(figsize=(11, 6))

    if forward_values:
        ax.bar(
            [pos - width / 2 for pos in positions[:len(forward_values)]],
            forward_values,
            width,
            label="Newton Forward",
        )

    if backward_values:
        ax.bar(
            [pos + width / 2 for pos in positions[:len(backward_values)]],
            backward_values,
            width,
            label="Newton Backward",
        )

    ax.set_title("Newton Forward and Newton Backward Error Estimates")
    ax.set_xlabel("Interpolation order n")
    ax.set_ylabel("Absolute Error |E|")
    ax.set_xticks(positions[:max_rows])
    ax.set_xticklabels([f"n={i}" for i in range(1, max_rows + 1)])
    ax.legend()

    for i, value in enumerate(forward_values):
        ax.text(i - width / 2, value, f"{value:.3e}", ha="center", va="bottom", fontsize=8)

    for i, value in enumerate(backward_values):
        ax.text(i + width / 2, value, f"{value:.3e}", ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path


# ------------------------------------------------------------------------------------------------
# Polynomial
# ------------------------------------------------------------------------------------------------

def lagrange_polynomial_coefficients(x, y):
    """
    Return coefficients in descending powers for the interpolating polynomial
    through all supplied points.
    """
    n = len(x)
    coefficients = [0.0] * n

    for i in range(n):
        basis = [1.0]
        denominator = 1.0

        for j in range(n):
            if i == j:
                continue

            new_basis = [0.0] * (len(basis) + 1)
            for k, coefficient in enumerate(basis):
                new_basis[k] += coefficient
                new_basis[k + 1] -= coefficient * x[j]
            basis = new_basis
            denominator *= (x[i] - x[j])

        scale = y[i] / denominator
        for k, coefficient in enumerate(basis):
            coefficients[k] += scale * coefficient

    return coefficients


def evaluate_polynomial(coefficients, value):
    result = 0.0
    for coefficient in coefficients:
        result = result * value + coefficient
    return result


def polynomial_to_string(coefficients):
    degree = len(coefficients) - 1
    terms = []

    for i, coefficient in enumerate(coefficients):
        power = degree - i
        if abs(coefficient) < 1e-12:
            continue

        sign = "+" if coefficient >= 0 else "-"
        magnitude = abs(coefficient)

        if power == 0:
            term = f"{magnitude:.8f}"
        elif power == 1:
            term = f"{magnitude:.8f}x"
        else:
            term = f"{magnitude:.8f}x^{power}"

        if not terms:
            terms.append(term if coefficient >= 0 else f"-{term}")
        else:
            terms.append(f" {sign} {term}")

    return "".join(terms) if terms else "0"


def show_polynomial(x, y, xp, folder):
    line()
    print("INTERPOLATION POLYNOMIAL")
    line()

    coefficients = lagrange_polynomial_coefficients(x, y)
    degree = len(x) - 1
    value = evaluate_polynomial(coefficients, xp)

    print(f"Maximum possible degree = n - 1 = {len(x)} - 1 = {degree}")
    print(f"P(x) = {polynomial_to_string(coefficients)}")
    print(f"P({xp:.8f}) = {value:.10f}")
    line()

    path = os.path.join(folder, "polynomial_result.png")

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.axis("off")
    text = (
        "INTERPOLATION POLYNOMIAL\n\n"
        f"Maximum degree = {degree}\n\n"
        f"P(x) = {polynomial_to_string(coefficients)}\n\n"
        f"P({xp:.8f}) = {value:.10f}"
    )
    ax.text(
        0.5, 0.5, text,
        ha="center", va="center",
        fontsize=12, wrap=True
    )
    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    return coefficients, value, path


# ------------------------------------------------------------------------------------------------
# Formula calculations
# ------------------------------------------------------------------------------------------------

def central_origin(x, xp):
    """Choose the data point nearest to xp."""
    return min(range(len(x)), key=lambda i: abs(x[i] - xp))


def stirling(x, y, table, xp, h):
    c = central_origin(x, xp)
    p = (xp - x[c]) / h
    result = table[0][c]

    # Half-step first difference terms
    if c >= 1 and c < len(table[1]):
        result += (p / 2.0) * (table[1][c - 1] + table[1][c])

    if len(table) > 2 and c < len(table[2]):
        result += (p * p / math.factorial(2)) * table[2][c]

    if len(table) > 3 and c >= 1 and c < len(table[3]):
        result += (
            p * (p * p - 1) / math.factorial(3)
        ) * table[3][c - 1]

    if len(table) > 4 and c < len(table[4]):
        result += (
            p * p * (p * p - 1) / math.factorial(4)
        ) * table[4][c]

    return result, c, p


def bessel(x, y, table, xp, h):
    c = central_origin(x, xp)
    if c >= len(x) - 1:
        c -= 1

    p = (xp - x[c]) / h

    result = (table[0][c] + table[0][c + 1]) / 2.0

    if len(table) > 1:
        result += (p - 0.5) * table[1][c]

    if len(table) > 2:
        result += (
            p * (p - 1) / math.factorial(2)
        ) * ((table[2][c - 1] + table[2][c]) / 2.0)

    if len(table) > 3 and c - 1 >= 0:
        result += (
            (p * (p - 1) * (p - 0.5)) / math.factorial(3)
        ) * table[3][c - 1]

    return result, c, p


def everett(x, y, table, xp, h):
    c = central_origin(x, xp)
    if c >= len(x) - 1:
        c -= 1

    p = (xp - x[c]) / h
    q = 1.0 - p

    result = q * table[0][c] + p * table[0][c + 1]

    if len(table) > 2 and c >= 1 and c < len(table[2]):
        result += (
            p * q / math.factorial(2)
        ) * (q * table[2][c - 1] + p * table[2][c])

    if len(table) > 4 and c >= 2 and c - 2 < len(table[4]):
        result += (
            p * q * (q * q - 1) / math.factorial(4)
        ) * table[4][c - 2]

    return result, c, p


def gaussian_forward(x, y, table, xp, h):
    c = central_origin(x, xp)
    p = (xp - x[c]) / h

    result = table[0][c]

    if len(table) > 1 and c < len(table[1]):
        result += p * table[1][c]

    if len(table) > 2 and c - 1 >= 0:
        result += (
            p * (p - 1) / math.factorial(2)
        ) * table[2][c - 1]

    if len(table) > 3 and c - 1 >= 0:
        result += (
            (p + 1) * p * (p - 1) / math.factorial(3)
        ) * table[3][c - 1]

    if len(table) > 4 and c - 2 >= 0:
        result += (
            (p + 1) * p * (p - 1) * (p - 2) / math.factorial(4)
        ) * table[4][c - 2]

    return result, c, p


def gaussian_backward(x, y, table, xp, h):
    c = central_origin(x, xp)
    p = (xp - x[c]) / h

    result = table[0][c]

    if len(table) > 1 and c - 1 >= 0:
        result += p * table[1][c - 1]

    if len(table) > 2 and c - 1 >= 0:
        result += (
            p * (p + 1) / math.factorial(2)
        ) * table[2][c - 1]

    if len(table) > 3 and c - 2 >= 0:
        result += (
            (p - 1) * p * (p + 1) / math.factorial(3)
        ) * table[3][c - 2]

    if len(table) > 4 and c - 2 >= 0:
        result += (
            (p - 1) * p * (p + 1) * (p + 2) / math.factorial(4)
        ) * table[4][c - 2]

    return result, c, p


def newton_forward(x, y, table, xp, h):
    p = (xp - x[0]) / h
    result = table[0][0]

    for order in range(1, len(table)):
        product = 1.0
        for k in range(order):
            product *= p - k
        result += (product / math.factorial(order)) * table[order][0]

    return result, 0, p


def newton_backward(x, y, table, xp, h):
    p = (xp - x[-1]) / h
    result = table[0][-1]

    for order in range(1, len(table)):
        product = 1.0
        for k in range(order):
            product *= p + k
        result += (product / math.factorial(order)) * table[order][-1]

    return result, len(x) - 1, p


# ------------------------------------------------------------------------------------------------
# Detailed working
# ------------------------------------------------------------------------------------------------

def detailed_working(name, x, y, table, xp, h, result, origin, p):
    line()
    print(f"DETAILED WORKING - {name.upper()}")
    line()

    formulas = {
        "Stirling":
            "fp = f0 + (p/2)(δf−1/2 + δf+1/2) + "
            "(p²/2!)δ²f0 + [p(p²−1)/3!]δ³f... + ...",
        "Bessel":
            "fp = (f0+f1)/2 + (p−1/2)Δf0 + "
            "[p(p−1)/2!](Δ²f−1+Δ²f0)/2 + ...",
        "Everett":
            "fp = qf0 + pf1 + (pq/2!)[qΔ²f−1 + pΔ²f0] + ...",
        "Gaussian Forward":
            "fp = f0 + pΔf0 + [p(p−1)/2!]Δ²f−1 + "
            "[(p+1)p(p−1)/3!]Δ³f−1 + ...",
        "Gaussian Backward":
            "fp = f0 + pΔf−1 + [p(p+1)/2!]Δ²f−1 + "
            "[(p−1)p(p+1)/3!]Δ³f−2 + ...",
        "Newton Forward":
            "fp = f0 + pΔf0 + [p(p−1)/2!]Δ²f0 + "
            "[p(p−1)(p−2)/3!]Δ³f0 + ...",
        "Newton Backward":
            "fp = f0 + p∇f0 + [p(p+1)/2!]∇²f0 + "
            "[p(p+1)(p+2)/3!]∇³f0 + ..."
    }

    print("Formula:")
    print(formulas[name])
    print()
    print(f"x0 = {x[origin]:.10f}")
    print(f"h  = {h:.10f}")
    print(f"xp = {xp:.10f}")
    print(f"p  = (xp - x0) / h = {p:.10f}")
    print()
    print("Step-by-step calculation:")

    # Detailed terms for the formulas, matching the style of the previous program.
    if name == "Newton Forward":
        print("\nTerm 1:")
        print(f"f0 = {table[0][0]:.10f}")

        total = table[0][0]
        for order in range(1, len(table)):
            product = 1.0
            factors = []
            for k in range(order):
                factor = p - k
                product *= factor
                factors.append(f"({factor:.10f})")

            coefficient = product / math.factorial(order)
            term = coefficient * table[order][0]
            total += term

            print(f"\nTerm {order + 1}:")
            print(f"coefficient = {coefficient:.10f}")
            print(f"factors = {' × '.join(factors)}")
            print(f"Δ^{order}f0 = {table[order][0]:.10f}")
            print(
                f"Term = {coefficient:.10f} × "
                f"{table[order][0]:.10f} = {term:.10f}"
            )

        print("\nFinal calculation:")
        print(f"f(xp) = {total:.10f}")
        print(f"f(xp) = {result:.10f}")

    elif name == "Newton Backward":
        print("\nTerm 1:")
        print(f"f0 = {table[0][-1]:.10f}")

        total = table[0][-1]
        for order in range(1, len(table)):
            product = 1.0
            factors = []
            for k in range(order):
                factor = p + k
                product *= factor
                factors.append(f"({factor:.10f})")

            coefficient = product / math.factorial(order)
            term = coefficient * table[order][-1]
            total += term

            print(f"\nTerm {order + 1}:")
            print(f"coefficient = {coefficient:.10f}")
            print(f"factors = {' × '.join(factors)}")
            print(f"∇^{order}f0 = {table[order][-1]:.10f}")
            print(
                f"Term = {coefficient:.10f} × "
                f"{table[order][-1]:.10f} = {term:.10f}"
            )

        print("\nFinal calculation:")
        print(f"f(xp) = {total:.10f}")
        print(f"f(xp) = {result:.10f}")

    else:
        # Generic term display for the central formulas.
        print(f"\nStarting value near interpolation point = {table[0][origin]:.10f}")
        print("\nThe program evaluates the required central-difference terms")
        print("using the displayed formula and the generated difference table.")
        print(f"\nFinal interpolated value = {result:.10f}")

    line()


# ------------------------------------------------------------------------------------------------
# Newton Forward and Newton Backward error formulas from Lecture 6
# ------------------------------------------------------------------------------------------------

def newton_forward_error_analysis(x, table, xp, h):
    """
    Newton Forward error formula:

        R_n(x) ≈ p(p-1)(p-2)...(p-n) / (n+1)! × Δ^(n+1)y_0

    where
        p = (xp - x_0) / h

    The available error estimates use the forward difference at the
    beginning of the table.
    """
    p = (xp - x[0]) / h
    rows = []

    # Δ^(n+1) exists when n+1 <= highest difference order.
    max_available_order = len(table) - 2

    for n in range(1, max_available_order + 1):
        next_difference_order = n + 1
        delta_value = table[next_difference_order][0]

        product = 1.0
        factors = []

        for k in range(n + 1):
            factor = p - k
            product *= factor
            factors.append(f"({factor:.10f})")

        denominator = math.factorial(n + 1)
        error = (product / denominator) * delta_value

        rows.append({
            "order": n,
            "parameter": p,
            "parameter_name": "p",
            "factors": factors,
            "product": product,
            "denominator": denominator,
            "next_difference_order": next_difference_order,
            "difference_symbol": "Δ",
            "difference_value": delta_value,
            "difference_location": "y0",
            "error": error,
        })

    return rows


def newton_backward_error_analysis(x, table, xp, h):
    """
    Newton Backward error formula supplied in the Lab/Lecture material:

        R_n(x) ≈ v(v+1)(v+2)...(v+n) / (n+1)! × ∇^(n+1)y_n

    where
        v = (xp - x_n) / h

    The backward difference ∇^(k)y_n is the last entry of the kth
    forward-difference column, so it can be obtained directly from the
    generated difference table.
    """
    v = (xp - x[-1]) / h
    rows = []

    max_available_order = len(table) - 2

    for n in range(1, max_available_order + 1):
        next_difference_order = n + 1
        nabla_value = table[next_difference_order][-1]

        product = 1.0
        factors = []

        for k in range(n + 1):
            factor = v + k
            product *= factor
            factors.append(f"({factor:.10f})")

        denominator = math.factorial(n + 1)
        error = (product / denominator) * nabla_value

        rows.append({
            "order": n,
            "parameter": v,
            "parameter_name": "v",
            "factors": factors,
            "product": product,
            "denominator": denominator,
            "next_difference_order": next_difference_order,
            "difference_symbol": "∇",
            "difference_value": nabla_value,
            "difference_location": "yn",
            "error": error,
        })

    return rows


def print_error_analysis(x, table, xp, h, folder):
    """Print both Newton Forward and Newton Backward error analyses."""
    forward_rows = newton_forward_error_analysis(x, table, xp, h)
    backward_rows = newton_backward_error_analysis(x, table, xp, h)

    p = (xp - x[0]) / h
    v = (xp - x[-1]) / h

    line()
    print("NEWTON FORWARD AND NEWTON BACKWARD ERROR ANALYSIS")
    line()

    print("1. NEWTON FORWARD ERROR FORMULA")
    print("R_n(x) ≈ p(p−1)(p−2) ... (p−n) / (n+1)! × Δ^(n+1)y0")
    print()
    print("p = (xp - x0) / h")
    print(f"p = ({xp:.10f} - {x[0]:.10f}) / {h:.10f}")
    print(f"p = {p:.10f}")

    print("\nForward error calculations:")
    for row in forward_rows:
        n = row["order"]
        print()
        print(f"Error estimate for n = {n}")
        print("-" * 80)
        print(
            f"R_{n}(x) = [{' × '.join(row['factors'])}] / "
            f"{row['denominator']} × "
            f"Δ^{row['next_difference_order']}y0"
        )
        print(f"Product = {row['product']:.10f}")
        print(f"(n+1)! = {row['denominator']}")
        print(
            f"Δ^{row['next_difference_order']}y0 = "
            f"{row['difference_value']:.10f}"
        )
        print(
            f"R_{n}(x) = ({row['product']:.10f} / {row['denominator']}) × "
            f"{row['difference_value']:.10f}"
        )
        print(f"R_{n}(x) = {row['error']:.12e}")
        print(f"|R_{n}(x)| = {abs(row['error']):.12e}")

    line()
    print("2. NEWTON BACKWARD ERROR FORMULA")
    print("R_n(x) ≈ v(v+1)(v+2) ... (v+n) / (n+1)! × ∇^(n+1)yn")
    print()
    print("v = (xp - xn) / h")
    print(f"v = ({xp:.10f} - {x[-1]:.10f}) / {h:.10f}")
    print(f"v = {v:.10f}")
    print()
    print("For the backward formula, ∇^(k)yn is taken from the last entry")
    print("of the kth difference column of the generated difference table.")

    print("\nBackward error calculations:")
    for row in backward_rows:
        n = row["order"]
        print()
        print(f"Error estimate for n = {n}")
        print("-" * 80)
        print(
            f"R_{n}(x) = [{' × '.join(row['factors'])}] / "
            f"{row['denominator']} × "
            f"∇^{row['next_difference_order']}yn"
        )
        print(f"Product = {row['product']:.10f}")
        print(f"(n+1)! = {row['denominator']}")
        print(
            f"∇^{row['next_difference_order']}yn = "
            f"{row['difference_value']:.10f}"
        )
        print(
            f"R_{n}(x) = ({row['product']:.10f} / {row['denominator']}) × "
            f"{row['difference_value']:.10f}"
        )
        print(f"R_{n}(x) = {row['error']:.12e}")
        print(f"|R_{n}(x)| = {abs(row['error']):.12e}")

    print()
    print("Important:")
    highest_difference = len(table) - 1
    print(f"The table contains differences up to order {highest_difference}.")
    print(
        f"Therefore the n = {highest_difference} error estimate would require "
        f"a difference of order {highest_difference + 1}, which is unavailable."
    )
    print("The program does not invent or assume an unavailable difference.")

    if forward_rows:
        largest_forward = max(forward_rows, key=lambda r: abs(r["error"]))
        print(
            f"\nLargest available Newton Forward |R_n|: "
            f"n = {largest_forward['order']}, "
            f"{abs(largest_forward['error']):.12e}"
        )

    if backward_rows:
        largest_backward = max(backward_rows, key=lambda r: abs(r["error"]))
        print(
            f"Largest available Newton Backward |R_n|: "
            f"n = {largest_backward['order']}, "
            f"{abs(largest_backward['error']):.12e}"
        )

    line()

    path = save_error_analysis_image(forward_rows, backward_rows, folder)
    print("Error analysis image saved as:")
    print(path)
    line()

    return forward_rows, backward_rows, path


# ------------------------------------------------------------------------------------------------
# Input and validation
# ------------------------------------------------------------------------------------------------

def read_data():
    print("\nEnter the number of equally spaced data points.")
    while True:
        try:
            n = int(input("n = "))
            if n < 2:
                print("Please enter at least 2 data points.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")

    print("\nEnter x values:")
    x = []
    for i in range(n):
        while True:
            try:
                value = float(input(f"x[{i}] = "))
                x.append(value)
                break
            except ValueError:
                print("Please enter a valid number.")

    print("\nEnter corresponding f(x) values:")
    y = []
    for i in range(n):
        while True:
            try:
                value = float(input(f"f[{i}] = "))
                y.append(value)
                break
            except ValueError:
                print("Please enter a valid number.")

    h = x[1] - x[0]
    tolerance = 1e-10

    if abs(h) < tolerance:
        raise ValueError("Consecutive x values must not be equal.")

    for i in range(1, n - 1):
        current_h = x[i + 1] - x[i]
        if abs(current_h - h) > tolerance:
            raise ValueError(
                "The x values are not equally spaced. "
                "Central-difference interpolation requires equally spaced data."
            )

    print(f"\nEqual spacing verified: h = {h:.10f}")

    return x, y, h


def read_interpolation_point(x):
    while True:
        try:
            xp = float(input("\nEnter interpolation point xp: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if xp < min(x) or xp > max(x):
            print(
                f"Warning: xp = {xp} is outside the data range "
                f"[{min(x)}, {max(x)}]."
            )
            print("Interpolation is valid inside the range; this would require extrapolation.")
            continue

        return xp


# ------------------------------------------------------------------------------------------------
# Formula menu / execution
# ------------------------------------------------------------------------------------------------

FORMULA_FUNCTIONS = {
    "Stirling": stirling,
    "Bessel": bessel,
    "Everett": everett,
    "Gaussian Forward": gaussian_forward,
    "Gaussian Backward": gaussian_backward,
    "Newton Forward": newton_forward,
    "Newton Backward": newton_backward,
}


def calculate_all_formulas(x, y, table, xp, h, folder):
    results = {}
    details = {}

    for name, function in FORMULA_FUNCTIONS.items():
        result, origin, p = function(x, y, table, xp, h)
        results[name] = result
        details[name] = (origin, p)

    line()
    print("COMPARISON OF INTERPOLATION FORMULAE")
    line()
    print(
        f"{'Formula':<28}{'Origin':>14}{'p':>16}"
        f"{'Interpolated value':>24}"
    )
    print("-" * 82)

    for name in FORMULA_FUNCTIONS:
        origin, p = details[name]
        print(
            f"{name:<28}{x[origin]:>14.6f}{p:>16.8f}"
            f"{results[name]:>24.10f}"
        )
    line()

    comparison_path = save_comparison_image(results, xp, folder)
    print("\nComparison image saved as:")
    print(comparison_path)

    print("\nDetailed working for every formula:")
    first_formula_working_path = None

    for index, (name, function) in enumerate(FORMULA_FUNCTIONS.items()):
        result, origin, p = function(x, y, table, xp, h)
        detailed_working(name, x, y, table, xp, h, result, origin, p)

        if index == 0:
            first_formula_working_path = save_formula_working_image(
                name, result, xp, folder
            )

    if first_formula_working_path:
        print("Detailed working image (first formula) saved as:")
        print(first_formula_working_path)

    print_error_analysis(x, table, xp, h, folder)

    return results


def calculate_selected_formula(x, y, table, xp, h, folder):
    print("\nFormula Menu")
    print("1. Stirling")
    print("2. Bessel")
    print("3. Everett")
    print("4. Gaussian Forward")
    print("5. Gaussian Backward")
    print("6. Newton Forward")
    print("7. Newton Backward")

    choices = list(FORMULA_FUNCTIONS.keys())

    while True:
        try:
            choice = int(input("Choose formula: "))
            if 1 <= choice <= len(choices):
                break
            print("Please choose a number from 1 to 7.")
        except ValueError:
            print("Please enter a valid number.")

    name = choices[choice - 1]
    function = FORMULA_FUNCTIONS[name]

    result, origin, p = function(x, y, table, xp, h)
    detailed_working(name, x, y, table, xp, h, result, origin, p)

    formula_working_path = save_formula_working_image(
        name, result, xp, folder
    )
    print("Detailed formula working image saved as:")
    print(formula_working_path)

    selected_results = {name: result}
    comparison_path = save_comparison_image(selected_results, xp, folder)

    print_error_analysis(x, table, xp, h, folder)

    return result, comparison_path


# ------------------------------------------------------------------------------------------------
# Main program
# ------------------------------------------------------------------------------------------------

def main():
    folder = os.path.dirname(os.path.abspath(__file__))

    while True:
        line()
        print("NUMERICAL METHODS - LAB 6")
        print("INTERPOLATION WITH CENTRAL DIFFERENCES")
        line()
        print("1. Enter Data To Calculate For All Formulas")
        print("2. Enter Data To Calculate For Selected Formula")
        print("3. Exit")
        line()

        choice = input("Enter your choice: ").strip()

        if choice == "3":
            print("Program ended.")
            break

        if choice not in ("1", "2"):
            print("Invalid choice. Please select 1, 2, or 3.")
            continue

        try:
            x, y, h = read_data()

            table = difference_table(y)
            print()
            print_difference_table(x, table)
            print_difference_calculations(table)

            difference_path = save_difference_table_image(x, table, folder)
            print("\nDifference table image saved as:")
            print(difference_path)

            xp = read_interpolation_point(x)

            if choice == "1":
                calculate_all_formulas(x, y, table, xp, h, folder)

                coefficients, polynomial_value, polynomial_path = show_polynomial(
                    x, y, xp, folder
                )

                print("\nGenerated files:")
                print("1. difference_table.png")
                print("2. comparison.png")
                print("3. polynomial_result.png")
                print("4. formula_working.png")
                print("5. error_analysis.png")

            elif choice == "2":
                calculate_selected_formula(x, y, table, xp, h, folder)

                coefficients, polynomial_value, polynomial_path = show_polynomial(
                    x, y, xp, folder
                )

                print("\nGenerated files:")
                print("1. difference_table.png")
                print("2. comparison.png")
                print("3. polynomial_result.png")
                print("4. formula_working.png")
                print("5. error_analysis.png")

        except ValueError as error:
            print(f"\nInput Error: {error}")
        except Exception as error:
            print(f"\nUnexpected error: {error}")


if __name__ == "__main__":
    main()
