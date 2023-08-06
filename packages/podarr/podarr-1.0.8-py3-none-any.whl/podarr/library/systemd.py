from configobj import ConfigObj
from time import sleep

import podarr


class Systemd:
    """
    1. This class will be used to create, remove, start, and stop systemd units.
    """

    def __init__(self) -> None:
        self.directory = podarr.Directory().DIR_USER_SYSTEMD
        if not self.directory:
            podarr.Basher(f'mkdir -p {self.directory}',
                          msg=f'Creating {self.directory}')
        self.podman = podarr.Basher('which podman').stdout

    @staticmethod
    def status(service: podarr.Service) -> bool:
        """
        1. The function status takes a service argument
        (a string) and returns an object.
        2. The function status checks if the podarr service file exists.
        3. If the file exists, the function status calls the basher
        class to check if the podarr service is enabled and active or not.
        4. If the podarr service file exists, the function status
        returns an instance of the class SystemdStatus, which takes
        the results from the basher class calls.
        """
        return podarr.Basher(
            f'systemctl --user is-enabled podarr-{service.name}.service').return_bool

    def create(self, service: podarr.Service, command: str) -> bool:
        """
        This function creates systemd units for the services.
        Containerized services have different unit files.
        The function received arguments: service and command.
        It will return True if the file was sucessfuly created.
        """
        obj = ConfigObj(self.directory.joinpath(
            f'podarr-{service.name}.service').as_posix(), list_values=False)
        if service.image is not None:
            obj['Unit'] = {
                'Description': f"podarr's {service.name} systemd unit",
                'Wants': 'network-online.target',
                'After': 'network-online.target',
                'RequiresMountsFor': '%t/containers',
            }
            obj['Service'] = {
                'Environment': 'PODMAN_SYSTEMD_UNIT=%n',
                'Restart': 'failure',
                'TimeoutStopSec': '70',
                'ExecStartPre': '/bin/rm -f %t/%n.ctr-id',
                'ExecStart': f'{self.podman} run --cidfile=%t/%n.ctr-id --cgroups=no-conmon --rm '
                f'--sdnotify=conmon -d --replace --name=podarr-{service.name} {command}',
                'ExecStop': f'{self.podman} stop --ignore --cidfile=%t/%n.ctr-id',
                'ExecStopPost': f'{self.podman} rm -f --ignore --cidfile=%t/%n.ctr-id',
                'Type': 'notify',
                'NotifyAccess': 'all',
            }
            obj['Install'] = {
                'WantedBy': 'default.target',
            }
        else:
            obj["Unit"] = {
                'Description': f"podarr's {service.name} systemd unit",
                'After': 'network.target',
                'Wants': 'network-online.target',
            }
            obj["Service"] = {
                'Restart': 'always',
                'RestartSec': '10s',
                'ExecStart': f'{command}',
            }
            obj['Install'] = {'WantedBy': 'default.target'}
        obj.write()
        if podarr.Directory.DIR_USER_SYSTEMD.joinpath(
            f'podarr-{service.name}.service').exists():
            return True
        return False

    def remove(self, service: podarr.Service) -> bool:
        """
        1. If the service is not running and not a container, continue.
        2. If the systemd unit exists, remove it and return True.
        3. Return False if the systemd unit does not exist.
        4. Return False if the service or a container is running.
        """
        if not self.status(service) and not podarr.Podman().status(service):
            if self.directory.joinpath(f'podarr-{service.name}.service').exists():
                return podarr.Basher(f'rm {self.directory.joinpath(f"podarr-{service.name}.service")}',
                                     msg=f'Removing systemd unit: {service.repr}').return_bool
            return False
        return False

    def start(self, service: podarr.Service) -> bool:
        """
        1. The method runs podarr.Basher to reload the user's
        systemd manager configuration.
        2. Checks if the service or the container is not running.
        3. Starts the service.
        4. The method returns a boolean.
        """
        if not self.status(service) and not podarr.Podman().status(service):
            return podarr.Basher(f'systemctl --user enable --now podarr-{service.name}.service',
                                 msg=f'Starting service: {service.repr}').return_bool
        return False

    def stop(self, service: podarr.Service) -> bool:
        """
        1. If the service is running, it will be stopped and return True.
        2. If the service is not running, it'll return False.
        """
        if self.status(service):
            stop = podarr.Basher(f'systemctl --user disable --now podarr-{service.name}.service',
                                 msg=f'Stopping service: {service.repr}').return_bool
            while (self.status(service) or podarr.Podman().status(service)):
                sleep(1)
            if stop:
                return True
        return False
