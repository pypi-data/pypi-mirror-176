import podarr


class FRONTEND(podarr.BaseService):

    def __init__(self) -> None:
        super().__init__('frontend')
        self.directories = {
            'base': podarr.Directory.DIR_BASE.joinpath('frontend'),
        }
        self.container_pars = f'-e PUID={self.uid} '\
            f'-e PGID={self.gid} '\
            f'-p {self.service.ports[0].number}:3000 '\
            f'{self.service.image}:{self.service.tag}'

    def backup(self) -> None:
        pass

    def restore(self) -> None:
        pass
