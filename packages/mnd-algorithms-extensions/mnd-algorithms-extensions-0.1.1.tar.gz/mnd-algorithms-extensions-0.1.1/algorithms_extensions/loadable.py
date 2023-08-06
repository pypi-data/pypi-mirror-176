from abc import abstractmethod


class ILoadable:
    """
    Clase que representa un objeto que debe cargarse/inicializarse antes de ser usado.
    """

    @abstractmethod
    def is_loaded(self) -> bool:
        """
        True si está cargado, False en caso contrario.
        :return:
        """
        pass

    @abstractmethod
    def load(self):
        """
        Cargar los datos necesarios.
        :return:
        """
        pass

    @abstractmethod
    def unload(self):
        """
        Liberar los recursos utilizados.
        :return:
        """
        pass

    def load_if_not_loaded(self):
        if not self.is_loaded():
            self.load()

    def __getstate__(self):
        self.unload()
        d = self.__dict__.copy()

        try:
            super_d = super(ILoadable, self).__getstate__()
            d.update(super_d)
        except AttributeError:
            pass

        return d
