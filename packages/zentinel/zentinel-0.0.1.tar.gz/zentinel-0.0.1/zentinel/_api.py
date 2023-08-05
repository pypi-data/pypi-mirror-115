from ._argparse import construct_namespace


def main():
    args_namespace = construct_namespace()
    print(args_namespace)
    return 125
