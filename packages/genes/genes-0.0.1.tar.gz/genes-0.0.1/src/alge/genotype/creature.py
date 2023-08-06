
from alge.genotype.phenotype import Phenotype


class Creature():

    _phenotype: Phenotype
    _fitness: float

    def __init__(self, phenotype: Phenotype, fitness: float = 0):
        self._phenotype = phenotype
        self._fitness = fitness

    def phenotype(self) -> Phenotype:
        return self._phenotype

    def fitness(self) -> float:
        return self._fitness

    def set_fitness(self, value: float) -> None:
        self._fitness = value
