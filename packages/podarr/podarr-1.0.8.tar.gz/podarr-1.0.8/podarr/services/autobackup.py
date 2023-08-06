from datetime import datetime, timedelta

from inquirer import list_input, text

import podarr


class AUTOBACKUP(podarr.BaseService):

    def __init__(self) -> None:
        super().__init__('auto_backup')
        self.directories = {
            'base': podarr.Directory.DIR_USER_SYSTEMD
        }

    def select_backup_day_time(self) -> datetime:
        """
        This function will help selecting the next backup date for the first time.
        """
        day_week = list_input("What is the best day of the week to automatically backup?",
                              choices=[
                                  ('Monday', 0), ('Tuesday',
                                                  1), ('Wednesday', 2),
                                  ('Thursday', 3), ('Friday',
                                                      4), ('Saturday', 5),
                                  ('Sunday', 6)
                              ])
        time_day = int(text('And at what hour (1-24)?'))
        days = (int(day_week) - datetime.now().weekday() + 7) % 7
        next_bkp = (datetime.now() + timedelta(days=days)
                    ).replace(hour=time_day, minute=0, second=0)
        if next_bkp.date() == datetime.today().date():
            next_bkp = next_bkp + timedelta(days=7)
        return next_bkp

    def register_auto_backup_dt(self) -> bool:
        """
        This function will register the next backup date,
        locking the auto_backup service.
        """
        if not self.service.locks:
            next_bkp = self.select_backup_day_time()
            self.service.locks.append(podarr.Lock(
                name='backup', datetime=next_bkp))
        else:
            next_bkp = datetime.now() + timedelta(days=7)
            for lock in self.service.locks:
                if lock.name == 'backup':
                    lock.datetime = next_bkp
        self.session.commit()
        self.session.refresh(self.service)
        podarr.Notification('yellow_alert').print(
            f'Auto backups will run every {next_bkp.strftime("%A")} at {next_bkp.strftime("%I %p")}.')
        for lock in self.service.locks:
            if lock.name == 'backup' and lock.datetime == next_bkp:
                return True
        return False

    def install(self) -> bool:
        """
        Installs the service.
        """
        if self.service.enabled:
            bkp = self.register_auto_backup_dt()
            systemd = podarr.Systemd().create(self.service,
                                              f'{podarr.Basher("which python").stdout} -m podarr backup --auto')
            if bkp and systemd:
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
                                          f'{podarr.Basher("which python").stdout} -m podarr backup --auto')
        if systemd:
            create = True
        self.stop()
        if started:
            self.start()
        if remove and create:
            return True
        return False
