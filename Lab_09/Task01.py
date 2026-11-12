"""
================================================================================
Lab 09 — Numerical Differentiation using Newton's Forward Interpolation
================================================================================

MAIN MENU:
    1) Lab function   f(x) = x^3 + 2x^2 + x + 1   on [0,1], h = 0.1
    2) Custom values  (user enters x and y points)
    3) Exit

TASK MENU (opens after 1 or 2):
    1) Task 1 — Function table                       (image saved)
    2) Task 2 — Forward difference tables            (saves TWO images: origin 0.0 and 0.1)
    3) Task 3 — f'(0.1): term-by-term, FULL vs TRUNCATED vs EXACT
    4) Task 4 — Exact derivative & % error at x = 0.1
    5) Task 5 — f'(0.0) vs f'(0.1) with accuracy statement
    6) Second derivative at x = 0.1                  (full & truncated)
    7) Third derivative  at x = 0.1                  (full & truncated)
    8) Run ALL tasks (1–7) and save a derivatives-summary image
    9) Back to main menu

Images saved AUTOMATICALLY (no menu option):
    function_table.png
    forward_table_origin_0.0.png   (origin row highlighted in blue)
    forward_table_origin_0.1.png   (origin row highlighted in blue)
    derivatives_summary.png        (derivatives, exact, % errors, truncation reason)
================================================================================
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os


# =============================================================================
# 0. FORMATTER — kills "-0.0000"
# =============================================================================
def fmt(v, dp=4):
    """
    Format v to dp decimals.  Any value whose rounded form is zero is
    printed without a minus sign, so floating-point noise like
    -1.1e-16 or +2e-9 never appears as '-0.0000'.
    """
    s = f"{v:.{dp}f}"
    if s.startswith("-") and float(s) == 0.0:
        s = s[1:]              # strip '-' from '-0.0000'
    return s


# =============================================================================
# 1. DATA BUILDING
# =============================================================================
def build_lab_function():
    """Task 1 — Evaluate f(x) = x³ + 2x² + x + 1 on [0,1] with h = 0.1."""
    h = 0.1
    n = 11
    x = np.array([round(i * h, 10) for i in range(n)])
    y = np.array([xi**3 + 2*xi**2 + xi + 1 for xi in x])
    d1 = lambda t: 3*t**2 + 4*t + 1          # exact f'(x)
    d2 = lambda t: 6*t + 4                   # exact f''(x)
    d3 = lambda t: 6.0                       # exact f'''(x)
    return x, y, h, d1, d2, d3, "f(x) = x³ + 2x² + x + 1"


def build_custom_data():
    """Ask user for equally-spaced (x, y) points."""
    print("\n--- CUSTOM (x, y) DATA ENTRY ---")
    print("Enter comma-separated lists. Example:")
    print("  x = 0.0,0.2,0.4,0.6,0.8,1.0")
    print("  y = 0.0000,0.0456,0.1278,0.3494,0.4027,0.4825")
    try:
        xs = [float(v) for v in input("x values: ").split(",")]
        ys = [float(v) for v in input("y values: ").split(",")]
    except ValueError:
        print("[!] Invalid input — returning to main menu.")
        return None
    if len(xs) != len(ys) or len(xs) < 3:
        print("[!] Need matching lists with at least 3 points.")
        return None
    xs = np.array(xs)
    diffs = np.diff(xs)
    h = diffs[0]
    if not np.allclose(diffs, h, atol=1e-9):
        print(f"[!] x must be equally spaced. Got spacings {diffs}.")
        return None
    return xs, np.array(ys), round(h, 10), None, None, None, "custom data"


# =============================================================================
# 2. FORWARD DIFFERENCE TABLE
# =============================================================================
def forward_table(y):
    """table[k][i] = Δ^k y_i."""
    n = len(y)
    table = [list(y)]
    for k in range(1, n):
        prev = table[-1]
        table.append([prev[i+1] - prev[i] for i in range(len(prev)-1)])
    return table


# =============================================================================
# 3. FORWARD DERIVATIVE SERIES  (Lecture 7, p = 0 form)
# =============================================================================
def forward_derivative_terms(table, h, order):
    """
    List of (label, coefficient, delta_value, term_value) for the forward
    derivative of the given order, read from the ORIGIN ROW (index 0).
    """
    if order == 1:
        coeffs = [1.0]
        for k in range(2, len(table)):
            coeffs.append((1 if k % 2 else -1) / k)
        labels = [f"Δ^{k}y0" if k > 1 else "Δy0"
                  for k in range(1, len(table))]
        scale, start = 1.0 / h, 1
    elif order == 2:
        coeffs = [1.0, -1.0, 11/12, -5/6, 137/180, -7/10]
        labels = [f"Δ^{k}y0" for k in range(2, 2 + len(coeffs))]
        scale, start = 1.0 / h**2, 2
    elif order == 3:
        coeffs = [1.0, -1.5, 1.75, -1.875, 2.0]
        labels = [f"Δ^{k}y0" for k in range(3, 3 + len(coeffs))]
        scale, start = 1.0 / h**3, 3
    else:
        raise ValueError("order must be 1, 2 or 3")

    terms = []
    for idx, k in enumerate(range(start, len(table))):
        if idx >= len(coeffs):
            break
        dval = table[k][0]
        term = scale * coeffs[idx] * dval
        terms.append((labels[idx], coeffs[idx], dval, term))
        if abs(dval) < 1e-14 and k > start:
            break
    return terms


def general_p_forward_terms(table, h, order, p):
    """General-p forward coefficients (used when the origin is shifted)."""
    terms = []
    if order == 1:
        for k in range(1, len(table)):
            dval = table[k][0]
            if k == 1:   co = 1.0
            elif k == 2: co = (2*p - 1) / 2
            elif k == 3: co = (3*p*p - 6*p + 2) / 6
            elif k == 4: co = (4*p**3 - 18*p*p + 22*p - 6) / 24
            else:        co = 0.0
            tv = (1.0 / h) * co * dval
            terms.append((f"Δ^{k}y0", co, dval, tv))
            if abs(dval) < 1e-14 and k > 2:
                break
    elif order == 2:
        for k in range(2, len(table)):
            dval = table[k][0]
            if k == 2:   co = 1.0
            elif k == 3: co = p - 1.0
            elif k == 4: co = (6*p*p - 18*p + 11) / 12
            else:        co = 0.0
            tv = (1.0 / h**2) * co * dval
            terms.append((f"Δ^{k}y0", co, dval, tv))
            if abs(dval) < 1e-14 and k > 3:
                break
    else:  # order 3
        for k in range(3, len(table)):
            dval = table[k][0]
            if k == 3:   co = 1.0
            elif k == 4: co = p - 1.5
            elif k == 5: co = (3*p*p - 9*p + 7) / 4
            else:        co = 0.0
            tv = (1.0 / h**3) * co * dval
            terms.append((f"Δ^{k}y0", co, dval, tv))
            if abs(dval) < 1e-14 and k > 4:
                break
    return terms


# =============================================================================
# 4. TEXT DISPLAY HELPERS
# =============================================================================
def print_function_table(x, y, h):
    print("\n" + "=" * 74)
    print(" TASK 1 — FUNCTION TABLE  (uniform grid, h = %.4f)" % h)
    print("=" * 74)
    print(f"{'i':>3} {'x_i':>10} {'f(x_i)':>14}")
    print("-" * 74)
    for i, (xi, yi) in enumerate(zip(x, y)):
        print(f"{i:>3} {fmt(xi):>10} {fmt(yi):>14}")
    print("-" * 74)
    print(f"  {len(x)} equally-spaced points — consecutive x differ by "
          f"h = {h:.4f}.")


def print_forward_table(x, table):
    n = len(x)
    print("\n" + "=" * 74)
    print(" TASK 2 — FORWARD DIFFERENCE TABLE")
    print("=" * 74)
    header = f"{'x':>6} {'f(x)':>12}"
    for k in range(1, n):
        header += f" {'Δ^' + str(k):>10}"
    print(header)
    print("-" * len(header))
    for i in range(n):
        row = f"{x[i]:>6.2f} {fmt(table[0][i]):>12}"
        for k in range(1, n):
            if i < len(table[k]):
                row += f" {fmt(table[k][i]):>10}"
            else:
                row += f" {'':>10}"
        print(row)
    print("-" * len(header))
    for k in range(1, n):
        vals = table[k]
        if len(vals) >= 2 and all(abs(v - vals[0]) < 1e-9 for v in vals):
            print(f"\n  Δ^{k} is CONSTANT  ( = {fmt(vals[0])})")
            if k + 1 < n:
                print(f"  Δ^{k+1} and all higher orders are ZERO.")
            print(f"  → the data is a polynomial of degree {k}.")
            return k
    print("\n  No constant order found within the table.")
    return None


def show_derivative_series(title, terms, exact, symbol, truncation_reason):
    print("\n" + "=" * 74)
    print(" " + title)
    print("=" * 74)
    print(f"{'Term':<12}{'Coefficient':>14}{'Δ-value':>14}"
          f"{'Term value':>16}{'Running':>16}")
    print("-" * 74)
    running = 0.0
    running_list = []
    for lab, co, dv, tv in terms:
        running += tv
        running_list.append(running)
        print(f"{lab:<12}{co:>14.4f}{fmt(dv):>14}{tv:>16.6f}{running:>16.6f}")
    print("-" * 74)

    full = running
    trunc = running_list[-2] if len(running_list) >= 2 else full
    last_label = terms[-1][0] if len(terms) >= 2 else "—"

    print(f"FULL SERIES   {symbol} = {full:.6f}   (all {len(terms)} term(s))")
    if len(terms) >= 2:
        print(f"TRUNCATED     {symbol} = {trunc:.6f}   "
              f"(kept {len(terms)-1} term(s), dropped '{last_label}')")
        print(f"Truncation order: stopped after the term just BEFORE "
              f"'{last_label}'.")
        print(f"Reason: {truncation_reason}")
        print(f"Δ (full − truncated) = {full - trunc:.6e}")

    if exact is not None:
        err_full = abs(full - exact) / abs(exact) * 100 if exact else float("nan")
        err_tr = abs(trunc - exact) / abs(exact) * 100 if exact else float("nan")
        print(f"\nEXACT         {symbol} = {exact:.6f}")
        print(f"FULL-SERIES       % error = {err_full:.6e} %")
        print(f"TRUNCATED-SERIES  % error = {err_tr:.6e} %")
        print(f"Error introduced by dropping last term = "
              f"{abs(err_tr - err_full):.6e} %")
    else:
        err_full = err_tr = None
        print("\nEXACT value unavailable (custom data).")
    print("=" * 74)

    return {
        "symbol": symbol, "full": full, "trunc": trunc, "exact": exact,
        "err_full": err_full, "err_tr": err_tr, "terms": terms,
        "truncation_reason": truncation_reason,
    }


# =============================================================================
# 5. IMAGE — FUNCTION TABLE
# =============================================================================
def save_function_table_image(x, y, h, label, filename="function_table.png"):
    n = len(x)
    fig, ax = plt.subplots(figsize=(6, max(4, n * 0.4)))
    ax.axis("off")

    ax.text(0.25, 1.02, "i", ha="center", va="center",
            fontsize=10, fontweight="bold")
    ax.text(0.55, 1.02, "x_i", ha="center", va="center",
            fontsize=10, fontweight="bold")
    ax.text(0.85, 1.02, "f(x_i)", ha="center", va="center",
            fontsize=10, fontweight="bold")
    ax.plot([0.05, 0.95], [1.0, 1.0], color="black", lw=1)

    for i, (xi, yi) in enumerate(zip(x, y)):
        yy = 0.98 - i * (0.95 / n)
        if i % 2 == 0:
            ax.add_patch(mpatches.Rectangle((0.05, yy - 0.02), 0.9, 0.04,
                                            facecolor="#f5f5f5",
                                            edgecolor="none", zorder=0))
        ax.text(0.25, yy, f"{i}", ha="center", va="center", fontsize=9)
        ax.text(0.55, yy, fmt(xi), ha="center", va="center", fontsize=9)
        ax.text(0.85, yy, fmt(yi), ha="center", va="center", fontsize=9)

    ax.set_title(f"Function Table — {label}\n"
                 f"(h = {h:.4f}, {n} equally-spaced points)",
                 fontsize=11, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[INFO] Function-table image saved: {os.path.abspath(filename)}")


# =============================================================================
# 6. IMAGE — FORWARD DIFFERENCE TABLE (origin highlighted, no -0.0000)
# =============================================================================
def save_forward_image(x, table, origin_idx, filename):
    """
    Highlighted forward-difference table:
      - constant order   → orange
      - zero higher rows → green
      - ORIGIN row       → blue  (with '← ORIGIN' tag)
    """
    n = len(x)
    ncols = 2 + (n - 1)
    nrows = n

    fig, ax = plt.subplots(figsize=(max(13, ncols * 1.5),
                                    max(5, nrows * 0.6)))
    ax.set_xlim(0, ncols)
    ax.set_ylim(0, nrows + 1)
    ax.axis("off")

    const_k = None
    for k in range(1, n):
        vals = table[k]
        if len(vals) >= 2 and all(abs(v - vals[0]) < 1e-9 for v in vals):
            const_k = k
            break

    headers = ["x", "f(x)"] + [f"Δ^{k}" for k in range(1, n)]
    for j, htxt in enumerate(headers):
        ax.add_patch(mpatches.Rectangle((j, nrows), 1, 1,
                                        facecolor="#1f3a5f",
                                        edgecolor="white"))
        ax.text(j + 0.5, nrows + 0.5, htxt, ha="center", va="center",
                color="white", fontsize=9, fontweight="bold")

    for i in range(n):
        is_origin = (i == origin_idx)

        x_face = "#9ec5e8" if is_origin else "#f0f0f0"
        ax.add_patch(mpatches.Rectangle((0, nrows - 1 - i), 1, 1,
                                        facecolor=x_face, edgecolor="white"))
        ax.text(0.5, nrows - 1 - i + 0.5, fmt(x[i]),
                ha="center", va="center", fontsize=8,
                fontweight="bold" if is_origin else "normal")

        f_face = ("#9ec5e8" if is_origin else
                  ("#ffffff" if i % 2 == 0 else "#f7f7f7"))
        ax.add_patch(mpatches.Rectangle((1, nrows - 1 - i), 1, 1,
                                        facecolor=f_face, edgecolor="white"))
        ax.text(1.5, nrows - 1 - i + 0.5, fmt(table[0][i]),
                ha="center", va="center", fontsize=8,
                fontweight="bold" if is_origin else "normal")

        for k in range(1, n):
            col = k + 1
            if i < len(table[k]):
                val = table[k][i]
                if is_origin:
                    face = "#9ec5e8"
                elif const_k is not None and k == const_k:
                    face = "#fce5cd"
                elif const_k is not None and k > const_k and abs(val) < 1e-9:
                    face = "#d9ead3"
                else:
                    face = "#ffffff" if i % 2 == 0 else "#f7f7f7"
                ax.add_patch(mpatches.Rectangle((col, nrows - 1 - i), 1, 1,
                                                facecolor=face,
                                                edgecolor="white"))
                ax.text(col + 0.5, nrows - 1 - i + 0.5, fmt(val),
                        ha="center", va="center", fontsize=8,
                        fontweight="bold" if is_origin else "normal")

        if is_origin:
            ax.text(ncols + 0.1, nrows - 1 - i + 0.5, "← ORIGIN",
                    ha="left", va="center", fontsize=9,
                    color="#1f3a5f", fontweight="bold")

    ax.legend(handles=[
        mpatches.Patch(facecolor="#9ec5e8", edgecolor="gray",
                       label="origin row"),
        mpatches.Patch(facecolor="#fce5cd", edgecolor="gray",
                       label="constant Δ"),
        mpatches.Patch(facecolor="#d9ead3", edgecolor="gray",
                       label="zero higher"),
    ], loc="upper right", bbox_to_anchor=(1.0, 1.05), fontsize=8)

    ax.set_title(f"Forward Difference Table (origin highlighted: x = {x[origin_idx]:.1f})",
                 fontsize=12, fontweight="bold", pad=10)
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[INFO] Difference-table image saved: {os.path.abspath(filename)}")


# =============================================================================
# 7. IMAGE — DERIVATIVES SUMMARY (derivatives + exact + % errors)
# =============================================================================
def save_summary_image(reports, filename="derivatives_summary.png"):
    n = len(reports)
    fig, ax = plt.subplots(figsize=(14, max(3, 0.75 * n + 1.5)))
    ax.axis("off")

    headers = ["Derivative", "FULL", "TRUNCATED", "EXACT",
               "% err (full)", "% err (trunc)", "Truncation order & reason"]
    col_x = [0.03, 0.13, 0.25, 0.39, 0.52, 0.65, 0.78]

    for hx, htxt in zip(col_x, headers):
        ax.text(hx, 0.95, htxt, fontsize=9, fontweight="bold",
                ha="left", va="center")
    ax.plot([0.02, 0.98], [0.92, 0.92], color="black", lw=1)

    for i, rep in enumerate(reports):
        y = 0.88 - i * (0.85 / max(n, 1))
        ax.text(col_x[0], y, rep["symbol"], fontsize=9,
                ha="left", va="center")
        ax.text(col_x[1], y, f"{rep['full']:.6f}", fontsize=9,
                ha="left", va="center")
        ax.text(col_x[2], y, f"{rep['trunc']:.6f}", fontsize=9,
                ha="left", va="center")
        ax.text(col_x[3], y,
                f"{rep['exact']:.6f}" if rep["exact"] is not None else "N/A",
                fontsize=9, ha="left", va="center")
        ax.text(col_x[4], y,
                f"{rep['err_full']:.4e}" if rep["err_full"] is not None else "N/A",
                fontsize=9, ha="left", va="center")
        ax.text(col_x[5], y,
                f"{rep['err_tr']:.4e}" if rep["err_tr"] is not None else "N/A",
                fontsize=9, ha="left", va="center")
        ax.text(col_x[6], y, rep["truncation_reason"], fontsize=8,
                ha="left", va="center", wrap=True)

    ax.set_title("Newton's Forward Differentiation — Summary",
                 fontsize=12, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[INFO] Summary image saved: {os.path.abspath(filename)}")


# =============================================================================
# 8. TASK ROUTINES
# =============================================================================
def task_function_table(x, y, h, label):
    print_function_table(x, y, h)
    save_function_table_image(x, y, h, label)


def task_difference_table(x, y, h, label):
    table = forward_table(y)
    print_forward_table(x, table)
    # Generate two images for the two origins used in this lab
    save_forward_image(x, table, origin_idx=0, filename="forward_table_origin_0.0.png")
    save_forward_image(x, table, origin_idx=1, filename="forward_table_origin_0.1.png")
    return table


def _derive_terms_at(x, y, h, xp, order):
    idx = 0
    for i in range(len(x) - 1):
        if x[i] <= xp <= x[i + 1]:
            idx = i
            break
    p = (xp - x[idx]) / h
    local_table = forward_table(y[idx:])
    if abs(p) < 1e-12:
        terms = forward_derivative_terms(local_table, h, order)
    else:
        terms = general_p_forward_terms(local_table, h, order, p)
    return terms, idx, p


def _truncation_reason(table, order, xp, h):
    n = len(table)
    zero_from = None
    for k in range(order + 1, n):
        vals = table[k]
        if len(vals) >= 1 and all(abs(v) < 1e-12 for v in vals):
            zero_from = k
            break
    if zero_from is not None:
        return (f"truncated after Δ^{zero_from-1}: Δ^{zero_from} and every "
                f"higher difference are zero for this data → the series "
                f"terminates exactly.")
    return (f"truncated after the last available nonzero term; remaining "
            f"terms are below numerical precision at h = {h:.4f}.")


def task_derivative(x, y, h, order, exact_func, symbol, label, xp):
    terms, idx, p = _derive_terms_at(x, y, h, xp, order)
    local_table = forward_table(y[idx:])
    reason = _truncation_reason(local_table, order, xp, h)

    exact = exact_func(xp) if exact_func is not None else None
    title = (f"FORWARD {['','FIRST','SECOND','THIRD'][order]} DERIVATIVE "
             f"at x = {xp:.4f}   (origin x0 = {x[idx]:.4f}, p = {p:.4f})"
             f"\n[data: {label}]")
    return show_derivative_series(title, terms, exact, symbol, reason)


def task_comparison(x, y, h, d1, label):
    print("\n" + "=" * 74)
    print(" TASK 5 — f'(0.0) vs f'(0.1) — SAME FORMULA, SAME TABLE")
    print("=" * 74)

    r0 = task_derivative(x, y, h, 1, d1, "f'(0.0)", label, xp=0.0)
    r1 = task_derivative(x, y, h, 1, d1, "f'(0.1)", label, xp=0.1)

    print("\n--- ACCURACY COMPARISON ---")
    print(f"{'Position':<12}{'TRUNCATED':>14}{'EXACT':>14}"
          f"{'% err (trunc)':>16}")
    print("-" * 60)
    for sym, rep in (("x = 0.0", r0), ("x = 0.1", r1)):
        ex = rep["exact"] if rep["exact"] is not None else float("nan")
        er = rep["err_tr"] if rep["err_tr"] is not None else float("nan")
        print(f"{sym:<12}{rep['trunc']:>14.6f}{ex:>14.6f}{er:>16.6e}")

    if d1 is not None:
        same = abs(r0["err_tr"] - r1["err_tr"]) < 1e-6
        answer = ("YES — both positions give essentially the SAME accuracy."
                  if same else
                  "NO — the two positions differ in accuracy; see the errors above.")
        print(f"\n  Do the two positions give the same accuracy?  {answer}")
        print("  Reason: the forward series terminates at Δ³ for this cubic;")
        print("  any residual comes only from the 4-decimal rounding of the")
        print("  function table, not from the formula or the origin choice.")
    else:
        print("\n  Exact derivative unavailable for custom data — "
              "accuracy statement skipped.")
    print("=" * 74)

    return [r0, r1]


def run_all_tasks(x, y, h, d1, d2, d3, label):
    task_function_table(x, y, h, label)
    task_difference_table(x, y, h, label)

    r1_d1 = task_derivative(x, y, h, 1, d1, "f'(0.1)",  label, xp=0.1)
    r1_d2 = task_derivative(x, y, h, 2, d2, "f''(0.1)", label, xp=0.1)
    r1_d3 = task_derivative(x, y, h, 3, d3, "f'''(0.1)", label, xp=0.1)

    r0_d1, r1_d1_again = task_comparison(x, y, h, d1, label)

    save_summary_image([r1_d1, r1_d2, r1_d3, r0_d1, r1_d1_again])


# =============================================================================
# 9. TASK MENU
# =============================================================================
def task_menu(x, y, h, d1, d2, d3, label):
    while True:
        print("\n" + "=" * 74)
        print(f" TASK MENU  —  data: {label}   ({len(x)} points, h = {h})")
        print("=" * 74)
        print("  1) Task 1 — Function table                  (image saved)")
        print("  2) Task 2 — Forward difference table        (origin 0.0 and 0.1 highlighted, images saved)")
        print("  3) Task 3 — f'(0.1): FULL vs TRUNCATED vs EXACT, term-by-term")
        print("  4) Task 4 — Exact derivative & % error at x = 0.1")
        print("  5) Task 5 — f'(0.0) vs f'(0.1) with accuracy statement")
        print("  6) Second derivative at x = 0.1             (full & truncated)")
        print("  7) Third derivative  at x = 0.1             (full & truncated)")
        print("  8) Run ALL tasks 1–7 (summary image saved)")
        print("  9) Back to main menu")
        print("=" * 74)
        c = input("Choice: ").strip()

        if c == "1":
            task_function_table(x, y, h, label)
        elif c == "2":
            task_difference_table(x, y, h, label)
        elif c == "3":
            task_derivative(x, y, h, 1, d1, "f'(0.1)", label, xp=0.1)
        elif c == "4":
            if d1 is None:
                print("\n[!] Exact derivative unavailable for custom data.")
            task_derivative(x, y, h, 1, d1, "f'(0.1)", label, xp=0.1)
        elif c == "5":
            task_comparison(x, y, h, d1, label)
        elif c == "6":
            task_derivative(x, y, h, 2, d2, "f''(0.1)", label, xp=0.1)
        elif c == "7":
            task_derivative(x, y, h, 3, d3, "f'''(0.1)", label, xp=0.1)
        elif c == "8":
            run_all_tasks(x, y, h, d1, d2, d3, label)
        elif c == "9":
            return
        else:
            print("[!] Invalid choice.")


# =============================================================================
# 10. MAIN MENU
# =============================================================================
def main():
    print("=" * 74)
    print("  LAB 09 — NEWTON'S FORWARD DIFFERENTIATION")
    print("=" * 74)
    while True:
        print("\n" + "=" * 74)
        print("  MAIN MENU")
        print("=" * 74)
        print("  1) Lab function   f(x) = x³ + 2x² + x + 1   on [0,1], h = 0.1")
        print("  2) Custom values  (enter x and y points)")
        print("  3) Exit")
        print("=" * 74)
        choice = input("Choice: ").strip()

        if choice == "1":
            x, y, h, d1, d2, d3, label = build_lab_function()
            print(f"\n[INFO] Lab function loaded: {len(x)} points, h = {h}")
            task_menu(x, y, h, d1, d2, d3, label)
        elif choice == "2":
            res = build_custom_data()
            if res is None:
                continue
            x, y, h, d1, d2, d3, label = res
            print(f"[INFO] Custom data loaded: {len(x)} points, h = {h}")
            task_menu(x, y, h, d1, d2, d3, label)
        elif choice == "3":
            print("\nExiting. Goodbye!")
            break
        else:
            print("[!] Invalid choice — enter 1, 2 or 3.")


if __name__ == "__main__":
    main()