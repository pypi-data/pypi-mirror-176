# TODO: All Rclone operations through a single port.
from json import loads
from pathlib import Path
from datetime import datetime, timedelta
from configobj import ConfigObj
from sqlalchemy.sql import update
from re import sub
from inquirer import confirm, list_input

import podarr


class RCLONE(podarr.BaseService):

    def __init__(self) -> None:
        super().__init__('rclone')
        self.directories = {
            'base': podarr.Directory.DIR_BASE.joinpath('rclone'),
            'cache': podarr.Directory.DIR_TMP.joinpath('cache'),
            'library': podarr.Directory.DIR_BASE.joinpath('rclone', 'remote', 'library')
        }
        self.service.remote_directories = {
            'base': '/media',
            'movies': '/media/movies',
            'tv': '/media/tv',
            'music': '/media/music',
            'backups': '/backups'
        }
        if not self.directories["cache"].exists() and self.service.enabled:
            podarr.Directory().mkdir(self.directories["cache"])
            self.cache_size = round(int(sub("\\D", "", podarr.Basher(
                f'df -P {self.directories["cache"]} | tail -1 | '
                'awk "{{print $4}}"').stdout)) / 1024 ** 2 * 50 / 100)
        else:
            self.cache_size = 0

    def get_container_base_args(self) -> str:
        """This function returns updated container arguments."""
        return '--rm '\
            f'-e PUID={self.uid} '\
            f'-e PGID={self.gid} '\
            f'-v {self.directories["base"]}:/config/rclone '\
            f'{self.service.image}:{self.service.tag} '\
            '--config /config/rclone/rclone.conf'

    def get_container_args(self) -> str:
        """This function returns updated container arguments."""
        return '--cap-add=sys_admin '\
            '--device /dev/fuse '\
            f'-e PUID={self.uid} '\
            f'-e PGID={self.gid} '\
            f'-p {self.service.ports[0].number}:{self.service.ports[0].number} '\
            f'-p {self.service.ports[1].number}:{self.service.ports[1].number} '\
            f'-p {self.service.ports[2].number}:{self.service.ports[2].number} '\
            f'-v {self.directories["base"]}:/config/rclone '\
            f'-v {self.directories["library"]}:/data/remote/library:shared '\
            f'-v {self.directories["cache"]}:/data/cache '\
            f'-v {podarr.Directory.DIR_BACKUPS}:/data/backups '\
            f'-v {podarr.Directory.DIR_DATA_LOCAL}:/data/local '\
            f'{self.service.image}:{self.service.tag} '\
            f'mount {self.service.remote}:{self.service.remote_directories["base"]} '\
            '/data/remote/library '\
            f'--uid {self.uid} '\
            f'--gid {self.gid} '\
            '--allow-other '\
            '--cache-dir="/data/cache" '\
            '--dir-cache-time 5000h '\
            '--vfs-cache-mode full '\
            f'--vfs-cache-max-size {self.cache_size}G '\
            '--vfs-cache-max-age 5000h '\
            '--vfs-cache-poll-interval 5m '\
            '--vfs-read-ahead 2G '\
            '--poll-interval 10s '\
            '--rc '\
            f'--rc-addr :{self.service.ports[0].number} '\
            '--rc-no-auth '\
            '--allow-non-empty'

    def get_container_run_args(self) -> str:
        """This function returns updated container arguments."""
        return '--rm '\
            f'-e PUID={self.uid} '\
            f'-e PGID={self.gid} '\
            f'-v {self.directories["base"]}:/config/rclone '\
            f'{self.service.image}:{self.service.tag} '

    def create_config(self) -> bool:
        """
        This method creates the rclone config file.
        """
        remote_cfg = False
        crypt_cfg = None
        remote_opts = {
            'scope': 'drive',
            'stop_on_upload_limit': 'true',
            'stop_on_download_limit': 'true',
        }
        crypt_opts = {}
        podarr.Directory().set_ownership(self.directories['base'])
        podarr.Notification('yellow_alert').print('Setting up Rclone...')
        podarr.Notification('yellow_alert').print(
            "Let's start configuring the remote provider.")
        podarr.Notification('red_alert').print(
            "For now, podarr only supports setting up Google Drive.")

        # Ask for client_id/secret.
        if confirm('Use Google Application Client ID/Secret?', default=True):
            remote_opts['client_id'] = podarr.Notification(
                'question').text('Enter client ID')
            remote_opts['client_secret'] = podarr.Notification(
                'question').text('Enter client secret')

        # Get the auth code from the URL.
        config_token = loads(podarr.Podman().run(
            f'--name=podarr-rclone-config {self.get_container_base_args()} '
            'config create --non-interactive '
            f'remote drive config_is_local false '
            f'{" ".join(f"{k} {v}" for k, v in remote_opts.items())}',
            msg="Getting auth token").stdout)['Option']['Help']
        config_token = config_token.replace(
            '\n\nThen paste the result.\n', '\n')
        config_token = podarr.Notification('question').text(
            f'{config_token}\nWrite the auth_code back here to proceed setting up remote')
        remote_opts['config_token'] = config_token

        # Get the remote settings.
        if confirm('Is it a team drive?'):
            remote_opts['team_drive'] = podarr.Notification(
                'question').text('Enter the team drive id')

        # Get the crypt settings.
        crypt_cfg = confirm('Is it encrypted?', default=True)
        if crypt_cfg:
            self.service.remote = 'remote-crypt'
            crypt_opts['password'] = podarr.Notification(
                'question').text('Enter the crypt password')
            if confirm('Does the encryption require a second password (salt)?'):
                crypt_opts['password2'] = podarr.Notification(
                    'question').text('Enter the second crypt password (salt)')
            if confirm('Should directories be encrypted?', default=True):
                crypt_opts['directory_name_encryption'] = 'true'
            else:
                crypt_opts['directory_name_encryption'] = 'false'
            crypt_opts['filename_encryption'] = list_input(
                'How files should be encrypted?', choices=[
                    ('Encrypt the filenames (standard)',
                        'standard'),
                    ('Very simple filename obfuscation (obfuscate)',
                        'obfuscate'),
                    ("Don't encrypt the file names (off; adds a \".bin\" to the extension only)",
                        'off')
                ])
        else:
            self.service.remote = 'remote'
        self.session.commit()
        self.session.refresh(self.service)
        remote_cfg = podarr.Podman().run(f'--name=podarr-rclone-config {self.get_container_base_args()} config '
                                         'create remote drive config_is_local false '
                                         f'{" ".join(f"{k} {v}" for k, v in remote_opts.items())}',
                                         msg='Setting up the remote provider').return_bool
        if self.service.remote == 'remote-crypt':
            crypt_cfg = podarr.Podman().run(f'--name=podarr-rclone-config {self.get_container_base_args()} config '
                                            'create --non-interactive '
                                            f'remote-crypt crypt remote remote: '
                                            f'{" ".join(f"{k} {v}" for k, v in crypt_opts.items())}',
                                            msg='Setting up the remote encryption').return_bool
        if crypt_cfg is None:
            return remote_cfg
        if remote_cfg and crypt_cfg:
            return True
        return False

    def select_remote(self) -> bool:
        """This function allows the user to change Rclone remote that is currently being used."""
        self.service.remote = list_input(
            'Which remote would you like to use?',
            choices=[str(remote) for remote in ConfigObj(
                Path(self.directories['base']).joinpath('rclone.conf').as_posix(), list_values=False).keys()])
        commit = self.session.commit()
        self.session.refresh(self.service)
        if commit:
            return True
        return False

    def copy_existing_config(self) -> bool:
        """
        This function allows the user to select an existing Rclone config file.
        It will first try to find one at the default Rclone config path: ~/.config/rclone.
        If one is found, it w
        """
        def config_from_custom_path() -> bool:
            existing_config = podarr.Notification('question').text(
                'Type the absolute path of the existing .conf file: ')
            if Path(existing_config).exists():
                if podarr.Podman().unshare(
                        f'cp {existing_config} {self.directories["base"]}').return_bool:
                    return True
            else:
                podarr.Notification('red_alert').print(
                    "The file doesn't exist! Run the installer again.")
                return False
            return False

        existing_config = list(podarr.Directory.DIR_HOME.joinpath(
            '.config', 'rclone').rglob('*.conf'))
        config_ok = False
        if existing_config:
            podarr.Notification('yellow_alert').print(
                f'Found an existing Rclone config in {existing_config[0].as_posix()}')
            if confirm('Would you like to use it?', default=True):
                if podarr.Podman().unshare(f'cp {existing_config[0]} {self.directories["base"]}').return_bool:
                    config_ok = True
            else:
                config_ok = config_from_custom_path()
        else:
            podarr.Notification('yellow_alert').print(
                f'No existing conf files found in {existing_config[0].as_posix()}')
            config_ok = config_from_custom_path()
        if config_ok:
            self.select_remote()
        if self.service.remote is not None:
            return True
        return False

    def create_remote_directories(self) -> None:
        """
        This method creates remote directory structure.
        """
        for directory in self.service.remote_directories.values():
            podarr.Podman().run(f'{self.get_container_base_args()} mkdir {self.service.remote}:{directory}',
                                msg=f'Creating remote directory {directory}')

    def upload(self) -> bool:
        """
        A naive upload system.
        """
        backups = None
        media = None
        lock = None
        for service_lock in self.service.locks:
            if service_lock.name == 'upload':
                lock = service_lock
        if self.service.locks and datetime.now() < self.service.locks[0].datetime:
            podarr.Notification('red_alert').print(
                f"Google Drive's upload limit reached. Will try again at "
                f"{self.service.locks[0].datetime}.")
            return False
        if podarr.Podman().exec(self.service,
                                'rclone rc --rc-addr=192.168.1.104:'
                                f'{self.service.ports[1].number} core/stats').return_bool:
            podarr.Notification('red_alert').print('Already uploading.')
            return False
        backup_files = int(podarr.Basher(
            f'find {podarr.Directory.DIR_BACKUPS} -type f | wc -l').stdout)
        media_files = int(podarr.Basher(f'{podarr.Basher("which podman").stdout} '
                                        'exec -it podarr-mergerfs '
                                        f'find /data/local/backups -type f | wc -l').stdout)
        if backup_files and media_files == 0:
            raise Exception('Nothing to upload.')
        if backup_files != 0:
            backups = podarr.Podman().exec(self.service,
                                           f'rclone move /data/backups {self.service.remote}:/backups/ '
                                           '--delete-empty-src-dirs --bwlimit 30M --transfers 8 '
                                           f'--rc --rc-addr 0.0.0.0:{self.service.ports[1].number} --rc-no-auth',
                                           msg='Uploading backups').stdout
        if media_files != 0:
            media = podarr.Podman().exec(self.service,
                                         f'rclone move /data/local/library {self.service.remote}:/media/ '
                                         '--delete-empty-src-dirs --bwlimit 30M --transfers 8 '
                                         f'--rc --rc-addr 0.0.0.0:{self.service.ports[1].number} --rc-no-auth',
                                         msg='Uploading media').stdout
        if (backups is not None and 'userRateLimitExceeded' in backups) or (
                media is not None and 'userRateLimitExceeded' in media):
            if lock is not None:
                lock.datetime = datetime.now() + timedelta(hours=24)
            else:
                self.service.locks.append(
                    name='upload',
                    service=self.service,
                    datetime=datetime.now() + timedelta(hours=24)
                )
            self.session.commit()
            self.session.refresh(self.service)
            podarr.Notification('red_alert').print(
            f'Upload locked until {self.service.locks[0].datetime}.')
            return False
        return True

    def install(self) -> bool:
        """
        This is the Rclone installation function.
        It must return a bool: True if everything succeeds.
        Not sure what to return when service is not enabled.
        1. Edit service properties.
        2. Pull service image.
        3. Create service directories.
        4. Create the service container.
        5. Create the service systemd unit.
        6. Start the service.
        """
        if self.service.enabled:
            image = podarr.Podman().pull_image(self.service)
            directories = True
            for directory in self.directories.values():
                if not podarr.Directory().mkdir(directory):
                    directories = False
            if 'skip-config' not in podarr.__arguments__:
                if list_input('Would you like to use an existing Rclone config or create a new one?',
                              choices=['Create a new one', 'Use an existing config']) == 'Create a new one':
                    podarr.RCLONE().create_config()
                else:
                    self.copy_existing_config()
            else:
                self.copy_existing_config()
            podarr.RCLONE().create_remote_directories()
            container = podarr.Podman().create_container(
                self.service, self.get_container_args())
            systemd = podarr.Systemd().create(self.service, self.get_container_args())
            if image and directories and container and systemd:
                self.service.installed = True
                self.session.commit()
                self.session.refresh(self.service)
                self.start()
                return True
            return False
        return False

    def start(self) -> bool:
        """
        Rclone needs to bind mount library and data directories
        before starting itself.
        """
        if self.service.enabled and self.service.installed:
            podarr.Directory().set_ownership(self.directories['base'])
            podarr.Directory().bind_mount(
                self.directories['library'])
            return podarr.Systemd().start(self.service)
        return False

    def stop(self) -> bool:
        """
        Rclone needs to unmount library and data directories
        before stopping itself.
        """
        if self.service.enabled and self.service.installed:
            podarr.Directory().bind_unmount(
                self.directories['library'])
            stop = podarr.Systemd().stop(self.service)
            podarr.Directory().revoke_ownership(self.directories['base'])
            return stop
        return False

    def backup(self) -> None:
        pass

    def restore(self) -> None:
        pass
