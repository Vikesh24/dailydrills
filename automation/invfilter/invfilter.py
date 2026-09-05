import argparse
import json
import re
import sys


def filter_sku(log_lines, sku, min_abs_delta) -> tuple[list[dict], int]:

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
    parser = argparse.ArgumentParser()
    parser.add_argument("--sku-prefix", required=True)
    parser.add_argument("--min-abs-delta", type=int, default=0)
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
