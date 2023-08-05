import argparse


def construct_namespace() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("foo", action="store", default="bar", type=str, help="Foo of course!")
    return parser.parse_args()
