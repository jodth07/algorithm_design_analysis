import argparse


def to_snake_case(input: str) -> str:
    return input.lower().replace(" ", "_").replace("-", "_")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ProgramName",
        description="parse inputs into different cases",
    )
    parser.add_argument("-s", "--snake-case", default=False, action="store_true")
    args = parser.parse_args()
    print(args)
    if args.snake_case:
        print(to_snake_case(args[0]))
