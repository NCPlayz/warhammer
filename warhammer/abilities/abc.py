from abc import ABCMeta, abstractmethod


class BaseAbility(metaclass=ABCMeta):

    @abstractmethod
    def handle(self, action):
        raise NotImplementedError
