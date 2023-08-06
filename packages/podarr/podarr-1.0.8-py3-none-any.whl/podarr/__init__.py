"""
The importing order matters.
"""

__version__ = '1.0.8'
# Last number is related to bug fixes or minor improvements.
# Middle number is related to new features.
# First number is related to major updates, meaning how the module itself works.
# The counters never resets.

__available_commands__ = [
    'install',
    'uninstall',
    'start',
    'stop',
    'restart',
    'enable',
    'disable',
    'update',
    'upload',
    'backup',
    'restore',
    'status',
    'recreate-systemd',
    'start-web-server',
    'help',
]

__available_extra_args__ = [
    'debug',
    'debugerrors',
    'auto',
    'latest',
    'skip-config',
]

__arguments__ = {}

__command__ = None

from sys import argv
from os import path, chdir
from inquirer import checkbox, confirm
from uvicorn import run as start_server

# From here, importing order matters.
from .library.basher import *
from .library.system_info import *
from .library.notifications import *
from .library.directories import *

from .database.base import *
from .database.models import *

from .library.podman import *
from .library.systemd import *

from .api.endpoints import *

from .services.base import *
from .services.mergerfs import *
from .services.rclone import *
from .services.bazarr import *
from .services.lidarr import *
from .services.plex import *
from .services.prowlarr import *
from .services.qbittorrent import *
from .services.radarr import *
from .services.sabnzbd import *
from .services.sonarr import *
from .services.backend import *
from .services.frontend import *
from .services.autobackup import *
from .services.autoupload import *

for index, arg in enumerate(argv[1:]):
    if index == 0:
        if arg in __available_commands__:
            __command__ = arg
        else:
            raise Exception('Invalid command.')
    else:
        if '--' == arg[:2]:
            if "=" in arg:
                key, val = [x.strip() for x in arg[2:].split("=", 1)]
            else:
                key, val = arg[2:], True
            __arguments__[key] = val
        else:
            raise Exception('Invalid argument.')

chdir(path.abspath(path.dirname(__file__)))  # DO NOT REMOVE.

# Setup the database if it doesn't already exist.
if not podarr.Directory.DIR_BASE.joinpath('podarr.db').exists() and __command__ == 'install':
    Directory().create_base_dirs()
    podarr.Database().create_tables()
    podarr.Database().create_instances()


def run():
    """
    1. This function will process and execute the command and args passed to the module.
    """
    asc_services = Query().get_all_services("priority")
    desc_services = Query().get_all_services("priority", desc=True)
    if __command__ in ['install', 'uninstall', 'start', 'restart',
                       'stop', 'enable', 'disable', 'update',
                       'backup', 'restore', 'recreate-systemd']:
        if not __arguments__ or (len(__arguments__) == 1
                                 and any(x in __available_extra_args__ for x in __arguments__)):
            if __command__ in __available_commands__:
                if __command__ == 'install':
                    selected_services = checkbox(
                        'What services would you like to install?',
                        choices=[(service.repr, service)
                                 for service in asc_services])
                    if selected_services:
                        for service in selected_services:
                            getattr(podarr, service.name.upper().replace(  # type: ignore
                                '_', ''))().enable()
                        Notification('yellow_alert').print(
                            "These are the settings of the services you've choosen:\n")
                        Database().print_settings(enabled_only=True)
                        if confirm('Would you like to edit these settings?'):
                            for service in selected_services:
                                getattr(podarr, service.name.upper().replace(  # type: ignore
                                    '_', ''))().edit_settings()
                elif __command__ == 'uninstall':
                    for service in desc_services:
                        getattr(getattr(podarr, service.name.upper().replace(
                                '_', ''))(), __command__.replace("-", "_"))()
                    Directory().remove_base_dirs()
                elif __command__ == 'backup' and 'auto' in __arguments__:
                    mk_bkp = False
                    current_bkp_dt = datetime.now()
                    if 'auto' in podarr.__arguments__:
                        for lock in AUTOBACKUP().service.locks:
                            if lock.name == 'backup' and lock.datetime <= datetime.now():
                                mk_bkp = True
                                current_bkp_dt = lock.datetime
                    else:
                        mk_bkp = True
                    if not mk_bkp:
                        podarr.Notification('red_alert').print(
                            f'Next backup date at {current_bkp_dt}.')
                        return False
                    for service in asc_services:
                        if getattr(podarr, service.name.upper().replace(
                                '_', ''))().backup():
                            if 'auto' in podarr.__arguments__:
                                for lock in AUTOBACKUP().service.locks:
                                    if lock.name == 'backup':
                                        lock.datetime = current_bkp_dt + \
                                            timedelta(days=7)
                                        SESSION_MAKER.commit()
                                        SESSION_MAKER.refresh(
                                            AUTOBACKUP().service)
                # Services should be stopped in descending order.
                elif __command__ not in ['stop']:
                    for service in asc_services:
                        getattr(getattr(podarr, service.name.upper().replace(
                            '_', ''))(), __command__.replace("-", "_"))()
                else:
                    for service in desc_services:
                        getattr(getattr(podarr, service.name.upper().replace(
                            '_', ''))(), __command__.replace("-", "_"))()
            else:
                Notification('red_alert').print(
                    'Command not yet implemented or disabled.')
        else:
            for _arg in __arguments__:
                if _arg in [service.name for service in Query().get_all_services('priority')]:
                    if __command__ in __available_commands__:
                        if __command__ == 'install':
                            getattr(podarr, _arg.upper().replace(
                                '_', ''))().enable()
                        getattr(getattr(podarr, _arg.upper().replace(
                            '_', ''))(), __command__.replace("-", "_"))()
                    else:
                        Notification('red_alert').print(
                            'Command not yet implemented or disabled.')
                else:
                    if _arg not in __available_extra_args__:
                        Notification('red_alert').print(
                            'Invalid service or argument.')
    elif __command__ == 'upload':
        RCLONE().upload()
    elif __command__ == 'start-web-server':
        start_server('podarr.api.endpoints:app', host='0.0.0.0',
                     port=8000, log_level='info')
    elif __command__ == 'help':
        print(f"""
    Available commands: {', '.join([service for service in __available_commands__ if service != 'start-web-server'])}.

    Available services: {', '.join([service.repr for service in Query().get_all_services('priority')])}.

    To run a command to all services (example): podarr restart

    To run a command to a specific service (example): podarr restart --plex

    The restore command can receive additional parameter (--latest), to automatically choose the latest backups (example): podarr restore --latest

    Pass --debug parameter to debug every command ran by podarr (example): podarr restart --debug
    
    Pass --debugerrors parameter to debug errors of every command ran by podarr (example): podarr restart --debugerrors
        """)
    else:
        Notification('red_alert').print(
            'Command not yet implemented or disabled.')
    SESSION_MAKER.close()  # Close the database connection.
