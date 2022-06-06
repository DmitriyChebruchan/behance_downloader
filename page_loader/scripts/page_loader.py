#!/usr/bin/env python3
from page_loader.cli.cli import parcer
from page_loader.page_loader.page_loader import download


def main():
    parce = parcer()
    result = download(*parce)
    return result


if __name__ == '__main__':
    main()
