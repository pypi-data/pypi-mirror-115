import argparse
import asyncio
import json
import sys

from mahiru.heart import Heart


def parse_args(argv):
    parser = argparse.ArgumentParser()
    config_group = parser.add_mutually_exclusive_group(required=True)
    config_group.add_argument('--config')
    config_group.add_argument('--config-file')
    return parser.parse_args(argv)


async def main(argv):
    args = parse_args(argv)
    if args.config_file:
        with open(args.config_file) as config_file:
            config = json.load(config_file)
    else:
        config = args.config
    heart = Heart()
    await heart.initialize(config)
    await heart.run()
    await heart.join()


if __name__ == '__main__':
    asyncio.run(main(sys.argv[1:]))
