import pandas as pd
from src import consts

pd.set_option('display.max_rows', 250)
pd.set_option('display.max_columns', 100)


DATA_FILE_PATH = None
AT_FILE_PATH = None


def main():
    df = pd.read_csv(DATA_FILE_PATH, encoding=consts.ENCODING, header=None)


if __name__ == "__main__":
    main()


# id activity tracker, file name, time + keys (pair)