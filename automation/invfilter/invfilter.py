import argparse
import json
import re
import sys


def filter_sku(log_lines, sku, min_abs_delta) -> tuple[list[dict], int]:
    """
    Filter JSON log entries by SKU prefix and minimum absolute delta value.

    Each non-empty line in `log_lines` is expected to contain a JSON object
    with at least the keys `sku` and `delta`. Entries are included in the
    result when:

    - The entry's SKU starts with the specified `sku` value (case-insensitive).
    - The absolute value of `delta` is greater than or equal to
      `min_abs_delta`.

    Malformed lines (invalid JSON, missing required keys, or invalid types)
    are skipped and counted.

    Args:
        log_lines: Iterable of log lines, where each line is expected to be a
            JSON object.
        sku: SKU prefix to match against the `sku` field.
        min_abs_delta: Minimum absolute delta threshold required for an entry
            to be included.

    Returns:
        A tuple containing:
            - listFiltered log entries matching the SKU and delta
              criteria.
            - int: Number of malformed lines encountered and skipped.
    """
    filtered_log_lines = []
    malformed_lines = 0
    re_pattern = f"^{sku.lower()}"

    for line_number, line in enumerate(log_lines):

        if line.strip():
            try:
                j_line = json.loads(line.strip())

                if re.search(re_pattern, j_line["sku"].lower()) and abs(j_line["delta"]) >= min_abs_delta:
                    filtered_log_lines.append(j_line)
            except (json.JSONDecodeError, TypeError, KeyError) as e:
                print(
                    f"Malformed line at line number: {line_number + 1}, {e}",
                    file=sys.stderr,
                )
                malformed_lines += 1

    return filtered_log_lines, malformed_lines


def main():
    parser = argparse.ArgumentParser(
        description="Filter log entries by SKU prefix and minimum absolute delta"
    )
    parser.add_argument(
        "--sku-prefix", 
        required=True,
        type=str.lower,
        help="Case-insensitive SKU prefix to match.",
        )
    parser.add_argument(
        "--min-abs-delta", 
        type=int, 
        default=0,
        help="minimum absolute delts value."
        )
    args = parser.parse_args()
    filtered_lines, malformed_line = filter_sku(
        sys.stdin, args.sku_prefix.lower(), args.min_abs_delta
    )

    for line in filtered_lines:
        print(json.dumps(line))

    if malformed_line:
        sys.exit(1)


if __name__ == "__main__":
    main()
