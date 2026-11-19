"""
Lab 10 — Numerical Differentiation: Speed vs Time
==================================================
Full implementation:
  • 12 evenly-spaced data points (Speed vs Time)
  • Newton Forward, Newton Backward, Stirling Central formulas
  • Correct Stirling μδ³ formula
  • Forward/Backward difference tables saved as PNG (gold origin + pink diagonal)
  • ★ Stirling central difference table saved as PNG (gold origin + green neighbour
    + pink centered differences used in formula)
  • Comparison table printed AND saved as PNG (best method highlighted green)
  • Derivative bar charts + swept derivative comparison plots
  • Interactive loop re-prompts for xp
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from tabulate import tabulate
import os

np.random.seed(42)
os.makedirs("output", exist_ok=True)

# ============================================================
# 0. DATA  (12 evenly-spaced points)
# ============================================================
N_POINTS = 12
t = np.linspace(0.0, 5.5, N_POINTS)
h = t[1] - t[0]

# --- TRUE functions (vectorized) ---
def true_speed(x):
    x = np.asarray(x, dtype=float)
    return 3*x**2 - 2*x + 5

def true_d1(x):
    x = np.asarray(x, dtype=float)
    return 6*x - 2

def true_d2(x):
    x = np.asarray(x, dtype=float)
    return np.full_like(x, 6.0)

speed = true_speed(t) + np.random.normal(0, 0.02, N_POINTS)

# ============================================================
# 1. DIFFERENCE TABLE BUILDERS
# ============================================================
def build_forward_difference_table(y):
    n = len(y)
    T = np.zeros((n, n))
    T[:, 0] = y
    for j in range(1, n):
        for i in range(n - j):
            T[i, j] = T[i+1, j-1] - T[i, j-1]
    return T

def build_backward_difference_table(y):
    n = len(y)
    T = np.zeros((n, n))
    T[:, 0] = y
    for j in range(1, n):
        for i in range(j, n):
            T[i, j] = T[i, j-1] - T[i-1, j-1]
    return T

# ============================================================
# 2. DERIVATIVE FORMULAS
# ============================================================
def newton_forward_derivatives(xp, x, y):
    """Forward at start of sub-table; needs 0 <= p < 1."""
    h_ = x[1] - x[0]
    p = (xp - x[0]) / h_
    if not (0 <= p < 1 + 1e-9):
        raise ValueError(f"Forward needs 0<=p<1, got p={p:.4f}")
    D = build_forward_difference_table(y)
    d1 = D[0, 1] + (2*p-1)/2*D[0, 2] \
       + (3*p**2-6*p+2)/6*D[0, 3] \
       + (2*p**3-9*p**2+11*p-3)/12*D[0, 4]
    d1 /= h_
    d2 = D[0, 2] + (p-1)*D[0, 3] \
       + (6*p**2-18*p+11)/12*D[0, 4]
    d2 /= h_**2
    return d1, d2


def newton_backward_derivatives(xp, x, y):
    """Backward at end of sub-table; needs -1 < p <= 0."""
    h_ = x[1] - x[0]
    p = (xp - x[-1]) / h_
    if not (-1 - 1e-9 < p <= 0):
        raise ValueError(f"Backward needs -1<p<=0, got p={p:.4f}")
    D = build_backward_difference_table(y)
    n = len(y) - 1
    d1 = D[n, 1] + (2*p+1)/2*D[n, 2] \
       + (3*p**2+6*p+2)/6*D[n, 3] \
       + (2*p**3+9*p**2+11*p+3)/12*D[n, 4]
    d1 /= h_
    d2 = D[n, 2] + (p+1)*D[n, 3] \
       + (6*p**2+18*p+11)/12*D[n, 4]
    d2 /= h_**2
    return d1, d2


def stirling_derivatives(xp, x, y):
    """
    TRUE Stirling central-difference formula.

    Let i0 be nearest node, p = (xp - x[i0]) / h.

    Centered differences:
        δ²y_i      = y[i+1] - 2y[i] + y[i-1]
        δ⁴y_i      = δ²y_{i+1} - 2δ²y_i + δ²y_{i-1}
        δ³y_{i-½}  = δ²y_i - δ²y_{i-1}
        μδ²y_{i0}  = (δ²y_{i0} + δ²y_{i0+1}) / 2
        μδ³y_{i0}  = (δ³y_{i0-½} + δ³y_{i0+½}) / 2

    Stirling formulas:
        f'(xp)  = (1/h) [ δy_{i0-½} + p·μδ²y_{i0}
                          + (p²-¼)/6 · δ³y_{i0-½}
                          + p(p²-1)/12 · δ⁴y_{i0} ]
        f''(xp) = (1/h²)[ δ²y_{i0} + p·μδ³y_{i0}
                          + (p²-1/12) · δ⁴y_{i0} ]
    """
    n = len(x)
    h_ = x[1] - x[0]
    i0 = int(np.argmin(np.abs(np.asarray(x) - xp)))
    i0 = max(1, min(i0, n - 3))
    p = (xp - x[i0]) / h_

    d2 = np.full(n, np.nan)
    for k in range(1, n - 1):
        d2[k] = y[k+1] - 2*y[k] + y[k-1]

    d4 = np.full(n, np.nan)
    for k in range(2, n - 2):
        d4[k] = d2[k+1] - 2*d2[k] + d2[k-1]

    dy_half   = y[i0] - y[i0-1]
    d3_half   = d2[i0] - d2[i0-1]
    d3_half_p = d2[i0+1] - d2[i0] if i0+1 <= n-2 else d3_half

    mu_d2 = (d2[i0] + d2[i0+1]) / 2
    mu_d3 = (d3_half + d3_half_p) / 2

    if not np.isnan(d4[i0]):
        d4_c = d4[i0]
    elif not np.isnan(d4[i0-1]):
        d4_c = d4[i0-1]
    else:
        d4_c = 0.0

    d1 = dy_half + p*mu_d2 + (p**2 - 0.25)/6 * d3_half \
         + p*(p**2 - 1)/12 * d4_c
    d1 /= h_

    d2_val = d2[i0] + p*mu_d3 + (p**2 - 1/12) * d4_c
    d2_val /= h_**2

    return d1, d2_val


# ============================================================
# 3. SELECTOR + ALL-METHOD COMPUTE
# ============================================================
def choose_formula(xp, x_data):
    n = len(x_data)
    h_ = x_data[1] - x_data[0]
    p_fwd = (xp - x_data[0]) / h_
    p_bwd = (xp - x_data[-1]) / h_
    if 0 <= p_fwd < 1:
        return "Newton Forward", 0, p_fwd
    elif -1 < p_bwd <= 0:
        return "Newton Backward", n - 1, p_bwd
    idx = int(np.argmin(np.abs(np.asarray(x_data) - xp)))
    return "Stirling Central", idx, (xp - x_data[idx]) / h_


def compute_all_methods(xp, x, y):
    n = len(x)
    h_ = x[1] - x[0]
    i_floor = int(np.floor((xp - x[0]) / h_))
    i_floor = max(0, min(i_floor, n - 2))

    results = {}

    # FORWARD
    try:
        lo = i_floor
        hi = min(lo + 5, n - 1)
        results["Newton Forward"] = newton_forward_derivatives(
            xp, x[lo:hi+1], y[lo:hi+1])
    except Exception:
        results["Newton Forward"] = (np.nan, np.nan)

    # BACKWARD
    try:
        hi = i_floor + 1
        lo = max(0, hi - 5)
        results["Newton Backward"] = newton_backward_derivatives(
            xp, x[lo:hi+1], y[lo:hi+1])
    except Exception:
        results["Newton Backward"] = (np.nan, np.nan)

    # STIRLING
    try:
        results["Stirling Central"] = stirling_derivatives(xp, x, y)
    except Exception:
        results["Stirling Central"] = (np.nan, np.nan)

    return results


# ============================================================
# 4. COMPARISON TABLE
# ============================================================
REASONS = {
    "Newton Forward":  "Best near start (0<p<1); top diagonal used",
    "Newton Backward": "Best near end (-1<p<0); bottom diagonal used",
    "Stirling Central":"Best for interior points; symmetric differences",
}

def build_comparison_rows(results, d1_true, d2_true):
    rows = []
    for meth, (d1, d2) in results.items():
        if np.isnan(d1) or np.isnan(d2):
            rows.append(dict(method=meth, d1="N/A", e1=np.inf,
                             d2="N/A", e2=np.inf,
                             reason=REASONS[meth], combined=np.inf))
            continue
        e1 = abs(d1 - d1_true); e2 = abs(d2 - d2_true)
        rows.append(dict(method=meth, d1=f"{d1:.6f}", e1=e1,
                         d2=f"{d2:.6f}", e2=e2,
                         reason=REASONS[meth], combined=e1+e2))
    return sorted(rows, key=lambda r: r["combined"])


def print_comparison_table(rows, d1_true, d2_true, xp):
    best = rows[0]["method"]
    headers = ["Method", "v'(xp) [m/s²]", "|Err 1| [m/s²]",
               "v''(xp) [m/s³]", "|Err 2| [m/s³]",
               "Why chosen / suitability", "Combined |Err|"]
    display = []
    for r in rows:
        mark = " ★ BEST" if r["method"] == best else ""
        e1 = f"{r['e1']:.3e}" if np.isfinite(r["e1"]) else "N/A"
        e2 = f"{r['e2']:.3e}" if np.isfinite(r["e2"]) else "N/A"
        cb = f"{r['combined']:.3e}" if np.isfinite(r["combined"]) else "N/A"
        display.append([r["method"]+mark, r["d1"], e1,
                        r["d2"], e2, r["reason"], cb])
    print("\n" + "=" * 90)
    print(f"METHOD COMPARISON TABLE  (xp = {xp:.4f} s)")
    print("=" * 90)
    print(tabulate(display, headers=headers, tablefmt="grid"))
    print(f"\nTrue reference:  v'({xp}) = {d1_true:.6f} m/s²,"
          f"  v''({xp}) = {d2_true:.6f} m/s³")
    print(f"\n★ BEST METHOD for xp = {xp:.4f} s  →  {best}")
    print("=" * 90)
    return best


def save_comparison_table_image(rows, d1_true, d2_true, xp, filename):
    best = rows[0]["method"]
    headers = ["Method", "v'(xp)\n[m/s²]", "|Err 1|\n[m/s²]",
               "v''(xp)\n[m/s³]", "|Err 2|\n[m/s³]",
               "Why chosen / suitability", "Combined\n|Err|"]
    cw = [0.16, 0.10, 0.10, 0.10, 0.10, 0.32, 0.12]
    fig_w = 16.0
    fig_h = max(3.0, (len(rows) + 1) * 0.11 * fig_w / 6 + 1.0)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    top_y, header_h = 0.94, 0.10
    ax.text(0.5, 0.99, f"Method Comparison Table  —  xp = {xp:.4f} s",
            ha="center", va="top", fontsize=15, fontweight="bold")

    xc = 0.01
    for j, htxt in enumerate(headers):
        w = cw[j]
        ax.add_patch(plt.Rectangle((xc, top_y-header_h), w, header_h,
                                   facecolor="#1F3A5F", edgecolor="white",
                                   transform=ax.transAxes))
        ax.text(xc+w/2, top_y-header_h/2, htxt,
                ha="center", va="center", color="white",
                fontsize=9, fontweight="bold")
        xc += w

    body_h = (top_y - header_h - 0.06) / len(rows)
    yt = top_y - header_h
    for i, r in enumerate(rows):
        is_best = (r["method"] == best)
        fc = "#D4F5D4" if is_best else ("#F7F7F7" if i % 2 else "white")
        bc = "#2E7D32" if is_best else "#CCCCCC"
        lw = 2.0 if is_best else 0.5
        cells = [
            r["method"] + ("  ★ BEST" if is_best else ""),
            r["d1"],
            f"{r['e1']:.3e}" if np.isfinite(r["e1"]) else "N/A",
            r["d2"],
            f"{r['e2']:.3e}" if np.isfinite(r["e2"]) else "N/A",
            r["reason"],
            f"{r['combined']:.3e}" if np.isfinite(r["combined"]) else "N/A",
        ]
        xc = 0.01
        for j, val in enumerate(cells):
            w = cw[j]
            ax.add_patch(plt.Rectangle((xc, yt-body_h), w, body_h,
                                       facecolor=fc, edgecolor=bc, lw=lw,
                                       transform=ax.transAxes))
            ax.text(xc+w/2, yt-body_h/2, val,
                    ha="center", va="center", fontsize=8.5,
                    fontweight="bold" if (is_best and j == 0) else "normal",
                    color="#1B5E20" if is_best else "black")
            xc += w
        yt -= body_h

    ax.text(0.5, yt - 0.02,
            f"True reference:  v'(xp) = {d1_true:.6f} m/s²,   "
            f"v''(xp) = {d2_true:.6f} m/s³      |      "
            f"★ Best = lowest combined absolute error",
            ha="center", va="top", fontsize=10, fontweight="bold",
            color="#1B5E20")
    plt.savefig(filename, dpi=170, bbox_inches="tight")
    plt.close()
    print(f"[saved] {filename}")


# ============================================================
# 5. DIFFERENCE TABLE IMAGES
# ============================================================
def plot_difference_table(x, y, mode, highlight_row, xp, filename):
    """Forward or Backward difference table image."""
    n = len(y)
    table = build_forward_difference_table(y) if mode == "forward" \
            else build_backward_difference_table(y)
    op = "Δ" if mode == "forward" else "∇"

    n_rows, n_cols = n+1, n+1
    fig, ax = plt.subplots(figsize=(max(14, n_cols*1.1),
                                     max(4, n_rows*0.55+1.5)))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    row_h = 1.0/n_rows; col_w = 1.0/n_cols

    headers = ["x (s)", "f(x)"] + [f"{op}{k}" for k in range(1, n)]
    for j, txt in enumerate(headers):
        ax.add_patch(plt.Rectangle((j*col_w, 1-row_h), col_w, row_h,
                                   facecolor="#1F3A5F", edgecolor="white"))
        ax.text(j*col_w+col_w/2, 1-row_h/2, txt,
                ha="center", va="center", color="white",
                fontsize=9, fontweight="bold")

    for i in range(n):
        y0 = 1 - (i+2)*row_h
        ax.add_patch(plt.Rectangle((0, y0), col_w, row_h,
                                   facecolor="#EFEFEF", edgecolor="gray", lw=0.6))
        ax.text(col_w/2, y0+row_h/2, f"{x[i]:.3f}",
                ha="center", va="center", fontsize=8, fontweight="bold")

        fc_fx = "#FFD700" if i == highlight_row else "white"
        ax.add_patch(plt.Rectangle((col_w, y0), col_w, row_h,
                                   facecolor=fc_fx, edgecolor="gray", lw=0.6))
        ax.text(col_w+col_w/2, y0+row_h/2, f"{y[i]:.6f}",
                ha="center", va="center", fontsize=7.5)

        for j in range(1, n):
            if mode == "forward":
                val = table[i, j] if i < n-j else None
            else:
                val = table[i, j] if i >= j else None
            if val is None:
                continue
            if mode == "forward":
                fc = "#FFB6C1" if i == 0 else ("#AEE7FF" if i == highlight_row else "white")
            else:
                fc = "#FFB6C1" if i == n-1 else ("#AEE7FF" if i == highlight_row else "white")
            ax.add_patch(plt.Rectangle(((j+1)*col_w, y0), col_w, row_h,
                                       facecolor=fc, edgecolor="gray", lw=0.6))
            ax.text((j+1)*col_w+col_w/2, y0+row_h/2, f"{val:.6f}",
                    ha="center", va="center", fontsize=7.5)

    ax.set_title(f"Newton {mode.capitalize()} Difference Table (xp = {xp:.3f} s)",
                 fontsize=13, fontweight="bold", pad=15)
    ax.legend(handles=[
        mpatches.Patch(color="#FFD700", label="Origin row"),
        mpatches.Patch(color="#FFB6C1", label="Diagonal values used"),
        mpatches.Patch(color="#AEE7FF", label="Row nearest to xp"),
        mpatches.Patch(color="#EFEFEF", label="x values"),
    ], loc="upper center", bbox_to_anchor=(0.5, 0.02), ncol=4,
       fontsize=8, frameon=False)
    plt.tight_layout()
    plt.savefig(filename, dpi=170, bbox_inches="tight")
    plt.close()
    print(f"[saved] {filename}")


def plot_stirling_table(x, y, xp, filename):
    """
    Stirling central difference table image.
    Highlights:
      • Gold       = nearest node to xp (origin i0)
      • Light-green = symmetric neighbour row (i0-1)
      • Pink       = centered differences δ², δ³, δ⁴ used in Stirling formula
    """
    n = len(y)
    i0 = int(np.argmin(np.abs(np.asarray(x) - xp)))
    i0 = max(1, min(i0, n - 3))

    # Centered differences
    d2 = np.full(n, np.nan)
    for k in range(1, n - 1):
        d2[k] = y[k+1] - 2*y[k] + y[k-1]

    d3 = np.full(n, np.nan)
    for k in range(2, n - 1):
        d3[k] = d2[k] - d2[k-1]

    d4 = np.full(n, np.nan)
    for k in range(2, n - 2):
        d4[k] = d2[k+1] - 2*d2[k] + d2[k-1]

    n_cols = 6
    n_rows = n + 1
    fig, ax = plt.subplots(figsize=(max(14, n_cols*2.2),
                                     max(4, n_rows*0.55 + 1.5)))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    row_h = 1.0 / n_rows
    col_w = 1.0 / (n_cols + 1)

    headers = ["x (s)", "f(x) = y", "δ¹y (Δy)",
               "δ²y (central)", "δ³y (central)", "δ⁴y (central)"]

    for j, txt in enumerate(headers):
        ax.add_patch(plt.Rectangle((j*col_w, 1-row_h), col_w, row_h,
                                   facecolor="#1F3A5F", edgecolor="white"))
        ax.text(j*col_w + col_w/2, 1-row_h/2, txt,
                ha="center", va="center", color="white",
                fontsize=9, fontweight="bold")

    rows_used = {i0, i0-1}

    for i in range(n):
        y0 = 1 - (i + 2) * row_h

        # x column
        ax.add_patch(plt.Rectangle((0, y0), col_w, row_h,
                                   facecolor="#EFEFEF", edgecolor="gray", lw=0.6))
        ax.text(col_w/2, y0 + row_h/2, f"{x[i]:.3f}",
                ha="center", va="center", fontsize=8, fontweight="bold")

        # f(x) column
        if i == i0:
            fc_fx = "#FFD700"
        elif i == i0 - 1:
            fc_fx = "#E8F7D0"
        else:
            fc_fx = "white"
        ax.add_patch(plt.Rectangle((col_w, y0), col_w, row_h,
                                   facecolor=fc_fx, edgecolor="gray", lw=0.6))
        ax.text(col_w + col_w/2, y0 + row_h/2, f"{y[i]:.6f}",
                ha="center", va="center", fontsize=7.5)

        # δ¹y (forward diff at row i)
        if i < n - 1:
            dy = y[i+1] - y[i]
            fc = "#FFB6C1" if i == i0 - 1 else "white"
            ax.add_patch(plt.Rectangle((2*col_w, y0), col_w, row_h,
                                       facecolor=fc, edgecolor="gray", lw=0.6))
            ax.text(2*col_w + col_w/2, y0 + row_h/2, f"{dy:.6f}",
                    ha="center", va="center", fontsize=7.5)

        # δ²y
        if not np.isnan(d2[i]):
            fc = "#FFB6C1" if i in (i0, i0+1) else "white"
            ax.add_patch(plt.Rectangle((3*col_w, y0), col_w, row_h,
                                       facecolor=fc, edgecolor="gray", lw=0.6))
            ax.text(3*col_w + col_w/2, y0 + row_h/2, f"{d2[i]:.6f}",
                    ha="center", va="center", fontsize=7.5)

        # δ³y
        if not np.isnan(d3[i]):
            fc = "#FFB6C1" if i in (i0, i0+1) else "white"
            ax.add_patch(plt.Rectangle((4*col_w, y0), col_w, row_h,
                                       facecolor=fc, edgecolor="gray", lw=0.6))
            ax.text(4*col_w + col_w/2, y0 + row_h/2, f"{d3[i]:.6f}",
                    ha="center", va="center", fontsize=7.5)

        # δ⁴y
        if not np.isnan(d4[i]):
            fc = "#FFB6C1" if i in (i0-1, i0, i0+1) else "white"
            ax.add_patch(plt.Rectangle((5*col_w, y0), col_w, row_h,
                                       facecolor=fc, edgecolor="gray", lw=0.6))
            ax.text(5*col_w + col_w/2, y0 + row_h/2, f"{d4[i]:.6f}",
                    ha="center", va="center", fontsize=7.5)

    ax.set_title(f"Stirling Central Difference Table  (xp = {xp:.3f} s, "
                 f"nearest node t = {x[i0]:.3f} s)",
                 fontsize=13, fontweight="bold", pad=15)

    ax.legend(handles=[
        mpatches.Patch(color="#FFD700", label="Nearest node i₀ to xp (origin)"),
        mpatches.Patch(color="#E8F7D0", label="Symmetric neighbour row (i₀−1)"),
        mpatches.Patch(color="#FFB6C1", label="Centered differences used in Stirling formula"),
        mpatches.Patch(color="#EFEFEF", label="x values"),
    ], loc="upper center", bbox_to_anchor=(0.5, 0.02), ncol=4,
       fontsize=8, frameon=False)

    plt.tight_layout()
    plt.savefig(filename, dpi=170, bbox_inches="tight")
    plt.close()
    print(f"[saved] {filename}")


# ============================================================
# 6. DERIVATIVE COMPARISON GRAPHS
# ============================================================
def plot_derivative_comparison(xp, results, x, y):
    """Sweep xp over whole domain, plot f'(x) and f''(x) from all 3 methods."""
    xs = np.linspace(x[0], x[-1], 200)
    true1 = np.asarray(true_d1(xs))
    true2 = np.asarray(true_d2(xs))

    f1 = np.full_like(xs, np.nan); f2 = np.full_like(xs, np.nan)
    b1 = np.full_like(xs, np.nan); b2 = np.full_like(xs, np.nan)
    s1 = np.full_like(xs, np.nan); s2 = np.full_like(xs, np.nan)

    for i, xq in enumerate(xs):
        r = compute_all_methods(xq, x, y)
        f1[i], f2[i] = r["Newton Forward"]
        b1[i], b2[i] = r["Newton Backward"]
        s1[i], s2[i] = r["Stirling Central"]

    fig, axes = plt.subplots(2, 1, figsize=(12, 9))

    ax = axes[0]
    ax.plot(xs, true1, 'k-', lw=2.5, label="True v'(t)")
    ax.plot(xs, f1, 'r--', lw=1.4, label="Newton Forward")
    ax.plot(xs, b1, 'b--', lw=1.4, label="Newton Backward")
    ax.plot(xs, s1, 'g-.', lw=1.8, label="Stirling")
    ax.plot(x, y, 'o', ms=5, mfc='steelblue', mec='k', label="Data")
    ax.axvline(xp, color='red', ls=':', lw=1.2, label=f"xp = {xp:.2f} s")
    ax.set_xlabel("Time t (s)")
    ax.set_ylabel("Acceleration v'(t) (m/s²)")
    ax.set_title("First Derivative — All Methods vs True")
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(alpha=0.3)

    ax = axes[1]
    ax.plot(xs, true2, 'k-', lw=2.5, label="True v''(t)")
    ax.plot(xs, f2, 'r--', lw=1.4, label="Newton Forward")
    ax.plot(xs, b2, 'b--', lw=1.4, label="Newton Backward")
    ax.plot(xs, s2, 'g-.', lw=1.8, label="Stirling")
    ax.axvline(xp, color='red', ls=':', lw=1.2, label=f"xp = {xp:.2f} s")
    ax.set_xlabel("Time t (s)")
    ax.set_ylabel("Jerk v''(t) (m/s³)")
    ax.set_title("Second Derivative — All Methods vs True")
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"output/derivative_comparison_xp{xp:.2f}.png", dpi=150)
    plt.close()
    print(f"[saved] output/derivative_comparison_xp{xp:.2f}.png")


def plot_derivative_at_xp(xp, results, d1_true, d2_true):
    """Bar charts for v'(xp) and v''(xp) across the 3 methods."""
    meths = list(results.keys())
    d1v = [results[m][0] for m in meths]
    d2v = [results[m][1] for m in meths]
    colors = ["#4C72B0", "#DD8452", "#55A868"]

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    ax = axes[0]
    bars = ax.bar(meths, d1v, color=colors, edgecolor='k')
    ax.axhline(d1_true, color='red', ls='--', lw=2,
               label=f"True v' = {d1_true:.4f}")
    ax.set_ylabel("v'(xp) [m/s²]")
    ax.set_title(f"First Derivative at xp = {xp:.2f} s")
    ax.legend(); ax.grid(axis='y', alpha=0.3)
    for b, v in zip(bars, d1v):
        if not np.isnan(v):
            ax.text(b.get_x()+b.get_width()/2, v, f"{v:.3f}",
                    ha='center', va='bottom', fontsize=8)
    plt.setp(ax.get_xticklabels(), rotation=12, ha='right')

    ax = axes[1]
    bars = ax.bar(meths, d2v, color=colors, edgecolor='k')
    ax.axhline(d2_true, color='red', ls='--', lw=2,
               label=f"True v'' = {d2_true:.4f}")
    ax.set_ylabel("v''(xp) [m/s³]")
    ax.set_title(f"Second Derivative at xp = {xp:.2f} s")
    ax.legend(); ax.grid(axis='y', alpha=0.3)
    for b, v in zip(bars, d2v):
        if not np.isnan(v):
            ax.text(b.get_x()+b.get_width()/2, v, f"{v:.3f}",
                    ha='center', va='bottom', fontsize=8)
    plt.setp(ax.get_xticklabels(), rotation=12, ha='right')

    plt.tight_layout()
    plt.savefig(f"output/derivative_bars_xp{xp:.2f}.png", dpi=150)
    plt.close()
    print(f"[saved] output/derivative_bars_xp{xp:.2f}.png")


# ============================================================
# 7. MAIN ANALYSIS
# ============================================================
def run_analysis(xp):
    if xp < t[0] or xp > t[-1]:
        print(f"❌ xp = {xp} outside range [{t[0]:.2f}, {t[-1]:.2f}]")
        return

    print("\n" + "=" * 90)
    print(f"ANALYSIS AT xp = {xp:.4f} s")
    print("=" * 90)

    method, origin_idx, p_val = choose_formula(xp, t)
    print(f"Chosen method : {method}")
    print(f"Origin index  : {origin_idx}  (t = {t[origin_idx]:.3f} s)")
    print(f"p value       : {p_val:.6f}")

    results = compute_all_methods(xp, t, speed)
    d1_true = float(true_d1(xp))
    d2_true = float(true_d2(xp))

    rows = build_comparison_rows(results, d1_true, d2_true)
    best = print_comparison_table(rows, d1_true, d2_true, xp)
    save_comparison_table_image(rows, d1_true, d2_true, xp,
                                f"output/comparison_table_xp{xp:.2f}.png")

    # Difference tables — forward, backward, AND Stirling
    plot_difference_table(t, speed, "forward", origin_idx, xp,
                          f"output/forward_difference_table_xp{xp:.2f}.png")
    plot_difference_table(t, speed, "backward", N_POINTS-1, xp,
                          f"output/backward_difference_table_xp{xp:.2f}.png")
    plot_stirling_table(t, speed, xp,
                        f"output/stirling_difference_table_xp{xp:.2f}.png")

    # Derivative plots
    plot_derivative_at_xp(xp, results, d1_true, d2_true)
    plot_derivative_comparison(xp, results, t, speed)


# ============================================================
# 8. INTERACTIVE LOOP
# ============================================================
if __name__ == "__main__":
    print("=" * 90)
    print("NUMERICAL DIFFERENTIATION — SPEED vs TIME (Lab 10)")
    print("=" * 90)
    print(f"Data: {N_POINTS} points, t ∈ [{t[0]:.2f}, {t[-1]:.2f}] s, h = {h:.4f} s\n")

    while True:
        user_in = input(f"Enter xp (between {t[0]:.2f} and {t[-1]:.2f}) "
                        f"[default 2.75]: ").strip()
        if user_in == "":
            xp = 2.75
        else:
            try:
                xp = float(user_in)
            except ValueError:
                print("⚠ Invalid number.")
                continue
        if xp < t[0] or xp > t[-1]:
            print(f"⚠ xp must be between {t[0]:.2f} and {t[-1]:.2f}")
            continue
        run_analysis(xp)
        if input("\nAnalyze another xp? (y/n) [y]: ").strip().lower() == "n":
            break

    print("\nAll images saved in ./output/")