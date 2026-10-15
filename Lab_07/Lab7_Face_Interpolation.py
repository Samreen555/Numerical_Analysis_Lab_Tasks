
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, Polygon


# =====================================================
# LAB 7: NUMERICAL INTERPOLATION
# Newton Forward and Backward Difference Formulas
# =====================================================

OUTPUT_DIR = Path(__file__).resolve().parent

# Given coordinate data
y_data = np.array([0, 2, 4, 6, 8, 10], dtype=float)
x_data = np.array([0.0, 1.1, 1.8, 2.4, 2.0, 1.3], dtype=float)

h = y_data[1] - y_data[0]
n = len(x_data)


# =====================================================
# TASK 1: CONSTRUCT THE FORWARD DIFFERENCE TABLE
# =====================================================

def build_difference_table(values):
    table = np.full((len(values), len(values)), np.nan)
    table[:, 0] = values

    for order in range(1, len(values)):
        for i in range(len(values) - order):
            table[i, order] = (
                table[i + 1, order - 1]
                - table[i, order - 1]
            )

    return table


difference_table = build_difference_table(x_data)


def print_difference_table():
    # ASCII-only headings avoid Windows cp1252 encoding errors.
    headers = [
        "y", "x", "D1 x", "D2 x",
        "D3 x", "D4 x", "D5 x"
    ]

    print("\nFORWARD DIFFERENCE TABLE")
    print(" | ".join(f"{item:>10}" for item in headers))
    print("-" * 85)

    for i in range(n):
        row = [f"{y_data[i]:.2f}"]

        for j in range(n):
            value = difference_table[i, j]

            if np.isnan(value):
                row.append("-")
            else:
                row.append(f"{value:.4f}")

        print(" | ".join(f"{item:>10}" for item in row))


# =====================================================
# TASK 2: NEWTON FORWARD DIFFERENCE INTERPOLATION
# =====================================================

def newton_forward(y, origin_index):
    """
    Newton Forward formula:

    p = (y - y0) / h

    x = x0 + p*D1x0
        + p*(p-1)/2! * D2x0
        + p*(p-1)*(p-2)/3! * D3x0 + ...
    """
    p = (y - y_data[origin_index]) / h

    result = difference_table[origin_index, 0]
    product = 1.0

    for order in range(1, n - origin_index):
        product *= p - (order - 1)

        result += (
            product
            * difference_table[origin_index, order]
            / math.factorial(order)
        )

    return result


# =====================================================
# TASK 3: NEWTON BACKWARD DIFFERENCE INTERPOLATION
# =====================================================

def newton_backward(y):
    """
    Newton Backward formula:

    p = (y - yn) / h

    x = xn + p*N1xn
        + p*(p+1)/2! * N2xn
        + p*(p+1)*(p+2)/3! * N3xn + ...
    """
    p = (y - y_data[-1]) / h

    result = x_data[-1]
    product = 1.0

    for order in range(1, n):
        # Backward difference of order k at the final point
        # equals the forward difference at row n-k-1.
        backward_difference = difference_table[
            n - order - 1, order
        ]

        product *= p + order - 1

        result += (
            product
            * backward_difference
            / math.factorial(order)
        )

    return result


# =====================================================
# TASK 4: GENERATE INTERMEDIATE OUTLINE POINTS
# =====================================================

def interpolate_outline(points_per_interval=100):
    y_parts = []
    x_parts = []

    for i in range(n - 1):

        # Generate points inside each interval.
        y_segment = np.linspace(
            y_data[i],
            y_data[i + 1],
            points_per_interval,
            endpoint=False
        )

        if i == n - 2:
            # Use the backward formula near the end.
            x_segment = np.array([
                newton_backward(y)
                for y in y_segment
            ])
        else:
            # Shift the forward origin to the lower point.
            x_segment = np.array([
                newton_forward(y, i)
                for y in y_segment
            ])

        y_parts.append(y_segment)
        x_parts.append(x_segment)

    # Add the final original data point.
    y_parts.append(np.array([y_data[-1]]))
    x_parts.append(np.array([x_data[-1]]))

    return np.concatenate(y_parts), np.concatenate(x_parts)


y_smooth, x_distance = interpolate_outline()

# Reflect the outline across the vertical midline x = 0.
x_left = -x_distance
x_right = x_distance


# =====================================================
# COMMON PLOTTING FUNCTION
# =====================================================

def prepare_axes(ax, title):
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel("Horizontal distance (x)")
    ax.set_ylabel("Vertical position (y)")
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.set_aspect("equal", adjustable="box")


# =====================================================
# IMAGE 1: LEFT HALF OF THE OUTLINE
# =====================================================

fig, ax = plt.subplots(figsize=(7, 8))

ax.plot(
    x_left, y_smooth,
    linewidth=2.5,
    label="Left outline"
)

ax.scatter(
    -x_data, y_data,
    s=35,
    label="Given data points"
)

prepare_axes(ax, "Image 1: Left Half of Face Outline")
ax.legend()
fig.tight_layout()

fig.savefig(
    OUTPUT_DIR / "Lab7_Image1_Left_Half.png",
    dpi=300
)

plt.close(fig)


# =====================================================
# IMAGE 2: RIGHT HALF OF THE OUTLINE
# =====================================================

fig, ax = plt.subplots(figsize=(7, 8))

ax.plot(
    x_right, y_smooth,
    linewidth=2.5,
    label="Right outline"
)

ax.scatter(
    x_data, y_data,
    s=35,
    label="Mirrored data points"
)

prepare_axes(ax, "Image 2: Right Half of Face Outline")
ax.legend()
fig.tight_layout()

fig.savefig(
    OUTPUT_DIR / "Lab7_Image2_Right_Half.png",
    dpi=300
)

plt.close(fig)


# =====================================================
# IMAGE 3: COMBINED SYMMETRICAL OUTLINE
# =====================================================

fig, ax = plt.subplots(figsize=(8, 8))

ax.plot(
    x_left, y_smooth,
    linewidth=2.5,
    label="Left half"
)

ax.plot(
    x_right, y_smooth,
    linewidth=2.5,
    label="Right half"
)

ax.scatter(-x_data, y_data, s=30)
ax.scatter(x_data, y_data, s=30)

ax.axvline(
    0,
    linestyle=":",
    color="gray",
    label="Vertical midline"
)

prepare_axes(ax, "Image 3: Combined Symmetrical Outline")
ax.legend()
fig.tight_layout()

fig.savefig(
    OUTPUT_DIR / "Lab7_Image3_Combined_Outline.png",
    dpi=300
)

plt.close(fig)


# =====================================================
# IMAGE 4: ENHANCED FACE
# Facial features are added manually using Matplotlib.
# =====================================================

fig, ax = plt.subplots(figsize=(8, 9))

# Fill the interpolated face outline.
ax.fill_betweenx(
    y_smooth,
    x_left,
    x_right,
    color="#f4d5bd",
    alpha=0.9
)

# Draw both sides of the face.
ax.plot(
    x_left, y_smooth,
    color="#49352b",
    linewidth=2.5
)

ax.plot(
    x_right, y_smooth,
    color="#49352b",
    linewidth=2.5
)

# Ears
ax.add_patch(
    Ellipse(
        (-1.95, 5.4),
        0.42, 1.0,
        facecolor="#f0c7aa",
        edgecolor="#49352b"
    )
)

ax.add_patch(
    Ellipse(
        (1.95, 5.4),
        0.42, 1.0,
        facecolor="#f0c7aa",
        edgecolor="#49352b"
    )
)

# Eyebrows
ax.plot(
    [-1.25, -0.55],
    [7.25, 7.45],
    color="#49352b",
    linewidth=5,
    solid_capstyle="round"
)

ax.plot(
    [0.55, 1.25],
    [7.45, 7.25],
    color="#49352b",
    linewidth=5,
    solid_capstyle="round"
)

# Eyes and pupils
for center_x in [-0.88, 0.88]:

    ax.add_patch(
        Ellipse(
            (center_x, 6.85),
            0.62, 0.30,
            facecolor="white",
            edgecolor="#49352b",
            linewidth=1.5
        )
    )

    ax.add_patch(
        Circle(
            (center_x, 6.85),
            0.105,
            color="#49352b"
        )
    )

    ax.add_patch(
        Circle(
            (center_x - 0.03, 6.89),
            0.03,
            color="white"
        )
    )

# Nose
ax.plot(
    [0.0, -0.12, 0.0, 0.22],
    [6.6, 5.7, 5.45, 5.55],
    color="#a46f57",
    linewidth=2.2
)

ax.plot(
    [-0.18, 0.0, 0.18],
    [5.42, 5.35, 5.42],
    color="#a46f57",
    linewidth=1.4
)

# Mouth
mouth_x = np.linspace(-0.48, 0.48, 80)

mouth_y = (
    4.35
    + 0.18 * (mouth_x / 0.48) ** 2
)

ax.plot(
    mouth_x,
    mouth_y,
    color="#9f4f55",
    linewidth=2.8
)

# Hair: an illustrative polygon, not interpolated data.
hair_points = [
    (-1.38, 8.0),
    (-1.52, 9.15),
    (-1.1, 10.1),
    (-0.45, 10.55),
    (0.35, 10.55),
    (1.1, 10.1),
    (1.52, 9.15),
    (1.38, 8.0),
    (1.05, 8.65),
    (0.58, 8.95),
    (0.0, 8.72),
    (-0.58, 8.98),
    (-1.05, 8.65)
]

ax.add_patch(
    Polygon(
        hair_points,
        closed=True,
        facecolor="#49352b",
        edgecolor="#49352b"
    )
)

# Redraw the outline so it stays visible.
ax.plot(
    x_left, y_smooth,
    color="#49352b",
    linewidth=2.5
)

ax.plot(
    x_right, y_smooth,
    color="#49352b",
    linewidth=2.5
)

ax.set_title(
    "Image 4: Enhanced Face Using Interpolation",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Horizontal distance (x)")
ax.set_ylabel("Vertical position (y)")

ax.set_xlim(-3, 3)
ax.set_ylim(-0.5, 11)

ax.set_aspect("equal", adjustable="box")
ax.grid(True, linestyle="--", alpha=0.2)

fig.tight_layout()

fig.savefig(
    OUTPUT_DIR / "Lab7_Image4_Enhanced_Full_Face.png",
    dpi=300
)

plt.close(fig)


# =====================================================
# DISPLAY RESULTS
# =====================================================

print_difference_table()

print("\nINTERPOLATION CHECKS")

for i in range(n):

    if i == n - 1:
        estimated_x = newton_backward(y_data[i])
    else:
        estimated_x = newton_forward(y_data[i], i)

    print(
        f"y = {y_data[i]:.1f}, "
        f"given x = {x_data[i]:.4f}, "
        f"interpolated x = {estimated_x:.4f}"
    )

print("\nFOUR IMAGES SAVED SUCCESSFULLY")
print(f"Output folder: {OUTPUT_DIR}")

print("1. Lab7_Image1_Left_Half.png")
print("2. Lab7_Image2_Right_Half.png")
print("3. Lab7_Image3_Combined_Outline.png")
print("4. Lab7_Image4_Enhanced_Full_Face.png")


# Display the enhanced face
image_path = OUTPUT_DIR / "Lab7_Image4_Enhanced_Full_Face.png"

image = plt.imread(image_path)

plt.figure(figsize=(7, 8))
plt.imshow(image)
plt.axis("off")
plt.title("Enhanced Face - Lab 7")
plt.tight_layout()
plt.show()
