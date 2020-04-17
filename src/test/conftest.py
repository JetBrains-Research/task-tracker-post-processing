# Copyright (c) 2020 Anastasiia Birillo, Elena Lyulina

from src.main.util.log_util import configure_logger


# Set file for logger before all tests
def pytest_configure(config):
    configure_logger(in_test_mode=True)
