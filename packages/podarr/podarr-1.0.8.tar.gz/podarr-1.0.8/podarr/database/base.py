"""
Database pre-defined queries.
"""
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import podarr

DATABASE_URL = f'sqlite:///{podarr.Directory.DIR_BASE.as_posix()}/podarr.db'

DATABASE_ENGINE = create_engine(DATABASE_URL, connect_args={
                                "check_same_thread": False})

SESSION_MAKER = sessionmaker(autoflush=False, bind=DATABASE_ENGINE)()

BASE_MODEL = declarative_base()


class Database:
    def __init__(self) -> None:
        self.session = podarr.SESSION_MAKER

    @staticmethod
    def create_tables():
        podarr.BASE_MODEL.metadata.create_all(
            bind=podarr.DATABASE_ENGINE)

    def create_instances(self):
        if not bool(self.session.query(podarr.Service).filter(podarr.Service.name == 'rclone').scalar()):
            self.session.add(podarr.Service(
                name='rclone',
                repr='Rclone',
                required=False,
                enabled=False,
                priority=0,
                image='docker.io/rclone/rclone',
                tag='latest',
                ports=[
                    podarr.Port(number=6000),
                    podarr.Port(number=6001),
                    podarr.Port(number=6002),
                ]
            ))
        if not bool(self.session.query(podarr.Service).filter(podarr.Service.name == 'mergerfs').scalar()):
            self.session.add(podarr.Service(
                name='mergerfs',
                repr='MergerFS',
                required=True,
                enabled=False,
                priority=1,
                image='docker.io/hotio/mergerfs',
                tag='latest',
                ports=[]
            ))
        if not bool(self.session.query(podarr.Service).filter(podarr.Service.name == 'plex').scalar()):
            self.session.add(podarr.Service(
                name='plex',
                repr='Plex Media Server',
                required=False,
                enabled=False,
                priority=2,
                image='docker.io/linuxserver/plex',
                tag='latest',
                ports=[
                    podarr.Port(number=32400)
                ]
            ))
        if not bool(self.session.query(podarr.Service).filter(podarr.Service.name == 'radarr').scalar()):
            self.session.add(podarr.Service(
                name='radarr',
                repr='Radarr',
                required=False,
                enabled=False,
                priority=2,
                image='docker.io/linuxserver/radarr',
                tag='latest',
                ports=[
                    podarr.Port(number=7000)
                ]
            ))
        if not bool(self.session.query(podarr.Service).filter(podarr.Service.name == 'sonarr').scalar()):
            self.session.add(podarr.Service(
                name='sonarr',
                repr='Sonarr',
                required=False,
                enabled=False,
                priority=2,
                image='docker.io/linuxserver/sonarr',
                tag='latest',
                ports=[
                    podarr.Port(number=7001)
                ]
            ))
        if not bool(self.session.query(podarr.Service).filter(podarr.Service.name == 'lidarr').scalar()):
            self.session.add(podarr.Service(
                name='lidarr',
                repr='Lidarr',
                required=False,
                enabled=False,
                priority=2,
                image='docker.io/linuxserver/lidarr',
                tag='latest',
                ports=[
                    podarr.Port(number=7002)
                ]
            ))
        if not bool(self.session.query(podarr.Service).filter(podarr.Service.name == 'bazarr').scalar()):
            self.session.add(podarr.Service(
                name='bazarr',
                repr='Bazarr',
                required=False,
                enabled=False,
                priority=2,
                image='docker.io/linuxserver/bazarr',
                tag='latest',
                ports=[
                    podarr.Port(number=7003)
                ]
            ))
        if not bool(self.session.query(podarr.Service).filter(podarr.Service.name == 'prowlarr').scalar()):
            self.session.add(podarr.Service(
                name='prowlarr',
                repr='Prowlarr',
                required=False,
                enabled=False,
                priority=2,
                image='docker.io/linuxserver/prowlarr',
                tag='latest',
                ports=[
                    podarr.Port(number=7004)
                ]
            ))
        if not bool(self.session.query(podarr.Service).filter(podarr.Service.name == 'sabnzbd').scalar()):
            self.session.add(podarr.Service(
                name='sabnzbd',
                repr='SABnzbd',
                required=False,
                enabled=False,
                priority=2,
                image='docker.io/linuxserver/sabnzbd',
                tag='latest',
                ports=[
                    podarr.Port(number=7005),
                    podarr.Port(number=9090)
                ]
            ))
        if not bool(self.session.query(podarr.Service).filter(podarr.Service.name == 'qbittorrent').scalar()):
            self.session.add(podarr.Service(
                name='qbittorrent',
                repr='qBittorrent',
                required=False,
                enabled=False,
                priority=2,
                image='docker.io/linuxserver/qbittorrent',
                tag='latest',
                ports=[
                    podarr.Port(number=7006),
                    podarr.Port(number=6881)
                ]
            ))
        if not bool(self.session.query(podarr.Service).filter(podarr.Service.name == 'backend').scalar()):
            self.session.add(podarr.Service(
                name='backend',
                repr='Web API',
                required=False,
                enabled=False,
                priority=2,
                image=None,
                tag=None,
                ports=[
                    podarr.Port(number=8000)
                ]
            ))
        if not bool(self.session.query(podarr.Service).filter(podarr.Service.name == 'frontend').scalar()):
            self.session.add(podarr.Service(
                name='frontend',
                repr='Web GUI',
                required=False,
                enabled=False,
                priority=2,
                image='docker.io/podarr/frontend',
                tag='latest',
                ports=[
                    podarr.Port(number=8080)
                ]
            ))
        if not bool(self.session.query(podarr.Service).filter(podarr.Service.name == 'auto_backup').scalar()):
            self.session.add(podarr.Service(
                name='auto_backup',
                repr='Auto Backup',
                required=False,
                enabled=False,
                priority=3,
                image=None,
                tag=None,
                ports=[]
            ))
        if not bool(self.session.query(podarr.Service).filter(podarr.Service.name == 'auto_upload').scalar()):
            self.session.add(podarr.Service(
                name='auto_upload',
                repr='Auto Upload',
                required=False,
                enabled=False,
                priority=3,
                image=None,
                tag=None,
                ports=[]
            ))
            self.session.commit()

    def print_settings(self, enabled_only=False) -> None:
        """
        1. This procedure prints the current settiggs of the services.
        2. It will not print if the service doesn't have an image, a tag or ports.
        """
        # FIXME: Printing services without changeable settings (auto_backup/upload).
        if enabled_only:
            params = podarr.Service.enabled == 1 and podarr.Service.ports and podarr.Service.image != 'null' and podarr.Service.tag != 'null'
        else:
            params = podarr.Service.ports and podarr.Service.image != 'null' and podarr.Service.tag != 'null'
        for service in SESSION_MAKER.query(podarr.Service).where(params).all():
            print(f'{podarr.Notification.BOLD}{service.repr}'
                  f'{podarr.Notification.RESET}:')
            if service.image:
                print(f'\t{podarr.Notification.BOLD}Image'
                      f'{podarr.Notification.RESET}: {service.image}')
                print(f'\t{podarr.Notification.BOLD}Tag'
                      f'{podarr.Notification.RESET}: {service.tag}')
            if service.ports:
                if len(service.ports) > 1:
                    print(f'\t{podarr.Notification.BOLD}Ports'
                          f'{podarr.Notification.RESET}: '
                          f'{", ".join([port.number for port in service.ports])}')
                else:
                    print(f'\t{podarr.Notification.BOLD}Port'
                          f'{podarr.Notification.RESET}: '
                          f'{", ".join([port.number for port in service.ports])}')
        print()

class Query(Database):
    """
    This object contains methods with pre-defined queries.
    """

    def __init__(self) -> None:
        super().__init__()
        self.session = podarr.SESSION_MAKER

    def get_all_services(self, order_by: str, desc=False) -> list:
        """
        1. This will query all the service entries in the database
        and return it as a list.
        2. It can be ordered by any column in the database, in descending
        or ascending order.
        """
        return self.session.query(podarr.Service).order_by(
            text(f'{order_by} {"desc" if desc else "asc"}')).all()

    def get_all_users(self, order_by: str, desc=False) -> list:
        """
        1. This will query all the user entries in the database
        and return it as a list.
        2. It can be ordered by any column in the database, in descending
        or ascending order.
        """
        return self.session.query(podarr.User).order_by(
            text(f'{order_by} {"desc" if desc else "asc"}')).all()
