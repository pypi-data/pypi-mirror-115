# -*- coding: utf-8 -*-
# TBlock - An anti-capitalist ad-blocker that uses the hosts file
# Copyright (C) 2021 Twann <twann@ctemplar.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Standard libraries
import os
import re
import sqlite3
import datetime
import configparser

# External libraries
from colorama import init, Fore, Style

# Compatibility with Windows
# See: https://codeberg.org/tblock/tblock/pulls/17
if os.name == 'nt':
    # On POSIX, this breaks the colors
    init(convert=True)


class Font:
    BOLD = '\033[1m'
    DEFAULT = '\033[0m'
    UNDERLINE = '\033[4m'

    # The check mark appears weird on Windows, so replace it by 'v'
    if os.name == 'nt':
        CHECK_MARK = 'v'
    else:
        CHECK_MARK = '✓'


class Path:

    # The script is running on Termux
    if os.path.isdir('/data/data/com.termux/files/usr/lib/'):
        PREFIX = '/data/data/com.termux/files/usr/lib/tblock/'
        HOSTS = '/system/etc/hosts'
        TMP_DIR = '/data/data/com.termux/files/usr/tmp/tblock/'
        CONFIG = '/data/data/com.termux/files/usr/etc/tblock.conf'
        LOGS = '/data/data/com.termux/files/usr/var/log/tblock.log'
    elif os.name == 'posix':
        PREFIX = '/var/lib/tblock/'
        HOSTS = '/etc/hosts'
        TMP_DIR = '/tmp/tblock/'
        CONFIG = '/etc/tblock.conf'
        LOGS = '/var/log/tblock.log'

    # The script is running on Windows
    elif os.name == 'nt':
        PREFIX = os.path.join(os.path.expandvars('%ALLUSERSPROFILE%'), 'TBlock')
        HOSTS = os.path.join(os.path.expandvars('%WINDIR%'), 'System32', 'drivers', 'etc', 'hosts')
        TMP_DIR = os.path.join(os.path.expandvars('%TMP%'), 'tblock')
        CONFIG = os.path.join(PREFIX, 'conf.ini')
        LOGS = os.path.join(PREFIX, 'tblock.log')

    # If the script is running on an unsupported platform, raise an error
    else:
        raise OSError('TBlock is currently not supported on your operating system')

    # Other paths
    DATABASE = os.path.join(PREFIX, 'storage.sqlite')
    HOSTS_BACKUP = os.path.join(PREFIX, 'hosts')
    REPO_VERSION = os.path.join(PREFIX, 'repo')
    HOSTS_VERIFICATION = os.path.join(PREFIX, 'hosts_protection')
    DB_LOCK = os.path.join(PREFIX, '.db-lock')
    NEEDS_UPDATE = os.path.join(PREFIX, '.needs-update')


def log_message(message: str) -> None:
    """Log a message in TBlock logs

    Args:
        message (str): The message to log
    """
    try:
        with open(Path.LOGS, 'at') as logging:
            logging.write(message)
    except (PermissionError, FileNotFoundError):
        pass


def is_valid_ip(ip: str, allow_ipv6: bool = False) -> bool:
    """Check whether an IP address is valid or not

    Args:
        ip (str): Tĥe IP address to check
        allow_ipv6 (bool): Defaults to False. Allow IPv6 rules

    Returns:
        bool: True if IP address seems valid
    """
    if allow_ipv6 and re.match(r'^[:0-9A-f]*[:]?[0-9A-f:].', ip):
        return True
    elif 7 <= len(ip) <= 15:
        if len(re.findall(r"\.", ip)) == 3:
            return True
        else:
            return False
    else:
        return False


class Var:

    # The default IP address where to redirect blocked domains
    DEFAULT_IP = '127.0.0.1'
    DEFAULT_IPV6 = '::1'
    ALLOW_IPV6 = False

    # The list of all official mirrors of the remote filter repository that are available
    # Read more: https://tblock.codeberg.page/wiki/filters/remote-repository#mirrors
    REPO_MIRRORS = [
        'https://tblock.codeberg.page/repo/index.xml',
        'https://codeberg.org/tblock/repo/raw/branch/main/index.xml',
        'https://git.disroot.org/tblock/repo/raw/branch/main/index.xml',
        'https://0xacab.org/twann/repo/-/raw/main/index.xml',
        'http://wmj5kiic7b6kjplpbvwadnht2nh2qnkbnqtcv3dyvpqtz7ssbssftxid.onion/twann/repo/-/raw/main/index.xml'
    ]

    # Change default variables
    if os.path.isfile(Path.CONFIG):
        config = configparser.ConfigParser()
        config.read(Path.CONFIG)
        try:
            default_vars = config['default']
            ALLOW_IPV6 = bool(int(default_vars['allow_ipv6']))
            if is_valid_ip(default_vars['default_ip'].replace('"', ''), ALLOW_IPV6):
                DEFAULT_IP = default_vars['default_ip'].replace('"', '')
            else:
                log_message(f'[{datetime.datetime.now().strftime("%D %r")}] '
                            f'WARNING: {Path.CONFIG} is not a valid configuration file. Default values will be used.\n')
            if is_valid_ip(default_vars['default_ipv6'].replace('"', ''), ALLOW_IPV6):
                DEFAULT_IPV6 = default_vars['default_ipv6'].replace('"', '')
            else:
                log_message(f'[{datetime.datetime.now().strftime("%D %r")}] '
                            f'WARNING: {Path.CONFIG} is not a valid configuration file. Default values will be used.\n')
        except (KeyError, ValueError):
            log_message(f'[{datetime.datetime.now().strftime("%D %r")}] '
                        f'WARNING: {Path.CONFIG} is not a valid configuration file. Default values will be used.\n')
        else:
            del config
            del default_vars
    else:
        log_message(f'[{datetime.datetime.now().strftime("%D %r")}] '
                    f'WARNING: {Path.CONFIG} does not exist. Default values will be used.\n')


def setup_database(db_path: str) -> None:
    """Setup the SQLite3 database that is needed by TBlock in order to work
    Args:
        db_path (str): The path to the database to setup
    """
    with sqlite3.connect(db_path) as db:
        db.cursor().execute('''CREATE TABLE IF NOT EXISTS "rules" (
            "domain"	TEXT NOT NULL UNIQUE,
            "policy"	TEXT NOT NULL,
            "filter_id"	TEXT NOT NULL,
            "priority"	INTEGER NOT NULL,
            "ip"	TEXT,
            PRIMARY KEY("domain")
        );''')
        db.cursor().execute('''CREATE TABLE IF NOT EXISTS "filters" (
            "id"	TEXT NOT NULL UNIQUE,
            "source"	TEXT NOT NULL UNIQUE,
            "metadata"	TEXT NOT NULL,
            "subscribing"	INTEGER NOT NULL,
            "on_rfr"	INTEGER NOT NULL,
            "permissions"   TEXT,
            "mirrors"   TEXT,
            PRIMARY KEY("id")
        );''')
        try:
            db.cursor().execute('''ALTER TABLE "filters"
                    ADD COLUMN "mirrors" TEXT;
            ''')
        except sqlite3.OperationalError:
            pass
        else:
            print(
                f'{Fore.YELLOW}WARNING: database has been updated. Run "tblock -Yf" to finish update{Style.RESET_ALL}'
            )
        db.commit()


# NOTE: These lines should be executed every time TBlock is launched

def check_dirs() -> None:
    """Check and create directories and files that doesn't exist
    """
    # Check if the hosts file exists. If it doesn't, raise an error
    if not os.path.isfile(Path.HOSTS):
        raise OSError('TBlock is currently not supported on your operating system')

    # Create directories if they do not exist
    for d in [Path.PREFIX, Path.TMP_DIR]:
        if not os.path.isdir(d):
            try:
                os.mkdir(d)
            except PermissionError:
                continue

    # Update the database if needed
    try:
        with sqlite3.connect(Path.DATABASE) as db:
            db.cursor().execute('''SELECT mirrors FROM "filters";''').fetchall()    # Needed for db older than v1.2.0
    except (sqlite3.OperationalError, FileNotFoundError):
        try:
            setup_database(Path.DATABASE)
        except (PermissionError, sqlite3.OperationalError):
            pass


def get_hostname() -> str:
    """Get system hostname

    Returns:
        str: The hostname
    """
    if not os.name == 'posix' or os.path.isdir('/data/data/com.termux/files/usr/lib/'):
        return ''
    else:
        if os.path.isfile('/etc/hostname'):
            with open('/etc/hostname', 'rt') as f:
                for line in f.readlines():
                    if not re.match(r'#', line):
                        return line.split('\n')[0]
        elif os.path.isfile('/etc/conf.d/hostname'):
            with open('/etc/hostname', 'rt') as f:
                for line in f.readlines():
                    if not re.match(r'#', line):
                        return line.split('\n')[0].split('hostname="')[1].split('"')[0]
        else:
            return ''


# Check if TBlock is protecting the machine or not
global PROTECTING_STATUS
if os.path.isfile(Path.HOSTS_BACKUP):
    PROTECTING_STATUS = True
else:
    PROTECTING_STATUS = False
