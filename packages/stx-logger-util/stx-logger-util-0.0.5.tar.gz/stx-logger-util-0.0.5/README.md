# StxLoggerUtil

Library for a faster logger implementation

## Requirements

+ Python >= 3.6

## Getting Started

You can install the library with the following command:

    $ pip install stx-logger-util

Create a logger:

    from stx_logger_util.log_admin import LogEnv
    from stx_logger_util.log_admin import LogAdmin

    logger = LogAdmin.create_Logger(LogEnv.PRODUCTION, "app")

By default the entry log will show the timestamp. If you don't need it just set in false the variable "_timestamp":

    logger = LogAdmin.create_Logger(LogEnv.PRODUCTION, "app", _timestamp=False)
