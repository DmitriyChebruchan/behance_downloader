import argparse


def parcer():
    parser = argparse.ArgumentParser(description='Page loader')

    parser.add_argument('--output')
    result = [parser.parse_args().output]
    return result
