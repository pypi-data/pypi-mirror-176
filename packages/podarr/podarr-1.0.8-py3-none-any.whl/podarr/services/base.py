# TODO: Show backup file size.
from datetime import datetime
from importlib import import_module
from json import loads

from inquirer import confirm, list_input, text

import podarr


class BaseService:

    def __init__(self, service: str) -> None:
        self.module = import_module('podarr')
        self.session = podarr.SESSION_MAKER
        self.service = self.session.query(podarr.Service).where(
            podarr.Service.name == service).one()
        self.directories = {}
        self.container_pars = ''
        self.backup_pars = ''
        self.should_restart = False
        self.uid = podarr.SystemInfo.get_uid()
        self.gid = podarr.SystemInfo.get_gid()
        self.suid = podarr.SystemInfo.get_subuid()
        self.sgid = podarr.SystemInfo.get_subgid()

    def print_settings(self) -> None:
        """
        1. This procedure prints the current properties of the service.
        2. It will not print if the service doesn't have an image, a tag or ports.
        """
        if self.service.image or self.service.tag or self.service.ports:
            print()
            if self.service.image:
                print(f'{podarr.Notification.BOLD}Image'
                      f'{podarr.Notification.RESET}: {self.service.image}')
                print(f'{podarr.Notification.BOLD}Tag'
                      f'{podarr.Notification.RESET}: {self.service.tag}')
            if self.service.ports:
                if len(self.service.ports) > 1:
                    print(f'{podarr.Notification.BOLD}Ports'
                          f'{podarr.Notification.RESET}: '
                          f'{", ".join([port.number for port in self.service.ports])}')
                else:
                    print(f'{podarr.Notification.BOLD}Port'
                          f'{podarr.Notification.RESET}: '
                          f'{", ".join([port.number for port in self.service.ports])}')
            print()

    def edit_settings(self) -> None:
        """
        1. This procedure is used to edit service settings.
        """
        print(f'{podarr.Notification.BOLD}{self.service.repr}'
              f'{podarr.Notification.RESET} has the following settings:')
        self.print_settings()
        edit = confirm('Would you like to change it?')
        while edit:
            if self.service.image:
                self.service.image = text(
                    'Enter the desired image', default=self.service.image)
                self.service.tag = text(
                    'Enter the desired tag', default=self.service.tag)
            if self.service.ports:
                # FIXME: need to prevent UNIQUE constraint while changing port number.
                if len(self.service.ports) > 1:
                    for index, port in enumerate(self.service.ports):
                        self.service.ports[index].number = text(f'Enter the desired port {index + 1} number',
                                                                default=port.number)
                else:
                    self.service.ports[0].number = text('Enter the desired port number',
                                                        default=self.service.ports[0].number)
            self.session.commit()
            self.session.refresh(self.service)
            self.print_settings()
            if confirm('Would you like to confirm the following properties?', default=True):
                edit = False
            else:
                edit = True

    def start(self) -> bool:
        """
        1. This is a general start method. It should be replaced,
        deppending on the service, by a more specific method.
        2. Start the service and return the result.
        """
        # TODO: start/stop services should recreate/remove it's systemd unit.
        if self.service.enabled and self.service.installed:
            podarr.Directory().set_ownership(self.directories['base'])
            return podarr.Systemd().start(self.service)
        return False

    def stop(self) -> bool:
        """
        1. This is a general stop method. It should be replaced,
        deppending on the service, by a more specific method.
        2. Stop the service and return the result.
        """
        if self.service.enabled and self.service.installed:
            stop = podarr.Systemd().stop(self.service)
            podarr.Directory().revoke_ownership(self.directories['base'])
            return stop
        return False

    def restart(self) -> bool:
        """
        1. This is a general restart method. It should be replaced,
        deppending on the service, by a more specific method.
        2. Restart the service and return the result.
        """
        if self.service.enabled and self.service.installed:
            self.stop()
            return self.start()
        return False

    def install(self) -> bool:
        """
        This is a general service installation function.
        It should be replaced, deppending on the service, by a more specific one.
        It will run if the service is enabled.
        It must return a bool: True if everything succeeds.
        Not sure what to return when service is not enabled.
        1. Edit service settings.
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
            container = podarr.Podman().create_container(
                self.service, self.container_pars)
            systemd = podarr.Systemd().create(self.service, self.container_pars)
            if image and directories and container and systemd:
                self.service.installed = True
                self.session.commit()
                self.session.refresh(self.service)
                self.start()
                return True
            return False
        return False

    def uninstall(self, rm_img=False) -> bool:
        """
        This is a general service uninstallation function.
        It should be replaced, deppending on the service, by a more specific one.
        It must return a bool: True if everything succeeds.
        1. Stop the service if it's running.
        2. Remove the service's container.
        3. Remove the service's unit file.
        4. Remove the service's directories.
        5. Remove the service's image, if requested.
        """
        if self.service.installed:
            if podarr.Systemd.status(self.service) and podarr.Podman().status(self.service):
                self.stop()
            container = podarr.Podman().remove_container(self.service)
            systemd = podarr.Systemd().remove(self.service)
            if rm_img:
                image = podarr.Podman().remove_image(self.service)
            else:
                image = False
            directories = False
            for directory in self.directories.values():
                if podarr.Directory().rmdir(directory):
                    directories = True
            if image and directories and container and systemd:
                return True
            return False
        return False

    def update(self) -> bool:
        """
        1. This is a general update method. It should be replaced,
        deppending on the service, by a more specific method.
        2. Stop the service, remove the image, pull the new image.
        3. If everything succeeds, return True. Else, returns False.
        """
        if self.service.installed and self.service.enabled:
            if podarr.Systemd.status(self.service):
                self.should_restart = True
                self.stop()
            remove_return = podarr.Podman().remove_image(self.service)
            pull_return = podarr.Podman().pull_image(self.service)
            if self.should_restart:
                self.start()
            if remove_return and pull_return:
                return True
            return False
        return False

    def enable(self) -> bool:
        """
        1. This is a general enable method. It should be replaced,
        deppending on the service, by a more specific method.
        2. Enable the service and return the result.
        """
        auto_start = False
        if self.status()['running']:
            auto_start = True
        self.service.enabled = True
        self.session.commit()
        self.session.refresh(self.service)
        if self.service.enabled or self.status()['running']:
            podarr.Notification('yellow_alert').print(
                f'{self.service.repr} enabled')
            if auto_start:
                self.start()
            return True
        return False

    def disable(self) -> bool:
        """
        1. This is a general disable method. It should be replaced,
        deppending on the service, by a more specific method.
        2. Disable the service and return the result.
        """
        self.stop()
        self.service.enabled = False
        self.session.commit()
        self.session.refresh(self.service)

        if self.service.enabled or\
                podarr.Systemd.status(self.service)\
                or podarr.Podman().status(self.service):
            return False
        podarr.Notification('yellow_alert').print(
            f'{self.service.name} disabled')
        return True

    def backup(self) -> bool:
        # TODO: Only 3 backups of each service should be kept.
        """
        This is a general backup method. It should be replaced,
        deppending on the service, by a more specific method.
        1. Check if service is enabled and installed.
        2. Stop the service and get the current date and time.
        3. Make a tarball of the base directory.
        4. Mv the tarball to the backup directory.
        5. If everything succeeds, register the next backup date and time and
        return True. Else, returns False.
        """
        if self.service.installed and self.service.enabled:
            auto_restart = False
            if self.status()['running']:
                auto_restart = True
                self.stop()
            time_now = datetime.now().astimezone().strftime("%Y%m%d%H%M%S")
            bkp_cmd = podarr.Basher(
                f'{podarr.Basher("which tar").stdout} -cf '
                f'{podarr.Directory.DIR_TMP}/{self.service.name}_{time_now}.tar.gz -C '
                f'{self.directories["base"]} {self.backup_pars} '
                '--exclude="custom-services.d" .',
                msg=f"Performing backup: {self.service.repr}",
            )
            mv_bkp = podarr.Basher(f'mv {podarr.Directory.DIR_TMP}/{self.service.name}_'
                                   f'{time_now}.tar.gz {podarr.Directory.DIR_BACKUPS}')
            if auto_restart:
                self.start()
            if bkp_cmd.return_bool and mv_bkp.return_bool:
                return True
        return False

    def restore(self) -> bool:
        """
        1. This is a general restore method. It should be replaced,
        deppending on the service, by a more specific method.
        2. Create a list of the available backups.
        3. If there are no backups, return False.
        4. If there are backups, ask the user which one to restore.
        5. Download the backup and stop the service when done.
        3. Remove the current base directory of the service.
        4. Untar the tarball in the base directory and remove it.
        5. If everything succeeds, return True. Else, returns False.
        """
        if self.service.installed and self.service.enabled:
            backups = {}
            for file in loads(
                podarr.Podman().exec(podarr.RCLONE().service,
                                     f'rclone lsjson --files-only {podarr.RCLONE().service.remote}:/backups',
                                     msg=f"Fetching {self.service.repr}'s backup list").stdout):
                if self.service.name in file['Name']:
                    backup_file = file['Name']
                    backup_file_split = file['Name'].replace('.tar.gz', '')
                    backup_file_split = backup_file_split.split('_')
                    backups[f'{datetime.strptime(backup_file_split[1], "%Y%m%d%H%M%S")}'] = [
                        backup_file, podarr.SystemInfo.sizeof_fmt(file['Size'])]
            if backups.keys():
                if 'latest' in podarr.__arguments__:
                    backup_dt = sorted(backups.items(), reverse=True)[0][0]
                else:
                    backup_dt = list_input(
                        f"Choose which {self.service.repr} backup you'd like to restore",
                        choices=sorted(([(f'{dt} - {value[1]}', dt) for dt, value in backups.items()]), reverse=True))

                download_bkp = podarr.Podman().exec(podarr.RCLONE().service,
                                                    f'rclone copy {podarr.RCLONE().service.remote}:/backups/{backups[backup_dt][0]} '
                                                    f'/data/backups '
                                                    f'--rc --rc-addr 0.0.0.0:{podarr.RCLONE().service.ports[2].number} --rc-no-auth',
                                                    msg=f"Downloading {self.service.repr}'s "
                                                    f"backup from {backup_dt}").return_bool

                auto_restart = False
                if self.status()['running']:
                    auto_restart = True
                self.stop()

                rm_dir = podarr.Basher(
                    f'rm -rf {self.directories["base"]}/*',
                    msg=f'Removing previous {self.service.repr} instance').return_bool

                untar = podarr.Basher(f'{podarr.Basher("which tar").stdout} -xf '
                                      f'{podarr.Directory.DIR_BACKUPS.joinpath(backups[backup_dt][0])} -C '
                                      f'{self.directories["base"]}/',
                                      msg=f'Restoring backup: {self.service.repr}').return_bool

                podarr.Basher(f'rm {podarr.Directory.DIR_BACKUPS.joinpath(backups[backup_dt][0])}',
                              msg=f"Removing {self.service.repr}'s backup file")

                if auto_restart:
                    self.start()
                if download_bkp and rm_dir and untar:
                    return True

            podarr.Notification('red_alert').print(
                f'No backups found for {self.service.repr}.')
            return False
        return False

    def recreate_systemd(self) -> bool:
        """
        1. Remove and create a systemd unit for the service.
        2. If everything succeeds, return True. Else, return False.
        """
        if self.service.installed and self.service.enabled:
            started, remove, create, container_return = False, False, False, False
            if self.status()['running']:
                started = True
            self.stop()
            remove = podarr.Systemd().remove(self.service)
            container_return = podarr.Podman().create_container(
                self.service, getattr(
                    self.module,
                    self.service.name.upper().replace('_', ''))().container_pars)
            create = podarr.Systemd().create(self.service, self.container_pars)
            self.stop()
            if started:
                self.start()
            if remove and create and container_return:
                return True
            return False
        return False

    def status(self) -> dict:
        """
        Must return detailed status of the service as a dict:
        - enabled: if the service is enabled or not.
        - installed: if the service is installed or not.
        - running: if the systemd service is running.
        """
        return {
            'enabled': self.service.enabled,
            'installed': self.service.installed,
            'running': podarr.Systemd().status(self.service)
        }
