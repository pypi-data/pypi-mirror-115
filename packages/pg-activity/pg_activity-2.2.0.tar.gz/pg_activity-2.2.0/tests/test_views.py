import itertools


def test_header():
    columns = [
        [
            "Mem.:      39.2% - 1.78G/5.74G",
            "Swap:         0.0% - 0B/5.88G",
            "Load:         0.33 0.24 0.20",
        ],
        [
            "IO Max:        0/s",
            "Read:           0B/s - 0/s",
        ],
    ]
    column_widths = [
        max(len(column_row) for column_row in column) for column in columns
    ]
    print("\n" + "*" * 80)
    for row in itertools.zip_longest(*columns, fillvalue=""):
        print(" | ".join(cell.ljust(width) for width, cell in zip(column_widths, row)))
    print("*" * 80)
