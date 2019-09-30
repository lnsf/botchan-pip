from argparse import ArgumentParser
from counter.check import check
from counter.config import get_config

def main():
    bot_config = get_config()
    check(bot_config)

if __name__ == "__main__":
    main()
