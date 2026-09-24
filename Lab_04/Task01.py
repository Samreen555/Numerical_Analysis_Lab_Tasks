import matplotlib.pyplot as plt


# ============================================================
# LAB 04 - DIFFERENCE OPERATORS
# ============================================================


# ============================================================
# FORMAT NUMBER
# ============================================================

def format_number(value):

    if float(value).is_integer():
        return str(int(value))

    return f"{value:.4f}".rstrip("0").rstrip(".")


# ============================================================
# SUPERSCRIPT
# ============================================================

def superscript(number):

    table = str.maketrans(
        "0123456789",
        "⁰¹²³⁴⁵⁶⁷⁸⁹"
    )

    return str(number).translate(table)


# ============================================================
# SUBSCRIPT
# ============================================================

def subscript(number):

    table = str.maketrans(
        "0123456789-",
        "₀₁₂₃₄₅₆₇₈₉₋"
    )

    return str(number).translate(table)


# ============================================================
# BUILD DIFFERENCE TABLE
# ============================================================

def build_difference_table(y_values):

    table = [y_values.copy()]

    while len(table[-1]) > 1:

        previous = table[-1]

        new_column = []

        for i in range(len(previous) - 1):

            difference = (
                previous[i + 1]
                - previous[i]
            )

            new_column.append(difference)

        table.append(new_column)

    return table


# ============================================================
# PRINT DIFFERENCE TABLE
# ============================================================

def print_difference_table(x, table):

    print("\n")
    print("=" * 75)
    print("DIFFERENCE TABLE")
    print("=" * 75)

    print(f"{'x':>8}", end="")
    print(f"{'y':>10}", end="")

    for order in range(1, len(table)):

        heading = (
            str(order)
            + "th Diff"
        )

        print(f"{heading:>12}", end="")

    print()
    print("-" * 75)

    for row in range(len(x)):

        print(
            f"{format_number(x[row]):>8}",
            end=""
        )

        for order in range(len(table)):

            if row < len(table[order]):

                print(
                    f"{format_number(table[order][row]):>12}",
                    end=""
                )

            else:

                print(
                    f"{'':>12}",
                    end=""
                )

        print()


# ============================================================
# PRINT FORWARD DIFFERENCE TABLE
# ============================================================

def print_forward_table(x, table):

    print("\n")
    print("=" * 75)
    print("FORWARD DIFFERENCE TABLE (Δ)")
    print("=" * 75)

    print(f"{'x':>8}", end="")
    print(f"{'y':>10}", end="")

    for order in range(1, len(table)):

        heading = (
            "Δ"
            + superscript(order)
            + "y"
        )

        print(
            f"{heading:>12}",
            end=""
        )

    print()
    print("-" * 75)

    for row in range(len(x)):

        print(
            f"{format_number(x[row]):>8}",
            end=""
        )

        for order in range(len(table)):

            if row < len(table[order]):

                print(
                    f"{format_number(table[order][row]):>12}",
                    end=""
                )

            else:

                print(
                    f"{'':>12}",
                    end=""
                )

        print()


# ============================================================
# PRINT BACKWARD DIFFERENCE TABLE
# ============================================================

def print_backward_table(x, table):

    print("\n")
    print("=" * 75)
    print("BACKWARD DIFFERENCE TABLE (∇)")
    print("=" * 75)

    print(f"{'x':>8}", end="")
    print(f"{'y':>10}", end="")

    for order in range(1, len(table)):

        heading = (
            "∇"
            + superscript(order)
            + "y"
        )

        print(
            f"{heading:>12}",
            end=""
        )

    print()
    print("-" * 75)

    for row in range(len(x)):

        print(
            f"{format_number(x[row]):>8}",
            end=""
        )

        # y value
        print(
            f"{format_number(table[0][row]):>12}",
            end=""
        )

        # backward differences
        for order in range(1, len(table)):

            forward_index = (
                row - order
            )

            if (
                forward_index >= 0
                and forward_index
                < len(table[order])
            ):

                value = (
                    table[order][forward_index]
                )

                print(
                    f"{format_number(value):>12}",
                    end=""
                )

            else:

                print(
                    f"{'':>12}",
                    end=""
                )

        print()


# ============================================================
# PRINT CENTRAL DIFFERENCE TABLE
# ============================================================

def print_central_table(x, table):

    print("\n")
    print("=" * 75)
    print("CENTRAL DIFFERENCE TABLE (δ)")
    print("=" * 75)

    print(f"{'x':>8}", end="")
    print(f"{'y':>10}", end="")

    for order in range(1, len(table)):

        heading = (
            "δ"
            + superscript(order)
            + "y"
        )

        print(
            f"{heading:>12}",
            end=""
        )

    print()
    print("-" * 75)

    for row in range(len(x)):

        print(
            f"{format_number(x[row]):>8}",
            end=""
        )

        for order in range(len(table)):

            if row < len(table[order]):

                print(
                    f"{format_number(table[order][row]):>12}",
                    end=""
                )

            else:

                print(
                    f"{'':>12}",
                    end=""
                )

        print()


# ============================================================
# GENERIC IMAGE CREATOR
# ============================================================

def create_image(
        headers,
        rows,
        title,
        filename):

    height = max(
        5,
        len(rows) * 0.7
    )

    fig, ax = plt.subplots(
        figsize=(15, height)
    )

    ax.axis("off")

    table_plot = ax.table(
        cellText=rows,
        colLabels=headers,
        loc="center",
        cellLoc="center"
    )

    table_plot.auto_set_font_size(False)

    table_plot.set_fontsize(10)

    table_plot.scale(
        1,
        1.8
    )

    plt.title(
        title,
        fontsize=16
    )

    plt.savefig(
        filename,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()


# ============================================================
# IMAGE 1 - DIFFERENCE TABLE
# ============================================================

def create_difference_image(
        x,
        table):

    headers = [
        "x",
        "y"
    ]

    for order in range(1, len(table)):

        headers.append(
            str(order)
            + "th Difference"
        )

    rows = []

    for i in range(len(x)):

        row = [
            format_number(x[i])
        ]

        for order in range(len(table)):

            if i < len(table[order]):

                row.append(
                    format_number(
                        table[order][i]
                    )
                )

            else:

                row.append("")

        rows.append(row)

    create_image(
        headers,
        rows,
        "Difference Table",
        "1_Difference_Table.png"
    )


# ============================================================
# IMAGE 2 - FORWARD DELTA TABLE
# ============================================================

def create_forward_image(
        x,
        table,
        origin):

    headers = [
        "x",
        "y"
    ]

    for order in range(1, len(table)):

        headers.append(
            "Δ"
            + superscript(order)
            + "y"
        )

    rows = []

    for row_index in range(len(x)):

        relative_index = (
            row_index - origin
        )

        row = [
            format_number(x[row_index]),

            "y"
            + subscript(relative_index)
            + "\n= "
            + format_number(
                table[0][row_index]
            )
        ]

        for order in range(
                1,
                len(table)):

            if row_index < len(
                    table[order]):

                label = (
                    "Δ"
                    + superscript(order)
                    + "y"
                    + subscript(
                        relative_index
                    )
                )

                value = (
                    table[order][row_index]
                )

                row.append(
                    label
                    + "\n= "
                    + format_number(value)
                )

            else:

                row.append("")

        rows.append(row)

    create_image(
        headers,
        rows,
        "Forward Difference Table (Δ)",
        "2_Forward_Delta_Table.png"
    )


# ============================================================
# IMAGE 3 - BACKWARD NABLA TABLE
# ============================================================

def create_backward_image(
        x,
        table,
        origin):

    headers = [
        "x",
        "y"
    ]

    for order in range(1, len(table)):

        headers.append(
            "∇"
            + superscript(order)
            + "y"
        )

    rows = []

    for row_index in range(len(x)):

        relative_index = (
            row_index - origin
        )

        row = [
            format_number(x[row_index]),

            "y"
            + subscript(relative_index)
            + "\n= "
            + format_number(
                table[0][row_index]
            )
        ]

        for order in range(
                1,
                len(table)):

            forward_index = (
                row_index - order
            )

            if forward_index >= 0:

                value = (
                    table[order][forward_index]
                )

                label = (
                    "∇"
                    + superscript(order)
                    + "y"
                    + subscript(
                        relative_index
                    )
                )

                row.append(
                    label
                    + "\n= "
                    + format_number(value)
                )

            else:

                row.append("")

        rows.append(row)

    create_image(
        headers,
        rows,
        "Backward Difference Table (∇)",
        "3_Backward_Nabla_Table.png"
    )


# ============================================================
# IMAGE 4 - CENTRAL DELTA TABLE
# ============================================================

def create_central_image(
        x,
        table,
        origin):

    headers = [
        "Operator Label",
        "Value"
    ]

    rows = []

    # --------------------------------------------------------
    # Function values
    # --------------------------------------------------------

    for i in range(len(x)):

        relative = (
            i - origin
        )

        rows.append([
            "y"
            + subscript(relative),

            format_number(
                table[0][i]
            )
        ])

    # --------------------------------------------------------
    # Central differences
    # --------------------------------------------------------

    for order in range(
            1,
            len(table)):

        for i in range(
                len(table[order])):

            relative_forward = (
                i - origin
            )

            central_position = (
                relative_forward
                + order / 2
            )

            # Whole number
            if float(
                    central_position
            ).is_integer():

                position_text = (
                    subscript(
                        int(
                            central_position
                        )
                    )
                )

            # Half number
            else:

                numerator = int(
                    central_position * 2
                )

                position_text = (
                    subscript(numerator)
                    + "/₂"
                )

            label = (
                "δ"
                + superscript(order)
                + "y"
                + position_text
            )

            rows.append([
                label,
                format_number(
                    table[order][i]
                )
            ])

    create_image(
        headers,
        rows,
        "Central Difference Table (δ)",
        "4_Central_Delta_Table.png"
    )


# ============================================================
# GET OPERATOR VALUE
# ============================================================

def get_operator_value(
        table,
        operator,
        order,
        relative_index,
        origin):

    # --------------------------------------------------------
    # Validate order
    # --------------------------------------------------------

    if (
        order < 1
        or order >= len(table)
    ):

        return None

    # Convert integer-valued floats to int
    if float(relative_index).is_integer():

        relative_index = int(relative_index)

    # --------------------------------------------------------
    # FORWARD
    #
    # Δ^k y_r = table[k][origin + r]
    # --------------------------------------------------------

    if operator == "Δ":

        forward_index = (
            origin
            + relative_index
        )

    # --------------------------------------------------------
    # BACKWARD
    #
    # ∇^k y_r = Δ^k y_(r-k)
    # --------------------------------------------------------

    elif operator == "∇":

        forward_index = (
            origin
            + relative_index
            - order
        )

    # --------------------------------------------------------
    # CENTRAL
    #
    # δ^k y_(r + k/2) = Δ^k y_r
    #
    # So: δ^k y_{relative} = Δ^k y_{relative - k/2}
    #
    # forward_index = origin + relative_index - order/2
    # --------------------------------------------------------

    elif operator == "δ":

        forward_index = (
            origin
            + relative_index
            - order / 2
        )

    else:

        return None

    # --------------------------------------------------------
    # The mapped forward index must be an integer
    # --------------------------------------------------------

    if not float(forward_index).is_integer():

        return None

    forward_index = int(forward_index)

    # --------------------------------------------------------
    # Bounds check
    # --------------------------------------------------------

    if (
        0 <= forward_index
        < len(table[order])
    ):

        return table[order][forward_index]

    return None


# ============================================================
# PARSE QUERY
# ============================================================

def parse_query(query):

    query = query.strip()

    query = query.replace(
        " ",
        ""
    )

    if len(query) == 0:
        return None

    operator = query[0]

    if operator not in [
        "Δ",
        "∇",
        "δ"
    ]:

        return None

    remaining = query[1:]

    # Allow:
    # Δ^2y0
    # Δ2y0

    if remaining.startswith("^"):

        remaining = (
            remaining[1:]
        )

    if "y" not in remaining:

        return None

    parts = remaining.split(
        "y",
        1
    )

    order_text = parts[0]

    index_text = parts[1]

    try:

        order = int(
            order_text
        )

    except ValueError:

        return None

    # --------------------------------------------------------
    # Handle subscript characters
    # --------------------------------------------------------

    subscript_map = str.maketrans(
        "₀₁₂₃₄₅₆₇₈₉₋",
        "0123456789-"
    )

    index_text = (
        index_text.translate(
            subscript_map
        )
    )

    # --------------------------------------------------------
    # Handle fractional subscripts like 3/2, 1/2, -1/2
    # --------------------------------------------------------

    if "/" in index_text:

        parts = index_text.split("/")

        if len(parts) != 2:
            return None

        try:
            numerator = float(parts[0])
            denominator = float(parts[1])
            relative_index = numerator / denominator
        except ValueError:
            return None

    else:

        try:
            relative_index = float(index_text)
        except ValueError:
            return None

    return (
        operator,
        order,
        relative_index
    )


# ============================================================
# FIND LABELS FOR A VALUE
# ============================================================

def find_labels(
        table,
        target,
        origin):

    labels = []

    for order in range(
            1,
            len(table)):

        for i in range(
                len(table[order])):

            value = table[order][i]

            if abs(
                value - target
            ) < 0.000001:

                # ============================================
                # FORWARD LABEL
                # ============================================

                forward_relative = (
                    i - origin
                )

                forward_label = (
                    "Δ"
                    + superscript(order)
                    + "y"
                    + subscript(
                        forward_relative
                    )
                )

                labels.append(
                    forward_label
                )

                # ============================================
                # BACKWARD LABEL
                # ============================================

                backward_relative = (
                    forward_relative
                    + order
                )

                backward_label = (
                    "∇"
                    + superscript(order)
                    + "y"
                    + subscript(
                        backward_relative
                    )
                )

                labels.append(
                    backward_label
                )

                # ============================================
                # CENTRAL LABEL
                # ============================================

                central_relative = (
                    forward_relative
                    + order / 2
                )

                if float(
                    central_relative
                ).is_integer():

                    central_text = (
                        subscript(
                            int(
                                central_relative
                            )
                        )
                    )

                else:

                    numerator = int(
                        central_relative * 2
                    )

                    central_text = (
                        subscript(
                            numerator
                        )
                        + "/₂"
                    )

                central_label = (
                    "δ"
                    + superscript(order)
                    + "y"
                    + central_text
                )

                labels.append(
                    central_label
                )

    return labels


# ============================================================
# MAIN PROGRAM
# ============================================================

print("\n")
print("=" * 75)

print(
    "                 LAB 4 - DIFFERENCE OPERATORS"
)

print(
    " Difference-table builder with "
    "forward / backward / central /"
)

print(
    " value lookup."
)

print("=" * 75)


# ============================================================
# NUMBER OF POINTS
# ============================================================

n = int(
    input(
        "\nEnter number of data points, n : "
    )
)


# ============================================================
# INPUT DATA
# ============================================================

x_values = []
y_values = []

print(
    "\nEnter each data point as: x y"
)

for i in range(n):

    values = input().split()

    x = float(
        values[0]
    )

    y = float(
        values[1]
    )

    x_values.append(x)
    y_values.append(y)


# ============================================================
# CHECK EQUAL SPACING
# ============================================================

if n >= 2:

    h = (
        x_values[1]
        - x_values[0]
    )

    equally_spaced = True

    for i in range(
            1,
            n - 1):

        current_h = (
            x_values[i + 1]
            - x_values[i]
        )

        if abs(
            current_h - h
        ) > 0.000001:

            equally_spaced = False

    if equally_spaced:

        print(
            "\nEqual spacing confirmed."
        )

        print(
            "h =",
            format_number(h)
        )

    else:

        print(
            "\nWARNING:"
            " x-values are not equally spaced."
        )


# ============================================================
# DISPLAY DATA
# ============================================================

print("\nData:")

print(
    " x :",
    " ".join(
        format_number(value)
        for value in x_values
    )
)

print(
    " y :",
    " ".join(
        format_number(value)
        for value in y_values
    )
)


# ============================================================
# BUILD DIFFERENCE TABLE
# ============================================================

difference_table = (
    build_difference_table(
        y_values
    )
)


# ============================================================
# DISPLAY FOUR TABLES
# ============================================================

print_difference_table(
    x_values,
    difference_table
)

print_forward_table(
    x_values,
    difference_table
)

print_backward_table(
    x_values,
    difference_table
)

print_central_table(
    x_values,
    difference_table
)


# ============================================================
# SELECT ORIGIN
# ============================================================

print("\n")
print("=" * 75)
print("SELECT ORIGIN")
print("=" * 75)

for i in range(n):

    print(
        i + 1,
        "-> x =",
        format_number(
            x_values[i]
        ),
        ", y =",
        format_number(
            y_values[i]
        )
    )


origin_input = int(
    input(
        "\nSelect the origin point index: "
    )
)

origin = (
    origin_input - 1
)


# ============================================================
# VALIDATE ORIGIN
# ============================================================

if (
    origin < 0
    or origin >= n
):

    print(
        "\nInvalid origin."
    )

    exit()


print(
    "\nOrigin : y0 =",
    format_number(
        y_values[origin]
    ),
    "at x0 =",
    format_number(
        x_values[origin]
    )
)


# ============================================================
# CREATE FOUR IMAGES
# ============================================================

create_difference_image(
    x_values,
    difference_table
)

create_forward_image(
    x_values,
    difference_table,
    origin
)

create_backward_image(
    x_values,
    difference_table,
    origin
)

create_central_image(
    x_values,
    difference_table,
    origin
)


print("\n")
print("=" * 75)
print("IMAGES CREATED")
print("=" * 75)

print(
    "1. 1_Difference_Table.png"
)

print(
    "2. 2_Forward_Delta_Table.png"
)

print(
    "3. 3_Backward_Nabla_Table.png"
)

print(
    "4. 4_Central_Delta_Table.png"
)


# ============================================================
# OPERATOR VALUES AROUND ORIGIN
# ============================================================

print("\n")
print("-" * 75)

print(
    "Operator values evaluated at / around the origin"
)

print("-" * 75)


# ============================================================
# FORWARD DIFFERENCES
# ============================================================

print(
    "\nForward differences (Δ):"
)

for order in range(
        1,
        n):

    value = get_operator_value(
        difference_table,
        "Δ",
        order,
        0,
        origin
    )

    if value is not None:

        print(
            " Δ"
            + superscript(order)
            + "y₀ = "
            + format_number(value)
        )


# ============================================================
# BACKWARD DIFFERENCES
# ============================================================

print(
    "\nBackward differences (∇):"
)

for order in range(
        1,
        n):

    value = get_operator_value(
        difference_table,
        "∇",
        order,
        0,
        origin
    )

    if value is not None:

        print(
            " ∇"
            + superscript(order)
            + "y₀ = "
            + format_number(value)
        )


# ============================================================
# CENTRAL DIFFERENCES
# ============================================================

print(
    "\nCentral differences (δ):"
)

for order in range(
        1,
        n):

    value = get_operator_value(
        difference_table,
        "δ",
        order,
        0,
        origin
    )

    if value is not None:

        print(
            " δ"
            + superscript(order)
            + "y₀ = "
            + format_number(value)
        )


# ============================================================
# QUERY MODE
# ============================================================

print("\n")
print("-" * 75)

print(
    "QUERY MODE"
)

print(
    " enter a LABEL such as "
    "Δ^2y0 / ∇^1y0 / δ^2y0"
)

print(
    " enter a NUMBER such as 24 "
    "-> prints its LABEL(S)"
)

print(
    " enter q to quit"
)

print("-" * 75)


while True:

    query = input(
        "\nquery> "
    ).strip()


    # ========================================================
    # QUIT
    # ========================================================

    if query.lower() == "q":

        print(
            "\nGoodbye."
        )

        break


    # ========================================================
    # LABEL -> VALUE
    # ========================================================

    parsed = parse_query(
        query
    )

    if parsed is not None:

        operator = parsed[0]

        order = parsed[1]

        relative_index = parsed[2]

        value = get_operator_value(
            difference_table,
            operator,
            order,
            relative_index,
            origin
        )

        if value is not None:

            print(
                " "
                + query
                + " = "
                + format_number(value)
            )

        else:

            print(
                " "
                + query
                + " = "
                + "(not available)"
            )

        continue


    # ========================================================
    # NUMBER -> LABEL
    # ========================================================

    try:

        target = float(
            query
        )

        labels = find_labels(
            difference_table,
            target,
            origin
        )

        if len(labels) > 0:

            print(
                "\n value",
                format_number(target),
                "appears as:"
            )

            for label in labels:

                print(
                    " ",
                    label
                )

        else:

            print(
                "\n value",
                format_number(target),
                "not found in table."
            )

    except ValueError:

        print(
            "\nInvalid query."
        )


# ============================================================
# END
# ============================================================

print("\n")
print("=" * 75)

print(
    "End of run."
)

print("=" * 75)