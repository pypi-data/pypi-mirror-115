
from abc import ABC
from abc import abstractmethod
from alge.genotype.phenotype import Phenotype


class FitnessFunction(ABC):

    @abstractmethod
    def fit(self, phenotype: Phenotype) -> float:
        pass
