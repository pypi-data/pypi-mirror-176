from abc import ABC, abstractmethod


class IService(ABC):
    __is_built: bool = False

    @property
    def is_built(self):
        return self.__is_built

    @abstractmethod
    def build(self):
        self.__is_built = True

    @abstractmethod
    def run(self):
        if not self.is_built:
            raise NotBuiltException


class NotBuiltException(Exception):
    def __init__(self):
        message = (
            "The service has not been built please use build method. If you have used the build method and "
            "still see this exception please ensure the build method in the service calls "
            # f"super(ECGTrainerBuilder, self).build() "
        )

        super(NotBuiltException, self).__init__(message)
