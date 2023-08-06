from abc import ABC, abstractmethod


class Stats(ABC):

    # @abstractmethod
    # def add_fit_stats(self, stats: dict) -> None:
    #     pass

    @abstractmethod
    def add_action_stats(self, stats: dict) -> None:
        pass
