from uvicorn import run as start_server
import podarr


class BACKEND(podarr.BaseService):

    def __init__(self) -> None:
        super().__init__('backend')
        self.directories = {
            'systemd': podarr.Directory.DIR_USER_SYSTEMD
        }

    def start(self) -> bool:
        """
        1. This is a general start method. It should be replaced,
        deppending on the service, by a more specific method.
        2. Start the service and return the result.
        """
        if self.service.enabled and self.service.installed:
            return podarr.Systemd().start(self.service)
        return False

    def stop(self) -> bool:
        """
        1. This is a general stop method. It should be replaced,
        deppending on the service, by a more specific method.
        2. Stop the service and return the result.
        """
        if self.service.enabled and self.service.installed:
            return podarr.Systemd().stop(self.service)
        return False


    def install(self) -> bool:
        """
        Installs the service.
        """
        if self.service.enabled:
            systemd = podarr.Systemd().create(self.service,
                                              f'{podarr.Basher("which python").stdout} '
                                              '-m podarr start-web-server')
            if systemd:
                return True
            return False
        return False

    def uninstall(self, rm_img=None) -> bool:
        """
        Uninstalls the service.
        """
        if self.service.installed:
            if podarr.Systemd.status(self.service):
                self.stop()
            return podarr.Systemd().remove(self.service)
        return False

    def update(self) -> None:
        pass

    def backup(self) -> None:
        pass

    def restore(self) -> None:
        pass

    def recreate_systemd(self) -> bool:
        """
            1. Remove and create a systemd unit for the service.
            2. If everything succeeds, return True. Else, return False.
            """
        started, remove, create = False, False, False
        if self.status()['running']:
            started = True
        self.stop()
        remove = podarr.Systemd().remove(self.service)
        systemd = podarr.Systemd().create(self.service,
                                          f'{podarr.Basher("which python").stdout} '
                                          '-m podarr start-web-server')
        if systemd:
            create = True
        self.stop()
        if started:
            self.start()
        if remove and create:
            return True
        return False

    def start_webserver(self):
        start_server('podarr.api.endpoints:app', host='0.0.0.0',
                     port=8000, log_level='info')
