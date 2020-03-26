from logging import Logger


def log_and_raise_error(msg: str, log: Logger) -> None:
    log.error(msg)
    raise ValueError(msg)

# todo: add loger basic config?