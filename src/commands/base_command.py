from abc import ABC, abstractmethod

class BaseCommand(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError("Subclass not implemented")