# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from src.main.util.cli_util import ICli

# Todo: add cli for statistics plots


class StatisticsCli(ICli):

    def __init__(self):
        super().__init__()
        pass

    def configure_args(self) -> None:
        pass

    def parse_args(self) -> None:
        pass

    def main(self) -> None:
        pass


if __name__ == '__main__':
    statistics_cli = StatisticsCli()
    statistics_cli.main()