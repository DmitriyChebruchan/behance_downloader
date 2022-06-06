import argparse


def parcer():
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('--output')
    parser.add_argument('address')
    result = [parser.parse_args().address,
              parser.parse_args().output]
    return result
