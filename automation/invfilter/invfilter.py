import argparse
import json
import sys


def filter_sku(log_lines, sku, min_abs_delta) -> list[dict]:

    filtered_log_lines = []
    for line_number, line in enumerate(log_lines):

        if line.strip():
            try:
                j_line = json.loads(line.strip())

                if j_line["sku"] == sku:
                    filtered_log_lines.append(j_line)
            except json.JSONDecodeError as e:
                print(
                    f"Malformed line at line number: {line_number + 1}, {e.doc}",
                    file=sys.stderr,
                )
            except TypeError as e:
                print(
                    f"Invalid log format at line number: {line_number}, {e}",
                    file=sys.stderr,
                )

    if min_abs_delta:
        delta_filtered_lines = []

        for line in filtered_log_lines:

            if abs(line["delta"]) >= min_abs_delta:
                delta_filtered_lines.append(line)

        return delta_filtered_lines

    return filtered_log_lines


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sku-prefix", required=True)
    parser.add_argument("--min-abs-delta", type=int)
    args = parser.parse_args()
    filtered_lines = filter_sku(sys.stdin, args.sku_prefix, args.min_abs_delta)

    for line in filtered_lines:
        print(line)


if __name__ == "__main__":
    main()
