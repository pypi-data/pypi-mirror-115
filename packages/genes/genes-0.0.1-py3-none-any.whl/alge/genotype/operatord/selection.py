
from typing import List
from alge.genotype.operator import Operator
from alge.genotype.creature import Creature
from alge.genotype.population import Population


class Selection(Operator):

    CREATURES_TO_CHOOSE = 'pair_to_choose'

    _config: dict = {
        CREATURES_TO_CHOOSE: 2,
    }

    def __init__(self, config: dict = None):
        if config is not None:
            self._config = config

    def do(self, population: Population) -> Population:
        parents: List[Creature] = []
        quantity: int = self._config[self.CREATURES_TO_CHOOSE]

        if quantity > population.size():
            raise Exception('Population too small to choose %d parents' % (quantity,))

        population.sort_by_fitness()

        for i in range(0, quantity):
            parents.append(population[i])

        return Population(parents)
