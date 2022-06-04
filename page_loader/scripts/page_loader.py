#!/usr/bin/env python3
from page_loader.cli.cli import parcer
from page_loader.page_loader.page_loader import page_loader


def main():
    parce = parcer()
    result = page_loader(*parce)
    return result


if __name__ == '__main__':
    main()
