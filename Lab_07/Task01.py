
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle
from scipy.interpolate import PchipInterpolator
from pathlib import Path


# ============================================================
# LAB 7: NUMERICAL INTERPOLATION - ADVANCED APPLICATIONS
# Symmetrical Face Outline Reconstruction
# ============================================================

OUTPUT_DIR = Path(__file__).resolve().parent


# ------------------------------------------------------------
# 1. ORIGINAL DATA PROVIDED IN THE LAB HANDOUT
# ------------------------------------------------------------

# y = vertical position along the face
y_given = np.array([0, 2, 4, 6, 8, 10], dtype=float)

# x = distance from the vertical midline
x_given = np.array([0.0, 1.1, 1.8, 2.4, 2.0, 1.3], dtype=float)


# ------------------------------------------------------------
# 2. EXTRA DESIGN POINTS FOR THE ENHANCED FACE ONLY
# ------------------------------------------------------------
# These additional points are manually chosen to make the
# forehead, temples, cheeks and crown look more face-like.
# They are NOT part of the original lab data.

y_extended = np.array([
    0.0,
    0.8,
    2.0,
    3.2,
    4.0,
    5.0,
    6.0,
    7.0,
    8.0,
    9.0,
    10.0,
    10.8,
    11.4,
    12.0
], dtype=float)

x_extended = np.array([
    0.00,
    0.55,
    1.10,
    1.55,
    1.80,
    2.20,
    2.40,
    2.30,
    2.00,
    1.70,
    1.30,
    1.15,
    0.75,
    0.00
], dtype=float)


# ------------------------------------------------------------
# 3. INTERPOLATION FUNCTION
# ------------------------------------------------------------

def interpolate_outline(y_data, x_data, number_of_points=1000):
    """
    Interpolate x-distance values at closely spaced y positions.

    PCHIP is used to produce a smooth curve while reducing
    unwanted overshooting between data points.
    """

    interpolator = PchipInterpolator(y_data, x_data)

    y_smooth = np.linspace(
        y_data.min(),
        y_data.max(),
        number_of_points
    )

    x_distance = interpolator(y_smooth)

    return y_smooth, x_distance


# ------------------------------------------------------------
# 4. PRINT THE ORIGINAL DATA
# ------------------------------------------------------------

def display_original_data():
    print("\n" + "=" * 55)
    print("LAB 7 - NUMERICAL INTERPOLATION")
    print("Original data from the lab handout")
    print("=" * 55)

    print(f"{'y position':>15} {'x distance':>15}")
    print("-" * 32)

    for y, x in zip(y_given, x_given):
        print(f"{y:>15.2f} {x:>15.2f}")

    print("-" * 32)
    print("Interpolation method: PCHIP")
    print("Symmetry rule: x_right = -x_left")


# ------------------------------------------------------------
# 5. IMAGE 1 - LEFT HALF OF THE FACE
# ------------------------------------------------------------

def create_left_image():
    y_smooth, x_distance = interpolate_outline(
        y_given, x_given
    )

    # Left side uses negative x-coordinates.
    x_left = -x_distance

    fig, ax = plt.subplots(figsize=(7, 9))

    ax.plot(
        x_left, y_smooth,
        color="darkred",
        linewidth=3,
        label="Interpolated left outline"
    )

    # Original left-side data points.
    ax.scatter(
        -x_given, y_given,
        color="royalblue",
        edgecolors="black",
        s=65,
        zorder=3,
        label="Original data points"
    )

    ax.axvline(
        0,
        color="gray",
        linestyle="--",
        alpha=0.7,
        label="Vertical midline"
    )

    ax.set_title(
        "Image 1 - Left Half of Face",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Horizontal distance x")
    ax.set_ylabel("Vertical position y")
    ax.set_xlim(-3.0, 0.5)
    ax.set_ylim(-0.5, 10.5)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()

    path = OUTPUT_DIR / "Lab7_Image1_Left_Half.png"
    fig.savefig(path, dpi=250, bbox_inches="tight")
    print(f"Saved: {path}")

    plt.show()


# ------------------------------------------------------------
# 6. IMAGE 2 - RIGHT HALF OF THE FACE
# ------------------------------------------------------------

def create_right_image():
    y_smooth, x_distance = interpolate_outline(
        y_given, x_given
    )

    # Mirror the left-side distance values across x = 0.
    x_right = x_distance

    fig, ax = plt.subplots(figsize=(7, 9))

    ax.plot(
        x_right, y_smooth,
        color="darkorange",
        linewidth=3,
        label="Mirrored right outline"
    )

    # Mirrored data points.
    ax.scatter(
        x_given, y_given,
        color="darkorange",
        edgecolors="black",
        s=65,
        zorder=3,
        label="Mirrored data points"
    )

    ax.axvline(
        0,
        color="gray",
        linestyle="--",
        alpha=0.7,
        label="Vertical midline"
    )

    ax.set_title(
        "Image 2 - Right Half of Face",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Horizontal distance x")
    ax.set_ylabel("Vertical position y")
    ax.set_xlim(-0.5, 3.0)
    ax.set_ylim(-0.5, 10.5)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()

    path = OUTPUT_DIR / "Lab7_Image2_Right_Half.png"
    fig.savefig(path, dpi=250, bbox_inches="tight")
    print(f"Saved: {path}")

    plt.show()


# ------------------------------------------------------------
# 7. IMAGE 3 - COMBINE LEFT AND RIGHT HALVES
# ------------------------------------------------------------

def create_combined_image():
    y_smooth, x_distance = interpolate_outline(
        y_given, x_given
    )

    x_left = -x_distance
    x_right = x_distance

    fig, ax = plt.subplots(figsize=(8, 10))

    # Left boundary.
    ax.plot(
        x_left, y_smooth,
        color="royalblue",
        linewidth=3,
        label="Left half"
    )

    # Right boundary.
    ax.plot(
        x_right, y_smooth,
        color="darkorange",
        linewidth=3,
        label="Right half"
    )

    # Show the original and mirrored coordinates.
    ax.scatter(
        -x_given, y_given,
        color="royalblue",
        edgecolors="black",
        s=55,
        zorder=3,
        label="Original left points"
    )

    ax.scatter(
        x_given, y_given,
        color="darkorange",
        edgecolors="black",
        s=55,
        zorder=3,
        label="Mirrored right points"
    )

    ax.axvline(
        0,
        color="gray",
        linestyle="--",
        linewidth=1.5,
        label="Symmetry axis"
    )

    ax.set_title(
        "Image 3 - Combined Symmetrical Face Outline",
        fontsize=13,
        fontweight="bold"
    )

    ax.set_xlabel("Horizontal distance x")
    ax.set_ylabel("Vertical position y")
    ax.set_xlim(-3.0, 3.0)
    ax.set_ylim(-0.5, 10.5)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()

    path = OUTPUT_DIR / "Lab7_Image3_Combined_Outline.png"
    fig.savefig(path, dpi=250, bbox_inches="tight")
    print(f"Saved: {path}")

    plt.show()


# ------------------------------------------------------------
# 8. IMAGE 4 - ENHANCED FULL FACE
# ------------------------------------------------------------

def create_enhanced_face():
    # Use the manually extended design points for appearance.
    # The six original data points are still included.
    y_smooth, x_distance = interpolate_outline(
        y_extended, x_extended, number_of_points=1800
    )

    x_left = -x_distance
    x_right = x_distance

    fig, ax = plt.subplots(figsize=(9, 11))

    # --------------------------------------------------------
    # FACE FILL
    # --------------------------------------------------------

    ax.fill_betweenx(
        y_smooth,
        x_left,
        x_right,
        color="#F3CFB2",
        alpha=1.0,
        zorder=1,
        label="Enhanced face region"
    )

    # Outline both sides.
    ax.plot(
        x_left, y_smooth,
        color="#684333",
        linewidth=2.8,
        zorder=3
    )

    ax.plot(
        x_right, y_smooth,
        color="#684333",
        linewidth=2.8,
        zorder=3,
        label="Enhanced outline"
    )

    # --------------------------------------------------------
    # EARS
    # --------------------------------------------------------

    for sign in (-1, 1):
        ear = Ellipse(
            (sign * 2.35, 7.5),
            width=0.55,
            height=1.5,
            angle=sign * -8,
            facecolor="#E9B18D",
            edgecolor="#684333",
            linewidth=1.8,
            zorder=0
        )
        ax.add_patch(ear)

        # Inner ear detail.
        ax.plot(
            sign * np.array([2.30, 2.45, 2.35]),
            [7.9, 7.6, 7.2],
            color="#A66C52",
            linewidth=1.3,
            zorder=2
        )

    # --------------------------------------------------------
    # EYES, IRIS AND PUPILS
    # --------------------------------------------------------

    for sign in (-1, 1):
        eye_x = sign * 0.92
        eye_y = 8.35

        eye = Ellipse(
            (eye_x, eye_y),
            width=0.82,
            height=0.38,
            facecolor="white",
            edgecolor="#51382B",
            linewidth=1.5,
            zorder=4
        )
        ax.add_patch(eye)

        iris = Circle(
            (eye_x, eye_y),
            radius=0.15,
            facecolor="#527CA6",
            edgecolor="#263C53",
            linewidth=1,
            zorder=5
        )
        ax.add_patch(iris)

        pupil = Circle(
            (eye_x, eye_y),
            radius=0.065,
            facecolor="black",
            zorder=6
        )
        ax.add_patch(pupil)

        # Eyelid curve.
        eye_curve_x = eye_x + np.linspace(-0.41, 0.41, 60)
        eye_curve_y = eye_y + 0.19 * np.sin(
            np.linspace(0, np.pi, 60)
        )

        ax.plot(
            eye_curve_x, eye_curve_y,
            color="#51382B",
            linewidth=1.8,
            zorder=6
        )

    # --------------------------------------------------------
    # EYEBROWS
    # --------------------------------------------------------

    for sign in (-1, 1):
        brow_x = sign * np.linspace(0.48, 1.35, 70)
        brow_y = (
            8.95
            + 0.17 * np.sin(np.linspace(0, np.pi, 70))
        )

        ax.plot(
            brow_x, brow_y,
            color="#493026",
            linewidth=4,
            solid_capstyle="round",
            zorder=5
        )

    # --------------------------------------------------------
    # NOSE
    # --------------------------------------------------------

    # Nose bridge.
    ax.plot(
        [0.0, 0.0, -0.08],
        [8.1, 6.6, 5.7],
        color="#BD8A65",
        linewidth=2,
        zorder=4
    )

    # Nose tip.
    nose_x = np.array([
        -0.38, -0.28, -0.12, 0.0,
        0.12, 0.28, 0.38
    ])

    nose_y = np.array([
        5.65, 5.48, 5.38, 5.36,
        5.38, 5.48, 5.65
    ])

    ax.plot(
        nose_x, nose_y,
        color="#684333",
        linewidth=2,
        zorder=5
    )

    # Nostrils.
    for sign in (-1, 1):
        ax.add_patch(
            Ellipse(
                (sign * 0.22, 5.43),
                width=0.10,
                height=0.055,
                facecolor="#684333",
                edgecolor="none",
                zorder=5
            )
        )

    # --------------------------------------------------------
    # MOUTH AND LIPS
    # --------------------------------------------------------

    mouth_x = np.linspace(-0.65, 0.65, 100)

    upper_lip_y = (
        4.15
        + 0.08 * np.cos(np.pi * mouth_x / 0.65)
        - 0.09 * np.exp(-(mouth_x / 0.18) ** 2)
    )

    lower_lip_y = (
        3.98
        - 0.15 * np.cos(np.pi * mouth_x / 0.65)
    )

    ax.fill_between(
        mouth_x,
        upper_lip_y,
        3.98,
        color="#C96F79",
        alpha=0.95,
        zorder=4
    )

    ax.fill_between(
        mouth_x,
        3.98,
        lower_lip_y,
        color="#A94C5A",
        alpha=0.95,
        zorder=4
    )

    ax.plot(
        mouth_x, upper_lip_y,
        color="#773642",
        linewidth=1.4,
        zorder=5
    )

    ax.plot(
        mouth_x, lower_lip_y,
        color="#773642",
        linewidth=1.4,
        zorder=5
    )

    ax.plot(
        mouth_x,
        np.full_like(mouth_x, 3.98),
        color="#773642",
        linewidth=1.2,
        zorder=5
    )

    # --------------------------------------------------------
    # HAIR
    # --------------------------------------------------------

    # Hair cap sits over the upper forehead.
    hair_y = np.linspace(10.15, 12.0, 200)

    normalized = (hair_y - 10.15) / (12.0 - 10.15)

    hair_width = 1.45 * np.sqrt(
        np.clip(1.0 - normalized ** 2, 0, 1)
    )

    ax.fill_betweenx(
        hair_y,
        -hair_width,
        hair_width,
        color="#39251C",
        alpha=0.98,
        zorder=2
    )

    # Hairline curve.
    hairline_x = np.linspace(-1.25, 1.25, 150)

    hairline_y = (
        10.25
        + 0.20 * (1 - np.cos(np.pi * hairline_x / 1.25))
    )

    ax.plot(
        hairline_x,
        hairline_y,
        color="#241711",
        linewidth=2,
        zorder=4
    )

    # --------------------------------------------------------
    # ORIGINAL AND MIRRORED DATA POINTS
    # --------------------------------------------------------

    ax.scatter(
        -x_given,
        y_given,
        color="royalblue",
        edgecolors="black",
        s=45,
        zorder=7,
        label="Original lab points"
    )

    ax.scatter(
        x_given,
        y_given,
        color="darkorange",
        edgecolors="black",
        s=45,
        zorder=7,
        label="Mirrored lab points"
    )

    # Symmetry line.
    ax.axvline(
        0,
        color="gray",
        linestyle="--",
        linewidth=1,
        alpha=0.45,
        zorder=0
    )

    # --------------------------------------------------------
    # FINAL FORMATTING
    # --------------------------------------------------------

    ax.set_title(
        "Lab 7 - Enhanced Symmetrical Face",
        fontsize=15,
        fontweight="bold"
    )

    ax.set_xlabel("Horizontal distance from midline (x)")
    ax.set_ylabel("Vertical position along face (y)")

    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(-0.4, 12.5)

    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.18)
    ax.legend(loc="upper right", fontsize=8)

    fig.tight_layout()

    path = OUTPUT_DIR / "Lab7_Image4_Enhanced_Full_Face.png"
    fig.savefig(path, dpi=300, bbox_inches="tight")
    print(f"Saved: {path}")

    plt.show()


# ------------------------------------------------------------
# 9. MAIN PROGRAM
# ------------------------------------------------------------

def main():
    display_original_data()

    print("\nGenerating Image 1: Left half...")
    create_left_image()

    print("\nGenerating Image 2: Right half...")
    create_right_image()

    print("\nGenerating Image 3: Combined outline...")
    create_combined_image()

    print("\nGenerating Image 4: Enhanced full face...")
    create_enhanced_face()

    print("\n" + "=" * 55)
    print("ALL FOUR IMAGES GENERATED SUCCESSFULLY")
    print("=" * 55)

    print("\nOutput files:")
    print("1. Lab7_Image1_Left_Half.png")
    print("2. Lab7_Image2_Right_Half.png")
    print("3. Lab7_Image3_Combined_Outline.png")
    print("4. Lab7_Image4_Enhanced_Full_Face.png")


if __name__ == "__main__":
    main()
