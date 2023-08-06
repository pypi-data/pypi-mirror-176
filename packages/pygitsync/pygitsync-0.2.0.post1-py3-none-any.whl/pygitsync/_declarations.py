#
#  Copyright (c) 2022 Russell Smiley
#
#  This file is part of pygitsync.
#
#  You should have received a copy of the MIT License along with pygitsync.
#  If not, see <https://opensource.org/licenses/MIT>.
#

"""Common constants for command definitions."""

import pathlib

from click_logging_config import LoggingConfiguration

DEFAULT_CONSOLE_LOGGING_ENABLED = True
DEFAULT_FILE_LOGGING_ENABLED = False
DEFAULT_FILE_ROTATION_BACKUPS = 10
DEFAULT_FILE_ROTATION_ENABLED = False
DEFAULT_FILE_ROTATION_SIZE_MB = 1
DEFAULT_LOG_FILE = pathlib.Path("pygitsync.log")
DEFAULT_LOG_LEVEL = "warning"

DEFAULT_LOG_CONFIG = LoggingConfiguration.parse_obj(
    {
        "enable_console_logging": DEFAULT_CONSOLE_LOGGING_ENABLED,
        "enable_file_logging": DEFAULT_FILE_LOGGING_ENABLED,
        "file_logging": {
            "file_rotation_size_megabytes": DEFAULT_FILE_ROTATION_SIZE_MB,
            "log_file_path": DEFAULT_LOG_FILE,
            "max_rotation_backup_files": DEFAULT_FILE_ROTATION_BACKUPS,
        },
        "log_level": DEFAULT_LOG_LEVEL,
    }
)
