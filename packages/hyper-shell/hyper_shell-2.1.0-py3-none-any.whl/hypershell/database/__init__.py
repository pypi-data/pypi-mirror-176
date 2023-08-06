# SPDX-FileCopyrightText: 2022 Geoffrey Lentner
# SPDX-License-Identifier: Apache-2.0

"""Database interface, models, and methods."""


# standard libs
import sys

# external libs
from cmdkit.app import Application, exit_status
from cmdkit.cli import Interface
from cmdkit.config import ConfigurationError
from sqlalchemy import inspect

# internal libs
from hypershell.core.ansi import colorize_usage
from hypershell.core.logging import Logger
from hypershell.core.config import config
from hypershell.core.exceptions import write_traceback
from hypershell.database.core import engine, in_memory
from hypershell.database.model import Model

# public interface
__all__ = ['InitDBApp', 'initdb', 'truncatedb', 'checkdb', 'DatabaseUninitialized', 'DATABASE_ENABLED', ]

# initialize logger
log = Logger.with_name(__name__)


def initdb() -> None:
    """Initialize database tables."""
    Model.metadata.create_all(engine)


def truncatedb() -> None:
    """Truncate database tables."""
    log.warning('Truncating database')
    Model.metadata.drop_all(engine)
    Model.metadata.create_all(engine)


def checkdb() -> None:
    """Ensure database connection and tables exist."""
    if not inspect(engine).has_table('task'):
        raise DatabaseUninitialized('Use \'initdb\' to initialize the database')


class DatabaseUninitialized(Exception):
    """The database needs to be initialized before operations."""


INITDB_PROGRAM = 'hyper-shell initdb'
INITDB_USAGE = f"""\
Usage:
{INITDB_PROGRAM} [-h] [--truncate [--yes]]

Initialize database (not needed for SQLite).
Use --truncate to zero out the task metadata.\
"""

INITDB_HELP = f"""\
{INITDB_USAGE}

Options:
  -t, --truncate       Truncate database (task metadata will be lost).
  -y, --yes            Auto-confirm truncation (default will prompt).
  -h, --help           Show this message and exit.\
"""


class InitDBApp(Application):
    """Initialize database (not needed for SQLite)."""

    interface = Interface(INITDB_PROGRAM,
                          colorize_usage(INITDB_USAGE),
                          colorize_usage(INITDB_HELP))

    ALLOW_NOARGS = True

    truncate: bool = False
    interface.add_argument('-t', '--truncate', action='store_true')

    auto_confirm: bool = False
    interface.add_argument('-y', '--yes', action='store_true', dest='auto_confirm')

    def run(self) -> None:
        """Business logic for `initdb`."""
        if not DATABASE_ENABLED:
            raise ConfigurationError('No database configured')
        elif not self.truncate:
            initdb()
        elif self.auto_confirm:
            truncatedb()
        elif not sys.stdout.isatty():
            raise RuntimeError('Non-interactive prompt cannot confirm --truncate (see --yes).')
        else:
            if config.database.provider == 'sqlite':
                site = config.database.file
            else:
                site = config.database.get('host', 'localhost')
            print(f'Connected to: {config.database.provider} ({site})')
            response = input(f'Truncate database? [Y]es/no: ').strip()
            if response.lower() in ['', 'y', 'yes']:
                truncatedb()
            elif response.lower() in ['n', 'no']:
                print('Stopping')
            else:
                raise RuntimeError(f'Stopping (invalid response: "{response}")')


try:
    if not in_memory:
        DATABASE_ENABLED = True
    else:
        DATABASE_ENABLED = False
except Exception as error:
    write_traceback(error, module=__name__)
    sys.exit(exit_status.bad_config)
