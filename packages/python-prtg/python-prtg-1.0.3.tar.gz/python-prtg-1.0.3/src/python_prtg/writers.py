import abc


class Writer:
    def __init__(self, file: str) -> None:
        self.__filename = file

    @property
    def filename(self) -> str:
        return self.__filename

    @abc.abstractmethod
    def write(self) -> int:
        pass


class XmlWriter(Writer):
    def write(self) -> int:
        pass


class JsonWriter(Writer):
    def write(self) -> int:
        pass
