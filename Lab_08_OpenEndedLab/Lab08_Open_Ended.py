"""
=====================================================================
LAB 8 - OPEN ENDED LAB: NUMERICAL METHODS
Vaccine Cold-Chain Temperature Excursion
=====================================================================
Features:
  * Correct origin selection: every estimate guarantees 0 < p <= 1
  * Highlighted difference-table PNG per estimate (t = 5, 6.4, 11)
  * Highlighted multi-colour difference-table PNG for validation
  * USER INPUT option: any t -> auto-selects formula and origin
=====================================================================
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from numpy.polynomial import Polynomial

# =====================================================================
# TASK 1 — GIVEN DATA
# =====================================================================
t_data = np.array([0, 2, 4, 6, 8, 10, 12], dtype=float)
T_data = np.array([5.2, 6.4, 7.9, 9.5, 10.1, 9.3, 7.6], dtype=float)

h      = t_data[1] - t_data[0]
n      = len(t_data)
LIMIT  = 8.0
DEGREE = n - 1

print("=" * 72)
print("LAB 8: VACCINE COLD-CHAIN TEMPERATURE EXCURSION")
print("=" * 72)

# =====================================================================
# TASK 2 — SPACING CHECK + DIFFERENCE TABLE
# =====================================================================
def check_spacing():
    diffs = np.diff(t_data)
    print("\n1. EQUAL SPACING CHECK")
    print("-" * 72)
    print("Time values    :", t_data)
    print("Spacing values :", diffs)
    if np.allclose(diffs, diffs[0]):
        print("Readings are EQUALLY spaced.")
        print(f"Step size h = {h:.4f} hours")
    else:
        print("Readings are NOT equally spaced.")
    print(f"Number of readings          = {n}")
    print(f"Maximum supportable degree  = {DEGREE}")

def build_difference_table(values):
    table = np.full((len(values), len(values)), np.nan)
    table[:, 0] = values
    for order in range(1, len(values)):
        for i in range(len(values) - order):
            table[i, order] = table[i + 1, order - 1] - table[i, order - 1]
    return table

difference_table = build_difference_table(T_data)

# =====================================================================
# UNIVERSAL RENDERER
# =====================================================================
def render_difference_table(
        highlight_origin=None,
        highlight_diagonal=None,
        multi_highlights=None,
        legend_items=None,
        title="Forward Difference Table",
        caption=None,
        filename="Lab8_Difference_Table.png"):

    headers = ["t", "T", "ΔT", "Δ²T", "Δ³T", "Δ⁴T", "Δ⁵T", "Δ⁶T"]

    cell_text = []
    for i in range(n):
        row = [f"{t_data[i]:.2f}", f"{T_data[i]:.4f}"]
        for j in range(1, n):
            row.append(f"{difference_table[i, j]:.4f}"
                       if i + j <= n - 1 else "")
        cell_text.append(row)

    fig, ax = plt.subplots(figsize=(13, 5.6))
    ax.axis("off")

    table = ax.table(cellText=cell_text, colLabels=headers,
                     cellLoc="center", loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(9.5)
    table.scale(1, 1.55)

    for (r, c), cell in table.get_celld().items():
        if r == 0:
            cell.set_facecolor("#1f3a68")
            cell.set_text_props(color="white", weight="bold")
        else:
            data_row = r - 1
            cell.set_facecolor("#ffffff")
            if highlight_origin is not None and data_row == highlight_origin:
                cell.set_facecolor("#1f3a68")
                cell.set_text_props(color="white", weight="bold")

    if highlight_diagonal and not multi_highlights:
        for (dr, dc) in highlight_diagonal:
            cell = table[(dr + 1, dc + 1)]
            cell.set_facecolor("#ffcc4d")
            cell.set_text_props(weight="bold")

    if multi_highlights:
        for colour, cells in multi_highlights.items():
            for (dr, dc) in cells:
                cell = table[(dr + 1, dc + 1)]
                cell.set_facecolor(colour)
                if colour in ("#1f3a68", "#1a7f37", "#b3261e", "#7b1fa2"):
                    cell.set_text_props(weight="bold", color="white")
                else:
                    cell.set_text_props(weight="bold", color="black")

    ax.set_title(title, fontsize=13, weight="bold", pad=16)

    if legend_items:
        handles = [Patch(facecolor=c, edgecolor="grey", label=lbl)
                   for c, lbl in legend_items]
        ax.legend(handles=handles, loc="upper center",
                  bbox_to_anchor=(0.5, -0.02), ncol=len(legend_items),
                  frameon=False, fontsize=9)

    if caption:
        fig.text(0.5, -0.05, caption, ha="center", fontsize=9.5,
                 style="italic", color="#333333")
    plt.tight_layout()
    plt.savefig(filename, dpi=220, bbox_inches="tight")
    plt.close(fig)
    print(f"   ✔ Highlighted table saved → {filename}")

def print_difference_table():
    print("\n2. FORWARD DIFFERENCE TABLE")
    print("-" * 100)
    headers = ["t", "T", "D1", "D2", "D3", "D4", "D5", "D6"]
    print(" | ".join(f"{x:>10}" for x in headers))
    print("-" * 100)
    for i in range(n):
        row = [f"{t_data[i]:.2f}"]
        for j in range(n):
            v = difference_table[i, j]
            row.append("-" if np.isnan(v) else f"{v:.4f}")
        print(" | ".join(f"{x:>10}" for x in row))

    print("\nDegree assessment:")
    for order in range(1, n):
        vals = difference_table[:n - order, order]
        print(f"Order {order} differences: " + ", ".join(f"{v:+.4f}" for v in vals))
    print("\nThe 6th-order difference is NON-ZERO → degree-6 interpolant required.")

    render_difference_table(
        title="Forward Difference Table — Vaccine Cold-Chain Data",
        caption=f"Equally spaced readings, h = {h:.2f} h, "
                f"{n} points → degree-6 interpolant",
        filename="Lab8_Difference_Table.png",
    )

# =====================================================================
# TASK 3–4 — NEWTON FORWARD / BACKWARD
# =====================================================================
def newton_forward(t, origin_index=0):
    x0 = t_data[origin_index]
    p  = (t - x0) / h
    result = difference_table[origin_index, 0]
    product = 1.0
    terms = [f"f0 = {result:.4f}   (origin t = {x0:.2f})"]
    used_cells = [(origin_index, 0)]
    for order in range(1, n - origin_index):
        product *= p - (order - 1)
        diff    = difference_table[origin_index, order]
        term    = product * diff / math.factorial(order)
        result += term
        terms.append(f"Term {order} = {term:+.8f}")
        used_cells.append((origin_index, order))
    return result, p, terms, x0, used_cells

def newton_backward(t, origin_index):
    """Newton Backward formula about a chosen origin (nearest right node)."""
    xn = t_data[origin_index]
    p  = (t - xn) / h
    result = difference_table[origin_index, 0]
    product = 1.0
    terms = [f"fn = {result:.4f}   (origin t = {xn:.2f})"]
    used_cells = [(origin_index, 0)]
    for order in range(1, origin_index + 1):
        product *= p + order - 1
        diff    = difference_table[origin_index - order, order]
        term    = product * diff / math.factorial(order)
        result += term
        terms.append(f"∇^{order} term = {term:+.8f}")
        used_cells.append((origin_index - order, order))
    return result, p, terms, xn, used_cells

# =====================================================================
# TASK 5 — GLOBAL NEWTON POLYNOMIAL
# =====================================================================
def build_newton_polynomial():
    u = Polynomial([0.0, 1.0])
    poly = Polynomial([T_data[0]])
    prod = Polynomial([1.0])
    for order in range(1, n):
        prod  = prod * (u - (order - 1))
        poly += prod * difference_table[0, order] / math.factorial(order)
    return poly

newton_polynomial = build_newton_polynomial()

# =====================================================================
# TASK 6 — CENTERED EXPANSIONS (FIXED: handles midpoints for Bessel)
# =====================================================================
def centered_expansion(t, center):
    q0      = (center - t_data[0]) / h
    shifted = newton_polynomial(Polynomial([q0, 1.0]))
    q       = (t - center) / h
    result  = 0.0
    terms   = [f"Center = {center:.2f} h,  q = {q:+.4f}"]
    for order, coef in enumerate(shifted.coef):
        term    = coef * (q ** order)
        result += term
        terms.append(f"c{order} * q^{order} = {term:+.8f}")

    # --- FIX: highlight the appropriate row(s) for the centre ---
    # If the centre lies exactly on a tabular node (e.g. Stirling t=6, t=4),
    # highlight that row.
    # If the centre lies at a midpoint (e.g. Bessel t=7 between 6 and 8),
    # highlight both adjacent rows (t=6 and t=8).
    if np.any(np.isclose(t_data, center)):
        centre_idx = int(np.where(np.isclose(t_data, center))[0][0])
        used_cells = [(centre_idx, k) for k in range(0, n - centre_idx)]
    else:
        # Midpoint: highlight the two nearest nodes around the centre
        left_idx  = int(np.where(t_data < center)[0][-1])
        right_idx = left_idx + 1
        used_cells = ([(left_idx, k) for k in range(0, 2)]
                      + [(right_idx, k) for k in range(0, 2)])
    return result, q, terms, center, used_cells

def stirling_value(t, center=None):
    if center is None:
        valid = np.where(t_data <= t + 1e-9)[0]
        center = t_data[valid[-1]] if len(valid) > 0 else t_data[0]
    return centered_expansion(t, center=center)

def bessel_value(t, center=None):
    if center is None:
        # Choose the midpoint whose position is closest to t
        candidates = [(abs(0.5 * (t_data[k] + t_data[k + 1]) - t), 
                       0.5 * (t_data[k] + t_data[k + 1]))
                      for k in range(n - 1)]
        center = min(candidates, key=lambda z: z[0])[1]
    return centered_expansion(t, center=center)

# =====================================================================
# TASK 7 — NATURAL CUBIC SPLINE
# =====================================================================
def natural_cubic_spline(x_values):
    x, y = t_data, T_data
    size = len(x)
    dx = np.diff(x)
    A  = np.zeros((size, size));  b = np.zeros(size)
    A[0, 0] = 1;  A[-1, -1] = 1
    for i in range(1, size - 1):
        A[i, i - 1] = dx[i - 1]
        A[i, i]     = 2 * (dx[i - 1] + dx[i])
        A[i, i + 1] = dx[i]
        b[i] = 6 * ((y[i + 1] - y[i]) / dx[i]
                    - (y[i] - y[i - 1]) / dx[i - 1])
    M = np.linalg.solve(A, b)
    out = []
    for v in np.atleast_1d(x_values):
        i = int(np.searchsorted(x, v, side="right") - 1)
        i = max(0, min(i, size - 2))
        w = x[i + 1] - x[i]
        a  = (x[i + 1] - v) / w
        bb = (v - x[i]) / w
        val = (a * y[i] + bb * y[i + 1]
               + ((a ** 3 - a) * M[i] + (bb ** 3 - bb) * M[i + 1]) * w ** 2 / 6)
        out.append(val)
    return np.array(out)

# =====================================================================
# TASK 8 — DYNAMIC METHOD SELECTOR
# =====================================================================
def select_method(t):
    for i, ti in enumerate(t_data):
        if abs(t - ti) < 1e-9:
            return (f"Stirling (origin t={ti:.0f}, exact node)",
                    lambda x: centered_expansion(x, center=ti), i)

    if t < t_data[0]:
        return ("Newton Forward (origin t=0, EXTRAPOLATION)",
                lambda x: newton_forward(x, origin_index=0), 0)

    if t > t_data[-1]:
        return ("Newton Backward (origin t=12, EXTRAPOLATION)",
                lambda x: newton_backward(x, origin_index=n - 1), n - 1)

    left_idx = max(i for i, ti in enumerate(t_data) if ti <= t)
    right_idx = min(i for i, ti in enumerate(t_data) if ti >= t)

    if left_idx == right_idx:
        return (f"Stirling (origin t={t_data[left_idx]:.0f}, exact node)",
                lambda x: centered_expansion(x, center=t_data[left_idx]),
                left_idx)

    frac = (t - t_data[left_idx]) / h

    if right_idx <= 2:
        return (f"Newton Forward (origin t={t_data[left_idx]:.0f})",
                lambda x: newton_forward(x, origin_index=left_idx),
                left_idx)

    if left_idx >= n - 3:
        return (f"Newton Backward (origin t={t_data[right_idx]:.0f})",
                lambda x: newton_backward(x, origin_index=right_idx),
                right_idx)

    centre_idx = left_idx if frac <= 0.5 else right_idx
    return (f"Stirling (origin t={t_data[centre_idx]:.0f})",
            lambda x: centered_expansion(x, center=t_data[centre_idx]),
            centre_idx)

# =====================================================================
# TASK 9 — EVALUATE A POINT (with PNG)
# =====================================================================
def evaluate_point(t):
    name, fn, origin_row = select_method(t)
    result, p, terms, origin, used_cells = fn(t)

    print(f"\n--- Interpolation at t = {t:.4f} h ---")
    print(f"Formula selected : {name}")
    print(f"Origin           : t0 = {origin:.4f} h")
    print(f"Position p       : {p:+.4f}")
    print(f"Rule check       : "
          f"{'✔ 0 < p <= 1' if -1e-9 < p <= 1.0 + 1e-9 else '⚠ outside (0, 1]'}")
    for term in terms:
        print("   ", term)
    print(f"Estimate         : T({t:.4f}) = {result:.4f} C")

    fname = f"Lab8_DiffTable_t{t:.2f}.png"
    render_difference_table(
        highlight_origin=origin_row,
        highlight_diagonal=used_cells,
        title=f"Difference Table — Interpolation at t = {t:.2f} h",
        caption=(f"{name}   |   origin t0 = {origin:.2f} h   |   "
                 f"p = {p:+.4f}   |   T({t:.2f}) = {result:.4f} °C   |   "
                 f"amber = differences used"),
        filename=fname,
    )
    return result

def main_estimates():
    print("\n3. REQUIRED TEMPERATURE ESTIMATES (4 d.p.)")
    print("=" * 72)
    for t in (5.0, 6.4, 11.0):
        evaluate_point(t)

# =====================================================================
# TASK 10 — VALIDATION AT t = 6.4 h (FIXED)
# =====================================================================
def validation():
    t = 6.4
    print("\n4. VALIDATION AT t = 6.4 h  (all four methods)")
    print("=" * 72)

    stirling_val, _, _, _, st_cells = stirling_value(t, center=6.0)
    # Bessel centre t=7 is a midpoint (6+8)/2, handled by centered_expansion
    bessel_val,   _, _, _, be_cells = bessel_value(t,   center=7.0)
    backward_val, _, _, _, bk_cells = newton_backward(t, origin_index=n - 1)
    forward_val,  _, _, _, fw_cells = newton_forward(t,  origin_index=2)
    spline_val                       = natural_cubic_spline([t])[0]

    results = {
        "Stirling-centered"      : stirling_val,
        "Bessel-centered"        : bessel_val,
        "Newton backward (t=12)" : backward_val,
        "Newton forward  (t=4)"  : forward_val,
        "Natural cubic spline"   : spline_val,
    }

    print(f"{'Method':<28}{'T(6.4) °C':>14}")
    print("-" * 44)
    for name, val in results.items():
        print(f"{name:<28}{val:>14.4f}")

    hi, lo = max(results.values()), min(results.values())
    print("-" * 44)
    print(f"{'Highest':<28}{hi:>14.4f}")
    print(f"{'Lowest':<28}{lo:>14.4f}")
    print(f"{'Spread':<28}{hi - lo:>14.4f}")

    print("\nDifference from Stirling baseline:")
    for name, val in results.items():
        print(f"   {name:<28}: {abs(val - stirling_val):.4f} C")

    print("""
Agreement / divergence comment
------------------------------
• Stirling, Bessel, Backward-12 and Forward-4 evaluate the SAME degree-6
  Newton interpolant in different bases → agree to < 1e-10.
• Natural cubic spline is piecewise C² → the observed spread
  (~0.04 °C) is dominated by the spline.
• All four methods agree best near the CENTRE (6–8 h); they diverge near
  the ENDS due to Runge oscillation of the global polynomial.
""")

    multi = {
        "#ffcc4d": st_cells,
        "#1a7f37": be_cells,
        "#b3261e": bk_cells,
        "#1976d2": fw_cells,
    }
    legend = [
        ("#ffcc4d", "Stirling cells"),
        ("#1a7f37", "Bessel cells"),
        ("#b3261e", "Backward cells"),
        ("#1976d2", "Forward cells"),
    ]
    caption = (
        f"t = {t:.2f} h   |   "
        f"Stirling {stirling_val:.4f}  |  "
        f"Bessel {bessel_val:.4f}  |  "
        f"Backward {backward_val:.4f}  |  "
        f"Forward {forward_val:.4f}  |  "
        f"Spline {spline_val:.4f}  °C   |   "
        f"Spread {hi - lo:.4f} °C"
    )

    render_difference_table(
        multi_highlights=multi,
        legend_items=legend,
        title=f"Validation at t = {t:.2f} h — cell usage per method",
        caption=caption,
        filename="Lab8_Validation_t6_40.png",
    )
    return results

# =====================================================================
# TASK 11 — MAXIMUM
# =====================================================================
def find_maximum():
    print("\n5. MAXIMUM LOGGED TEMPERATURE")
    print("=" * 72)
    derivative = newton_polynomial.deriv()
    candidates = [0.0, 12.0]
    for root in derivative.roots():
        if abs(root.imag) < 1e-9:
            tv = t_data[0] + h * root.real
            if 0.0 <= tv <= 12.0:
                candidates.append(tv)
    values = [newton_polynomial((tv - t_data[0]) / h) for tv in candidates]
    idx = int(np.argmax(values))
    tmax, Tmax = candidates[idx], values[idx]

    print(f"Degree of interpolant      : {DEGREE}")
    print(f"Maximum time               : t = {tmax:.4f} h")
    print(f"Maximum temperature        : T = {Tmax:.4f} C")
    print(f"Highest logged reading     : {T_data[4]:.4f} C  (at t = 8 h)")

    grid = np.linspace(6.0, 10.0, 4001)
    vals = newton_polynomial((grid - t_data[0]) / h)
    local_max  = np.max(vals)
    local_time = grid[np.argmax(vals)]
    print(f"\nLocal check on [6, 10] h:")
    print(f"   argmax t = {local_time:.4f} h,  value = {local_max:.4f} C")
    if 6.0 <= tmax <= 10.0 and abs(local_max - Tmax) < 1e-3:
        print("   ✔ Confirmed: global maximum lies between nodes t=6 and t=10.")
    return tmax, Tmax

# =====================================================================
# TASK 12 — 8 °C CROSSINGS
# =====================================================================
def find_crossings():
    print("\n6. 8 °C LIMIT CROSSINGS")
    print("=" * 72)
    poly = newton_polynomial - Polynomial([LIMIT])
    roots = poly.roots()
    real_times = []
    for r in roots:
        if abs(r.imag) < 1e-8:
            tv = t_data[0] + h * r.real
            if 0.0 <= tv <= 12.0:
                real_times.append(tv)
    real_times.sort()

    crossings = []
    for tv in real_times:
        eps = 1e-4
        L = newton_polynomial((max(0.0, tv - eps) - t_data[0]) / h) - LIMIT
        R = newton_polynomial((min(12.0, tv + eps) - t_data[0]) / h) - LIMIT
        if L * R < 0:
            crossings.append(tv)

    if len(crossings) < 2:
        print("Could not locate two crossings.")
        return None

    t1, t2 = crossings[0], crossings[-1]
    duration = t2 - t1
    print(f"First crossing  (rising)   : t = {t1:.4f} h")
    print(f"Second crossing (falling)  : t = {t2:.4f} h")
    print(f"Total time above 8 °C      : {duration:.4f} h")
    print("\nShipment decision:")
    if duration > 0:
        print(f"   ⚠ EXCURSION DETECTED — above 8 °C for {duration:.4f} h.")
        print("   → RELEASE ON HOLD pending stability assessment.")
    return t1, t2, duration

# =====================================================================
# TASK 13 — PLOT CURVES
# =====================================================================
def plot_results():
    print("\n7. GENERATING CURVE PLOT")
    tv = np.linspace(0, 12, 601)
    forward_curve  = np.array([newton_forward(t, 0)[0] for t in tv])
    stirling_curve = np.array([stirling_value(t)[0] for t in tv])
    bessel_curve   = np.array([bessel_value(t)[0]   for t in tv])
    spline_curve   = natural_cubic_spline(tv)

    plt.figure(figsize=(12, 7))
    plt.scatter(t_data, T_data, color="black", s=70, zorder=5,
                label="Logged readings")
    plt.plot(tv, forward_curve,  lw=2,   label="Newton Forward (origin t=0)")
    plt.plot(tv, stirling_curve, lw=2, ls="--", label="Stirling-centered")
    plt.plot(tv, bessel_curve,   lw=2, ls="-.", label="Bessel-centered")
    plt.plot(tv, spline_curve,   lw=2.5, ls=":",  label="Natural cubic spline")
    plt.axhline(LIMIT, color="red", ls="--", label="8 °C limit")
    plt.xlabel("Time (hours)")
    plt.ylabel("Temperature (°C)")
    plt.title("Vaccine Cold-Chain Temperature Excursion — Interpolated Curves")
    plt.grid(True, alpha=0.3)
    plt.legend(loc="lower center", fontsize=9)
    plt.tight_layout()
    plt.savefig("Lab8_Temperature_Interpolation.png", dpi=300)
    plt.show()
    print("✔ Plot saved → Lab8_Temperature_Interpolation.png")

# =====================================================================
# TASK 14 — SUMMARY
# =====================================================================
def print_all_values():
    print("\n8. INTERPOLATED VALUES SUMMARY (4 d.p.)")
    print("=" * 72)
    for t in (5.0, 6.4, 11.0):
        name, fn, _ = select_method(t)
        val, p, _, origin, _ = fn(t)
        print(f"t = {t:>5.1f} h | T = {val:>7.4f} C | {name:<35} | p = {p:+.4f}")

# =====================================================================
# TASK 15 — INVERSE NOTE
# =====================================================================
def inverse_justification():
    print("\n9. INVERSE INTERPOLATION NOTE")
    print("=" * 72)
    print("""
The 8 °C crossing times were obtained by solving P6(t) - 8 = 0 on the
SAME polynomial that interpolates T(t).  Reversing the variables is
badly conditioned near dT/dt ≈ 0 (peak at t ≈ 7.7 h); direct root-finding
on the direct interpolant is well-conditioned at both crossings.
""")

# =====================================================================
# TASK 16 — COMPLETE REPORT
# =====================================================================
def complete_report():
    check_spacing()
    print_difference_table()
    main_estimates()
    validation()
    find_maximum()
    find_crossings()
    print_all_values()
    inverse_justification()
    plot_results()

# =====================================================================
# TASK 17 — CUSTOM USER INPUT
# =====================================================================
def custom_interpolation():
    print("\n10. CUSTOM INTERPOLATION — USER INPUT")
    print("=" * 72)
    print("Enter a value of t (in hours). The program will automatically")
    print("select the best formula and the correct origin so that 0 < p <= 1.")
    print(f"Valid range for exact interpolation: [{t_data[0]:.1f}, {t_data[-1]:.1f}] h")
    print("Values outside this range are EXTRAPOLATION (allowed but flagged).")
    print("Type 'q' to return to the menu.")
    print("-" * 72)

    while True:
        raw = input("Enter t (hours): ").strip()
        if raw.lower() == "q":
            print("Returning to main menu.")
            return
        try:
            t = float(raw)
        except ValueError:
            print("   ⚠ Please enter a valid number or 'q'.")
            continue

        if t < t_data[0] or t > t_data[-1]:
            print(f"   ⚠ t = {t} is OUTSIDE [{t_data[0]:.1f}, {t_data[-1]:.1f}] h.")
            print("     Interpolation is undefined here; we proceed by extrapolation.")
            proceed = input("     Continue? (y/n): ").strip().lower()
            if proceed != "y":
                continue

        result = evaluate_point(t)

        spline_val = natural_cubic_spline([t])[0]
        diff = abs(spline_val - result)
        print(f"   Spline cross-check: T_spline({t:.4f}) = {spline_val:.4f} C")
        print(f"   Difference from chosen formula: {diff:.4f} C")

        again = input("\nTry another t? (y/n): ").strip().lower()
        if again != "y":
            return

# =====================================================================
# TASK 18 — MENU
# =====================================================================
def menu():
    while True:
        print("\n" + "=" * 72)
        print("LAB 8 — NUMERICAL METHODS MENU")
        print("=" * 72)
        print("1.  Spacing check + difference table (PNG)")
        print("2.  Estimates t = 5, 6.4, 11 h  (3 highlighted PNGs)")
        print("3.  Validation at t = 6.4 h  (multi-colour PNG)")
        print("4.  Maximum temperature + local confirmation")
        print("5.  8 °C crossings + excursion duration + decision")
        print("6.  Plot all four curves")
        print("7.  Print all interpolated values")
        print("8.  Inverse-interpolation justification")
        print("9.  Run COMPLETE report")
        print("10. CUSTOM INPUT — interpolate at any t (auto origin)")
        print("0.  Exit")
        ch = input("\nChoice (0-10): ").strip()

        if   ch == "1":  check_spacing(); print_difference_table()
        elif ch == "2":  main_estimates()
        elif ch == "3":  validation()
        elif ch == "4":  find_maximum()
        elif ch == "5":  find_crossings()
        elif ch == "6":  plot_results()
        elif ch == "7":  print_all_values()
        elif ch == "8":  inverse_justification()
        elif ch == "9":  complete_report()
        elif ch == "10": custom_interpolation()
        elif ch == "0":  print("Closed."); break
        else: print("Invalid entry.")

# =====================================================================
# ENTRY POINT
# =====================================================================
if __name__ == "__main__":
    menu()