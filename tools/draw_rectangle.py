def create_box(label):
    """
    Create a minimal box for a single label without nesting.
    Returns a list of strings representing the box lines.
    """
    label_len = len(label)
    padding = max(label_len // 4, 2)
    width = label_len + padding * 2  # 2 for borders, 2 for spaces inside

    # Frame dimensions
    # top border, label line, bottom border
    height = 3

    # Create an empty frame:
    # We'll fill in the top and bottom borders and the label line
    box = []

    # Top border
    box.append("-" * width)
    # Label line (centered within the available space: width - 2 for borders)
    content_width = width - 2
    box.append("|" + label.center(content_width) + "|")
    # Bottom border
    box.append("-" * width)

    return box


def nest_box(inner_box, label):
    """
    Nest the inner_box inside a new box defined by 'label'.
    This function:
    1. Determines the required width and height of the new box.
    2. Creates a frame of that size.
    3. Places the label line at the top.
    4. Centers and places the inner_box lines within the frame.
    """
    # Determine the widest line in the inner box
    inner_box_width = max(len(line) for line in inner_box)
    label_len = len(label)
    padding = max(label_len // 4, 2)
    width = max(inner_box_width, label_len + padding * 2) + 2

    # Frame dimensions
    height = len(inner_box) + 3  # top border, label line, bottom border

    # Create an empty frame
    box = []

    # Top border
    box.append("-" * width)
    # Label line
    content_width = width - 2
    box.append("|" + label.center(content_width) + "|")
    # Inner box lines
    for line in inner_box:
        box.append("|" + line.center(content_width) + "|")
    # Bottom border
    box.append("-" * width)

    return box


# Create the nested boxes
llm_box = create_box("LLMs")
deep_learning_box = nest_box(llm_box, "Deep Learning")
machine_learning_box = nest_box(deep_learning_box, "Machine Learning")
ai_box = nest_box(machine_learning_box, "AI")

# Print the final nested box
for line in ai_box:
    print(line)
