import podarr


class AUTOUPLOAD(podarr.BaseService):

    def __init__(self) -> None:
        super().__init__('auto_upload')
        self.directories = {
            'base': podarr.Directory.DIR_USER_SYSTEMD
        }

    def install(self) -> bool:
        """
        Installs the service.
        """
        if self.service.enabled:
            systemd = podarr.Systemd().create(self.service,
                                              f'{podarr.Basher("which python").stdout} -m podarr upload')
            if systemd:
                self.service.installed = True
                self.session.commit()
                self.session.refresh(self.service)
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
            if podarr.Systemd().remove(self.service):
                self.service.installed = False
                self.service.enabled = False
                self.session.commit()
                self.session.refresh(self.service)
                return True
            return False
        return False

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
                                          f'{podarr.Basher("which python").stdout} -m podarr upload')
        if systemd:
            create = True
        self.stop()
        if started:
            self.start()
        if remove and create:
            return True
        return False